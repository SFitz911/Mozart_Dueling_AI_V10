# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import queue
import threading
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv

# ────────────────────────────────────────────────────────────────────────
# Env
HERE = Path(__file__).parent
for cand in (HERE / ".env.mozart", HERE / "env.mozart"):
    if cand.exists():
        load_dotenv(dotenv_path=cand)
        break
else:
    load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", "60"))
AGENT_NAME = os.getenv("AGENT_NAME", "Mozart")

# Providers + bases
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")

OPENAI_MODEL_DEFAULT = os.getenv("OPENAI_MODEL", "gpt-4o")
DEEPSEEK_MODEL_DEFAULT = os.getenv("DEEPSEEK_MODEL", "deepseek-coder")

# Reviewer config (can override in .env.mozart)
REVIEWER_A_NAME = os.getenv("REVIEWER_A_NAME", "Reviewer A")
REVIEWER_A_PROVIDER = os.getenv("REVIEWER_A_PROVIDER", "openai").lower()
REVIEWER_A_MODEL = os.getenv("REVIEWER_A_MODEL", OPENAI_MODEL_DEFAULT)

REVIEWER_B_NAME = os.getenv("REVIEWER_B_NAME", "Reviewer B")
REVIEWER_B_PROVIDER = os.getenv("REVIEWER_B_PROVIDER", "deepseek").lower()
REVIEWER_B_MODEL = os.getenv("REVIEWER_B_MODEL", DEEPSEEK_MODEL_DEFAULT)

JUDGE_PROVIDER = os.getenv("JUDGE_PROVIDER", "openai").lower()
JUDGE_MODEL = os.getenv("JUDGE_MODEL", OPENAI_MODEL_DEFAULT)

# Fail early if keys are missing for the selected providers
if "deepseek" in (REVIEWER_A_PROVIDER, REVIEWER_B_PROVIDER, JUDGE_PROVIDER) and not DEEPSEEK_API_KEY:
    raise SystemExit("Missing DEEPSEEK_API_KEY in server/.env.mozart")
if "openai" in (REVIEWER_A_PROVIDER, REVIEWER_B_PROVIDER, JUDGE_PROVIDER) and not OPENAI_API_KEY:
    raise SystemExit("Missing OPENAI_API_KEY in server/.env.mozart")

# ────────────────────────────────────────────────────────────────────────
# Review criteria options (all default ON per your request)
CHECK_OPTIONS = [
    "correctness",
    "security", 
    "performance",
    "clarity",
    "maintainability",
    "logic",
    "error handling",
    "testing",
    "scalability",
    "documentation",
    "design",
]

# ────────────────────────────────────────────────────────────────────────
# System prompts

def get_critic_system(selected_criteria: List[str]) -> str:
    """Generate dynamic CRITIC_SYSTEM prompt based on selected review criteria"""
    # Create dynamic scores schema based on selected criteria
    scores_schema = {}
    for criterion in selected_criteria:
        # Normalize criterion name for JSON key (replace spaces with underscores)
        key = criterion.replace(" ", "_").replace("-", "_").lower()
        scores_schema[key] = "0-10"
    
    scores_json = ",".join([f'"{k}":0-10' for k in scores_schema.keys()])
    
    return (
        "You are a principal engineer reviewing another AI assistant's reply.\n"
        "Return STRICT JSON ONLY with this schema:\n"
        "{"
        "\"summary\":\"\","
        "\"grade\":\"approve|revise\","
        f"\"scores\":{{{scores_json}}},"
        "\"issues\":[{\"type\":\"bug|security|style|perf|design\",\"severity\":\"low|medium|high\",\"msg\":\"\",\"snippet\":\"\"}],"
        "\"improvements\":[],"
        "\"tests_suggested\":[]"
        "}\n"
        f"IMPORTANT: You must provide numeric scores (0-10) for ALL of these criteria: {', '.join(selected_criteria)}.\n"
        "Each score should reflect how well the reply addresses that specific criterion.\n"
        "Use the full 0-10 range: 0-3=poor, 4-6=adequate, 7-8=good, 9-10=excellent.\n"
        "Consider all criteria equally important unless the context suggests otherwise."
    )

# Legacy constant for backward compatibility (uses all criteria)
CRITIC_SYSTEM = get_critic_system([
    "correctness", "security", "performance", "clarity", "maintainability",
    "logic", "error_handling", "testing", "scalability", "documentation", "design"
])

def get_judge_system(selected_criteria: List[str]) -> str:
    """Generate dynamic JUDGE_SYSTEM prompt based on selected review criteria"""
    # Create dynamic scores schema based on selected criteria
    scores_json = ",".join([f'"{criterion.replace(" ", "_").replace("-", "_").lower()}":0-10' 
                           for criterion in selected_criteria])
    
    return (
        "You are a staff engineer who merges two code reviews into one final, neutral report.\n"
        "Return STRICT JSON ONLY with this schema:\n"
        "{"
        "\"summary\":\"\","
        "\"grade\":\"approve|revise\","
        "\"winner\":\"A|B|tie\","
        "\"reason\":\"\","
        f"\"scores\":{{{scores_json}}},"
        "\"top_issues\":[{\"type\":\"bug|security|style|perf|design\",\"severity\":\"low|medium|high\",\"msg\":\"\",\"snippet\":\"\"}],"
        "\"recommended_changes\":[],"
        "\"tests_suggested\":[],"
        "\"notes\":[]"
        "}\n"
        f"IMPORTANT: Provide balanced scores (0-10) for these criteria: {', '.join(selected_criteria)}.\n"
        "Consider both reviews carefully and merge their insights into comprehensive scores.\n"
        "The winner should be the review with better overall analysis, not just higher scores."
    )

# Legacy constant for backward compatibility
JUDGE_SYSTEM = get_judge_system([
    "correctness", "security", "performance", "clarity", "maintainability",
    "logic", "error_handling", "testing", "scalability", "documentation", "design"
])

SOLUTION_SYSTEM = (
    "You are a senior engineer. Given the user's goal, context, and the two reviews (or a merged review), "
    "produce a single improved final answer or patch. Keep it concise, self-contained, and ready to paste. "
    "Return plain text (no JSON)."
)

# ────────────────────────────────────────────────────────────────────────
# HTTP chat helpers

def _chat_http(base_url: str, api_key: str, model: str, messages: List[Dict[str, str]], force_json: bool) -> str:
    url = f"{base_url}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload: Dict[str, Any] = {"model": model, "messages": messages}
    if force_json:
        payload["response_format"] = {"type": "json_object"}
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def chat_openai(messages: List[Dict[str, str]], force_json: bool = True, model: Optional[str] = None) -> str:
    return _chat_http(OPENAI_BASE, OPENAI_API_KEY, model or OPENAI_MODEL_DEFAULT, messages, force_json)

def chat_deepseek(messages: List[Dict[str, str]], force_json: bool = True, model: Optional[str] = None) -> str:
    try:
        return _chat_http(DEEPSEEK_BASE, DEEPSEEK_API_KEY, model or DEEPSEEK_MODEL_DEFAULT, messages, force_json)
    except Exception:
        # Some models reject forced JSON occasionally; retry without it.
        return _chat_http(DEEPSEEK_BASE, DEEPSEEK_API_KEY, model or DEEPSEEK_MODEL_DEFAULT, messages, False)

def chat_provider(provider: str, messages: List[Dict[str, str]], force_json: bool, model: Optional[str]) -> str:
    provider = (provider or "openai").lower()
    if provider == "deepseek":
        return chat_deepseek(messages, force_json, model)
    return chat_openai(messages, force_json, model)

# ────────────────────────────────────────────────────────────────────────
# Utilities

def safe_json(s: str) -> Dict[str, Any]:
    """Enhanced JSON parsing with better error handling for review data"""
    try:
        parsed = json.loads(s)
        # Ensure we have the basic structure even if some fields are missing
        if isinstance(parsed, dict):
            # Add default scores if missing
            if "scores" not in parsed:
                parsed["scores"] = {}
            # Add default grade if missing
            if "grade" not in parsed:
                parsed["grade"] = "revise"
            # Add default summary if missing
            if "summary" not in parsed:
                parsed["summary"] = "Review analysis incomplete"
        return parsed
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON parse failed: {str(e)}",
            "raw_content": s[:200] + "..." if len(s) > 200 else s,
            "scores": {},
            "grade": "revise",
            "summary": "Failed to parse review response"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "raw_content": s[:100] + "..." if len(s) > 100 else s,
            "scores": {},
            "grade": "revise", 
            "summary": "Review processing error"
        }

def format_criteria_list(criteria: List[str]) -> str:
    """Format criteria list with descriptions for better AI understanding"""
    criteria_descriptions = {
        "correctness": "Code accuracy, logic soundness, and correct implementation",
        "security": "Vulnerability assessment, secure coding practices, data protection",
        "performance": "Efficiency, speed optimization, resource usage, scalability",
        "clarity": "Code readability, naming conventions, structure organization",
        "maintainability": "Future-proofing, modularity, ease of modification",
        "logic": "Reasoning flow, algorithm design, decision-making processes",
        "error handling": "Exception management, edge cases, fault tolerance",
        "testing": "Test coverage, testability, quality assurance approaches",
        "scalability": "Growth handling, load management, architectural flexibility",
        "documentation": "Code comments, API docs, usage examples, explanations",
        "design": "Architecture patterns, design principles, structural quality"
    }
    
    if not criteria:
        return "General code review covering all aspects"
    
    formatted = []
    for criterion in criteria:
        desc = criteria_descriptions.get(criterion.lower(), "General assessment")
        formatted.append(f"• {criterion.title()}: {desc}")
    
    return "\n".join(formatted)

def generate_scoring_instructions(criteria: List[str]) -> str:
    """Generate specific scoring instructions for selected criteria"""
    if not criteria:
        return "Provide balanced scores considering general code quality factors."
    
    normalized_criteria = [c.replace(" ", "_").replace("-", "_").lower() for c in criteria]
    criteria_list = ", ".join([f'"{c}"' for c in normalized_criteria])
    
    return f"""
SCORING REQUIREMENTS:
- Provide numeric scores (0-10) for each criterion: {criteria_list}
- Use the full scale: 0-3 (poor), 4-6 (adequate), 7-8 (good), 9-10 (excellent)
- Base scores on how well the reply addresses each specific criterion
- Consider the context and goals when evaluating each dimension
- Be consistent in your scoring methodology
"""

def make_user_prompt(claude_reply: str, goal: str, context: str, checks: List[str]) -> str:
    """Enhanced user prompt with detailed criteria formatting and scoring guidance"""
    criteria_formatted = format_criteria_list(checks)
    scoring_instructions = generate_scoring_instructions(checks)
    
    # Build the prompt with clear sections
    prompt_parts = [
        "=" * 60,
        "REVIEW ASSIGNMENT",
        "=" * 60,
    ]
    
    # Add goal section
    if goal and goal.strip():
        prompt_parts.extend([
            "",
            "🎯 PRIMARY GOAL:",
            goal.strip(),
        ])
    
    # Add context section
    if context and context.strip():
        prompt_parts.extend([
            "",
            "📋 CONTEXT & CONSTRAINTS:",
            context.strip(),
        ])
    
    # Add criteria section
    prompt_parts.extend([
        "",
        "🔍 EVALUATION CRITERIA:",
        criteria_formatted,
        "",
        scoring_instructions,
    ])
    
    # Add the content to review
    prompt_parts.extend([
        "",
        "=" * 60,
        "CONTENT TO REVIEW",
        "=" * 60,
        "",
        claude_reply,
        "",
        "=" * 60,
        "INSTRUCTIONS",
        "=" * 60,
        "",
        "Evaluate the above content according to the specified criteria.",
        "Focus your analysis on the selected evaluation dimensions.",
        "Provide specific, actionable feedback in your JSON response.",
        "Return ONLY valid JSON - no additional text or explanations.",
    ])
    
    return "\n".join(prompt_parts)

def calculate_average_score(review_data: Dict[str, Any], selected_criteria: Optional[List[str]] = None) -> float:
    """Calculate average score from review data, handling variable criteria"""
    scores = review_data.get("scores", {})
    if not scores:
        return 0.0
    
    # If specific criteria are provided, only consider those
    if selected_criteria:
        normalized_criteria = [c.replace(" ", "_").replace("-", "_").lower() for c in selected_criteria]
        relevant_scores = []
        for criterion in normalized_criteria:
            if criterion in scores and isinstance(scores[criterion], (int, float)):
                relevant_scores.append(float(scores[criterion]))
        
        if relevant_scores:
            return sum(relevant_scores) / len(relevant_scores)
    
    # Otherwise, use all numeric scores available
    numeric_scores = []
    for value in scores.values():
        if isinstance(value, (int, float)):
            numeric_scores.append(float(value))
    
    return sum(numeric_scores) / max(1, len(numeric_scores))

def fast_evaluate(claude_reply: str, goal: str, context: str, checks: List[str]) -> Dict[str, Any]:
    """Run 2 parallel reviewers, pick the winner by average score."""
    # Generate dynamic system prompts based on selected criteria
    critic_system = get_critic_system(checks)
    prompt = make_user_prompt(claude_reply, goal, context, checks)

    a_raw = chat_provider(
        REVIEWER_A_PROVIDER,
        [{"role": "system", "content": critic_system},
         {"role": "user", "content": prompt}],
        True,
        REVIEWER_A_MODEL,
    )
    b_raw = chat_provider(
        REVIEWER_B_PROVIDER,
        [{"role": "system", "content": critic_system},
         {"role": "user", "content": prompt}],
        True,
        REVIEWER_B_MODEL,
    )

    a_data = safe_json(a_raw)
    b_data = safe_json(b_raw)

    # Calculate averages using the enhanced function
    a_avg = calculate_average_score(a_data, checks)
    b_avg = calculate_average_score(b_data, checks)
    
    if a_avg >= b_avg:
        winner_data = a_data
        winner = "A"
    else:
        winner_data = b_data
        winner = "B"

    solution = chat_provider(
        JUDGE_PROVIDER,
        [
            {"role": "system", "content": SOLUTION_SYSTEM},
            {"role": "user", "content":
                f"GOAL:\n{goal}\n\nCONTEXT:\n{context}\n\n"
                f"WINNING REVIEW:\n{json.dumps(winner_data, indent=2)}\n\n"
                "Produce the improved final answer/patch now."}
        ],
        False,
        JUDGE_MODEL,
    )

    return {
        "mode": "FAST",
        "final": winner_data,
        "a_review": a_data,
        "b_review": b_data,
        "a_name": REVIEWER_A_NAME,
        "b_name": REVIEWER_B_NAME,
        "winner": winner,
        "solution": solution,
        "selected_criteria": checks,  # Store for UI display
        "a_avg_score": a_avg,
        "b_avg_score": b_avg,
    }

def full_evaluate(claude_reply: str, goal: str, context: str, checks: List[str]) -> Dict[str, Any]:
    """Run 2 reviewers + judge + solution."""
    # Generate dynamic system prompts based on selected criteria
    critic_system = get_critic_system(checks)
    judge_system = get_judge_system(checks)
    prompt = make_user_prompt(claude_reply, goal, context, checks)

    a_raw = chat_provider(
        REVIEWER_A_PROVIDER,
        [{"role": "system", "content": critic_system},
         {"role": "user", "content": prompt}],
        True,
        REVIEWER_A_MODEL,
    )
    b_raw = chat_provider(
        REVIEWER_B_PROVIDER,
        [{"role": "system", "content": critic_system},
         {"role": "user", "content": prompt}],
        True,
        REVIEWER_B_MODEL,
    )

    merged_raw = chat_provider(
        JUDGE_PROVIDER,
        [{"role": "system", "content": judge_system},
         {"role": "user", "content": f"Review A:\n{a_raw}\n\nReview B:\n{b_raw}\n\nMerge into final JSON."}],
        True,
        JUDGE_MODEL,
    )

    solution = chat_provider(
        JUDGE_PROVIDER,
        [
            {"role": "system", "content": SOLUTION_SYSTEM},
            {"role": "user", "content":
                f"GOAL:\n{goal}\n\nCONTEXT:\n{context}\n\n"
                f"MERGED JUDGE JSON:\n{merged_raw}\n\n"
                "Produce the improved final answer/patch now."}
        ],
        False,
        JUDGE_MODEL,
    )

    a_data = safe_json(a_raw)
    b_data = safe_json(b_raw)
    final_data = safe_json(merged_raw)

    return {
        "mode": "FULL",
        "final": final_data,
        "a_review": a_data,
        "b_review": b_data,
        "a_name": REVIEWER_A_NAME,
        "b_name": REVIEWER_B_NAME,
        "solution": solution,
        "selected_criteria": checks,  # Store for UI display
        "a_avg_score": calculate_average_score(a_data, checks),
        "b_avg_score": calculate_average_score(b_data, checks),
        "final_avg_score": calculate_average_score(final_data, checks),
    }

# ────────────────────────────────────────────────────────────────────────
# GUI with Enhanced Text Selection and Context Menus

DARK_BG = "#1e1e1e"
DARK_PANEL = "#252526"
FG = "#d4d4d4"           # body text
HL = "#17b8aa"           # headings (teal color as you changed)
ACCENT = "#22c55e"       # progress green
GREEN_BTN = "#2d7d32"    # Green button background
GREEN_BTN_HOVER = "#388e3c"  # Green button hover

# Fast Mode colors
FAST_MODE_BG = "#1a4a3a"     # Green background for Fast Mode
FAST_MODE_FG = "#4ade80"     # Green text for Fast Mode
FAST_MODE_LIGHT = "#86efac"  # Light green for description

# Full Mode colors  
FULL_MODE_BG = "#1a3a4a"     # Blue background for Full Mode
FULL_MODE_FG = "#60a5fa"     # Blue text for Full Mode
FULL_MODE_LIGHT = "#93c5fd"  # Light blue for description

class TextWidgetWithContextMenu(tk.Text):
    """Enhanced Text widget with right-click context menu and selection support"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_context_menu()
        self.setup_bindings()
    
    def setup_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self, tearoff=0, bg=DARK_PANEL, fg=FG, 
                                   activebackground=HL, activeforeground="white")
        self.context_menu.add_command(label="📋 Copy", command=self.context_copy)
        self.context_menu.add_command(label="📄 Paste", command=self.context_paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔍 Select All", command=self.context_select_all)
        self.context_menu.add_command(label="✂️ Cut", command=self.context_cut)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Clear All", command=self.context_clear)
    
    def setup_bindings(self):
        """Setup keyboard shortcuts and right-click binding"""
        # Right-click context menu
        self.bind("<Button-3>", self.show_context_menu)
        
        # Standard keyboard shortcuts
        self.bind("<Control-c>", lambda e: self.context_copy())
        self.bind("<Control-v>", lambda e: self.context_paste())
        self.bind("<Control-x>", lambda e: self.context_cut())
        self.bind("<Control-a>", lambda e: self.context_select_all())
        
        # Enhanced selection with Shift+Click
        self.bind("<Shift-Button-1>", self.extend_selection)
        
        # Double-click to select word
        self.bind("<Double-Button-1>", self.select_word)
        
        # Triple-click to select line
        self.bind("<Triple-Button-1>", self.select_line)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        try:
            # Update menu state based on selection
            has_selection = bool(self.tag_ranges("sel"))
            clipboard_data = self.selection_get(selection="CLIPBOARD") if self.selection_own_get(selection="CLIPBOARD") else ""
            has_clipboard = bool(clipboard_data)
            
            # Enable/disable menu items
            self.context_menu.entryconfig("📋 Copy", state="normal" if has_selection else "disabled")
            self.context_menu.entryconfig("✂️ Cut", state="normal" if has_selection else "disabled")
            self.context_menu.entryconfig("📄 Paste", state="normal" if has_clipboard else "normal")  # Always allow paste attempt
            
            self.context_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass
        finally:
            self.context_menu.grab_release()
    
    def context_copy(self):
        """Copy selected text to clipboard"""
        try:
            if self.tag_ranges("sel"):
                selected_text = self.selection_get()
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                return "break"
        except tk.TclError:
            pass
    
    def context_paste(self):
        """Paste from clipboard at cursor position"""
        try:
            clipboard_text = self.clipboard_get()
            if self.tag_ranges("sel"):
                # Replace selection
                self.delete("sel.first", "sel.last")
            self.insert("insert", clipboard_text)
            return "break"
        except tk.TclError:
            pass
    
    def context_cut(self):
        """Cut selected text to clipboard"""
        try:
            if self.tag_ranges("sel"):
                selected_text = self.selection_get()
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.delete("sel.first", "sel.last")
                return "break"
        except tk.TclError:
            pass
    
    def context_select_all(self):
        """Select all text"""
        self.tag_add("sel", "1.0", "end")
        self.mark_set("insert", "1.0")
        self.see("insert")
        return "break"
    
    def context_clear(self):
        """Clear all text"""
        self.delete("1.0", "end")
    
    def extend_selection(self, event):
        """Extend selection on Shift+Click"""
        if not self.tag_ranges("sel"):
            return
        
        current_pos = self.index("@%s,%s" % (event.x, event.y))
        sel_start = self.index("sel.first")
        sel_end = self.index("sel.last")
        
        # Determine which end of selection to extend
        if self.compare(current_pos, "<", sel_start):
            self.tag_remove("sel", "1.0", "end")
            self.tag_add("sel", current_pos, sel_end)
        else:
            self.tag_remove("sel", "1.0", "end")
            self.tag_add("sel", sel_start, current_pos)
        
        return "break"
    
    def select_word(self, event):
        """Select word on double-click"""
        pos = self.index("@%s,%s" % (event.x, event.y))
        word_start = self.index("%s wordstart" % pos)
        word_end = self.index("%s wordend" % pos)
        
        self.tag_remove("sel", "1.0", "end")
        self.tag_add("sel", word_start, word_end)
        self.mark_set("insert", word_end)
        
        return "break"
    
    def select_line(self, event):
        """Select line on triple-click"""
        pos = self.index("@%s,%s" % (event.x, event.y))
        line_start = self.index("%s linestart" % pos)
        line_end = self.index("%s lineend" % pos)
        
        self.tag_remove("sel", "1.0", "end")
        self.tag_add("sel", line_start, line_end)
        self.mark_set("insert", line_end)
        
        return "break"

class ScrollableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{AGENT_NAME} Reviewer V10 - Dynamic Review Criteria")
        self.configure(bg=DARK_BG)
        self.geometry("1200x900")
        
        # Configure minimum window size
        self.minsize(800, 600)

        self._q: "queue.Queue[Tuple[str, Any]]" = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self.result_json: Dict[str, Any] = {}

        # Fast mode variable - DEFAULT TO TRUE (Fast Mode)
        self.fast_var = tk.BooleanVar(value=True)

        # Configure ttk styles
        self._setup_styles()
        
        # Create main scrollable container
        self._create_scrollable_container()
        
        # Create all content in the scrollable frame
        self._create_content()
        
        # Start the event pump
        self.after(100, self._pump)
        
        # Bind mouse wheel to canvas scrolling
        self._bind_mousewheel()

    def _setup_styles(self):
        """Configure ttk styles for dark theme with green buttons"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=DARK_BG)
        style.configure("Card.TFrame", background=DARK_PANEL, relief="flat")
        style.configure("TLabel", background=DARK_BG, foreground=FG)
        style.configure("H.TLabel", background=DARK_BG, foreground=HL, font=("Segoe UI", 11, "bold"))
        style.configure("Card.TLabel", background=DARK_PANEL, foreground=FG)
        style.configure("TButton", background=DARK_PANEL, foreground=FG)
        style.map("TButton", background=[("active", "#333333")])
        
        # Green button styles for specific buttons
        style.configure("Green.TButton", 
                       background=GREEN_BTN, 
                       foreground="white",
                       font=("Segoe UI", 9, "bold"))
        style.map("Green.TButton", 
                 background=[("active", GREEN_BTN_HOVER), ("pressed", "#1b5e20")])
        
        # Copy button style (smaller, secondary)
        style.configure("Copy.TButton", 
                       background="#404040", 
                       foreground="#d4d4d4",
                       font=("Segoe UI", 8))
        style.map("Copy.TButton", 
                 background=[("active", "#505050")])
        
        style.configure("Green.Horizontal.TProgressbar", troughcolor="#111", background=ACCENT)
        style.configure("Vertical.TScrollbar", background=DARK_PANEL, troughcolor=DARK_BG, 
                       bordercolor=DARK_BG, arrowcolor=FG, darkcolor=DARK_PANEL, lightcolor=DARK_PANEL)

    def _create_scrollable_container(self):
        """Create the main scrollable canvas and frame"""
        # Create main container frame
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(main_container, bg=DARK_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        
        # Create the scrollable frame that will contain all content
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure canvas scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas to update scrollable frame width
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def _on_canvas_configure(self, event):
        """Handle canvas resize to update scrollable frame width"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _bind_mousewheel(self):
        """Bind mouse wheel scrolling to the canvas"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel when entering the window
        self.bind('<Enter>', _bind_to_mousewheel)
        self.bind('<Leave>', _unbind_from_mousewheel)

    def _create_content(self):
        """Create all the content widgets in the scrollable frame"""
        # Add padding to the scrollable frame
        content_frame = ttk.Frame(self.scrollable_frame, padding=15)
        content_frame.pack(fill="both", expand=True)

        # Title section
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(fill="x", pady=(0, 10))
        title_label = ttk.Label(title_frame, text=f"{AGENT_NAME} Code Reviewer V10", 
                               style="H.TLabel", font=("Segoe UI", 14, "bold"))
        title_label.pack(anchor="w")
        subtitle_label = ttk.Label(title_frame, text="Dynamic Review Criteria • Enhanced Text Selection • Right-Click Menus", 
                                  style="TLabel", font=("Segoe UI", 9))
        subtitle_label.pack(anchor="w")

        # Goal section with copy button
        goal_frame = ttk.Frame(content_frame)
        goal_frame.pack(fill="x", pady=(0, 10))
        goal_header = ttk.Frame(goal_frame)
        goal_header.pack(fill="x")
        ttk.Label(goal_header, text="Goal / What Claude was asked to do:", style="H.TLabel").pack(side="left")
        ttk.Button(goal_header, text="📋 Copy", command=self._copy_goal, style="Copy.TButton").pack(side="right")
        
        self.goal_var = tk.StringVar()
        goal_entry = ttk.Entry(goal_frame, textvariable=self.goal_var, font=("Consolas", 10))
        goal_entry.pack(fill="x", pady=(5, 0))

        # Context section with copy button and enhanced text widget
        context_frame = ttk.Frame(content_frame)
        context_frame.pack(fill="x", pady=(0, 10))
        
        context_header = ttk.Frame(context_frame)
        context_header.pack(fill="x")
        ttk.Label(context_header, text="Optional context / constraints:", style="H.TLabel").pack(side="left")
        ttk.Button(context_header, text="📋 Copy", command=self._copy_context, style="Copy.TButton").pack(side="right")
        
        ctx_container = ttk.Frame(context_frame)
        ctx_container.pack(fill="x", pady=(5, 0))
        self.ctx = TextWidgetWithContextMenu(ctx_container, height=4, bg="#1b1b1b", fg=FG, insertbackground=FG, 
                          wrap="word", font=("Consolas", 9), selectbackground=HL, selectforeground="white")
        self.ctx.pack(side="left", fill="both", expand=True)
        self._attach_scrollbar(self.ctx, ctx_container)

        # Claude reply and checks section
        main_input_frame = ttk.Frame(content_frame)
        main_input_frame.pack(fill="x", pady=(0, 10))

        # Left side - Claude reply with copy button and enhanced text widget
        left_frame = ttk.Frame(main_input_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        reply_header = ttk.Frame(left_frame)
        reply_header.pack(fill="x")
        ttk.Label(reply_header, text="Claude reply to evaluate:", style="H.TLabel").pack(side="left")
        ttk.Button(reply_header, text="📋 Copy", command=self._copy_reply, style="Copy.TButton").pack(side="right")
        
        reply_container = ttk.Frame(left_frame)
        reply_container.pack(fill="both", expand=True, pady=(5, 0))
        self.reply = TextWidgetWithContextMenu(reply_container, height=10, bg="#141414", fg=FG, insertbackground=FG, 
                            wrap="word", font=("Consolas", 9), selectbackground=HL, selectforeground="white")
        self.reply.pack(side="left", fill="both", expand=True)
        self._attach_scrollbar(self.reply, reply_container)
        
        # Buttons for reply area - GREEN BUTTONS
        reply_buttons = ttk.Frame(left_frame)
        reply_buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(reply_buttons, text="📋 Paste", command=self._paste, style="Green.TButton").pack(side="left")
        ttk.Button(reply_buttons, text="🗑️ Clear", 
                  command=lambda: self.reply.delete("1.0", "end")).pack(side="left", padx=(8, 0))
        ttk.Button(reply_buttons, text="📁 Load File", command=self._load_file).pack(side="left", padx=(8, 0))

        # Right side - Check options and Mode selector
        right_frame = ttk.Frame(main_input_frame)
        right_frame.pack(side="right", fill="y")
        
        # Review Criteria section
        checks_label_frame = ttk.Frame(right_frame)
        checks_label_frame.pack(fill="x")
        ttk.Label(checks_label_frame, text="Review Criteria:", style="H.TLabel").pack(anchor="w")
        
        # Scrollable checks area
        checks_container = ttk.Frame(right_frame)
        checks_container.pack(fill="x", pady=(5, 0))
        
        checks_canvas = tk.Canvas(checks_container, bg=DARK_BG, highlightthickness=0, height=180, width=200)
        checks_scrollbar = ttk.Scrollbar(checks_container, orient="vertical", command=checks_canvas.yview)
        checks_frame = ttk.Frame(checks_canvas)
        
        checks_frame.bind("<Configure>", lambda e: checks_canvas.configure(scrollregion=checks_canvas.bbox("all")))
        checks_canvas.create_window((0, 0), window=checks_frame, anchor="nw")
        checks_canvas.configure(yscrollcommand=checks_scrollbar.set)
        
        checks_canvas.pack(side="left", fill="both", expand=True)
        checks_scrollbar.pack(side="right", fill="y")

        # Create checkboxes for review criteria (all default ON)
        default_on = set(CHECK_OPTIONS)
        self.chk_vars = {k: tk.BooleanVar(value=(k in default_on)) for k in CHECK_OPTIONS}
        for k, var in self.chk_vars.items():
            cb = ttk.Checkbutton(checks_frame, text=k.title(), variable=var, 
                               command=self._update_criteria_summary)
            cb.pack(anchor="w", pady=1)

        # Active Criteria Summary - NEW VISUAL FEEDBACK
        criteria_summary_frame = ttk.Frame(right_frame)
        criteria_summary_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(criteria_summary_frame, text="📋 Active Criteria:", 
                 style="H.TLabel", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        self.criteria_summary = tk.Text(criteria_summary_frame, height=3, bg="#2a2a2a", fg="#4ade80", 
                                       font=("Segoe UI", 8), wrap="word", relief="flat", 
                                       state="disabled", cursor="arrow")
        self.criteria_summary.pack(fill="x", pady=(2, 0))
        
        # Initialize criteria summary
        self._update_criteria_summary()

        # Fast Mode selector - MOVED BELOW and ALWAYS VISIBLE
        mode_selector_frame = ttk.Frame(right_frame)
        mode_selector_frame.pack(fill="x", pady=(10, 0))
        
        # Mode selector box with color-changing capability
        self.fast_mode_frame = tk.Frame(mode_selector_frame, relief="raised", bd=2, padx=8, pady=8)
        self.fast_mode_frame.pack(fill="x")
        
        self.fast_mode_label = tk.Label(self.fast_mode_frame, text="⚡ Review Mode:", 
                                       font=("Segoe UI", 9, "bold"))
        self.fast_mode_label.pack(anchor="w")
        
        self.fast_checkbutton = tk.Checkbutton(
            self.fast_mode_frame,
            text="🚀 Fast Mode (Default)",
            variable=self.fast_var,
            font=("Segoe UI", 9, "bold"),
            command=self._on_fast_mode_change
        )
        self.fast_checkbutton.pack(anchor="w", pady=(2, 0))
        
        # Mode description
        self.mode_desc = tk.Label(self.fast_mode_frame, 
                                 text="Two reviewers compete, winner by score",
                                 font=("Segoe UI", 8))
        self.mode_desc.pack(anchor="w")

        # Control buttons and status - GREEN EVALUATE BUTTON
        control_frame = ttk.Frame(content_frame)
        control_frame.pack(fill="x", pady=(10, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="left")
        ttk.Button(button_frame, text="🔍 Evaluate", command=self.on_evaluate, style="Green.TButton").pack(side="left")
        ttk.Button(button_frame, text="💾 Save JSON", command=self.save_json).pack(side="left", padx=(8, 0))
        ttk.Button(button_frame, text="📊 Export Report", command=self.export_report).pack(side="left", padx=(8, 0))
        
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side="right", fill="x", expand=True, padx=(20, 0))
        self.status = ttk.Label(status_frame, text="🟡 Ready (Fast Mode Default)", style="TLabel")
        self.status.pack(side="left")
        self.pb = ttk.Progressbar(status_frame, mode="determinate", 
                                 style="Green.Horizontal.TProgressbar", maximum=100, value=0)
        self.pb.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Score cards section with copy buttons for each card
        scores_frame = ttk.Frame(content_frame)
        scores_frame.pack(fill="x", pady=(10, 10))
        
        scores_title_frame = ttk.Frame(scores_frame)
        scores_title_frame.pack(fill="x")
        ttk.Label(scores_title_frame, text="Review Results:", style="H.TLabel").pack(side="left")
        ttk.Button(scores_title_frame, text="📋 Copy All Scores", command=self._copy_all_scores, style="Copy.TButton").pack(side="right")
        
        cards_container = ttk.Frame(scores_frame)
        cards_container.pack(fill="x", pady=(5, 0))

        # Reviewer A card with copy button
        card_a_frame = ttk.Frame(cards_container)
        card_a_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        card_a_header = ttk.Frame(card_a_frame)
        card_a_header.pack(fill="x")
        ttk.Label(card_a_header, text=f"👨‍💻 Reviewer A: {REVIEWER_A_NAME}", style="H.TLabel", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(card_a_header, text="📋", command=self._copy_reviewer_a, style="Copy.TButton").pack(side="right")
        
        self.card_a = ttk.LabelFrame(card_a_frame, text="", padding=10, style="Card.TFrame")
        self.card_a.pack(fill="x")
        self._scores_a = self._make_score_block(self.card_a)  # Will be updated with criteria during evaluation

        # Reviewer B card with copy button
        card_b_frame = ttk.Frame(cards_container)
        card_b_frame.pack(side="left", fill="x", expand=True, padx=(5, 5))
        
        card_b_header = ttk.Frame(card_b_frame)
        card_b_header.pack(fill="x")
        ttk.Label(card_b_header, text=f"👩‍💻 Reviewer B: {REVIEWER_B_NAME}", style="H.TLabel", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(card_b_header, text="📋", command=self._copy_reviewer_b, style="Copy.TButton").pack(side="right")
        
        self.card_b = ttk.LabelFrame(card_b_frame, text="", padding=10, style="Card.TFrame")
        self.card_b.pack(fill="x")
        self._scores_b = self._make_score_block(self.card_b)  # Will be updated with criteria during evaluation

        # Winner card with copy button
        card_w_frame = ttk.Frame(cards_container)
        card_w_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        card_w_header = ttk.Frame(card_w_frame)
        card_w_header.pack(fill="x")
        ttk.Label(card_w_header, text="🏆 Judge's Results", style="H.TLabel", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(card_w_header, text="📋", command=self._copy_judge_results, style="Copy.TButton").pack(side="right")
        
        self.card_w = ttk.LabelFrame(card_w_frame, text="", padding=10, style="Card.TFrame")
        self.card_w.pack(fill="x")
        self.winner_label = ttk.Label(self.card_w, text="—", style="H.TLabel")
        self.winner_label.pack(anchor="w")
        self.winner_reason = ttk.Label(self.card_w, text="", style="Card.TLabel", 
                                      wraplength=280, justify="left")
        self.winner_reason.pack(anchor="w", pady=(5, 0))

        # Result JSON section with enhanced text widget
        json_frame = ttk.Frame(content_frame)
        json_frame.pack(fill="x", pady=(10, 10))
        
        json_header = ttk.Frame(json_frame)
        json_header.pack(fill="x")
        ttk.Label(json_header, text="📋 Detailed Results (JSON):", style="H.TLabel").pack(side="left")
        ttk.Button(json_header, text="📄 Copy JSON", command=self.copy_json, style="Copy.TButton").pack(side="right")
        
        json_container = ttk.Frame(json_frame)
        json_container.pack(fill="x", pady=(5, 0))
        self.out = TextWidgetWithContextMenu(json_container, height=8, bg="#0f0f0f", fg=FG, insertbackground=FG, 
                          wrap="word", font=("Consolas", 9), selectbackground=HL, selectforeground="white")
        self.out.pack(side="left", fill="both", expand=True)
        self._attach_scrollbar(self.out, json_container)

        # Solution section - GREEN COPY SOLUTION BUTTON with enhanced text widget
        solution_frame = ttk.Frame(content_frame)
        solution_frame.pack(fill="x", pady=(10, 20))
        
        solution_header = ttk.Frame(solution_frame)
        solution_header.pack(fill="x")
        ttk.Label(solution_header, text="💡 AI-Generated Solution:", style="H.TLabel").pack(side="left")
        
        solution_buttons = ttk.Frame(solution_header)
        solution_buttons.pack(side="right")
        ttk.Button(solution_buttons, text="📋 Copy Solution", command=self.copy_solution, style="Green.TButton").pack(side="left")
        ttk.Button(solution_buttons, text="🚀 Submit to Claude", command=self.submit_to_claude).pack(side="left", padx=(8, 0))
        
        solution_container = ttk.Frame(solution_frame)
        solution_container.pack(fill="x", pady=(5, 0))
        self.solution = TextWidgetWithContextMenu(solution_container, height=8, bg="#101417", fg=FG, insertbackground=FG, 
                               wrap="word", font=("Consolas", 9), selectbackground=HL, selectforeground="white")
        self.solution.pack(side="left", fill="both", expand=True)
        self._attach_scrollbar(self.solution, solution_container)

        # Initialize mode colors and description
        self._on_fast_mode_change()

    def _on_fast_mode_change(self):
        """Update mode colors and description when fast mode changes"""
        if self.fast_var.get():
            # Fast Mode - Green colors
            self.fast_mode_frame.config(bg=FAST_MODE_BG)
            self.fast_mode_label.config(bg=FAST_MODE_BG, fg=FAST_MODE_FG)
            self.fast_checkbutton.config(
                bg=FAST_MODE_BG, 
                fg=FAST_MODE_FG,
                selectcolor=GREEN_BTN,
                activebackground=FAST_MODE_BG,
                activeforeground=FAST_MODE_FG,
                text="🚀 Fast Mode (Default)"
            )
            self.mode_desc.config(
                bg=FAST_MODE_BG, 
                fg=FAST_MODE_LIGHT,
                text="Two reviewers compete, winner by score"
            )
            self.status.config(text="🟡 Ready (Fast Mode)")
        else:
            # Full Mode - Blue colors
            self.fast_mode_frame.config(bg=FULL_MODE_BG)
            self.fast_mode_label.config(bg=FULL_MODE_BG, fg=FULL_MODE_FG, text="🎭 Review Mode:")
            self.fast_checkbutton.config(
                bg=FULL_MODE_BG, 
                fg=FULL_MODE_FG,
                selectcolor="#1565c0",
                activebackground=FULL_MODE_BG,
                activeforeground=FULL_MODE_FG,
                text="🎭 Full Mode (Comprehensive)"
            )
            self.mode_desc.config(
                bg=FULL_MODE_BG, 
                fg=FULL_MODE_LIGHT,
                text="A + B + Judge + Solution (comprehensive)"
            )
            self.status.config(text="🟡 Ready (Full Mode)")

    # Copy functionality methods
    def _copy_to_clipboard(self, content: str, description: str):
        """Helper method to copy content to clipboard and show status"""
        if content.strip():
            self.clipboard_clear()
            self.clipboard_append(content)
            self.status.config(text=f"📋 {description} copied to clipboard")
            self.after(2000, lambda: self.status.config(text="🟢 Ready"))
        else:
            messagebox.showwarning("Nothing to Copy", f"No {description.lower()} available to copy")

    def _copy_goal(self):
        """Copy goal to clipboard"""
        goal = self.goal_var.get()
        self._copy_to_clipboard(goal, "Goal")

    def _copy_context(self):
        """Copy context to clipboard"""
        context = self.ctx.get("1.0", "end").strip()
        self._copy_to_clipboard(context, "Context")

    def _copy_reply(self):
        """Copy Claude reply to clipboard"""
        reply = self.reply.get("1.0", "end").strip()
        self._copy_to_clipboard(reply, "Claude Reply")

    def _copy_reviewer_a(self):
        """Copy Reviewer A results to clipboard"""
        if self.result_json and "a_review" in self.result_json:
            content = json.dumps(self.result_json["a_review"], indent=2)
            self._copy_to_clipboard(content, f"Reviewer A ({self.result_json.get('a_name', 'A')}) Results")
        else:
            messagebox.showwarning("Nothing to Copy", "No Reviewer A results available")

    def _copy_reviewer_b(self):
        """Copy Reviewer B results to clipboard"""
        if self.result_json and "b_review" in self.result_json:
            content = json.dumps(self.result_json["b_review"], indent=2)
            self._copy_to_clipboard(content, f"Reviewer B ({self.result_json.get('b_name', 'B')}) Results")
        else:
            messagebox.showwarning("Nothing to Copy", "No Reviewer B results available")

    def _copy_judge_results(self):
        """Copy Judge/Final results to clipboard"""
        if self.result_json and "final" in self.result_json:
            content = json.dumps(self.result_json["final"], indent=2)
            self._copy_to_clipboard(content, "Judge/Final Results")
        else:
            messagebox.showwarning("Nothing to Copy", "No Judge results available")

    def _copy_all_scores(self):
        """Copy all score results in a formatted way with expanded criteria"""
        if not self.result_json:
            messagebox.showwarning("Nothing to Copy", "No evaluation results available")
            return
        
        # Get selected criteria for better formatting
        selected_criteria = self.result_json.get('selected_criteria', [])
        criteria_text = ", ".join(selected_criteria) if selected_criteria else "All criteria"
        
        # Create enhanced formatted summary
        content = f"""# Mozart V10 Review Results Summary

## Evaluation Details:
- **Mode**: {self.result_json.get('mode', 'Unknown')}
- **Selected Criteria**: {criteria_text}
- **Timestamp**: {self.result_json.get('timestamp', 'Not recorded')}

## Reviewer A ({self.result_json.get('a_name', 'Unknown')}):
**Average Score**: {self.result_json.get('a_avg_score', 'N/A')}/10

### Detailed Review:
{json.dumps(self.result_json.get('a_review', {}), indent=2)}

## Reviewer B ({self.result_json.get('b_name', 'Unknown')}):
**Average Score**: {self.result_json.get('b_avg_score', 'N/A')}/10

### Detailed Review:
{json.dumps(self.result_json.get('b_review', {}), indent=2)}

## Final/Judge Results:
**Final Average Score**: {self.result_json.get('final_avg_score', 'N/A')}/10

### Judge Analysis:
{json.dumps(self.result_json.get('final', {}), indent=2)}

## Competition Results:
**Winner**: {self.result_json.get('winner', 'Unknown')}

## Selected Review Criteria Analysis:
"""
        
        # Add detailed criteria breakdown if available
        if selected_criteria:
            content += "\n### Criteria-Specific Scores:\n"
            a_scores = self.result_json.get('a_review', {}).get('scores', {})
            b_scores = self.result_json.get('b_review', {}).get('scores', {})
            final_scores = self.result_json.get('final', {}).get('scores', {})
            
            for criterion in selected_criteria:
                normalized = criterion.replace(" ", "_").replace("-", "_").lower()
                content += f"\n**{criterion.title()}:**\n"
                content += f"- Reviewer A: {a_scores.get(normalized, 'N/A')}/10\n"
                content += f"- Reviewer B: {b_scores.get(normalized, 'N/A')}/10\n"
                content += f"- Final/Judge: {final_scores.get(normalized, 'N/A')}/10\n"
        
        self._copy_to_clipboard(content, "All Review Results")

    def _update_criteria_summary(self):
        """Update the visual criteria summary showing active criteria"""
        try:
            # Get currently selected criteria
            selected = [k for k, v in self.chk_vars.items() if v.get()]
            
            # Create summary text
            if not selected:
                summary_text = "⚠️ No criteria selected - evaluation will use general review"
                text_color = "#fb923c"  # Orange warning
            elif len(selected) == len(CHECK_OPTIONS):
                summary_text = f"✅ All {len(selected)} criteria selected for comprehensive review"
                text_color = "#4ade80"  # Green success
            else:
                # Show first few criteria and count
                shown_criteria = selected[:3]
                summary_parts = [f"✅ {len(selected)} criteria: {', '.join(shown_criteria)}"]
                if len(selected) > 3:
                    summary_parts.append(f"... +{len(selected) - 3} more")
                summary_text = ''.join(summary_parts)
                text_color = "#60a5fa"  # Blue partial
            
            # Update the summary widget
            self.criteria_summary.config(state="normal", fg=text_color)
            self.criteria_summary.delete("1.0", "end")
            self.criteria_summary.insert("1.0", summary_text)
            self.criteria_summary.config(state="disabled")
            
        except AttributeError:
            # Criteria summary widget not yet created
            pass

    # UI helper methods
    def _attach_scrollbar(self, text_widget: tk.Text, parent: ttk.Frame):
        """Attach a scrollbar to a text widget"""
        sb = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def _make_score_block(self, parent: ttk.LabelFrame, criteria: Optional[List[str]] = None) -> Dict[str, ttk.Label]:
        """Create a dynamic score display block based on selected criteria"""
        # Handle None parent for testing
        if parent is None:
            return {}
            
        # Clear any existing content
        for widget in parent.winfo_children():
            widget.destroy()
            
        grid = ttk.Frame(parent, style="Card.TFrame")
        grid.pack(fill="x", pady=5)
        labels: Dict[str, ttk.Label] = {}
        
        # Always show grade first
        self._add_score_row(grid, 0, "grade", "📊", "Grade", "—", labels, is_selected=True)
        row = 1
        
        # If no criteria specified, show all available criteria
        if not criteria:
            criteria = CHECK_OPTIONS
            
        # Add score rows for all criteria (both selected and unselected)
        all_criteria_emojis = {
            "correctness": "✅", "security": "🔒", "performance": "⚡", 
            "clarity": "📖", "maintainability": "🔧", "logic": "🧠",
            "error handling": "🛡️", "testing": "🧪", "scalability": "📈",
            "documentation": "📝", "design": "🎨"
        }
        
        # Show selected criteria first (highlighted)
        for criterion in criteria:
            if criterion in all_criteria_emojis:
                emoji = all_criteria_emojis[criterion]
                self._add_score_row(grid, row, criterion, emoji, criterion.title(), "—", labels, is_selected=True)
                row += 1
        
        # Add separator for unselected criteria if we have selected ones
        if criteria and len(criteria) < len(CHECK_OPTIONS):
            separator = ttk.Separator(grid, orient="horizontal")
            separator.grid(row=row, column=0, columnspan=3, sticky="ew", pady=3)
            row += 1
            
            # Show unselected criteria (dimmed)
            unselected = [c for c in CHECK_OPTIONS if c not in criteria]
            for criterion in unselected[:3]:  # Limit to prevent overcrowding
                if criterion in all_criteria_emojis:
                    emoji = all_criteria_emojis[criterion]
                    self._add_score_row(grid, row, criterion, emoji, criterion.title(), "—", labels, is_selected=False)
                    row += 1
            
            if len(unselected) > 3:
                # Add "more..." indicator
                more_label = ttk.Label(grid, text="... +{} more criteria available".format(len(unselected) - 3), 
                                     style="Card.TLabel", font=("Segoe UI", 8), foreground="#888888")
                more_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=2)
                row += 1
        
        # Always show total at the end
        separator = ttk.Separator(grid, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=3, sticky="ew", pady=3)
        row += 1
        self._add_score_row(grid, row, "total", "🎯", "Average", "—", labels, is_selected=True)
        
        return labels
    
    def _add_score_row(self, parent: ttk.Frame, row: int, key: str, emoji: str, label: str, 
                      default_value: str, labels: Dict[str, ttk.Label], is_selected: bool = True):
        """Add a single score row to the grid"""
        # Create emoji label
        emoji_label = ttk.Label(parent, text=emoji, style="Card.TLabel")
        emoji_label.grid(row=row, column=0, sticky="w", padx=(0, 5), pady=1)
        
        # Create text label with conditional styling
        if is_selected:
            text_label = ttk.Label(parent, text=f"{label}:", style="Card.TLabel", 
                                 font=("Segoe UI", 9))
        else:
            text_label = ttk.Label(parent, text=f"{label}:", style="Card.TLabel", 
                                 font=("Segoe UI", 9), foreground="#666666")
        text_label.grid(row=row, column=1, sticky="w", padx=(0, 10), pady=1)
        
        # Create value label
        if is_selected:
            value_label = ttk.Label(parent, text=default_value, style="Card.TLabel", 
                                  font=("Consolas", 9, "bold"))
        else:
            value_label = ttk.Label(parent, text="—", style="Card.TLabel", 
                                  font=("Consolas", 9), foreground="#888888")
        value_label.grid(row=row, column=2, sticky="w", pady=1)
        
        # Store reference for updates
        labels[key] = value_label

    # Event handlers and business logic methods
    def _paste(self):
        """Paste clipboard content to the reply text widget"""
        try:
            clipboard_content = self.clipboard_get()
            self.reply.delete("1.0", "end")
            self.reply.insert("1.0", clipboard_content)
        except:
            messagebox.showwarning("Paste Error", "Could not paste from clipboard")

    def _load_file(self):
        """Load a file into the reply text widget"""
        file_path = filedialog.askopenfilename(
            title="Select file to review",
            filetypes=[
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("TypeScript files", "*.ts"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.reply.delete("1.0", "end")
                self.reply.insert("1.0", content)
                self.goal_var.set(f"Review the code in {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("File Error", f"Could not load file: {e}")

    def on_evaluate(self):
        """Start the evaluation process with enhanced feedback"""
        if self._thread and self._thread.is_alive():
            messagebox.showwarning("Busy", "Already evaluating...")
            return

        goal = self.goal_var.get().strip()
        context = self.ctx.get("1.0", "end").strip()
        claude_reply = self.reply.get("1.0", "end").strip()
        
        if not claude_reply:
            messagebox.showwarning("Missing Input", "Please provide Claude's reply to evaluate")
            return

        checks = [k for k, v in self.chk_vars.items() if v.get()]
        fast_mode = self.fast_var.get()

        # Enhanced status feedback with criteria count
        mode_text = "FAST" if fast_mode else "FULL"
        criteria_count = len(checks)
        if criteria_count == 0:
            criteria_text = "general review"
        elif criteria_count == len(CHECK_OPTIONS):
            criteria_text = "all criteria"
        else:
            criteria_text = f"{criteria_count} criteria"
            
        self.status.config(text=f"🔄 Evaluating ({mode_text} Mode, {criteria_text})...")
        self.pb.config(value=10)
        
        # Update criteria summary to show evaluation in progress
        self.criteria_summary.config(state="normal", fg="#facc15")
        self.criteria_summary.delete("1.0", "end")
        self.criteria_summary.insert("1.0", f"⚡ Evaluating with {criteria_text}...")
        self.criteria_summary.config(state="disabled")
        
        def worker():
            try:
                if fast_mode:
                    result = fast_evaluate(claude_reply, goal, context, checks)
                else:
                    result = full_evaluate(claude_reply, goal, context, checks)
                self._q.put(("result", result))
            except Exception as e:
                self._q.put(("error", str(e)))

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()

    def save_json(self):
        """Save the current results to a JSON file"""
        if not self.result_json:
            messagebox.showwarning("No Data", "No evaluation results to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save JSON Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.result_json, f, indent=2)
                messagebox.showinfo("Saved", f"Results saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {e}")

    def export_report(self):
        """Export a formatted report"""
        if not self.result_json:
            messagebox.showwarning("No Data", "No evaluation results to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                report = self._generate_report()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Exported", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export report: {e}")

    def _generate_report(self) -> str:
        """Generate a comprehensive formatted markdown report with criteria analysis"""
        if not self.result_json:
            return "# No Results Available"
            
        result = self.result_json
        selected_criteria = result.get('selected_criteria', [])
        criteria_text = ", ".join(selected_criteria) if selected_criteria else "General review"
        
        report = f"""# {AGENT_NAME} V10 Code Review Report

## Executive Summary
- **Evaluation Mode**: {result.get('mode', 'Unknown')}
- **Review Criteria**: {criteria_text} ({len(selected_criteria)} criteria)
- **Overall Winner**: {result.get('winner', 'Unknown')}
- **Final Grade**: {result.get('final', {}).get('grade', 'N/A')}
- **Report Generated**: {threading.current_thread().name}

## Evaluation Criteria Analysis
"""
        
        # Add criteria-specific breakdown
        if selected_criteria:
            report += f"### Selected Criteria ({len(selected_criteria)} of {len(CHECK_OPTIONS)} available):\n"
            for criterion in selected_criteria:
                # Get criterion description
                descriptions = {
                    "correctness": "Code accuracy, logic soundness, and correct implementation",
                    "security": "Vulnerability assessment, secure coding practices, data protection",
                    "performance": "Efficiency, speed optimization, resource usage, scalability",
                    "clarity": "Code readability, naming conventions, structure organization",
                    "maintainability": "Future-proofing, modularity, ease of modification",
                    "logic": "Reasoning flow, algorithm design, decision-making processes",
                    "error handling": "Exception management, edge cases, fault tolerance",
                    "testing": "Test coverage, testability, quality assurance approaches",
                    "scalability": "Growth handling, load management, architectural flexibility",
                    "documentation": "Code comments, API docs, usage examples, explanations",
                    "design": "Architecture patterns, design principles, structural quality"
                }
                desc = descriptions.get(criterion.lower(), "General assessment")
                report += f"- **{criterion.title()}**: {desc}\n"
        
        # Comparative scoring table
        report += f"\n## Comparative Scoring\n\n| Criterion | Reviewer A | Reviewer B | Final/Judge |\n|-----------|------------|------------|-------------|\n"
        
        a_scores = result.get('a_review', {}).get('scores', {})
        b_scores = result.get('b_review', {}).get('scores', {})
        final_scores = result.get('final', {}).get('scores', {})
        
        # Add score rows for selected criteria
        for criterion in selected_criteria:
            normalized = criterion.replace(" ", "_").replace("-", "_").lower()
            a_score = a_scores.get(normalized, "—")
            b_score = b_scores.get(normalized, "—")
            final_score = final_scores.get(normalized, "—")
            report += f"| {criterion.title()} | {a_score}/10 | {b_score}/10 | {final_score}/10 |\n"
        
        # Add average scores
        report += f"| **Average** | **{result.get('a_avg_score', 'N/A')}/10** | **{result.get('b_avg_score', 'N/A')}/10** | **{result.get('final_avg_score', 'N/A')}/10** |\n"

        report += f"""

## Reviewer A: {result.get('a_name', 'Unknown')}
**Provider**: {REVIEWER_A_PROVIDER.title()} ({REVIEWER_A_MODEL})  
**Average Score**: {result.get('a_avg_score', 'N/A')}/10
"""
        
        a_review = result.get('a_review', {})
        if 'summary' in a_review:
            report += f"\n### Analysis Summary\n{a_review['summary']}\n"
            
        if 'issues' in a_review and a_review['issues']:
            report += "\n### Key Issues Identified\n"
            for issue in a_review['issues'][:5]:  # Limit to top 5
                severity = issue.get('severity', 'unknown').upper()
                issue_type = issue.get('type', 'general').title()
                message = issue.get('msg', 'No details provided')
                report += f"- **{severity} - {issue_type}**: {message}\n"
            
        report += f"""

## Reviewer B: {result.get('b_name', 'Unknown')}
**Provider**: {REVIEWER_B_PROVIDER.title()} ({REVIEWER_B_MODEL})  
**Average Score**: {result.get('b_avg_score', 'N/A')}/10
"""
        
        b_review = result.get('b_review', {})
        if 'summary' in b_review:
            report += f"\n### Analysis Summary\n{b_review['summary']}\n"
            
        if 'issues' in b_review and b_review['issues']:
            report += "\n### Key Issues Identified\n"
            for issue in b_review['issues'][:5]:  # Limit to top 5
                severity = issue.get('severity', 'unknown').upper()
                issue_type = issue.get('type', 'general').title()
                message = issue.get('msg', 'No details provided')
                report += f"- **{severity} - {issue_type}**: {message}\n"
        
        # Final judgment section
        final_review = result.get('final', {})
        if final_review:
            report += f"\n## Final Judgment\n**Average Score**: {result.get('final_avg_score', 'N/A')}/10\n"
            
            if 'summary' in final_review:
                report += f"\n### Judge's Assessment\n{final_review['summary']}\n"
                
            if 'winner' in final_review and 'reason' in final_review:
                report += f"\n### Winner Determination\n**Winner**: {final_review['winner']}\n**Reasoning**: {final_review['reason']}\n"
            
            if 'recommended_changes' in final_review and final_review['recommended_changes']:
                report += "\n### Recommended Changes\n"
                for change in final_review['recommended_changes'][:5]:
                    report += f"- {change}\n"
        
        # Solution section
        if 'solution' in result and result['solution'].strip():
            report += f"\n## AI-Generated Solution\n\n```\n{result['solution']}\n```\n"
        
        report += f"\n---\n*Generated by Mozart V10 Dynamic Review System*"
        
        return report

    def copy_json(self):
        """Copy JSON results to clipboard"""
        json_content = self.out.get("1.0", "end").strip()
        self._copy_to_clipboard(json_content, "JSON Results")

    def copy_solution(self):
        """Copy solution to clipboard"""
        solution_content = self.solution.get("1.0", "end").strip()
        self._copy_to_clipboard(solution_content, "Solution")

    def submit_to_claude(self):
        """Open Claude.ai with the solution"""
        solution_content = self.solution.get("1.0", "end").strip()
        if solution_content:
            # Copy to clipboard first
            self.clipboard_clear()
            self.clipboard_append(solution_content)
            # Open Claude.ai
            webbrowser.open("https://claude.ai/")
            self.status.config(text="🚀 Solution copied and Claude.ai opened")
            self.after(3000, lambda: self.status.config(text="🟢 Ready"))
        else:
            messagebox.showwarning("No Solution", "No solution available to submit")

    def _pump(self):
        """Process queue messages"""
        try:
            while True:
                msg_type, data = self._q.get_nowait()
                if msg_type == "result":
                    self._handle_result(data)
                elif msg_type == "error":
                    self._handle_error(data)
        except queue.Empty:
            pass
        finally:
            self.after(100, self._pump)

    def _handle_result(self, result: Dict[str, Any]):
        """Handle successful evaluation result"""
        self.result_json = result
        self.pb.config(value=100)
        mode_text = "FAST" if self.fast_var.get() else "FULL"
        self.status.config(text=f"✅ Evaluation complete ({mode_text})")
        
        # Get selected criteria from result
        selected_criteria = result.get("selected_criteria", [])
        
        # Recreate score blocks with the selected criteria for better visual representation
        self._scores_a = self._make_score_block(self.card_a, selected_criteria)
        self._scores_b = self._make_score_block(self.card_b, selected_criteria)
        
        # Update score cards with the new criteria-aware system
        self._update_score_card(self._scores_a, result.get("a_review", {}), selected_criteria)
        self._update_score_card(self._scores_b, result.get("b_review", {}), selected_criteria)
        
        # Update winner information
        final_data = result.get("final", {})
        winner = final_data.get("winner", result.get("winner", "Unknown"))
        reason = final_data.get("reason", "")
        
        winner_text = f"Winner: {winner}"
        if winner == "A":
            winner_text = f"🥇 {result.get('a_name', 'Reviewer A')}"
        elif winner == "B":
            winner_text = f"🥇 {result.get('b_name', 'Reviewer B')}"
        elif winner == "tie":
            winner_text = "🤝 Tie"
            
        self.winner_label.config(text=winner_text)
        self.winner_reason.config(text=reason)
        
        # Update JSON output with enhanced formatting
        self.out.delete("1.0", "end")
        
        # Create enhanced JSON output with criteria summary
        enhanced_output = {
            "mozart_v10_results": {
                "evaluation_summary": {
                    "mode": result.get("mode", "Unknown"),
                    "selected_criteria": result.get("selected_criteria", []),
                    "criteria_count": len(result.get("selected_criteria", [])),
                    "timestamp": threading.current_thread().name,
                    "winner": result.get("winner", "Unknown")
                },
                "reviewer_a": {
                    "name": result.get("a_name", "Unknown"),
                    "provider": REVIEWER_A_PROVIDER,
                    "model": REVIEWER_A_MODEL,
                    "avg_score": result.get("a_avg_score", "N/A"),
                    "detailed_review": result.get("a_review", {})
                },
                "reviewer_b": {
                    "name": result.get("b_name", "Unknown"), 
                    "provider": REVIEWER_B_PROVIDER,
                    "model": REVIEWER_B_MODEL,
                    "avg_score": result.get("b_avg_score", "N/A"),
                    "detailed_review": result.get("b_review", {})
                },
                "final_judgment": {
                    "avg_score": result.get("final_avg_score", "N/A"),
                    "detailed_analysis": result.get("final", {})
                },
                "solution": result.get("solution", "No solution provided"),
                "raw_data": result  # Keep original for compatibility
            }
        }
        
        self.out.insert("1.0", json.dumps(enhanced_output, indent=2))
        
        # Update solution
        self.solution.delete("1.0", "end")
        self.solution.insert("1.0", result.get("solution", "No solution provided"))
        
        # Restore criteria summary after evaluation
        self._update_criteria_summary()
        
        # Reset progress bar after a delay
        self.after(2000, lambda: self.pb.config(value=0))
        self.after(2000, lambda: self.status.config(text="🟢 Ready"))

    def _handle_error(self, error_msg: str):
        """Handle evaluation error"""
        self.pb.config(value=0)
        self.status.config(text="❌ Error occurred")
        messagebox.showerror("Evaluation Error", f"Error during evaluation:\n{error_msg}")
        
        # Restore criteria summary after error
        self._update_criteria_summary()
        
        self.after(2000, lambda: self.status.config(text="🟡 Ready"))

    def _update_score_card(self, score_labels: Dict[str, ttk.Label], review_data: Dict[str, Any], 
                          selected_criteria: Optional[List[str]] = None):
        """Update a score card with review data based on dynamic criteria"""
        scores = review_data.get("scores", {})
        grade = review_data.get("grade", "—")
        
        # Update grade
        if "grade" in score_labels:
            grade_text = grade.upper() if grade and grade != "—" else "—"
            score_labels["grade"].config(text=grade_text)
        
        # Normalize criteria names for score lookup
        def normalize_criterion(name: str) -> str:
            return name.replace(" ", "_").replace("-", "_").lower()
        
        # Update scores for selected criteria
        total_score = 0
        score_count = 0
        
        if selected_criteria:
            for criterion in selected_criteria:
                normalized = normalize_criterion(criterion)
                
                if criterion in score_labels:  # Label exists
                    if normalized in scores and isinstance(scores[normalized], (int, float)):
                        score_value = scores[normalized]
                        score_labels[criterion].config(text=f"{score_value}/10")
                        total_score += float(score_value)
                        score_count += 1
                    else:
                        score_labels[criterion].config(text="—")
        else:
            # Fallback: use all available scores
            for key, label in score_labels.items():
                if key in ["grade", "total"]:
                    continue
                
                normalized = normalize_criterion(key)
                if normalized in scores and isinstance(scores[normalized], (int, float)):
                    score_value = scores[normalized]
                    label.config(text=f"{score_value}/10")
                    total_score += float(score_value)
                    score_count += 1
                else:
                    label.config(text="—")
        
        # Update total average
        if "total" in score_labels:
            if score_count > 0:
                avg_score = total_score / score_count
                score_labels["total"].config(text=f"{avg_score:.1f}/10")
            else:
                score_labels["total"].config(text="—")
        
        # Update visual feedback for score quality
        if "grade" in score_labels and score_count > 0:
            avg_score = total_score / score_count
            if avg_score >= 8:
                grade_color = "#4ade80"  # Green for excellent
            elif avg_score >= 6:
                grade_color = "#facc15"  # Yellow for good
            elif avg_score >= 4:
                grade_color = "#fb923c"  # Orange for adequate
            else:
                grade_color = "#f87171"  # Red for poor
                
            # Apply color to the grade label
            score_labels["grade"].config(foreground=grade_color)


def main():
    """Main entry point"""
    try:
        app = ScrollableApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
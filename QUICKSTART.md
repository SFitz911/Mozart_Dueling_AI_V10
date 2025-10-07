# Mozart AI V10 - Quick Start Guide

## Initial Setup (3 minutes)

1. **Get API Keys**:
   - OpenAI: https://platform.openai.com/api-keys
   - DeepSeek: https://platform.deepseek.com/api-keys

2. **Run the Automated Setup**:
   - Find `setup.py` in your Mozart AI folder
   - **Double-click `setup.py`** (or right-click → "Open with Python")
   - A setup window will appear
   - Enter your API keys when prompted
   - Click "Setup Environment"
   - Wait for "Setup completed successfully!" ✅

## Launching Mozart AI (Choose One Method)

### Method 1: Use Launch Scripts (Easiest)
- **Windows**: Double-click `LAUNCH_GUI.bat` in File Explorer
- **PowerShell**: Right-click `LAUNCH_GUI.ps1` → "Run with PowerShell"  
- **Python**: Double-click `LAUNCH_GUI.py`

### Method 2: Run Mozart Directly
- **Right-click `mozart_monitorV10.py`** → "Open with Python"
- **Or from terminal/command prompt**: `python mozart_monitorV10.py`

### Method 3: Use Visual Studio Code (Recommended for Developers)

**Step 1: Open Project in VS Code**
1. **Download VS Code** from https://code.visualstudio.com (if you don't have it)
2. **Open VS Code**
3. Click **"File"** → **"Open Folder"**
4. **Navigate to your Mozart AI folder** (where all the files are)
5. Click **"Select Folder"** - You'll see all Mozart AI files on the left side!

**Step 2: Run Mozart AI from VS Code**
1. **Open the terminal** in VS Code: Press **Ctrl + `** (backtick key)
2. **Choose one of these commands** to run in the terminal:
   - `python LAUNCH_GUI.py` (uses launch script with error checking)
   - `python mozart_monitorV10.py` (runs Mozart AI directly)
   - `.\LAUNCH_GUI.bat` (runs Windows batch script)
   - `.\LAUNCH_GUI.ps1` (runs PowerShell script)

**Step 3: Perfect Workflow**
1. **Write/edit your code** in VS Code (beautiful syntax highlighting!)
2. **Save your file** (Ctrl + S)
3. **Copy your code** (Ctrl + A, then Ctrl + C)
4. **Switch to Mozart AI** (Alt + Tab) and paste your code
5. **Get AI feedback**, then return to VS Code to improve your code!

**Pro Tips for VS Code:**
- Keep VS Code and Mozart AI **side by side** on your screen
- Use **File Explorer** in VS Code to organize your projects
- Install the **Python extension** for better code editing
- **Terminal stays open** - you can run Mozart AI multiple times easily

## Quick Review (30 seconds)

Once Mozart AI is running:

1. **Goal**: "Review this function for bugs"
2. **Context**: "Python function for user authentication"  
3. **Paste Code**: [your code here] or click "Load Text File"
4. **Criteria**: Keep all checkboxes selected (or pick specific areas)
5. **Mode**: Fast (quick) or Full (comprehensive)
6. **Click**: "Start Review"

## Launch Method Details

### Method 1: Launch Scripts (Recommended)
**Why use launch scripts?**
- They automatically check if everything is set up correctly
- Show helpful error messages if something is wrong
- Handle dependencies and configuration automatically

**Which launch script to use?**
- **LAUNCH_GUI.bat**: Best for Windows beginners (just double-click!)
- **LAUNCH_GUI.ps1**: Best for PowerShell users (colorful output)
- **LAUNCH_GUI.py**: Best for Python users or cross-platform

### Method 2: Direct Python Execution
**When to use this method?**
- You want to run Mozart AI directly
- You're familiar with Python
- You're running from a code editor like VS Code

**How to run mozart_monitorV10.py:**
- **File Explorer**: Right-click → "Open with Python"
- **Command Prompt**: Open cmd, navigate to folder, type `python mozart_monitorV10.py`
- **PowerShell**: Open PowerShell, navigate to folder, type `python mozart_monitorV10.py`

### Method 3: VS Code (Best for Developers)
**Why use VS Code?**
- **Professional environment** - Syntax highlighting, auto-complete, error detection
- **Integrated terminal** - Run Mozart AI without leaving the editor
- **File management** - Easy to organize and switch between projects
- **Side-by-side workflow** - Edit code in VS Code, review in Mozart AI

**VS Code Terminal Commands:**
- `python LAUNCH_GUI.py` - **Recommended** (includes error checking)
- `python mozart_monitorV10.py` - Direct execution
- `.\LAUNCH_GUI.bat` - Windows batch script
- `.\LAUNCH_GUI.ps1` - PowerShell script

**Workflow Benefits:**
- **Edit → Save → Copy → Review → Improve** - Seamless cycle
- **Multiple projects** - Easy to switch between different code files
- **Version control** - Git integration if you want to track changes
- **Extensions** - Add tools for different programming languages

**Note**: If you get errors about missing API keys or dependencies, use Method 1 instead!

## Output Options

- **Score Cards**: Visual comparison of AI reviewers
- **JSON**: Structured data for tools/CI/CD
- **Reports**: Professional markdown documentation
- **Copy**: Clipboard export for sharing

## Pro Tips

- **Security Reviews**: Select "security", "error handling", "logic"
- **Performance**: Choose "performance", "scalability", "design"  
- **Code Quality**: Pick "clarity", "maintainability", "documentation"
- **Full Analysis**: Select all 11 criteria + Full Mode

## Quick Troubleshooting

**If Mozart AI won't start:**
1. **Run `verify_setup.py`** - Double-click it to see what's broken
2. **Try setup.py again** - Re-run the setup if configuration is missing
3. **Check Python installation** - Make sure Python is installed correctly

**If you get API key errors:**
1. **Run setup.py again** and re-enter your API keys
2. **Check for typos** - Make sure keys are copied correctly (no extra spaces)
3. **Verify keys are active** - Test them on the respective AI platforms

**Still having issues?**
- Check `README.md` for detailed instructions
- Read `SETUP_INSTRUCTIONS.md` for comprehensive troubleshooting

That's it! Mozart AI will analyze your code with competing AI reviewers. 🎭
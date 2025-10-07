#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mozart Dueling AI Setup Script
Automatically sets up the environment and configures API keys through a GUI.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path
import json

# Constants
PROJECT_ROOT = Path(__file__).parent
ENV_FILE = PROJECT_ROOT / ".env.mozart"
ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.mozart.example"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

class SetupGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mozart Dueling AI - Setup")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # API key variables
        self.openai_key = tk.StringVar()
        self.deepseek_key = tk.StringVar()
        
        # Setup completed flag
        self.setup_completed = False
        
        self.create_widgets()
        self.check_existing_config()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Mozart Dueling AI Setup", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        desc_text = ("Welcome to Mozart Dueling AI!\n\n"
                    "This setup will:\n"
                    "• Install required Python packages\n"
                    "• Configure your API keys\n"
                    "• Create launch scripts\n\n"
                    "Please provide your API keys below:")
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify="left")
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # API Keys section
        api_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding="10")
        api_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        api_frame.columnconfigure(1, weight=1)
        
        # OpenAI API Key
        ttk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky="w", pady=5)
        openai_entry = ttk.Entry(api_frame, textvariable=self.openai_key, show="*", width=50)
        openai_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Button(api_frame, text="Show", 
                  command=lambda: self.toggle_password(openai_entry)).grid(row=0, column=2, padx=(5, 0))
        
        # DeepSeek API Key
        ttk.Label(api_frame, text="DeepSeek API Key:").grid(row=1, column=0, sticky="w", pady=5)
        deepseek_entry = ttk.Entry(api_frame, textvariable=self.deepseek_key, show="*", width=50)
        deepseek_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Button(api_frame, text="Show", 
                  command=lambda: self.toggle_password(deepseek_entry)).grid(row=1, column=2, padx=(5, 0))
        
        # Help text
        help_text = ("• OpenAI API Key: Get from https://platform.openai.com/api-keys\n"
                    "• DeepSeek API Key: Get from https://platform.deepseek.com/api-keys\n"
                    "• Both keys are required for full functionality")
        
        help_label = ttk.Label(api_frame, text=help_text, font=("Arial", 8), foreground="gray")
        help_label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(10, 0))
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to setup...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Check Dependencies", 
                  command=self.check_dependencies).pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="Setup Environment", 
                  command=self.setup_environment).pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side="right")
    
    def toggle_password(self, entry_widget):
        """Toggle password visibility"""
        if entry_widget['show'] == '*':
            entry_widget.config(show='')
        else:
            entry_widget.config(show='*')
    
    def check_existing_config(self):
        """Check if configuration already exists"""
        if ENV_FILE.exists():
            try:
                with open(ENV_FILE, 'r') as f:
                    content = f.read()
                    
                # Extract existing keys
                for line in content.split('\n'):
                    if line.startswith('OPENAI_API_KEY=') and not line.endswith('your_openai_api_key_here'):
                        key = line.split('=', 1)[1].strip()
                        if key and key != 'your_openai_api_key_here':
                            self.openai_key.set('*' * 20)  # Show asterisks for existing key
                    elif line.startswith('DEEPSEEK_API_KEY=') and not line.endswith('your_deepseek_api_key_here'):
                        key = line.split('=', 1)[1].strip()
                        if key and key != 'your_deepseek_api_key_here':
                            self.deepseek_key.set('*' * 20)  # Show asterisks for existing key
                
                if self.openai_key.get() or self.deepseek_key.get():
                    self.progress_var.set("Existing configuration found. You can update API keys if needed.")
                    
            except Exception as e:
                print(f"Error reading existing config: {e}")
    
    def check_dependencies(self):
        """Check if Python dependencies are installed"""
        self.progress_var.set("Checking dependencies...")
        self.progress_bar['value'] = 20
        self.root.update()
        
        try:
            # Check if required packages are available
            import requests
            import tkinter
            from dotenv import load_dotenv
            
            self.progress_var.set("All dependencies are installed!")
            self.progress_bar['value'] = 100
            messagebox.showinfo("Dependencies", "All required dependencies are installed!")
            
        except ImportError as e:
            self.progress_var.set("Missing dependencies detected.")
            self.progress_bar['value'] = 0
            
            result = messagebox.askyesno("Missing Dependencies", 
                                       f"Missing required packages.\n\nWould you like to install them automatically?")
            if result:
                self.install_dependencies()
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.progress_var.set("Installing dependencies...")
        self.progress_bar['value'] = 30
        self.root.update()
        
        try:
            # Install requirements
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)], 
                                  capture_output=True, text=True, check=True)
            
            self.progress_var.set("Dependencies installed successfully!")
            self.progress_bar['value'] = 100
            messagebox.showinfo("Success", "Dependencies installed successfully!")
            
        except subprocess.CalledProcessError as e:
            self.progress_var.set("Failed to install dependencies.")
            self.progress_bar['value'] = 0
            messagebox.showerror("Error", f"Failed to install dependencies:\n{e.stderr}")
        except Exception as e:
            self.progress_var.set("Error during installation.")
            self.progress_bar['value'] = 0
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def validate_api_keys(self):
        """Validate that API keys are provided"""
        openai_key = self.openai_key.get().strip()
        deepseek_key = self.deepseek_key.get().strip()
        
        # Skip validation if showing existing keys (asterisks)
        if openai_key.startswith('*') and deepseek_key.startswith('*'):
            return True
        
        if not openai_key or openai_key == 'your_openai_api_key_here':
            messagebox.showerror("Missing API Key", "Please provide your OpenAI API key.")
            return False
        
        if not deepseek_key or deepseek_key == 'your_deepseek_api_key_here':
            messagebox.showerror("Missing API Key", "Please provide your DeepSeek API key.")
            return False
        
        return True
    
    def setup_environment(self):
        """Setup the environment with API keys"""
        if not self.validate_api_keys():
            return
        
        self.progress_var.set("Setting up environment...")
        self.progress_bar['value'] = 25
        self.root.update()
        
        try:
            # Read template if .env.mozart doesn't exist or if we have new keys
            if not ENV_FILE.exists() or not (self.openai_key.get().startswith('*') and self.deepseek_key.get().startswith('*')):
                if ENV_EXAMPLE_FILE.exists():
                    with open(ENV_EXAMPLE_FILE, 'r') as f:
                        content = f.read()
                else:
                    content = self.get_default_env_content()
                
                # Replace API keys if they're not asterisks (existing keys)
                if not self.openai_key.get().startswith('*'):
                    content = content.replace('your_openai_api_key_here', self.openai_key.get().strip())
                
                if not self.deepseek_key.get().startswith('*'):
                    content = content.replace('your_deepseek_api_key_here', self.deepseek_key.get().strip())
                
                # Write to .env.mozart
                with open(ENV_FILE, 'w') as f:
                    f.write(content)
            
            self.progress_bar['value'] = 50
            self.root.update()
            
            # Create launch scripts
            self.create_launch_scripts()
            
            self.progress_bar['value'] = 100
            self.progress_var.set("Setup completed successfully!")
            self.setup_completed = True
            
            messagebox.showinfo("Setup Complete", 
                              "Mozart Dueling AI has been set up successfully!\n\n"
                              "Launch scripts created:\n"
                              "• LAUNCH_GUI.bat\n"
                              "• LAUNCH_GUI.ps1\n"
                              "• LAUNCH_GUI.py\n\n"
                              "You can now close this setup and use any of the launch scripts.")
            
        except Exception as e:
            self.progress_var.set("Setup failed.")
            self.progress_bar['value'] = 0
            messagebox.showerror("Setup Error", f"Failed to setup environment:\n{str(e)}")
    
    def get_default_env_content(self):
        """Get default environment file content if template doesn't exist"""
        return """# Mozart AI Environment Configuration
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# API Base URLs
OPENAI_BASE_URL=https://api.openai.com
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Model Configuration
OPENAI_MODEL=gpt-4o
DEEPSEEK_MODEL=deepseek-coder

# Reviewer Configuration
REVIEWER_A_NAME=Senior Engineer
REVIEWER_A_PROVIDER=openai
REVIEWER_A_MODEL=gpt-4o

REVIEWER_B_NAME=Code Specialist
REVIEWER_B_PROVIDER=deepseek
REVIEWER_B_MODEL=deepseek-coder

# Judge Configuration
JUDGE_PROVIDER=openai
JUDGE_MODEL=gpt-4o
"""
    
    def create_launch_scripts(self):
        """Create launch scripts for different environments"""
        self.progress_var.set("Creating launch scripts...")
        
        # Python script
        py_content = f'''#!/usr/bin/env python3
"""Launch Mozart Dueling AI"""
import os
import sys
from pathlib import Path

# Change to script directory
os.chdir(Path(__file__).parent)

# Import and run Mozart
try:
    import mozart_monitorV10
    if hasattr(mozart_monitorV10, 'main'):
        mozart_monitorV10.main()
    else:
        # If no main function, run the GUI directly
        print("Starting Mozart Dueling AI GUI...")
        exec(open('mozart_monitorV10.py').read())
except ImportError as e:
    print(f"Error: {{e}}")
    print("Please run setup.py first to install dependencies.")
    sys.exit(1)
except Exception as e:
    print(f"Error starting Mozart: {{e}}")
    sys.exit(1)
'''
        
        # Batch script
        bat_content = f'''@echo off
echo Starting Mozart Dueling AI...
cd /d "{PROJECT_ROOT}"
python LAUNCH_GUI.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start Mozart Dueling AI
    echo Please run setup.py first to install dependencies.
    pause
)
'''
        
        # PowerShell script
        ps1_content = f'''# Mozart Dueling AI Launcher
Write-Host "Starting Mozart Dueling AI..." -ForegroundColor Green

# Change to script directory
Set-Location "{PROJECT_ROOT}"

# Try to run Mozart
try {{
    python LAUNCH_GUI.py
    if ($LASTEXITCODE -ne 0) {{
        throw "Python script failed with exit code $LASTEXITCODE"
    }}
}}
catch {{
    Write-Host "Error: Failed to start Mozart Dueling AI" -ForegroundColor Red
    Write-Host "Please run setup.py first to install dependencies." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}}
'''
        
        # Write launch scripts
        scripts = [
            ("LAUNCH_GUI.py", py_content),
            ("LAUNCH_GUI.bat", bat_content),
            ("LAUNCH_GUI.ps1", ps1_content)
        ]
        
        for filename, content in scripts:
            script_path = PROJECT_ROOT / filename
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Make Python script executable on Unix systems
            if filename.endswith('.py'):
                try:
                    os.chmod(script_path, 0o755)
                except:
                    pass  # Windows doesn't support chmod
    
    def run(self):
        """Run the setup GUI"""
        self.root.mainloop()
        return self.setup_completed

def main():
    """Main setup function"""
    print("Mozart Dueling AI Setup")
    print("======================")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    
    # Create and run GUI
    setup_gui = SetupGUI()
    completed = setup_gui.run()
    
    if completed:
        print("\nSetup completed successfully!")
        print("You can now run Mozart Dueling AI using:")
        print("  • LAUNCH_GUI.bat (Windows)")
        print("  • LAUNCH_GUI.ps1 (PowerShell)")
        print("  • LAUNCH_GUI.py (Python)")
    else:
        print("\nSetup was cancelled or incomplete.")

if __name__ == "__main__":
    main()
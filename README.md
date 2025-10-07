# Mozart AI V10 - Dueling AI Code Review System 🎵

**A beginner-friendly AI tool that reviews your code using two different AI systems to give you better feedback!**

[![GitHub Repository](https://img.shields.io/badge/GitHub-Mozart_Dueling_AI_V10-blue.svg)](https://github.com/SFitz911/Mozart_Dueling_AI_V10)
![Mozart AI V10](https://img.shields.io/badge/Mozart-V10-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📥 Quick Installation

```bash
git clone https://github.com/SFitz911/Mozart_Dueling_AI_V10.git
cd Mozart_Dueling_AI_V10
python setup.py
```

## 🧪 Want to Test It Right Away?

**Check out `TEST_ERRORS.md`** - it contains real coding errors you can copy and paste to see Mozart AI in action! Perfect for:
- Testing the dual AI system
- Learning from common coding mistakes
- Breaking out of AI error loops with Cursor, Claude, etc.
- Seeing how multiple AI perspectives solve problems differently

## 🎯 What Does This Do?

Mozart AI is like having two expert programmers review your code at the same time! It uses two different AI systems (OpenAI's GPT-4 and DeepSeek) to:
- ✅ Check your code for bugs and problems
- 💡 Suggest improvements to make your code better
- 🔒 Find security issues that could be dangerous
- 📊 Give you detailed scores and explanations

**Think of it like having a friendly coding mentor that never gets tired and always gives detailed feedback!**

## ✨ What Can It Check?

Mozart AI can review your code for these important things:

🔍 **Correctness** - Does your code actually work correctly?
🔒 **Security** - Are there any security vulnerabilities?
⚡ **Performance** - Could your code run faster?
📖 **Clarity** - Is your code easy to read and understand?
🔧 **Maintainability** - Will it be easy to modify later?
🧠 **Logic** - Does the logic make sense?
⚠️ **Error Handling** - Does it handle errors properly?
🧪 **Testing** - Does it need more tests?
📈 **Scalability** - Will it work with lots of data?
📝 **Documentation** - Are there enough comments?
🏗️ **Design** - Is the code structure good?

## 🖥️ Easy-to-Use Interface

- **Simple Buttons**: Just click buttons to start reviews
- **Color Coding**: Green = good, Red = needs work, Yellow = in progress
- **Easy Reading**: Results are shown in plain English
- **Copy & Paste**: Easy to copy results to share with others

## � Recommended: Use Visual Studio Code (VS Code)

**What is VS Code?** It's a free, beginner-friendly code editor that makes working with code much easier!

### Why Use VS Code with Mozart AI?
- 📝 **Better Code Editing**: Syntax highlighting makes code colorful and easier to read
- 🔍 **Built-in Terminal**: Run Mozart AI directly from VS Code
- 📁 **File Management**: Easy to organize and open your code files
- 🎨 **Themes**: Make coding look pretty with dark/light themes
- 🔧 **Extensions**: Add helpful tools for different programming languages
- 💡 **IntelliSense**: Auto-complete and suggestions while typing

### How to Install and Set Up VS Code

**Step 1: Download VS Code**
1. Go to: **https://code.visualstudio.com**
2. Click the big blue **"Download for Windows"** button
3. Run the downloaded file
4. Follow the installation wizard (just click "Next" for everything)
5. **Check the box "Add to PATH"** if you see it

**Step 2: Open Your Mozart AI Project in VS Code**
1. **Open VS Code** (look for it in your Start menu)
2. Click **"File"** → **"Open Folder"**
3. Navigate to your Mozart AI folder (where setup.py is located)
4. Click **"Select Folder"**
5. VS Code will now show all your Mozart AI files on the left side!

**Step 3: Set Up the Terminal in VS Code**
1. In VS Code, press **Ctrl + `** (that's the backtick key, usually above Tab)
2. Or go to **"Terminal"** → **"New Terminal"**
3. A terminal will appear at the bottom of VS Code
4. You can now run Mozart AI commands directly from here!

### Using Mozart AI with VS Code

**Option A: Run Setup from VS Code**
1. Open VS Code with your Mozart AI folder
2. Open the terminal (Ctrl + `)
3. Type: `python setup.py`
4. The setup window will appear!

**Option B: Launch Mozart from VS Code**
1. In the VS Code terminal, type one of these:
   - `python LAUNCH_GUI.py` (direct Python)
   - `.\LAUNCH_GUI.bat` (batch file)
   - `.\LAUNCH_GUI.ps1` (PowerShell)

**Option C: Edit Code in VS Code, Review with Mozart**
1. **Write or edit your code** in VS Code (it looks beautiful with syntax highlighting!)
2. **Save your file** (Ctrl + S)
3. **Copy your code** (Ctrl + A, then Ctrl + C)
4. **Switch to Mozart AI** and paste your code for review
5. **Get feedback** and improve your code!

### Helpful VS Code Extensions for Beginners

**To install extensions:**
1. Click the **Extensions** icon on the left (looks like building blocks)
2. Search for the extension name
3. Click **"Install"**

**Recommended Extensions:**
- 🐍 **Python** - Essential for Python coding
- 🎨 **Prettier** - Makes your code look neat and organized
- 🌙 **One Dark Pro** - Beautiful dark theme
- 📁 **Material Icon Theme** - Pretty file icons
- 🔍 **Error Lens** - Shows errors right in your code

### VS Code Tips for Beginners

**Basic Shortcuts:**
- **Ctrl + S** - Save file
- **Ctrl + Z** - Undo
- **Ctrl + C** - Copy
- **Ctrl + V** - Paste
- **Ctrl + F** - Find text
- **Ctrl + `** - Open/close terminal

**Viewing Files:**
- Click any file in the **Explorer** (left panel) to open it
- **Right-click** files for more options
- **Drag files** around to organize them

**Making Code Look Pretty:**
- Right-click in your code → **"Format Document"**
- Or press **Shift + Alt + F**

## �🚀 Getting Started (Super Easy!)

**Don't worry - you don't need to be a tech expert! Just follow these simple steps:**

### Step 1: Make Sure You Have Python

**What is Python?** Python is a programming language that Mozart AI needs to run.

**Do I have Python?** Let's check:
1. Press `Windows Key + R` on your keyboard
2. Type `cmd` and press Enter
3. In the black window that opens, type: `python --version`
4. If you see something like "Python 3.11.4", you have Python! ✅
5. If you see an error, you need to install Python ❌

**If you need to install Python:**
1. Go to https://python.org/downloads
2. Click the big yellow "Download Python" button
3. Run the downloaded file
4. **IMPORTANT**: Check the box that says "Add Python to PATH" ⚠️
5. Click "Install Now"

### Step 2: Get Your AI API Keys

**What are API Keys?** Think of them like passwords that let Mozart AI talk to the AI services.

You need two keys:
1. **OpenAI API Key** (for GPT-4)
2. **DeepSeek API Key** (for DeepSeek)

**Getting OpenAI API Key:**
1. Go to https://platform.openai.com
2. Click "Sign Up" or "Log In"
3. Once logged in, click "API Keys" on the left side
4. Click "Create new secret key"
5. Copy the key (it starts with "sk-...")
6. **Keep this safe!** You can't see it again

**Getting DeepSeek API Key:**
1. Go to https://platform.deepseek.com
2. Sign up for an account
3. Go to API Keys section
4. Generate a new key
5. Copy and save the key

### Step 3: Run the Easy Setup

**This is the magic part - Mozart AI will set itself up!**

1. **Find Mozart AI folder**: Open File Explorer and navigate to where you downloaded Mozart AI
2. **Open the folder**: You should see files like `setup.py`, `LAUNCH_GUI.bat`, etc.
3. **Right-click** on `setup.py`
4. Choose **"Open with" → "Python"** (or just double-click if Python opens .py files)
5. **A window will pop up** - this is the setup wizard! 🧙‍♂️

**In the setup window:**
1. Click "Check Dependencies" (it will install anything missing)
2. Enter your OpenAI API key in the first box
3. Enter your DeepSeek API key in the second box
4. Click "Setup Environment"
5. Wait for it to say "Setup completed successfully!" ✅

### Step 4: Launch Mozart AI

**Now the fun part - actually using Mozart AI!**

You have 3 easy ways to start Mozart AI:

**Option A: Windows Batch File (Easiest)**
1. In File Explorer, find `LAUNCH_GUI.bat`
2. **Double-click it** (outside of VS Code, just in regular File Explorer)
3. A black window will appear, then Mozart AI will start!

**Option B: PowerShell (Pretty Easy)**
1. In File Explorer, find `LAUNCH_GUI.ps1`
2. **Right-click** on it
3. Choose **"Run with PowerShell"**
4. Mozart AI will start with colorful messages!

**Option C: Python Direct (For Tech-Savvy Users)**
1. In File Explorer, find `LAUNCH_GUI.py`
2. **Double-click it** or right-click and choose "Open with Python"

## 🔧 Troubleshooting & Verification

### If Something Goes Wrong

**Run the Verification Tool:**
1. In File Explorer, find `verify_setup.py`
2. **Double-click it** or right-click and choose "Open with Python"
3. It will check everything and tell you what's wrong

**Common Problems and Solutions:**

❌ **"Python is not recognized"**
- Solution: Reinstall Python and check "Add Python to PATH"

❌ **"Missing dependencies"**
- Solution: Run `setup.py` again and let it install missing parts

❌ **"Invalid API key"**
- Solution: Check your API keys are copied correctly (no extra spaces)

❌ **PowerShell won't run**
- Solution: Open PowerShell as Administrator and run: `Set-ExecutionPolicy RemoteSigned`

### Getting Help

If you're still stuck:
1. Run `verify_setup.py` and take a screenshot of the results
2. Check `SETUP_INSTRUCTIONS.md` for detailed help
3. Make sure you followed each step exactly

## 🎵 Using Mozart AI

Once Mozart AI starts:

1. **Load Your Code**: Click "Load Text File" or paste code into the big text box
2. **Choose What to Check**: Check the boxes for what you want reviewed (you can pick all of them!)
3. **Pick Review Mode**: 
   - **Fast Mode**: Quick review from both AIs
   - **Full Mode**: Detailed review with a judge AI
4. **Start Review**: Click the big "Start Review" button
5. **Wait**: The AIs will work on your code (this takes a minute or two)
6. **See Results**: You'll get detailed feedback, scores, and suggestions!

## 🔄 Perfect Workflow: VS Code + Mozart AI

**Here's the best way to write and improve code using both tools together:**

### Method 1: Side-by-Side Workflow
1. **Open VS Code** with your Mozart AI folder
2. **Start Mozart AI** from VS Code terminal: `python LAUNCH_GUI.py`
3. **Position windows side by side**:
   - VS Code on the left half of your screen
   - Mozart AI on the right half of your screen
4. **Write code in VS Code**, then **copy and paste into Mozart AI** for review
5. **Get feedback**, then **go back to VS Code** to make improvements
6. **Repeat until your code is perfect!**

### Method 2: File-Based Workflow
1. **Write your code** in VS Code and **save it** (Ctrl + S)
2. **Open Mozart AI**
3. **Click "Load Text File"** in Mozart AI
4. **Select your saved file** from VS Code
5. **Get your review**, then **switch back to VS Code** to edit
6. **Save again** and reload in Mozart AI to see improvements

### Method 3: Copy-Paste Workflow (Easiest)
1. **Write code in VS Code** (it looks prettier with syntax highlighting!)
2. **Select all your code** (Ctrl + A)
3. **Copy it** (Ctrl + C)
4. **Switch to Mozart AI**
5. **Paste in the text box** (Ctrl + V)
6. **Run your review**
7. **Copy suggestions back to VS Code** and improve your code

### Pro Tips for VS Code + Mozart AI

**🎯 Organize Your Files:**
- Create a **"projects"** folder in VS Code
- Keep each coding project in its own subfolder
- Use Mozart AI to review each file before you consider it "done"

**⚡ Quick Switching:**
- Use **Alt + Tab** to quickly switch between VS Code and Mozart AI
- Pin both applications to your taskbar for easy access

**📝 Save Your Reviews:**
- Copy Mozart AI feedback and paste it as comments in your VS Code files
- Create a **"reviews"** folder to save Mozart AI reports
- Use the "Copy to Clipboard" features in Mozart AI

**🔄 Iterative Improvement:**
1. Write code in VS Code
2. Review with Mozart AI
3. Fix issues highlighted by Mozart AI
4. Review again to see improvement
5. Repeat until you get high scores!

**📊 Track Your Progress:**
- Take screenshots of your Mozart AI scores
- Save before/after versions of your code
- See how your coding improves over time!
REVIEWER_A_NAME=Senior Engineer
REVIEWER_A_PROVIDER=openai
REVIEWER_B_NAME=Code Specialist
REVIEWER_B_PROVIDER=deepseek

# Optional: System settings
TIMEOUT_SECONDS=60
LOG_LEVEL=INFO
AGENT_NAME=Mozart
```

## 📋 Usage Guide

## 📋 Decision Tree - What Should I Do?

**Follow this simple flowchart to get Mozart AI working:**

```
🏁 START: Do you want to use Mozart AI?
    │
    ├─ � Step 0: Get VS Code (RECOMMENDED)
    │   ├─ Go to code.visualstudio.com
    │   ├─ Download and install VS Code
    │   ├─ Open your Mozart AI folder in VS Code
    │   └─ Now you have a professional coding setup! → Go to Step 1
    │
    ├─ �📱 Step 1: Do you have Python installed?
    │   ├─ ✅ YES → Go to Step 2
    │   └─ ❌ NO → Install Python from python.org (check "Add to PATH") → Go to Step 2
    │
    ├─ 🔑 Step 2: Do you have API keys?
    │   ├─ ✅ YES (both OpenAI & DeepSeek) → Go to Step 3
    │   ├─ 🔸 PARTIAL (only one) → Get the missing key → Go to Step 3
    │   └─ ❌ NO → Get keys from:
    │       ├─ OpenAI: platform.openai.com/api-keys
    │       └─ DeepSeek: platform.deepseek.com/api-keys
    │       └─ Go to Step 3
    │
    ├─ ⚙️ Step 3: Run Setup
    │   ├─ Find setup.py in Mozart AI folder (or VS Code)
    │   ├─ Right-click → "Open with Python" (or double-click)
    │   ├─ Follow the setup wizard
    │   ├─ Enter your API keys when asked
    │   ├─ Click "Setup Environment"
    │   └─ Wait for "Setup completed successfully!"
    │
    ├─ 🚀 Step 4: Launch Mozart AI
    │   ├─ 🥇 EASIEST: Double-click LAUNCH_GUI.bat (in File Explorer)
    │   ├─ 🥈 PRETTY EASY: Right-click LAUNCH_GUI.ps1 → "Run with PowerShell"
    │   ├─ 🥉 ALTERNATIVE: Double-click LAUNCH_GUI.py
    │   └─ 💻 VS CODE: Open terminal in VS Code, type: python LAUNCH_GUI.py
    │
    ├─ ❓ Having Problems?
    │   ├─ Run verify_setup.py (double-click it)
    │   ├─ Check what's broken
    │   ├─ Read SETUP_INSTRUCTIONS.md
    │   └─ Try setup.py again
    │
    └─ 🎉 SUCCESS: Mozart AI is running!
        ├─ Write code in VS Code (looks beautiful!)
        ├─ Copy code to Mozart AI for review
        ├─ Pick what to check (all the checkboxes)
        ├─ Choose Fast Mode or Full Mode
        ├─ Click "Start Review"
        ├─ Get awesome AI feedback! 🎵
        └─ Go back to VS Code and improve your code!
```

## � Quick Problem Solver

**Pick your problem:**

🔴 **"Python is not recognized"**
- Install Python from python.org
- Make sure "Add Python to PATH" is checked
- Restart your computer

🔴 **"Setup.py won't run"**
- Right-click setup.py → "Open with" → Choose Python
- Or open Command Prompt, navigate to folder, type: `python setup.py`

🔴 **"Can't run LAUNCH_GUI.bat"**
- Make sure you're double-clicking in File Explorer (not VS Code)
- Try LAUNCH_GUI.py instead

🔴 **"PowerShell execution policy error"**
- Open PowerShell as Administrator
- Type: `Set-ExecutionPolicy RemoteSigned`
- Press Y and Enter

🔴 **"Invalid API key error"**
- Check your keys don't have extra spaces
- Make sure they're the right keys (OpenAI starts with "sk-")
- Try running setup.py again

🔴 **"Missing packages error"**
- Run setup.py again
- Let it install missing packages automatically
- Or run: `pip install -r requirements.txt`

## 🎯 Summary

Mozart AI makes code review easy and fun! Just:
1. **Install Python** (if you don't have it)
2. **Get API keys** (from OpenAI and DeepSeek)
3. **Run setup.py** (it does everything automatically)
4. **Double-click LAUNCH_GUI.bat** (to start Mozart AI)
5. **Paste your code and get amazing feedback!**

**Remember**: You're not expected to be a tech expert. The setup is designed to be friendly for everyone! 🎵
├── README.md               # This file
├── LICENSE                 # MIT License
└── examples/              # Usage examples
    ├── basic_review.py    # Simple review example
    └── advanced_config.py # Advanced configuration
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Examples

### Basic Code Review
```python
# In the Mozart AI interface:
# Goal: "Review this function for correctness and performance"
# Context: "Python function for data processing"
# Code: [paste your code here]
# Criteria: Select "correctness" and "performance"
# Mode: Fast Mode
# Click "Evaluate"
```

### Comprehensive Security Review
```python
# Goal: "Security audit of authentication function"
# Context: "Web application login system handling user credentials"
# Criteria: Select "security", "error handling", "logic"
# Mode: Full Mode (includes judge analysis)
```

## 🤝 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Additional docs available in the `docs/` folder
- **Community**: Join discussions in GitHub Discussions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- DeepSeek for DeepSeek Coder API
- Python tkinter community for GUI inspiration
- Contributors and testers

## 🔄 Version History

- **V10**: Dynamic review criteria system with professional UI
- **V9**: Core dynamic system implementation
- **V8**: Enhanced text selection and context menus
- **V7**: Comprehensive copy functionality
- **V6**: Visual mode selector improvements
- **V5**: Integrated mode selection
- **V4**: Separate window experiments
- **V3**: Initial scrollable interface

---

**Mozart AI V10** - Where AI Critics Compete for Better Code! 🎭🎯
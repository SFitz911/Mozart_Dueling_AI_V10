# Mozart Dueling AI - Setup Instructions for Beginners 🎵

**Don't worry if you're not tech-savvy! This guide will walk you through everything step by step.**

## 🧪 Want to Test Before Full Setup?

**Quick Test**: Open `TEST_ERRORS.md` in this folder - it has ready-to-copy code examples that show Mozart AI in action! Perfect for understanding what the app does before setting it up.

## 🎯 What is Setup and Why Do I Need It?

**Setup** is like installing Mozart AI on your computer so it can work properly. Think of it like setting up a new phone - you need to:
- Install the right apps (dependencies)
- Enter your passwords (API keys)
- Configure settings

**What does `setup.py` do?**
- Checks if your computer has everything needed
- Downloads and installs missing parts automatically
- Creates a configuration file with your AI service passwords
- Makes easy-to-use shortcuts to start Mozart AI

## 🚀 Step-by-Step Setup (Super Detailed!)

### Step 1: Check if You Have Python

**What is Python?** It's a programming language that Mozart AI is built with.

**How to check:**
1. Press the **Windows key** (⊞) and **R** at the same time
2. Type `cmd` in the box that appears
3. Press **Enter**
4. A black window will open (don't worry, this is normal!)
5. Type exactly: `python --version`
6. Press **Enter**

**What you'll see:**
- ✅ **If you see something like "Python 3.11.4"** - You have Python! Go to Step 2
- ❌ **If you see "Python is not recognized"** - You need to install Python first

**Installing Python (if you need to):**
1. Open your web browser (Chrome, Firefox, etc.)
2. Go to: **https://python.org/downloads**
3. You'll see a big yellow button that says "Download Python 3.x.x"
4. **Click that button**
5. When the file downloads, **double-click it** to run it
6. **VERY IMPORTANT**: Check the box that says "Add Python to PATH" ⚠️
7. Click "Install Now"
8. Wait for it to finish
9. **Restart your computer** when it's done
10. Go back and check Step 1 again

### Step 1.5: Get Visual Studio Code (HIGHLY RECOMMENDED!)

**What is VS Code?** It's a free, beginner-friendly code editor that makes writing code much easier and prettier!

**Why should I get VS Code?**
- 📝 **Makes code colorful** - Easier to read and spot mistakes
- 🔧 **Built-in terminal** - Run Mozart AI right from VS Code
- 📁 **Organize files** - Keep all your projects neat and tidy
- 💡 **Auto-complete** - Helps you write code faster
- 🎨 **Looks professional** - Makes you feel like a real programmer!

**How to install VS Code:**
1. Go to: **https://code.visualstudio.com**
2. Click the big blue **"Download for Windows"** button
3. **Double-click** the downloaded file when it's done
4. Follow the installation steps (just click "Next" for everything)
5. **Check "Add to PATH"** if you see that option
6. Let it finish installing

**How to open Mozart AI in VS Code:**
1. **Open VS Code** (look for it in your Start menu)
2. Click **"File"** in the top menu
3. Click **"Open Folder"**
4. **Navigate to your Mozart AI folder** (where you downloaded it)
5. **Click "Select Folder"**
6. 🎉 **You'll now see all your Mozart AI files on the left side!**

**How to use VS Code with Mozart AI:**
1. **Write or edit code** in VS Code (it looks beautiful with colors!)
2. **Press Ctrl + `** to open the terminal at the bottom
3. **Run Mozart AI** by typing: `python LAUNCH_GUI.py`
4. **Copy your code** from VS Code and paste it into Mozart AI for review
5. **Get feedback** and go back to VS Code to improve your code!

### Step 2: Get Your AI Service Keys

**What are API keys?** Think of them like special passwords that let Mozart AI talk to OpenAI and DeepSeek AI services.

**You need TWO keys:**
1. **OpenAI API Key** (for GPT-4 AI)
2. **DeepSeek API Key** (for DeepSeek AI)

**Getting OpenAI API Key:**
1. Go to: **https://platform.openai.com**
2. Click "Sign Up" (or "Log In" if you have an account)
3. Create an account with your email
4. Once you're logged in, look for "API Keys" on the left side
5. Click "API Keys"
6. Click the button "Create new secret key"
7. Give it a name like "Mozart AI"
8. **Copy the key** (it will start with "sk-...")
9. **Save it somewhere safe** - you can't see it again!

**Getting DeepSeek API Key:**
1. Go to: **https://platform.deepseek.com**
2. Sign up for an account
3. Look for "API Keys" or "API" section
4. Generate a new API key
5. **Copy and save the key**

### Step 3: Run the Magical Setup

**This is where Mozart AI sets itself up automatically!**

1. **Find your Mozart AI folder**:
   - Open **File Explorer** (folder icon in taskbar)
   - Navigate to where you downloaded Mozart AI
   - You should see files like `setup.py`, `LAUNCH_GUI.bat`, etc.

2. **Run the setup**:
   - **Find the file called `setup.py`**
   - **Right-click on `setup.py`**
   - Choose **"Open with"** → **"Python"**
   - (Or if Python is set as default, just **double-click `setup.py`**)

3. **A window will pop up** - this is the setup wizard! 🧙‍♂️

**In the setup window:**
1. **First, click "Check Dependencies"**
   - This checks if your computer has everything needed
   - If something is missing, it will install it automatically
   - Wait for it to say "All dependencies are installed!" ✅

2. **Enter your API keys**:
   - In the "OpenAI API Key" box, paste your OpenAI key
   - In the "DeepSeek API Key" box, paste your DeepSeek key
   - **Tip**: The keys will show as stars (***) for security

3. **Click "Setup Environment"**
   - This creates all the configuration files
   - Wait for it to say "Setup completed successfully!" ✅

4. **Click the "Exit" button** when you're done

### Step 4: Launch Mozart AI (3 Easy Ways!)

**Now you can start using Mozart AI! Pick the easiest method for you:**

**Method A: Batch File (Easiest - Recommended for Beginners)**
1. In File Explorer, find the file called **`LAUNCH_GUI.bat`**
2. **Double-click it** (make sure you're in File Explorer, not VS Code!)
3. A black window will appear briefly, then Mozart AI will start!

**Method B: PowerShell (Pretty Easy)**
1. In File Explorer, find the file called **`LAUNCH_GUI.ps1`**
2. **Right-click on it**
3. Choose **"Run with PowerShell"**
4. You'll see colorful text, then Mozart AI will start!

**Method C: Python Direct (Alternative)**
1. In File Explorer, find the file called **`LAUNCH_GUI.py`**
2. **Double-click it** (or right-click → "Open with Python")
3. Mozart AI will start directly!

## 🔍 Using the Verification Tool

**What if something goes wrong?** Use the verification tool to check what's broken!

**How to use verify_setup.py:**
1. In File Explorer, find **`verify_setup.py`**
2. **Double-click it** (or right-click → "Open with Python")
3. A window will appear showing you:
   - ✅ What's working correctly
   - ❌ What's broken or missing
   - 💡 What you need to fix

**Example of what you might see:**
```
✅ Python 3.11.4
✅ setup.py
✅ LAUNCH_GUI.bat
✅ requests package
❌ OpenAI API key - Missing!
💡 Run setup.py again to add your API key
```

## ❗ Troubleshooting Common Problems

### "Python is not recognized" Error
**What this means:** Your computer can't find Python.

**How to fix:**
1. Reinstall Python from https://python.org
2. **Make sure** to check "Add Python to PATH" during installation
3. Restart your computer after installation
4. Try the python --version test again

### "Missing Dependencies" Error  
**What this means:** Mozart AI needs some extra Python packages.

**How to fix:**
1. Run `setup.py` again
2. Click "Check Dependencies" and let it install everything
3. Or open Command Prompt and type: `pip install -r requirements.txt`

### "Invalid API Key" Error
**What this means:** Your API keys aren't working.

**How to fix:**
1. Check your API keys don't have extra spaces at the beginning or end
2. Make sure your OpenAI key starts with "sk-"
3. Make sure you copied the complete key
4. Try running `setup.py` again and re-entering the keys

### PowerShell Won't Run (.ps1 file)
**What this means:** Windows is blocking PowerShell scripts for security.

**How to fix:**
1. Right-click the **Start button**
2. Choose **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**
3. Type exactly: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Press **Enter**
5. Type **Y** and press **Enter**
6. Close PowerShell
7. Try running the .ps1 file again

### "LAUNCH_GUI.bat won't work"
**Possible fixes:**
1. Make sure you're double-clicking in **File Explorer** (not VS Code)
2. Try right-clicking the .bat file and choosing "Run as administrator"
3. Use one of the other launch methods instead (LAUNCH_GUI.py)

### "Setup window won't open"
**Possible fixes:**
1. Right-click `setup.py` and choose "Open with" → "Python"
2. Open Command Prompt, navigate to the Mozart AI folder, and type: `python setup.py`
3. Make sure Python is properly installed

## 🆘 When All Else Fails

1. **Run verify_setup.py** - It will tell you exactly what's wrong
2. **Take a screenshot** of any error messages
3. **Read the error message carefully** - it often tells you what to do
4. **Try the setup process again** from the beginning
5. **Check that you're following each step exactly**

## 🎯 Quick Decision Tree

```
🤔 Something's not working?
    │
    ├─ 🔍 Run verify_setup.py first
    │   ├─ Shows what's broken
    │   └─ Follow its suggestions
    │
    ├─ ❌ Python not found?
    │   └─ Install Python (check "Add to PATH")
    │
    ├─ 🔑 API key errors?
    │   └─ Run setup.py again, re-enter keys carefully
    │
    ├─ 📦 Missing packages?
    │   └─ Run setup.py, click "Check Dependencies"
    │
    ├─ 🚫 PowerShell blocked?
    │   └─ Run Set-ExecutionPolicy as admin
    │
    └─ 🔄 Still stuck?
        └─ Start over from Step 1
```

## 🎉 Success! Now What?

Once Mozart AI is running, you'll see a window with:
- A big text box (where you paste your code)
- Checkboxes for what to review
- Buttons for Fast Mode and Full Mode
- A "Start Review" button

**To use Mozart AI:**
1. **Paste your code** in the big text box (or click "Load Text File")
2. **Check the boxes** for what you want reviewed (you can check all of them!)
3. **Choose Fast Mode** (quick review) or **Full Mode** (detailed review)
4. **Click "Start Review"**
5. **Wait a minute or two** while the AI works
6. **Read your results!** You'll get scores, suggestions, and improvements

**That's it! You're now using AI to make your code better!** 🎵
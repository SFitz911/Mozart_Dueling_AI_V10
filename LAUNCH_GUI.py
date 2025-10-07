#!/usr/bin/env python3
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
    print(f"Error: {e}")
    print("Please run setup.py first to install dependencies.")
    sys.exit(1)
except Exception as e:
    print(f"Error starting Mozart: {e}")
    sys.exit(1)

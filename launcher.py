"""
Voice Cloner Pro - Simple Launcher
Launches the desktop application with all dependencies
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    # Get the directory where this script is located
    app_dir = Path(__file__).parent
    
    print("\n" + "="*60)
    print("Voice Cloner Pro - Launcher")
    print("="*60 + "\n")
    
    # Change to app directory
    os.chdir(app_dir)
    
    # Install dependencies silently
    print("Checking dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"
        ], check=True, capture_output=True, timeout=60)
        print("[OK] Dependencies ready")
    except Exception as e:
        print(f"[WARNING] Could not install dependencies: {e}")
    
    print("\nLaunching Voice Cloner Pro...\n")
    print("="*60 + "\n")
    
    try:
        # Launch the desktop app
        subprocess.run([sys.executable, "src/desktop_app.py"], check=False)
    except Exception as e:
        print(f"\n[ERROR] Error launching application: {e}")
        input("\nPress Enter to exit...")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

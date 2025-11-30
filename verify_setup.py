#!/usr/bin/env python3
"""
Voice Cloner Desktop App - Setup Verification Checklist
Run this to verify everything is installed and ready to use
"""

import os
import sys
from pathlib import Path


def check_file_exists(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}")
        return False


def check_directory_exists(path, description):
    """Check if a directory exists"""
    if Path(path).is_dir():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}")
        return False


def check_python_module(module_name, description):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        print(f"✅ {description}")
        return True
    except ImportError:
        print(f"❌ {description} - Run: pip install {module_name}")
        return False


def main():
    """Run all checks"""
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("Voice Cloner Desktop App - Setup Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check project structure
    print("📁 PROJECT STRUCTURE")
    print("-" * 60)
    checks = [
        ("src/desktop_app.py", "PyQt6 Desktop Application"),
        ("src/branding.py", "Branding Configuration"),
        ("build_desktop.spec", "PyInstaller Configuration"),
        ("build_installer.py", "Installer Builder"),
        ("build.bat", "Windows Build Script"),
        ("build.sh", "Linux/macOS Build Script"),
        ("requirements.txt", "Python Dependencies"),
        ("assets/", "Assets Directory (for your logo)"),
    ]
    
    for item, desc in checks:
        if item.endswith("/"):
            result = check_directory_exists(item, desc)
        else:
            result = check_file_exists(item, desc)
        all_passed = all_passed and result
    
    print()
    
    # Check documentation
    print("📚 DOCUMENTATION")
    print("-" * 60)
    docs = [
        ("START_HERE_DESKTOP_APP.md", "Start Here Guide"),
        ("DESKTOP_APP_README.md", "Quick Start Guide"),
        ("DESKTOP_APP_GUIDE.md", "Detailed Setup Guide"),
        ("BRANDING_GUIDE.md", "Branding Customization"),
        ("DESKTOP_CUSTOMIZATION_EXAMPLES.md", "Visual Examples"),
        ("DESKTOP_APP_SETUP_COMPLETE.md", "Complete Setup"),
        ("DESKTOP_APP_ARCHITECTURE.md", "Architecture Doc"),
        ("DESKTOP_APPLICATION_COMPLETE.md", "Summary"),
        ("DESKTOP_APP_VISUAL_SUMMARY.md", "Visual Summary"),
        ("DESKTOP_APP_INDEX.md", "Complete Index"),
        ("assets/README.md", "Logo Setup Instructions"),
    ]
    
    for doc, desc in docs:
        result = check_file_exists(doc, desc)
        all_passed = all_passed and result
    
    print()
    
    # Check Python modules
    print("🐍 PYTHON DEPENDENCIES")
    print("-" * 60)
    
    modules = [
        ("torch", "PyTorch (AI/ML framework)"),
        ("librosa", "Librosa (Audio processing)"),
        ("soundfile", "SoundFile (Audio I/O)"),
        ("click", "Click (CLI framework)"),
        ("rich", "Rich (Console output)"),
    ]
    
    for module, desc in modules:
        result = check_python_module(module, desc)
        if not result:
            all_passed = False
    
    # Check GUI dependencies (optional for now)
    print()
    print("🎨 GUI DEPENDENCIES (Optional - install if needed)")
    print("-" * 60)
    
    gui_modules = [
        ("PyQt6", "PyQt6 (GUI Framework)"),
        ("pyinstaller", "PyInstaller (Build Tool)"),
    ]
    
    gui_available = True
    for module, desc in gui_modules:
        if module == "pyinstaller":
            check_result = check_python_module("PyInstaller", desc)
        else:
            check_result = check_python_module(module, desc)
        gui_available = gui_available and check_result
    
    print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print()
    
    if all_passed and gui_available:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Your Voice Cloner desktop application is ready to use!")
        print()
        print("Next steps:")
        print("1. Read: START_HERE_DESKTOP_APP.md")
        print("2. Prepare your logo files (PNG, ICO)")
        print("3. Edit: src/branding.py with your info")
        print("4. Run: python src/desktop_app.py")
        return 0
    
    elif all_passed and not gui_available:
        print("⚠️  CORE FILES READY, GUI LIBRARIES MISSING")
        print()
        print("Install GUI dependencies:")
        print("pip install PyQt6 pyinstaller")
        print()
        print("Then run: python src/desktop_app.py")
        return 1
    
    else:
        print("❌ SETUP INCOMPLETE")
        print()
        print("Missing files detected. Please ensure all files are in place.")
        print()
        print("If this is a fresh setup, run:")
        print("pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

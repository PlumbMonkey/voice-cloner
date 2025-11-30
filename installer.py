"""
Voice Cloner Pro - Windows Installer
Simple one-click installer for end users
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
import json


class VoiceClonerInstaller:
    def __init__(self):
        # Install to user's AppData for write access (better than Program Files)
        self.install_dir = Path(os.getenv('APPDATA')) / 'Voice Cloner Pro'
        self.shortcuts_dir = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        
    def create_directories(self):
        """Create installation directories"""
        self.install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created installation directory: {self.install_dir}")
        
    def copy_files(self):
        """Copy application files"""
        src = Path(__file__).parent
        
        # Copy source code
        src_dir = src / 'src'
        if src_dir.exists():
            dst_dir = self.install_dir / 'src'
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"✓ Copied source code")
        
        # Copy launcher and other essential files
        for file in ['requirements.txt', 'launcher.py', 'branding.py', '.env.example']:
            src_file = src / file
            if src_file.exists():
                shutil.copy2(src_file, self.install_dir / file)
        
        print(f"✓ Copied application files")
        
    def create_shortcut(self):
        """Create desktop shortcut"""
        try:
            import win32com.client
            
            desktop = Path.home() / 'Desktop'
            shortcut_path = desktop / 'Voice Cloner Pro.lnk'
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(self.install_dir / 'launcher.py')
            shortcut.WorkingDirectory = str(self.install_dir)
            shortcut.save()
            
            print(f"✓ Created desktop shortcut")
        except Exception as e:
            print(f"⚠ Could not create shortcut: {e}")
    
    def create_launcher(self):
        """Create launcher shortcuts"""
        # launcher.py will handle everything, no batch file needed
        print(f"✓ Launcher configured")
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        uninstaller = self.install_dir / 'uninstall.bat'
        uninstaller.write_text(f"""@echo off
echo Uninstalling Voice Cloner Pro...
cd /d "%~dp0"
cd ..
rmdir /s /q "Voice Cloner Pro"
echo Uninstall complete!
pause
""")
        print(f"✓ Created uninstaller")
    
    def install(self):
        """Run complete installation"""
        print("\n" + "="*60)
        print("Voice Cloner Pro - Installation")
        print("="*60 + "\n")
        
        try:
            self.create_directories()
            self.copy_files()
            self.create_launcher()
            self.create_uninstaller()
            self.create_shortcut()
            
            print("\n" + "="*60)
            print("✓ Installation Complete!")
            print("="*60)
            print(f"\nInstalled to: {self.install_dir}")
            print("\nTo run Voice Cloner Pro:")
            print(f"1. Run: {self.install_dir / 'run.bat'}")
            print("2. Or use the desktop shortcut")
            print("\nTo uninstall:")
            print(f"Run: {self.install_dir / 'uninstall.bat'}")
            print("\n" + "="*60 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Installation failed: {e}")
            return False


if __name__ == '__main__':
    installer = VoiceClonerInstaller()
    success = installer.install()
    sys.exit(0 if success else 1)

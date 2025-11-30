#!/usr/bin/env python3
"""
Production Build Script for Voice Cloner Desktop Application
Creates a complete .exe installer with all dependencies bundled
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command with error handling"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ Error during: {description}")
        return False
    return True

def main():
    """Build the production installer"""
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n" + "="*60)
    print("VOICE CLONER - PRODUCTION BUILD")
    print("="*60)
    
    # Step 1: Verify dependencies
    print("\n▶ Checking dependencies...")
    required_packages = ['pyinstaller', 'PyQt5']
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"  ✓ {pkg} installed")
        except ImportError:
            print(f"  ❌ {pkg} not found, installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)
    
    # Step 2: Clean previous builds
    print("\n▶ Cleaning previous builds...")
    for folder in ['build', 'dist', '__pycache__', 'src/__pycache__']:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"  ✓ Removed {folder}")
    
    # Step 3: Create PyInstaller spec file
    print("\n▶ Creating PyInstaller spec file...")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Voice Cloner Desktop Application

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys

block_cipher = None

# Collect all PyQt5 modules
qt_submodules = collect_submodules('PyQt5')

# Data files needed
datas = [
    ('assets', 'assets'),
    ('src/config', 'src/config'),
    ('src/branding.py', 'src'),
]

# Hidden imports for audio processing
hidden_imports = [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui', 
    'PyQt5.QtWidgets',
    'soundfile',
    'librosa',
    'librosa.core',
    'librosa.util',
    'scipy',
    'numpy',
    'torch',
] + qt_submodules

a = Analysis(
    ['src/desktop_app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoiceCloner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.ico' if Path('assets/logo.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VoiceCloner',
)
"""
    
    with open('VoiceCloner.spec', 'w') as f:
        f.write(spec_content)
    print("  ✓ Created VoiceCloner.spec")
    
    # Step 4: Build with PyInstaller
    if not run_command(
        f'{sys.executable} -m PyInstaller VoiceCloner.spec --distpath ./dist --workpath ./build -y',
        "Building executable with PyInstaller"
    ):
        print("\n❌ Build failed")
        return False
    
    # Step 5: Create Windows installer using Inno Setup (if available)
    print("\n▶ Checking for Inno Setup...")
    inno_path = Path("C:/Program Files (x86)/Inno Setup 6/ISCC.exe")
    
    if inno_path.exists():
        print("  ✓ Inno Setup found, creating installer...")
        
        # Create Inno Setup script
        iss_content = """[Setup]
AppName=Voice Cloner Pro
AppVersion=1.0.0
AppPublisher=PlumbMonkey
AppPublisherURL=https://github.com/PlumbMonkey/voice-cloner
DefaultDirName={pf}\\Voice Cloner Pro
DefaultGroupName=Voice Cloner Pro
OutputDir=dist
OutputBaseFilename=VoiceCloner_Setup_1.0.0
Compression=lz4
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIconTask}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\VoiceCloner\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\Voice Cloner Pro"; Filename: "{app}\\VoiceCloner.exe"
Name: "{commondesktop}\\Voice Cloner Pro"; Filename: "{app}\\VoiceCloner.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\VoiceCloner.exe"; Description: "{cm:LaunchProgram,Voice Cloner Pro}"; Flags: nowait postinstall skipifsilent
"""
        
        with open('VoiceCloner.iss', 'w') as f:
            f.write(iss_content)
        print("  ✓ Created VoiceCloner.iss")
        
        if not run_command(
            f'"{inno_path}" VoiceCloner.iss',
            "Building installer with Inno Setup"
        ):
            print("\n⚠️  Inno Setup build failed, but .exe was created")
    else:
        print("  ⚠️  Inno Setup not found, skipping installer creation")
        print("  ℹ️  Portable .exe available in dist/VoiceCloner/")
    
    # Step 6: Create portable batch installer
    print("\n▶ Creating portable installer...")
    batch_installer = """@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Voice Cloner Pro - Portable Installer
echo ==========================================
echo.

REM Get Program Files path
set "INSTALL_DIR=%ProgramFiles%\\Voice Cloner Pro"

echo Installation Directory: !INSTALL_DIR!
echo.

REM Create directory
if not exist "!INSTALL_DIR!" mkdir "!INSTALL_DIR!"

REM Copy files
echo Installing files...
xcopy "dist\\VoiceCloner\\*" "!INSTALL_DIR!\\" /E /I /Y >nul

REM Create shortcuts
echo Creating shortcuts...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Voice Cloner Pro.lnk')); $Shortcut.TargetPath = '!INSTALL_DIR!\\VoiceCloner.exe'; $Shortcut.Save()"

echo.
echo ✓ Installation complete!
echo ✓ Desktop shortcut created
echo.
pause
"""
    
    with open('PORTABLE_INSTALLER.bat', 'w') as f:
        f.write(batch_installer)
    print("  ✓ Created PORTABLE_INSTALLER.bat")
    
    # Step 7: Summary
    print("\n" + "="*60)
    print("✅ BUILD COMPLETE")
    print("="*60)
    print("\nOutput files:")
    print(f"  • Portable .exe: dist/VoiceCloner/VoiceCloner.exe")
    print(f"  • Installer: dist/VoiceCloner_Setup_1.0.0.exe (if Inno Setup available)")
    print(f"  • Batch installer: PORTABLE_INSTALLER.bat")
    print("\nNext steps:")
    print("  1. Run 'PORTABLE_INSTALLER.bat' to install")
    print("  2. Or copy 'dist/VoiceCloner' folder to Program Files")
    print("  3. Or distribute the .exe directly as portable app")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

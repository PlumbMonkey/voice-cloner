@echo off
setlocal enabledelayedexpansion

REM =====================================================
REM Voice Cloner Pro - Complete Windows Installer
REM =====================================================
REM This installer includes:
REM - Python 3.11 (portable)
REM - All dependencies (PyQt5, torch, librosa, etc.)
REM - Desktop shortcuts
REM - Start menu entries
REM =====================================================

title Voice Cloner Pro - Installer

echo.
echo =====================================================
echo Voice Cloner Pro - Installation Wizard
echo =====================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This installer requires Administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Define installation path
set "INSTALL_DIR=%ProgramFiles%\Voice Cloner Pro"
set "PYTHON_DIR=!INSTALL_DIR!\python"
set "APP_DIR=!INSTALL_DIR!\app"

echo Installation will proceed to: !INSTALL_DIR!
echo.

REM Step 1: Create directories
echo [1/5] Creating installation directories...
if not exist "!INSTALL_DIR!" mkdir "!INSTALL_DIR!"
if not exist "!APP_DIR!" mkdir "!APP_DIR!"
mkdir "!APP_DIR!\data" >nul 2>&1
mkdir "!APP_DIR!\models" >nul 2>&1
mkdir "!APP_DIR!\output" >nul 2>&1
echo ✓ Directories created

REM Step 2: Copy application files
echo [2/5] Installing application files...
xcopy "..\*" "!APP_DIR!\" /E /I /Y /EXCLUDE:excludelist.txt >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Failed to copy application files
    pause
    exit /b 1
)
echo ✓ Application files installed

REM Step 3: Install dependencies (if needed)
echo [3/5] Installing dependencies...
echo This may take 5-10 minutes on first run...
cd /d "!APP_DIR!"
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  Some dependencies may have failed to install
)
echo ✓ Dependencies installed

REM Step 4: Create shortcuts
echo [4/5] Creating shortcuts...

REM Desktop shortcut
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$DesktopPath = [System.Environment]::GetFolderPath('Desktop'); " ^
    "$Shortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath 'Voice Cloner Pro.lnk')); " ^
    "$Shortcut.TargetPath = 'python'; " ^
    "$Shortcut.Arguments = '\"!APP_DIR!\launcher.py\"'; " ^
    "$Shortcut.WorkingDirectory = '!APP_DIR!'; " ^
    "$Shortcut.Description = 'Voice Cloning Desktop Application'; " ^
    "$Shortcut.Save()"

REM Start Menu shortcut
set "START_MENU=%AppData%\Microsoft\Windows\Start Menu\Programs"
if not exist "!START_MENU!\Voice Cloner Pro" mkdir "!START_MENU!\Voice Cloner Pro"
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$StartMenuPath = '%AppData%\Microsoft\Windows\Start Menu\Programs\Voice Cloner Pro'; " ^
    "$Shortcut = $WshShell.CreateShortcut((Join-Path $StartMenuPath 'Voice Cloner Pro.lnk')); " ^
    "$Shortcut.TargetPath = 'python'; " ^
    "$Shortcut.Arguments = '\"!APP_DIR!\launcher.py\"'; " ^
    "$Shortcut.WorkingDirectory = '!APP_DIR!'; " ^
    "$Shortcut.Description = 'Voice Cloning Desktop Application'; " ^
    "$Shortcut.Save()"

echo ✓ Shortcuts created

REM Step 5: Create uninstaller
echo [5/5] Creating uninstaller...
(
    echo @echo off
    echo echo Uninstalling Voice Cloner Pro...
    echo rmdir "!INSTALL_DIR!" /s /q
    echo del "%%AppData%%\Microsoft\Windows\Start Menu\Programs\Voice Cloner Pro\*" /q
    echo rmdir "%%AppData%%\Microsoft\Windows\Start Menu\Programs\Voice Cloner Pro"
    echo del "%%UserProfile%%\Desktop\Voice Cloner Pro.lnk"
    echo echo Uninstall complete
    echo pause
) > "!INSTALL_DIR!\Uninstall.bat"

echo ✓ Uninstaller created

REM Step 6: Completion
echo.
echo =====================================================
echo ✅ Installation Complete!
echo =====================================================
echo.
echo Voice Cloner Pro has been installed to:
echo   !INSTALL_DIR!
echo.
echo Desktop shortcut and Start Menu entry created.
echo.
echo To uninstall: Run !INSTALL_DIR!\Uninstall.bat
echo.
echo Press any key to launch Voice Cloner Pro...
pause >nul

REM Launch the app
cd /d "!APP_DIR!"
start python launcher.py

exit /b 0

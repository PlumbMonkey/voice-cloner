@echo off
setlocal enabledelayedexpansion
title Voice Cloner Pro - Installation Wizard

echo.
echo ======================================================
echo Voice Cloner Pro - Installation Wizard
echo ======================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installer requires administrator privileges.
    echo Please run this file as Administrator.
    echo.
    pause
    exit /b 1
)

REM Define installation directory (use AppData for write permissions)
set INSTALL_DIR=%APPDATA%\Voice Cloner Pro

echo Installing to: %INSTALL_DIR%
echo.

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✓ Created installation directory
) else (
    echo ⚠ Installation directory already exists, updating files...
)

REM Copy files
echo.
echo Copying application files...
xcopy /E /I /Y "src" "%INSTALL_DIR%\src" >nul 2>&1
if %errorlevel% equ 0 echo ✓ Copied source code
xcopy /E /I /Y "assets" "%INSTALL_DIR%\assets" >nul 2>&1
if %errorlevel% equ 0 echo ✓ Copied assets
copy /Y "requirements.txt" "%INSTALL_DIR%\" >nul 2>&1
if %errorlevel% equ 0 echo ✓ Copied dependencies list
copy /Y "branding.py" "%INSTALL_DIR%\" >nul 2>&1
if %errorlevel% equ 0 echo ✓ Copied branding configuration

REM Create launcher script
echo.
echo Creating launcher scripts...
(
    echo @echo off
    echo title Voice Cloner Pro
    echo cd /d "%%~dp0"
    echo echo Installing dependencies...
    echo python -m pip install -q -r requirements.txt
    echo echo.
    echo echo Launching Voice Cloner Pro...
    echo python src\desktop_app.py
    echo if errorlevel 1 pause
) > "%INSTALL_DIR%\VoiceCloner.bat"
echo ✓ Created launcher

REM Create uninstaller
(
    echo @echo off
    echo echo Uninstalling Voice Cloner Pro...
    echo timeout /t 2 /nobreak
    echo cd /d "%%~dp0.."
    echo rmdir /s /q "Voice Cloner Pro"
    echo echo Uninstall complete!
    echo pause
) > "%INSTALL_DIR%\UNINSTALL.bat"
echo ✓ Created uninstaller

REM Create desktop shortcut using VBScript
echo.
echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Voice Cloner Pro.lnk

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%SHORTCUT_PATH%"
    echo Set oLink = oWS.CreateShortCut(sLinkFile^)
    echo oLink.TargetPath = "%INSTALL_DIR%\VoiceCloner.bat"
    echo oLink.WorkingDirectory = "%INSTALL_DIR%"
    echo oLink.IconLocation = "%INSTALL_DIR%\assets\logo.ico"
    echo oLink.Description = "Voice Cloner Pro - Desktop Application"
    echo oLink.Save
) > "%INSTALL_DIR%\CreateShortcut.vbs"

cscript.exe //nologo "%INSTALL_DIR%\CreateShortcut.vbs" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Created desktop shortcut
) else (
    echo ⚠ Could not create desktop shortcut (icon file may be missing^)
)

REM Create Start Menu shortcut
echo Creating Start Menu entry...
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Voice Cloner Pro

if not exist "%START_MENU%" mkdir "%START_MENU%"

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%START_MENU%\Voice Cloner Pro.lnk"
    echo Set oLink = oWS.CreateShortCut(sLinkFile^)
    echo oLink.TargetPath = "%INSTALL_DIR%\VoiceCloner.bat"
    echo oLink.WorkingDirectory = "%INSTALL_DIR%"
    echo oLink.Description = "Voice Cloner Pro - Desktop Application"
    echo oLink.Save
) > "%INSTALL_DIR%\CreateStartMenuShortcut.vbs"

cscript.exe //nologo "%INSTALL_DIR%\CreateStartMenuShortcut.vbs" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Created Start Menu entry
) else (
    echo ⚠ Could not create Start Menu entry
)

REM Final message
echo.
echo ======================================================
echo ✓ Installation Complete!
echo ======================================================
echo.
echo Installation Location: %INSTALL_DIR%
echo.
echo Next Steps:
echo 1. Click "Voice Cloner Pro" on your Desktop
echo 2. Or find it in your Start Menu
echo 3. Application will launch with all dependencies
echo.
echo To Uninstall:
echo Run: %INSTALL_DIR%\UNINSTALL.bat
echo Or: Just delete the folder from AppData\Voice Cloner Pro
echo.
echo ======================================================
echo.
pause

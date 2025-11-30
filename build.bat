@echo off
REM Voice Cloner Desktop Application Build Script
REM Automates the entire build and packaging process

setlocal enabledelayedexpansion

echo.
echo ============================================
echo Voice Cloner Desktop App Builder
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Download from: https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install PyQt6 pyinstaller
)

REM Menu
:menu
echo.
echo What would you like to do?
echo.
echo 1. Run desktop app (development)
echo 2. Build Windows executable
echo 3. Build Windows installer (NSIS)
echo 4. Build all installers
echo 5. Clean build artifacts
echo 6. Open branding config
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto build_exe
if "%choice%"=="3" goto build_installer
if "%choice%"=="4" goto build_all
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto edit_branding
if "%choice%"=="7" goto exit

echo Invalid choice. Please try again.
goto menu

:run_app
echo.
echo Starting Voice Cloner desktop app...
echo.
python src\desktop_app.py
goto menu

:build_exe
echo.
echo Building Windows executable...
echo This may take 2-5 minutes...
echo.
python -m PyInstaller build_desktop.spec
if errorlevel 1 (
    echo Build failed!
    pause
) else (
    echo.
    echo Build successful!
    echo Executable location: dist\VoiceCloner\VoiceCloner.exe
    pause
)
goto menu

:build_installer
echo.
echo Generating NSIS installer script...
echo.
python build_installer.py 3
if errorlevel 1 (
    echo Failed to generate installer script!
    pause
) else (
    echo.
    echo Installer script generated: VoiceCloner-Installer.nsi
    echo.
    echo To build the installer, you need NSIS:
    echo 1. Download: https://nsis.sourceforge.io/
    echo 2. Install NSIS
    echo 3. Run: "C:\Program Files (x86)\NSIS\makensis.exe" VoiceCloner-Installer.nsi
    echo.
    pause
)
goto menu

:build_all
echo.
echo Building all installers...
echo This may take 5-10 minutes...
echo.
python build_installer.py 6
if errorlevel 1 (
    echo Build failed!
    pause
) else (
    echo.
    echo All builds successful!
    pause
)
goto menu

:clean
echo.
echo Cleaning build artifacts...
echo.
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
echo Build artifacts cleaned!
pause
goto menu

:edit_branding
echo.
echo Opening branding configuration...
echo.
start notepad src\branding.py
echo.
echo Edit the branding.py file to customize your app
echo.
pause
goto menu

:exit
echo.
echo Goodbye!
echo.
pause

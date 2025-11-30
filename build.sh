#!/bin/bash
# Voice Cloner Desktop Application Build Script
# Automates the entire build and packaging process for Linux/macOS

set -e

clear

echo "============================================"
echo "Voice Cloner Desktop App Builder"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    echo "Install with: brew install python3 (macOS) or apt install python3 (Linux)"
    exit 1
fi

# Check if dependencies are installed
python3 -c "import PyQt6" 2>/dev/null || {
    echo "Installing required packages..."
    pip3 install PyQt6 pyinstaller
}

menu() {
    clear
    echo "============================================"
    echo "Voice Cloner Desktop App Builder"
    echo "============================================"
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1. Run desktop app (development)"
    echo "2. Build executable"
    echo "3. Build app bundle (macOS) or AppImage (Linux)"
    echo "4. Build all"
    echo "5. Clean build artifacts"
    echo "6. Edit branding config"
    echo "7. Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice

    case $choice in
        1) run_app ;;
        2) build_exe ;;
        3) build_bundle ;;
        4) build_all ;;
        5) clean_build ;;
        6) edit_branding ;;
        7) exit 0 ;;
        *) echo "Invalid choice. Please try again." && sleep 2 && menu ;;
    esac
}

run_app() {
    clear
    echo "Starting Voice Cloner desktop app..."
    echo ""
    python3 src/desktop_app.py
    menu
}

build_exe() {
    clear
    echo "Building executable..."
    echo "This may take 2-5 minutes..."
    echo ""
    python3 -m PyInstaller build_desktop.spec
    if [ $? -eq 0 ]; then
        echo ""
        echo "Build successful!"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "App bundle location: dist/VoiceCloner.app"
        else
            echo "Executable location: dist/VoiceCloner/VoiceCloner"
        fi
    else
        echo "Build failed!"
    fi
    read -p "Press enter to continue..."
    menu
}

build_bundle() {
    clear
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Building macOS app bundle..."
    else
        echo "Building AppImage..."
    fi
    echo ""
    python3 build_installer.py
    read -p "Press enter to continue..."
    menu
}

build_all() {
    clear
    echo "Building all installers..."
    echo "This may take 5-10 minutes..."
    echo ""
    python3 build_installer.py 6
    if [ $? -eq 0 ]; then
        echo ""
        echo "All builds successful!"
    else
        echo "Build failed!"
    fi
    read -p "Press enter to continue..."
    menu
}

clean_build() {
    clear
    echo "Cleaning build artifacts..."
    echo ""
    rm -rf dist build __pycache__ *.egg-info
    echo "Build artifacts cleaned!"
    read -p "Press enter to continue..."
    menu
}

edit_branding() {
    clear
    echo "Opening branding configuration..."
    echo ""
    if command -v nano &> /dev/null; then
        nano src/branding.py
    elif command -v vim &> /dev/null; then
        vim src/branding.py
    else
        echo "Please edit: src/branding.py"
        read -p "Press enter when done..."
    fi
    menu
}

# Make menu function executable
menu

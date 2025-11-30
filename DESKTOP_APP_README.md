# 🎤 Voice Cloner Pro - Desktop Application

Your Voice Cloner project is now set up as a professional, branded desktop application with full installer support!

## ✨ Features

### Professional GUI
- Modern PyQt6-based interface
- Dark theme with custom branding colors
- Intuitive 6-tab workflow (Setup, Preprocess, Train, Infer, Settings)
- Real-time progress indicators
- Live log output
- File dialogs for easy file selection

### Cross-Platform Support
- **Windows:** EXE executable + NSIS installer
- **macOS:** App Bundle
- **Linux:** AppImage support

### Custom Branding
- Your company logo and colors
- Custom application title
- Branded about dialog
- Support links in help menu
- Copyright and license information

### Complete Packaging
- PyInstaller automated builds
- Installer generation (NSIS for Windows)
- Auto-update support (configurable)
- Single-file or directory distribution

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Branding

**Step 1: Prepare your logo**
- Save your logo as PNG (transparent background recommended)
- Convert to ICO for Windows icon

**Step 2: Add files to `assets/` folder**
```
assets/
├── logo.png        (150x150px)
├── icon.ico        (256x256px) - Windows
└── icon.png        (512x512px) - Linux/macOS
```

See `assets/README.md` for detailed instructions.

**Step 3: Edit `src/branding.py`**
```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="Voice Cloner Pro",  # Your app name
    company_name="Your Company",   # Your company
    company_website="https://yourcompany.com",
    company_email="support@yourcompany.com",
    primary_color=(13, 71, 161),   # Your brand color (RGB)
    accent_color=(0, 204, 0),      # Accent color (RGB)
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
    copyright_year="2025",
)
```

### 3. Run Desktop App

**Development mode:**
```bash
python src/desktop_app.py
```

**Using build script (Windows):**
```bash
build.bat
# Choose option 1
```

**Using build script (Linux/macOS):**
```bash
bash build.sh
# Choose option 1
```

## 📦 Building Installers

### Windows Executable

```bash
python build_installer.py 1
```

Creates: `dist/VoiceCloner/VoiceCloner.exe`

**Or using build script:**
```bash
build.bat
# Choose option 2
```

### Windows Installer (NSIS)

```bash
python build_installer.py 3
```

Creates: `VoiceCloner-Installer.nsi`

Then build with NSIS:
1. Install NSIS from https://nsis.sourceforge.io/
2. Run: `"C:\Program Files (x86)\NSIS\makensis.exe" VoiceCloner-Installer.nsi`

**Or using build script:**
```bash
build.bat
# Choose option 3
```

### macOS App Bundle

```bash
python build_installer.py 4
```

Creates: `dist/VoiceCloner.app`

### Linux AppImage

```bash
python build_installer.py 5
```

Generates configuration for AppImage creation.

### Build All Formats

```bash
python build_installer.py 6
```

## 🎨 Customization

### Colors
Edit RGB values in `src/branding.py`:
```python
primary_color=(13, 71, 161)      # Blue
primary_light=(21, 101, 192)     # Light blue
accent_color=(0, 204, 0)         # Green
```

### Application Title
```python
app_name="Your App Name"
app_version="1.0.0"
app_tagline="Your tagline here"
```

### Company Information
```python
company_name="Your Company"
company_website="https://yourcompany.com"
support_url="https://yourcompany.com/support"
```

### Support Links
```python
support_url="https://yourcompany.com/support"
documentation_url="https://yourcompany.com/docs"
bug_report_url="https://github.com/yourcompany/voicecloner/issues"
privacy_policy_url="https://yourcompany.com/privacy"
```

### Features
```python
enable_auto_updates=True      # Auto-update support
enable_telemetry=False        # User tracking (privacy)
enable_feedback=True          # Feedback form
```

## 📋 Application Structure

```
Voice Cloner/
├── src/
│   ├── desktop_app.py          # Main PyQt6 application
│   ├── branding.py             # Branding configuration
│   ├── orchestrator.py         # Workflow coordinator
│   ├── modules/                # Processing modules
│   └── utils/                  # Utilities
├── assets/                     # Your logo and icons
│   ├── logo.png
│   ├── icon.ico
│   └── icon.png
├── build_desktop.spec          # PyInstaller config
├── build_installer.py          # Installer builder
├── build.bat                   # Windows build script
├── build.sh                    # Linux/macOS build script
├── requirements.txt            # Dependencies
└── DESKTOP_APP_GUIDE.md       # Detailed guide
```

## 🔧 Advanced Configuration

### Custom UI
Edit `src/desktop_app.py` to customize:
- Page layouts
- Button styles
- Window size and position
- Dialog messages

### Add New Pages
```python
def create_pages(self):
    # Add new page
    self.stacked_widget.addWidget(self.create_custom_page())
    
def create_custom_page(self):
    widget = QWidget()
    layout = QVBoxLayout()
    # Add your widgets
    widget.setLayout(layout)
    return widget
```

### Styling
Edit `get_stylesheet()` in `desktop_app.py`:
```python
def get_stylesheet(self, theme: str = "dark") -> str:
    # Customize QSS (Qt Style Sheets)
    # See PyQt6 documentation
```

## ✅ Distribution Checklist

- [ ] Logo files added to `assets/`
- [ ] Branding configured in `src/branding.py`
- [ ] Company information updated
- [ ] Support URLs configured
- [ ] Color scheme customized
- [ ] Tested in development mode
- [ ] Installer built successfully
- [ ] Tested on target platform
- [ ] Version number updated
- [ ] Ready for distribution

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"
```bash
pip install PyQt6
```

### "Cannot find PyInstaller"
```bash
pip install pyinstaller
```

### Logo not showing in app
1. Check `assets/logo.png` exists
2. Verify path in `src/branding.py`
3. Check file permissions
4. Run in development mode first: `python src/desktop_app.py`

### Executable won't start
1. Check all dependencies installed: `pip install -r requirements.txt`
2. Verify Python 3.8+: `python --version`
3. Try running in development mode first
4. Check console for error messages

### Build fails with PyInstaller
1. Ensure all dependencies installed
2. Try clean build: `python build_installer.py 5` (clean)
3. Update PyInstaller: `pip install --upgrade pyinstaller`
4. Check file permissions

### Icon not showing in Windows
1. Ensure `assets/icon.ico` exists and is valid
2. Update path in `build_desktop.spec`
3. Rebuild with PyInstaller
4. Windows may cache old icons - restart app or clear cache

## 📚 File Reference

- `src/desktop_app.py` - Main application (1000+ lines)
- `src/branding.py` - Branding configuration
- `build_desktop.spec` - PyInstaller configuration
- `build_installer.py` - Installer builder (500+ lines)
- `build.bat` - Windows build automation
- `build.sh` - Linux/macOS build automation
- `assets/README.md` - Logo setup instructions

## 🔐 Security & Privacy

The desktop application is completely local - no data collection by default:
- ✅ No telemetry (unless explicitly enabled)
- ✅ No tracking
- ✅ No internet connection required
- ✅ No account needed
- ✅ Open source (view the code!)

Update privacy settings in `src/branding.py`:
```python
enable_telemetry=False      # Disable tracking
enable_feedback=True        # Allow feedback
```

## 📞 Support

For issues or questions:
1. Check `DESKTOP_APP_GUIDE.md` for detailed documentation
2. Review troubleshooting section above
3. Check logs in `logs/` directory
4. Contact support at your configured email

## 📄 License

Voice Cloner Pro
© 2025 Your Company
License: MIT

See LICENSE file for details.

---

**Next Steps:**
1. Add your logo to `assets/` folder
2. Edit `src/branding.py` with your info
3. Run `python src/desktop_app.py` to test
4. Build installers with `python build_installer.py 1` (Windows) or `python build_installer.py 4` (macOS)

**Questions?** See DESKTOP_APP_GUIDE.md for complete documentation!

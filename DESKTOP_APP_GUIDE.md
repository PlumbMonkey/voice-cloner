# Voice Cloner - Desktop Application Setup Guide

## Desktop App Setup

Your Voice Cloner project is now set up as a professional desktop application!

### 📦 Installation Requirements

```bash
# Install PyQt6 for GUI
pip install PyQt6

# Install PyInstaller for packaging
pip install pyinstaller
```

### 🎨 Branding Your Application

Before building, customize your app by editing `src/branding.py`:

```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="Your App Name",
    company_name="Your Company",
    company_website="https://yourcompany.com",
    company_email="support@yourcompany.com",
    primary_color=(13, 71, 161),  # Your brand color RGB
    accent_color=(0, 204, 0),  # Accent color RGB
    logo_path=Path("assets/logo.png"),  # Your logo file
    icon_path=Path("assets/icon.ico"),  # Your app icon
)
```

### 🖼️ Adding Your Logo

1. **Create `assets/` directory:**
   ```bash
   mkdir assets
   ```

2. **Add your files:**
   - `assets/logo.png` - Main logo (150x150px recommended)
   - `assets/icon.ico` - App icon (256x256px, convert PNG to ICO)

3. **Tools for icon conversion:**
   - Online: https://convertio.co/png-ico/
   - Python: `pip install Pillow` then use `PIL.Image`

### ▶️ Running the Desktop App

**Development mode:**
```bash
python src/desktop_app.py
```

**Production build with PyInstaller:**
```bash
pyinstaller build_desktop.spec
```

The executable will be created in `dist/VoiceCloner/` folder.

### 📋 Application Features

- **Home Dashboard** - Quick start guide
- **Setup Wizard** - Environment detection and installation
- **Preprocessing Panel** - Audio file management
- **Training Console** - Model training with parameter control
- **Conversion Tool** - Voice cloning interface
- **Settings Page** - Application information and help

### 🎯 Customization Options

**Color Scheme:**
- Modify RGB tuples in `branding.py`
- Colors auto-apply to all UI elements

**Application Title:**
- Edit `app_name` in `branding.py`
- Version auto-updates from `app_version`

**Support Links:**
- Update URLs in `branding.py`
- Links appear in Help menu and About dialog

**Company Info:**
- Company name in About dialog
- Copyright year in footer
- Support email in help sections

### 🚀 Building for Distribution

**Windows Executable:**
```bash
# Build standalone executable
pyinstaller build_desktop.spec --onefile

# Output: dist/VoiceCloner.exe
```

**Create Installer (optional):**
```bash
pip install pyinstaller-versionfile nuitka
# Additional setup for NSIS installer
```

**macOS App Bundle:**
```bash
pyinstaller build_desktop.spec --osx-bundle-identifier com.yourcompany.voicecloner
# Output: dist/VoiceCloner.app
```

### 📊 Application Structure

```
Voice Cloner/
├── src/
│   ├── desktop_app.py          # Main PyQt6 application
│   ├── branding.py             # Branding configuration
│   ├── orchestrator.py         # Workflow coordinator
│   └── modules/                # Processing modules
├── assets/                     # Logos and icons
│   ├── logo.png
│   └── icon.ico
├── build_desktop.spec          # PyInstaller configuration
└── docs/                       # Documentation
```

### 🔧 Advanced Customization

**Custom Stylesheets:**
- Edit `get_stylesheet()` in `desktop_app.py`
- Uses PyQt6 QSS (Qt Style Sheets)
- RGB colors configurable in `branding.py`

**Additional UI Pages:**
- Extend `create_pages()` in `desktop_app.py`
- Add new navigation buttons in `create_sidebar()`
- Each page is a PyQt6 `QWidget`

**Auto-Updates:**
Enable in `branding.py`:
```python
enable_auto_updates: bool = True
```

### 📝 License & Copyright

Update in `branding.py`:
```python
license_type: str = "MIT"
copyright_year: str = "2025"
privacy_policy_url: str = "https://yourcompany.com/privacy"
```

### ✅ Checklist Before Release

- [ ] Logo files added to `assets/` folder
- [ ] Branding configured in `src/branding.py`
- [ ] Company information updated
- [ ] Support URLs configured
- [ ] Tested in development mode
- [ ] PyInstaller build successful
- [ ] Executable tested on target system
- [ ] Installer created (if distributing)

### 🆘 Troubleshooting

**"No module named PyQt6"**
```bash
pip install PyQt6
```

**Icon not showing in executable**
- Ensure `assets/icon.ico` exists
- Update path in `build_desktop.spec`
- Rebuild with PyInstaller

**Application won't start**
- Check dependencies: `pip install -r requirements.txt`
- Verify Python version: Python 3.8+
- Check console for error messages

**Need to add Python packages to build?**
- Update `hiddenimports` list in `build_desktop.spec`
- Re-run PyInstaller

---

For complete Voice Cloner documentation, see:
- [README.md](README.md) - Project overview
- [USER_GUIDE.md](docs/USER_GUIDE.md) - Usage guide
- [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Installation

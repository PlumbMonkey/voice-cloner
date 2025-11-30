# Voice Cloner - Branding & Customization Guide

Complete guide to customize Voice Cloner with your logo, colors, and company information.

## 🎨 Visual Branding

### Logo Setup

Your logo appears in multiple places:
1. **Application window** - Top center of main window
2. **Task bar** - Windows taskbar icon
3. **Desktop shortcut** - Shortcut icon
4. **Installer** - Setup wizard icon
5. **About dialog** - About window

### Step 1: Prepare Your Logo Files

**Create three versions of your logo:**

1. **logo.png** (150×150px)
   - Used in application header
   - PNG format with transparency
   - RGB or RGBA color space
   - Save as: `assets/logo.png`

2. **icon.ico** (256×256px)
   - Windows application icon
   - ICO format (Windows icon)
   - Used for: taskbar, shortcuts, installer
   - Save as: `assets/icon.ico`

3. **icon.png** (512×512px)
   - Linux/macOS icon
   - PNG format with transparency
   - Used for: AppImage, app bundle
   - Save as: `assets/icon.png`

### Step 2: Convert PNG to ICO

**Option A: Online Tool (Easiest)**
1. Visit: https://convertio.co/png-ico/
2. Upload `logo.png`
3. Select "Windows Icon (ICO)"
4. Download as `icon.ico`
5. Save to `assets/` folder

**Option B: Python Script**
```python
from PIL import Image

# Open your logo
img = Image.open("logo.png")

# Ensure it's RGB
if img.mode == "RGBA":
    img = img.convert("RGB")

# Save as ICO
img.save("assets/icon.ico", "ICO", sizes=[(256, 256)])

print("✅ icon.ico created!")
```

**Option C: Command Line (ImageMagick)**
```bash
convert logo.png -define icon:auto-resize=256,128,96,64,48,32,16 assets/icon.ico
```

## 🎯 Color Customization

Colors are defined as RGB tuples (Red, Green, Blue) where each value is 0-255.

### Current Color Scheme

```python
primary_color=(13, 71, 161)        # Dark blue
primary_light=(21, 101, 192)       # Light blue  
accent_color=(0, 204, 0)           # Bright green
text_color=(255, 255, 255)         # White
background_dark=(43, 43, 43)       # Dark gray
background_darker=(30, 30, 30)     # Darker gray
```

### RGB Color Reference

**Blues:**
- Navy: (0, 0, 128)
- Blue: (0, 0, 255)
- Dark Blue: (13, 71, 161)
- Light Blue: (21, 101, 192)
- Sky Blue: (135, 206, 235)

**Greens:**
- Dark Green: (0, 100, 0)
- Green: (0, 128, 0)
- Bright Green: (0, 255, 0)
- Lime: (0, 204, 0)
- Light Green: (144, 238, 144)

**Reds:**
- Dark Red: (139, 0, 0)
- Red: (255, 0, 0)
- Crimson: (220, 20, 60)
- Salmon: (250, 128, 114)

**Purples:**
- Dark Purple: (75, 0, 130)
- Purple: (128, 0, 128)
- Indigo: (75, 0, 130)
- Magenta: (255, 0, 255)

**Neutral:**
- Black: (0, 0, 0)
- White: (255, 255, 255)
- Gray: (128, 128, 128)
- Dark Gray: (64, 64, 64)

### Color Picker Tools
- https://coolors.co/ - Generate color palettes
- https://www.colorhexa.com/ - RGB converter
- https://www.rapidtables.com/web/color/RGB_to_HEX.html - RGB to Hex

### Custom Color Scheme Example

```python
# Modern Blue & Purple Theme
primary_color=(63, 81, 181)        # Indigo
primary_light=(66, 165, 245)       # Light blue
accent_color=(156, 39, 176)        # Purple

# Professional Gray Theme
primary_color=(33, 33, 33)         # Dark gray
primary_light=(66, 66, 66)         # Medium gray
accent_color=(3, 169, 244)         # Cyan

# Vibrant Orange & Blue
primary_color=(33, 150, 243)       # Blue
primary_light=(65, 105, 225)       # Royal blue
accent_color=(255, 152, 0)         # Orange
```

## 📝 Text & Metadata

Edit `src/branding.py`:

### Application Identity

```python
app_name = "Your App Name"         # Shown in window title
app_version = "1.0.0"              # Version number
app_tagline = "Your tagline here"  # Shown in about dialog
```

### Company Information

```python
company_name = "Your Company"
company_website = "https://yourcompany.com"
company_email = "support@yourcompany.com"
copyright_year = "2025"
license_type = "MIT"
```

### Support Links

```python
support_url = "https://yourcompany.com/support"
documentation_url = "https://yourcompany.com/docs"
bug_report_url = "https://github.com/yourcompany/voicecloner/issues"
privacy_policy_url = "https://yourcompany.com/privacy"
terms_url = "https://yourcompany.com/terms"
```

### Example Configuration

```python
DEFAULT_BRANDING = BrandingConfig(
    # Identity
    app_name="Voice Cloner Pro",
    app_version="1.0.0",
    app_tagline="Professional AI Voice Cloning for Musicians",
    
    # Company
    company_name="CreativeSound Studios",
    company_website="https://creativesound.io",
    company_email="hello@creativesound.io",
    
    # Branding
    primary_color=(45, 52, 82),       # Dark purple
    primary_light=(68, 79, 124),      # Light purple
    accent_color=(76, 175, 80),       # Green
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
    
    # Legal
    copyright_year="2025",
    license_type="Commercial",
    privacy_policy_url="https://creativesound.io/privacy",
    terms_url="https://creativesound.io/terms",
    
    # Support
    support_url="https://creativesound.io/support",
    documentation_url="https://creativesound.io/docs",
    bug_report_url="https://creativesound.io/report",
    
    # Features
    enable_auto_updates=True,
    enable_telemetry=False,
    enable_feedback=True,
)
```

## 🚀 Applying Changes

### After editing `src/branding.py`:

1. **Restart the application:**
   ```bash
   python src/desktop_app.py
   ```

2. **Changes appear in:**
   - Window title
   - About dialog
   - Help menu links
   - Status messages
   - All buttons and labels

3. **Rebuild installer if distributing:**
   ```bash
   python build_installer.py 1  # Windows EXE
   python build_installer.py 4  # macOS app
   ```

## 🎨 UI Customization

### Button Styles

Edit `get_button_style()` in `src/desktop_app.py`:

```python
def get_button_style(self, primary=False):
    if primary:
        return """
            QPushButton {
                background-color: #00cc00;
                color: black;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
            }
        """
```

### Complete Stylesheet

Edit `get_stylesheet()` to customize colors, fonts, spacing:

```python
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}
QPushButton {
    background-color: YOUR_COLOR;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
}
QTextEdit {
    background-color: #1e1e1e;
    color: #00ff00;
    border: 1px solid #3e3e3e;
}
```

### Font Customization

```python
# In any page creation function
title = QLabel("🎤 Voice Cloner Pro")
title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
```

## 📦 Distribution Branding

### Windows Installer

Edit `build_installer.py` section `build_nsis_installer()`:

```nsis
Name "Your App Name v{version}"
OutFile "YourApp-Setup-{version}.exe"
```

### macOS App Bundle

Edit `build_desktop.spec`:

```python
exe = EXE(
    ...
    name='Your App Name',
    ...
)
```

## ✅ Branding Checklist

- [ ] Logo files created (PNG, ICO)
- [ ] Logo files placed in `assets/`
- [ ] `src/branding.py` updated with company name
- [ ] Colors updated to match brand
- [ ] Support URLs configured
- [ ] Copyright year updated
- [ ] App name and version set
- [ ] Tagline/description added
- [ ] Application tested in dev mode
- [ ] Installer rebuilt with branding

## 🎯 Pre-Build Verification

Before building the final installer:

1. **Test in development:**
   ```bash
   python src/desktop_app.py
   ```

2. **Verify all branding appears:**
   - Window title
   - Logo in header
   - Company name in about
   - Support links work

3. **Check file paths:**
   - `assets/logo.png` exists
   - `assets/icon.ico` exists
   - All paths in `branding.py` are correct

4. **Test all buttons:**
   - Help → About
   - Help → Documentation
   - All menu items functional

5. **Rebuild installers:**
   ```bash
   python build_installer.py 1  # or appropriate option
   ```

## 📞 Support

For branding issues:
1. Verify all files in `assets/` are present
2. Check `src/branding.py` configuration
3. Try running in development mode first
4. Review error logs in `logs/` directory

---

**Your Voice Cloner app is now fully branded and ready for distribution!** 🎉

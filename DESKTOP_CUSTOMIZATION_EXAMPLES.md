# Desktop App - Visual Customization Examples

This document shows visual examples of how your branding will appear in the desktop application.

## 🎨 Color Scheme Examples

### Example 1: Professional Blue
```python
primary_color=(13, 71, 161)        # Dark blue
primary_light=(21, 101, 192)       # Light blue
accent_color=(0, 204, 0)           # Bright green
```
**Good for:** Professional software, business apps, music industry

### Example 2: Modern Purple
```python
primary_color=(63, 81, 181)        # Indigo
primary_light=(66, 165, 245)       # Light blue
accent_color=(156, 39, 176)        # Purple
```
**Good for:** Creative apps, design software, AI products

### Example 3: Vibrant Orange
```python
primary_color=(33, 150, 243)       # Bright blue
primary_light=(65, 105, 225)       # Royal blue
accent_color=(255, 152, 0)         # Orange
```
**Good for:** Creative tools, content creation, music production

### Example 4: Dark Tech
```python
primary_color=(33, 33, 33)         # Near black
primary_light=(66, 66, 66)         # Dark gray
accent_color=(0, 200, 255)         # Cyan
```
**Good for:** Developer tools, technical software, dark UI enthusiasts

### Example 5: Vibrant Green
```python
primary_color=(27, 94, 32)         # Dark green
primary_light=(56, 142, 60)        # Medium green
accent_color=(255, 215, 0)         # Gold
```
**Good for:** Audio processing, nature-inspired apps

## 🖼️ Logo Placement in App

Your logo appears in these locations:

```
┌─────────────────────────────────────────┐
│  🎤 Voice Cloner Pro              [_][□][✕] │
├──────────────┬──────────────────────────┤
│              │                          │
│ 🏠 Home      │    YOUR LOGO HERE        │
│ 🔧 Setup     │    (150x150px)          │
│ 🎵 Preprocess│                          │
│ 🧠 Train     │    Welcome Message       │
│ 🎙️ Infer     │                          │
│ ⚙️ Settings  │    [Start Setup Button]  │
│              │                          │
└──────────────┴──────────────────────────┘
```

## 📋 About Dialog

Your company branding appears in the About dialog:

```
┌──────────────────────────────────┐
│         About Voice Cloner Pro    │
├──────────────────────────────────┤
│                                  │
│    [YOUR LOGO]                   │
│                                  │
│  Voice Cloner Pro v1.0.0          │
│                                  │
│  AI-Powered Voice Cloning        │
│  for Music Production            │
│                                  │
│  © 2025 Your Company Name        │
│  MIT License                     │
│                                  │
│  Website: yourcompany.com        │
│  Support: support@yourcompany.com│
│                                  │
│            [  OK  ]              │
└──────────────────────────────────┘
```

## 🎯 Help Menu

Your support links appear in the Help menu:

```
Help
├── About
│   └── Shows: app name, logo, company, website
├── Documentation
│   └── Opens: yoursite.com/docs
└── Settings
    └── Support: support@yourcompany.com
```

## 🎨 Customization Scenarios

### Scenario 1: Solo Creator

```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="VoiceCloner",
    company_name="YourName Productions",
    company_website="https://yoursite.com",
    company_email="hello@yoursite.com",
    primary_color=(13, 71, 161),
    accent_color=(0, 204, 0),
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
)
```

**Result:** 
- Window title: "VoiceCloner"
- About shows: "© 2025 YourName Productions"
- Support link shows your email

### Scenario 2: Small Studio

```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="Studio Voice Pro",
    company_name="Creative Audio Studio",
    company_website="https://creativestudio.io",
    company_email="support@creativestudio.io",
    primary_color=(63, 81, 181),      # Purple
    accent_color=(76, 175, 80),       # Green
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
    support_url="https://creativestudio.io/support",
)
```

**Result:**
- Window title: "Studio Voice Pro"
- Purple and green interface
- Studio branding throughout
- Support portal link in help menu

### Scenario 3: Commercial Product

```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="VoiceCloner Enterprise",
    company_name="ProAudio Software Corp",
    company_website="https://proaudio.com",
    company_email="enterprise@proaudio.com",
    primary_color=(33, 150, 243),     # Professional blue
    accent_color=(255, 152, 0),       # Orange accent
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
    copyright_year="2025",
    license_type="Commercial",
    support_url="https://proaudio.com/support",
    documentation_url="https://docs.proaudio.com",
    bug_report_url="https://proaudio.com/issues",
    privacy_policy_url="https://proaudio.com/privacy",
    terms_url="https://proaudio.com/terms",
    enable_auto_updates=True,
    enable_feedback=True,
)
```

**Result:**
- Professional branding throughout
- Multiple support resources
- Auto-update support
- Commercial appearance

## 📦 Installer Branding

Your logo and colors appear in:

### Windows Installer
```
┌────────────────────────────────────┐
│  Voice Cloner Pro Installation     │
├────────────────────────────────────┤
│                                    │
│    [YOUR LOGO]                     │
│                                    │
│  Install Voice Cloner Pro          │
│  v1.0.0                            │
│                                    │
│  © 2025 Your Company               │
│                                    │
│  Installation Folder:              │
│  C:\Program Files\VoiceCloner\     │
│                                    │
│  [ Next > ]  [ Cancel ]            │
└────────────────────────────────────┘
```

### macOS App Bundle
- App name in Finder: "Voice Cloner Pro"
- App icon: Your custom icon
- About window: Your company branding

### Linux AppImage
- Icon in app menu: Your custom icon
- App title: "Voice Cloner Pro"
- .desktop file includes: Your company info

## 🎯 Icon Requirements by Platform

### Windows
- **Taskbar icon:** 32×32 (from ICO)
- **Desktop shortcut:** 32×32 (from ICO)
- **Installer:** 256×256 (from ICO)
- **File format:** .ico

### macOS
- **App icon:** 512×512 (from PNG)
- **Retina display:** @2x versions
- **File format:** .icns (converted from PNG)

### Linux
- **App menu icon:** 512×512 (PNG)
- **Desktop icon:** 128×128 (PNG)
- **File format:** .png

## 🎨 Font & Text Customization

You can customize fonts in `src/desktop_app.py`:

```python
# Example: Change title font
title = QLabel("🎤 Voice Cloner Pro")
title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
layout.addWidget(title)

# Available fonts:
# - Arial, Helvetica, Times New Roman, Courier
# - Sizes: 8-72pt
# - Weights: Light, Normal, Bold, Black
# - Styles: Normal, Italic
```

## 🌈 HSL to RGB Conversion

If you have colors in other formats:

```python
import colorsys

# Convert HSL to RGB
hue = 210 / 360      # 0-1
saturation = 0.9    # 0-1
lightness = 0.4     # 0-1

r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
rgb = (int(r * 255), int(g * 255), int(b * 255))

print(f"RGB: {rgb}")  # e.g., (13, 71, 161)
```

## 📐 Design System

The app follows this design system:

| Element | Purpose |
|---------|---------|
| **Primary Color** | Main buttons, highlights, active states |
| **Primary Light** | Button hover states, secondary highlights |
| **Accent Color** | Progress bars, success messages, important alerts |
| **Text Color** | Labels, descriptions, regular text (white) |
| **Background Dark** | Sidebar, main background |
| **Background Darker** | Text areas, input fields, nested elements |

## ✨ Pro Tips

1. **Logo Design:**
   - Keep logos simple (looks good at small sizes)
   - Use 1-3 colors max (easier to scale)
   - Leave transparent padding around logo
   - Test at 150×150px (app window size)

2. **Color Selection:**
   - Primary color: Use for interactive elements
   - Accent color: Use sparingly for success/alerts
   - Maintain high contrast for dark theme (white text)
   - Test colors on dark background (#2b2b2b)

3. **Branding Consistency:**
   - Use same colors across website and app
   - Match your brand guidelines
   - Test on multiple screen sizes
   - Get feedback from team members

4. **Icon Design:**
   - Convert from PNG to ICO without quality loss
   - Test icon at 16×16 (small taskbar)
   - Use tools: Figma, Adobe XD, Canva, Inkscape
   - Professional icon makers: FlatIcon, IcoMoon

## 🚀 Before Distributing

Checklist:

- [ ] Logo files created and placed in `assets/`
- [ ] Colors verified in app (run `python src/desktop_app.py`)
- [ ] Company info correct in `branding.py`
- [ ] Support links active and correct
- [ ] About dialog shows branding correctly
- [ ] Icon appears in taskbar and shortcuts
- [ ] Installer looks professional
- [ ] All text displays without truncation
- [ ] Links in Help menu work
- [ ] App runs on target platforms

## 📞 Getting Help

**Logo Design:**
- Hire designer: Fiverr, Upwork, 99designs
- DIY: Canva (easiest), Figma, Adobe XD
- Free: Inkscape (open source)

**Icon Creation:**
- Online converter: https://convertio.co/png-ico/
- Python PIL/Pillow library
- Professional icon designer

**Color Selection:**
- Color palette generator: https://coolors.co/
- Brand color tools: https://www.brandisty.com/
- Accessibility check: https://webaim.org/resources/contrastchecker/

---

**Ready to customize?** Start with your logo, then edit `src/branding.py`! 🎨

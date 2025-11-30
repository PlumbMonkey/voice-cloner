# Assets - Branding Files

Place your custom branding files here:

## Logo Files

- **logo.png** - Application logo (150x150px PNG)
  - Used in main window header
  - Should include transparency
  - Format: PNG (recommended)

- **icon.ico** - Application icon for Windows (256x256px ICO)
  - Used for taskbar, desktop shortcut, installer
  - Format: ICO (Windows icon)
  - Convert from PNG using: https://convertio.co/png-ico/

- **icon.png** - Icon file for Linux/macOS (512x512px PNG)
  - Used in AppImage and macOS app bundle
  - Format: PNG with transparency

## Favicon

- **favicon.ico** - Website favicon (32x32px ICO)
  - For web documentation (if applicable)

## How to Create Icons from Your Logo

### Method 1: Online Converter (Easiest)
1. Go to: https://convertio.co/png-ico/
2. Upload your PNG logo
3. Download as ICO
4. Place in assets/

### Method 2: Python PIL/Pillow
```python
from PIL import Image

# Open your PNG
img = Image.open("logo.png")

# Resize to icon size
img = img.resize((256, 256), Image.Resampling.LANCZOS)

# Save as ICO
img.save("icon.ico")

print("✅ icon.ico created!")
```

### Method 3: ImageMagick
```bash
convert logo.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico
```

## Customization Tips

- **Logo Format:** PNG with transparent background works best
- **Color Space:** Use RGB or RGBA
- **Background:** Transparent background recommended
- **Size:** Design at 512x512px, then scale down as needed
- **Font:** Use clear, readable fonts
- **Simplicity:** Keep design simple for small sizes

## Using Custom Branding

After adding files, update `src/branding.py`:

```python
DEFAULT_BRANDING = BrandingConfig(
    app_name="Your App Name",
    company_name="Your Company",
    logo_path=Path("assets/logo.png"),
    icon_path=Path("assets/icon.ico"),
)
```

## File Checklist

- [ ] logo.png (150x150px)
- [ ] icon.ico (256x256px)
- [ ] icon.png (512x512px)
- [ ] favicon.ico (32x32px) - optional
- [ ] Colors updated in branding.py
- [ ] Company info updated in branding.py

## Recommended Tools

- **Design:** Adobe XD, Figma, Canva
- **Conversion:** https://convertio.co/, ImageMagick
- **Icon Design:** https://www.flaticon.com/, https://www.icoconvert.com/
- **Color Picker:** https://coolors.co/

---

After adding your logo files, run:
```bash
python src/desktop_app.py
```

Your logo will appear in the application!

# Voice Cloner Pro - Installation & Usage Guide

## 📦 Installation

### For End Users (Easiest Method)

1. **Download the installer**
   - Get `INSTALL.bat` from the project folder

2. **Run the installer**
   - Right-click `INSTALL.bat`
   - Select **"Run as Administrator"**
   - Click "Yes" when prompted for admin rights
   - Wait for the installation to complete

3. **Verify installation**
   - Look for **"Voice Cloner Pro"** shortcut on your Desktop
   - Or find it in your Start Menu

### What the installer does:
- ✅ Copies all application files to `Program Files\Voice Cloner Pro`
- ✅ Creates a Desktop shortcut for easy access
- ✅ Adds entry to Windows Start Menu
- ✅ Creates an uninstaller script

---

## 🚀 Running the Application

### Method 1: Desktop Shortcut (Recommended)
1. Double-click the **"Voice Cloner Pro"** shortcut on your Desktop
2. Application launches immediately

### Method 2: Start Menu
1. Press **Windows Key** or click Start
2. Type **"Voice Cloner Pro"**
3. Click the result to launch

### Method 3: Manual Launch
1. Navigate to: `C:\Program Files\Voice Cloner Pro`
2. Double-click `VoiceCloner.bat`
3. Application launches in a command window

---

## 📋 Application Features

The desktop application has 6 main tabs:

### 1. **Home Tab**
- Overview of Voice Cloner Pro
- Quick start guide
- System information

### 2. **Setup Tab**
- Configure model path
- Set output directory
- Verify installation
- Download dependencies if needed

### 3. **Preprocess Tab**
- Upload or record audio samples
- Audio quality checks
- Preprocessing options
- Save preprocessed data

### 4. **Train Tab**
- Start model training
- Adjust training parameters
- Monitor training progress
- Save trained models

### 5. **Infer Tab**
- Select trained model
- Input text or audio
- Generate voice clone
- Play preview and download results

### 6. **Settings Tab**
- Application preferences
- Theme selection (Light/Dark)
- Audio device selection
- Advanced options

---

## ⚙️ System Requirements

- **OS:** Windows 10 or later
- **RAM:** 8GB minimum (16GB recommended for training)
- **Storage:** 5GB free space
- **GPU:** Optional (NVIDIA GPU recommended for faster training)
- **Audio:** Microphone and speakers for recording/playback

---

## 🔧 First Time Setup

When you launch the application for the first time:

1. **Go to Settings Tab**
   - Configure your preferred audio device
   - Select light or dark theme
   - Adjust other preferences

2. **Go to Setup Tab**
   - Click "Verify Installation"
   - If needed, follow prompts to install dependencies
   - Set your preferred model and output directories

3. **You're ready!**
   - Go to Preprocess tab to get started with voice data

---

## 📖 Workflow: Voice Cloning Steps

### Step 1: Prepare Audio (Preprocess Tab)
- Record or upload 10-30 seconds of clear speech samples
- Application analyzes audio quality
- Preprocesses files for training

### Step 2: Train Model (Train Tab)
- Select your preprocessed audio
- Choose training duration (10-60 minutes typical)
- Monitor progress
- Save trained model

### Step 3: Clone Voice (Infer Tab)
- Load your trained model
- Enter text or upload audio
- Click "Generate"
- Preview and download results

---

## ❌ Uninstalling

### Remove Voice Cloner Pro

1. Navigate to: `C:\Program Files\Voice Cloner Pro`
2. Double-click `UNINSTALL.bat`
3. Click "Yes" to confirm uninstall
4. Application folder is completely removed

### Manual Uninstall (if needed)
1. Press **Windows Key + R**
2. Type: `%ProgramFiles%`
3. Delete the **"Voice Cloner Pro"** folder
4. Remove desktop shortcut (right-click → Delete)

---

## 🆘 Troubleshooting

### Application won't start
- **Solution:** Run as Administrator
- Ensure Python 3.10+ is installed
- Check that Windows Defender isn't blocking it

### Missing audio devices
- **Solution:** Connect microphone/speakers and restart app
- Go to Settings → Audio Device → Select correct device

### Training is very slow
- **Solution:** GPU training is faster - install NVIDIA CUDA if available
- Close other applications to free RAM
- Reduce training duration

### "Permission Denied" errors
- **Solution:** Run installer as Administrator
- Check that installation folder isn't read-only

### Model files not saving
- **Solution:** Ensure you have write permissions to output directory
- Check available disk space (need ~2-5GB free)

---

## 📞 Support

For issues or questions:
1. Check the in-app Help section
2. Review the documentation in the application
3. Visit the GitHub repository for updates

---

## 🎯 Tips for Best Results

✅ **Audio Quality**
- Use a good quality microphone
- Record in a quiet room
- Speak clearly and naturally
- Aim for consistent tone throughout

✅ **Training Data**
- Collect 15-30 seconds of speech
- Use diverse speech patterns
- Avoid background noise
- Include various phonemes

✅ **Generated Voice**
- Start with short text (5-20 words)
- Adjust parameters gradually
- Use similar voice tone in reference audio
- Export high-quality audio files

---

## 📝 File Locations

| Purpose | Location |
|---------|----------|
| Application | `C:\Program Files\Voice Cloner Pro` |
| Desktop Shortcut | `C:\Users\[YourName]\Desktop\` |
| Start Menu | `C:\Users\[YourName]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\` |
| Output Files | Configurable in Setup tab |
| Models | Configurable in Setup tab |

---

## Version & Updates

**Current Version:** 1.0.0  
**Last Updated:** November 2025

Check the GitHub repository for the latest updates and new features.

---

**Enjoy using Voice Cloner Pro!** 🎙️

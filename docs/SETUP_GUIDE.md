# Setup Guide - Voice Cloner

Complete setup instructions for getting Voice Cloner ready to use.

## Prerequisites

- Windows 10/11, Ubuntu 20.04+, or macOS 12+
- Python 3.8-3.10
- 8GB RAM minimum
- 10GB free disk space
- (Optional) NVIDIA GPU with 6GB+ VRAM for faster training

## Step 1: System Requirements Check

### Windows

```powershell
# Check Python version
python --version

# Should output: Python 3.8.x, 3.9.x, or 3.10.x
```

### Linux/macOS

```bash
# Check Python version
python3 --version

# Should output: Python 3.8.x, 3.9.x, or 3.10.x
```

### GPU Check (Optional)

```bash
# Windows (Command Prompt)
nvidia-smi

# Linux
nvidia-smi

# Should show your NVIDIA GPU details
```

## Step 2: Clone/Download Project

```bash
# Option A: Clone from Git
git clone https://github.com/[repo]/Voice-Cloner.git
cd Voice-Cloner

# Option B: Extract ZIP
unzip Voice-Cloner.zip
cd Voice-Cloner
```

## Step 3: Create Virtual Environment

### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get permission denied:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install base requirements
pip install -r requirements.txt
```

### For GPU Support (Optional)

```bash
# Install CUDA-enabled PyTorch (choose one based on GPU)

# For RTX 30/40 series (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For RTX 20 series or older (CUDA 11.7)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

## Step 5: Initialize Project

```bash
# Windows
python -m src.main init

# Linux/macOS
python3 -m src.main init
```

## Step 6: Detect Environment

```bash
# Windows
python -m src.main detect

# Linux/macOS
python3 -m src.main detect
```

You should see:
- ✓ OS Compatibility
- ✓ Python Version
- ✓ GPU Availability (if available)
- ✓ System Specifications

## Step 7: Complete Environment Setup

```bash
# Windows
python -m src.main setup

# Linux/macOS
python3 -m src.main setup
```

This will:
1. Create isolated Python environment
2. Install all dependencies
3. Clone SO-VITS-SVC repository
4. Download pretrained models

**This may take 10-20 minutes depending on internet speed.**

## Step 8: Verify Installation

```bash
# Check status
python -m src.main status

# Generate report
python -m src.main report
```

All phases should show as complete.

## Troubleshooting Setup

### Issue: Python command not found

**Windows:**
```powershell
# Try python3
python3 --version

# If not found, add Python to PATH
```

**Linux/macOS:**
```bash
# Use python3 explicitly
python3 -m src.main init
```

### Issue: Permission denied (Linux/macOS)

```bash
chmod +x src/main.py
python3 -m src.main init
```

### Issue: Git not found

Install Git from https://git-scm.com/

### Issue: No GPU detected

This is normal if you don't have NVIDIA GPU. Training will use CPU (slower but works).

### Issue: CUDA version mismatch

```bash
# Check CUDA version
nvidia-smi

# Reinstall PyTorch for your CUDA version
pip install torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/cuXXX
```

### Issue: Out of disk space

```bash
# Requires ~50GB for optimal training
# Minimum 10GB for preprocessing
# Check your disk: df -h (Linux/macOS) or diskpart (Windows)
```

## Next Steps

After successful setup:

1. **Prepare your voice recordings**
   - Record 15-30 minutes of clean singing
   - Place in `./data/input/` folder

2. **Run quickstart**
   ```bash
   python -m src.main quickstart
   ```

3. **Wait for training to complete**
   - Check progress: `python -m src.main status`

4. **Convert voice**
   ```bash
   python -m src.main infer vocals_input.wav vocals_output.wav
   ```

5. **Import into FL Studio**
   - Follow the FL Studio integration guide

## Getting Help

If setup fails:

1. Check error messages in console
2. Review logs: `./logs/voice_cloner.log`
3. Run detection again: `python -m src.main detect`
4. Verify all system requirements are met

---

**Setup complete! Ready to train your AI voice. 🎤**

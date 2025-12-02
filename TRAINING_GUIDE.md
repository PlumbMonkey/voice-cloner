# Voice Cloner - Training Guide

This guide walks you through training your personal voice model.

## Overview

Training teaches the AI your unique voice characteristics so it can apply them to any audio. Once trained, you can use your model unlimited times for conversions.

## Prerequisites

✅ Voice samples (8 files, 94 MB) - Ready!
✅ so-vits-svc-fork installed - Ready!
✅ Python 3.10+ - Ready!

## Training Step by Step

### Option 1: WebUI (Recommended) ⭐

The WebUI provides a visual interface for preprocessing and training.

#### Windows

1. **Download WebUI**
   - Go to: https://github.com/voicepaw/so-vits-svc-fork/releases
   - Download: `so-vits-svc-fork-webui.exe`
   - Run the executable

2. **Use WebUI to Train**
   - Navigate to **"Preprocess"** tab
   - Set source directory: `./samples`
   - Set output sample rate: `44100`
   - Click **"Preprocess"**
   - Wait for preprocessing (5-10 mins)

3. **Train the Model**
   - Navigate to **"Train"** tab
   - Settings:
     - Batch size: `16`
     - Learning rate: `0.0001`
     - Epochs: `100-200` (more = better quality, longer training)
     - Save interval: `50`
   - Click **"Train"**
   - Wait 30 mins - 2 hours

4. **Find Your Model**
   - After training, find model in `./checkpoints/`
   - Typically named like: `G_XXX.pth`

#### macOS/Linux

1. **Clone and setup**
   ```bash
   git clone https://github.com/voicepaw/so-vits-svc-fork.git
   cd so-vits-svc-fork
   pip install -e .
   ```

2. **Run WebUI**
   ```bash
   python -m so_vits_svc_fork.webui.new_ui
   ```

3. **Follow same steps as Windows above**

### Option 2: Command Line

If WebUI doesn't work, use the command line:

```bash
# Step 1: Preprocess (resample to 44.1kHz)
svc pre-resample --sr 44100 --in-dir samples

# Step 2: Extract voice features (HuBERT)
svc pre-hubert --in-dir samples/44k

# Step 3: Train the model
svc train --config configs/config.json

# Monitoring training:
# - Logs saved to ./logs/
# - Model checkpoints saved to ./checkpoints/ every 50 epochs
```

**Training time:** 30 mins - 2 hours (depends on GPU)

### Option 3: Python API (Advanced)

For programmatic control:

```python
from so_vits_svc_fork.train import main as train_main
from so_vits_svc_fork.preprocess import main as preprocess_main

# Preprocess
preprocess_main(
    dataset_path="samples",
    output_path="samples/44k",
    sr=44100
)

# Extract features
hubert_main(dataset_path="samples/44k")

# Train
train_main(config_path="configs/config.json")
```

## Monitoring Training

During training, check:

1. **Training Logs**
   ```bash
   # View real-time training progress
   cat logs/training.log
   ```

2. **Model Checkpoints**
   ```bash
   # Look in checkpoints/ folder
   dir checkpoints/
   ```

3. **GPU Usage**
   - Use `nvidia-smi` to monitor GPU memory
   - Should use 6-8 GB VRAM on RTX 3070

## After Training

Once training completes:

1. **Find Your Model**
   - Location: `checkpoints/G_XXXXX.pth`
   - Size: ~100-200 MB

2. **Test Your Model**
   ```bash
   python convert.py input/vocal_stem.wav
   ```

3. **Adjust Quality if Needed**
   ```bash
   # More of your voice
   python convert.py input/vocals.wav --index-rate 0.8
   
   # Less aggressive
   python convert.py input/vocals.wav --index-rate 0.3
   ```

## Troubleshooting

### Training Fails / Out of Memory

**Problem:** "CUDA out of memory"

**Solutions:**
- Reduce batch size in config: `"batch_size": 8` (instead of 16)
- Train on CPU (slower but always works)
- Use a simpler config

### Poor Quality Results

**Problem:** Converted audio sounds weird or like original voice

**Reasons & Fixes:**
1. **Bad training samples**
   - Voice samples need to be consistent
   - Remove files with background noise
   - Retrain with better samples

2. **Insufficient training**
   - Train longer (increase epochs to 200)
   - Use more voice samples (20-30 minutes ideal)

3. **Model overfitting**
   - If samples are too similar, model can overfit
   - Collect more diverse samples (different speaking styles, emotions)

### WebUI Won't Start

**Problem:** WebUI executable won't launch

**Solution:** Use CLI instead:
```bash
python -m so_vits_svc_fork.inference.main --help
```

### "No module named 'so_vits_svc_fork'"

**Problem:** Import error

**Solution:** Reinstall:
```bash
pip install --force-reinstall so-vits-svc-fork
```

## Training Tips for Best Quality

### 1. Voice Sample Preparation
- ✅ **Use clear, clean recordings**
- ✅ **Record in quiet environment**
- ✅ **Ensure consistent quality across samples**
- ❌ Don't use heavily compressed audio
- ❌ Don't mix multiple voices

### 2. Sample Diversity
- Include different speaking/singing styles
- Mix of speech and singing (if you want both)
- Vary emotion/energy levels
- Aim for 15-30 minutes minimum

### 3. Training Parameters
- **Batch size**: 16 (default) or 8 (if out of memory)
- **Learning rate**: 0.0001 (standard)
- **Epochs**: 100-200 (more = better, but slower)
- **Save interval**: 50 (save checkpoint every 50 epochs)

### 4. Hardware Optimization
- Use GPU if available (RTX 3070+)
- Close other programs to free RAM
- Use SSD for faster I/O

## Validation Checklist

Before converting audio, verify:

- [ ] Training completed without errors
- [ ] Model file exists in `checkpoints/`
- [ ] Model file size is 100-200 MB
- [ ] You can run `python convert.py input/test.wav` without errors
- [ ] Output audio sounds reasonable

## Next Steps

Once training is complete:

1. **Convert Your First Audio**
   ```bash
   python convert.py input/vocal_stem.wav
   ```

2. **Fine-tune with Parameters**
   ```bash
   python convert.py input/vocals.wav --index-rate 0.6 --pitch-shift 0
   ```

3. **Use in FL Studio**
   - Import converted audio back into FL Studio
   - Layer with other stems
   - Adjust timing/EQ as needed

4. **Share Your Results**
   - Tweet @PlumbMonkey
   - Share on GitHub discussions
   - Show the community!

## Performance Expectations

| Scenario | Quality | Notes |
|---|---|---|
| 10 mins training data | 5/10 | Baseline, okay results |
| 20 mins training data | 7/10 | Good quality |
| 30 mins training data | 8.5/10 | Very good |
| 50+ mins training data | 9/10 | Excellent |

**Formula:** More data + More training = Better quality

## Reference

- **so-vits-svc-fork**: https://github.com/voicepaw/so-vits-svc-fork
- **Original so-vits-svc**: https://github.com/svc-develop-team/so-vits-svc
- **Training Guide**: See their README for advanced options

---

**Questions?** Check our [QUICKSTART.md](QUICKSTART.md) or open an issue on GitHub.

**Happy training!** 🎵

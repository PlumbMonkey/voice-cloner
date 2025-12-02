# Voice Cloner - Quick Start Guide

## What You Need to Know

Voice Cloner converts any audio to sound like YOUR voice using AI. It has two main steps:

1. **Train** - Teach the AI your voice (30 mins - 2 hours, one time)
2. **Convert** - Use your trained voice to convert other audio (fast, unlimited)

---

## Installation

### Prerequisites
- Python 3.10+
- NVIDIA GPU (recommended but optional)
- 10-30 minutes of your voice recordings

### Setup

```bash
# Clone and setup
git clone https://github.com/PlumbMonkey/voice-cloner.git
cd voice-cloner

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Step 1: Prepare Your Voice

1. **Collect voice samples** - Record 10-30 minutes of YOUR voice
   - Clear speech or singing
   - Minimal background noise
   - Format: WAV or MP3

2. **Place in `samples/` folder**
   ```
   voice-cloner/
   └── samples/
       ├── recording1.wav
       ├── recording2.wav
       ├── recording3.wav
       └── recording4.wav
   ```

3. **Verify quality**
   - Listen to each file
   - Make sure it's all YOUR voice
   - No other speakers or heavy background noise

✅ **Your samples are ready!** Run:
```bash
python train.py
```

---

## Step 2: Train Your Voice Model

### Option A: Use WebUI (Easiest) ⭐ RECOMMENDED

1. **Download WebUI**
   - GitHub: https://github.com/voicepaw/so-vits-svc-fork/releases
   - Windows: Download `so-vits-svc-fork-webui.exe`
   - Or use command line (see Option B)

2. **Use WebUI to Train**
   - Open the WebUI
   - Point to your `samples/` folder
   - Click "Preprocess" then "Train"
   - Wait 30 mins - 2 hours
   - Model saves to `checkpoints/`

### Option B: Use Command Line

```bash
# Preprocess your voice
svc pre-resample --sr 44100 --in-dir samples

# Extract voice features
svc pre-hubert --in-dir samples/44k

# Train the model
svc train --config configs/config.json
```

⏱️ **Training time:** 30 mins - 2 hours (depending on GPU)

---

## Step 3: Convert Audio to Your Voice

Once training is complete:

```bash
# Place vocal stem in input/
# Then run conversion:
python convert.py input/vocal_stem.wav

# Output appears in output/ folder
```

### Adjust Quality

```bash
python convert.py input/vocals.wav \
  --pitch-shift 0          # Adjust pitch if needed
  --index-rate 0.5         # Voice blend strength (0.3-0.7 recommended)
  --f0-method crepe        # Method: crepe, parselmouth, dio
  --output output/my_voice.wav
```

---

## FL Studio Workflow

1. **Break down your song into stems** in FL Studio
2. **Export vocal stem** as WAV (16-bit, 44.1kHz)
3. **Place in `input/` folder**
4. **Run conversion**
   ```bash
   python convert.py "input/My Song - Vocals.wav"
   ```
5. **Import converted vocals** back into FL Studio
6. **Mix with other stems**

---

## Troubleshooting

### "Model not found"
→ Train your model first using `python train.py` and follow Option A or B

### "CUDA out of memory"
→ Use `--index-rate 0.3` for faster processing
→ Or train on CPU (slower but works)

### "Conversion sounds wrong"
→ Your training samples might not be good quality
→ Retrain with more/better voice recordings
→ Adjust `--index-rate` (try 0.3, 0.5, 0.7)

### "Audio quality is bad"
→ Use high-quality input audio (WAV, 44.1kHz+)
→ Train with more voice samples (20-30 minutes)
→ Tune pitch with `--pitch-shift`

---

## Performance

| Task | Time (RTX 3070) | Time (CPU) |
|------|---|---|
| Train | 30 mins - 2 hours | 5-10 hours |
| Convert 10s | ~2 seconds | ~20 seconds |
| Convert 1m | ~20 seconds | ~3 minutes |

**Faster?** Use a better GPU (RTX 4070, A100, etc.)

---

## File Structure

```
voice-cloner/
├── samples/          # Your voice recordings (10-30 mins)
├── input/            # Audio to convert (vocals, stems)
├── output/           # Converted audio (automatic)
├── checkpoints/      # Your trained model (after training)
├── models/           # Pre-trained models (optional)
├── src/
│   ├── core/         # Voice conversion engine
│   └── utils/        # Audio utilities
├── convert.py        # Main conversion tool
├── train.py          # Training setup guide
├── requirements.txt  # Dependencies
└── README.md         # Full documentation
```

---

## System Requirements

| | Minimum | Recommended |
|---|---|---|
| **OS** | Windows/Mac/Linux | Windows 10+ |
| **Python** | 3.10 | 3.11+ |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 10 GB | 30 GB |
| **GPU** | Optional | NVIDIA RTX 3060+ |

**GPU Acceleration:** ~5-10x faster with NVIDIA GPU

---

## Advanced Parameters

```bash
python convert.py input/vocals.wav \
  --speaker-id 0              # Speaker ID (if multiple in model)
  --pitch-shift -2            # Lower pitch (-12 to +12 semitones)
  --f0-method crepe           # F0 extraction method
  --index-rate 0.7            # Feature retrieval strength (0.0-1.0)
  --output output/custom.wav  # Custom output path
```

### F0 Methods Explained
- **crepe** - Most accurate (slower, ~3-5s per 10s)
- **parselmouth** - Faster, good quality (fastest)
- **dio/harvest** - Very fast, lower quality

### Pitch Shift Tips
- Negative = lower pitch (sounds more male)
- Positive = higher pitch (sounds more female)
- Example: `-5` = half step lower, `+7` = half step higher

---

## Command Cheat Sheet

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Prepare
python train.py

# Convert
python convert.py input/vocals.wav

# Advanced conversion
python convert.py input/vocals.wav --pitch-shift 2 --index-rate 0.6

# List models
python convert.py --list-models
```

---

## Licensing & Attribution

This project uses **open-source components**:
- **so-vits-svc-fork** - Voice conversion (AGPL-3.0)
- **Voice Cloner wrapper** - MIT License

See LICENSE file for details.

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Prepare your voice samples
3. ⏳ Train your model (30 mins - 2 hours)
4. 🎵 Convert your first audio
5. 🚀 Share your results!

**Having issues?** Check troubleshooting section above.

**Want to contribute?** Visit: https://github.com/PlumbMonkey/voice-cloner

---

**Happy cloning! 🎤**

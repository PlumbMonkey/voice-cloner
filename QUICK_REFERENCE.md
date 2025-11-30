# Voice Cloner - Quick Reference Card

## Installation (30 seconds)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source venv/bin/activate

# Install
pip install -r requirements.txt
```

## Basic Commands

```bash
# Check system
python -m src.main detect

# Full setup
python -m src.main setup

# Preprocess audio
python -m src.main preprocess ./data/input

# Train model (100 epochs)
python -m src.main train --epochs 100

# Convert voice
python -m src.main infer input.wav output.wav

# Batch convert
python -m src.main batch_infer ./input ./output
```

## Quick Workflow (All-in-One)

```bash
python -m src.main quickstart
# Follow interactive prompts
```

## File Preparation

```
Place your vocal recordings in:
Voice-Cloner/
└── data/
    └── input/
        ├── vocal_1.wav
        ├── vocal_2.wav
        └── vocal_3.wav
        
Minimum: 10 minutes total audio
Recommended: 20-30 minutes
Format: WAV, MP3, FLAC, OGG
```

## FL Studio Import (3 Steps)

1. **Open Edison** → Mixer → Edison plugin
2. **Drag converted WAV** → into Edison window
3. **Export** → to new track

## Parameter Adjustment

```bash
# More epochs = better quality
python -m src.main train --epochs 200

# Pitch shift (semitones)
python -m src.main infer input.wav output.wav --pitch-shift 5

# Different F0 method
python -m src.main infer input.wav output.wav --f0-method harvest
```

## Pitch Shift Reference

```
+12  = 1 octave higher
+5   = Medium increase
0    = No change
-5   = Medium decrease
-12  = 1 octave lower
```

## F0 Methods

```
crepe   = Highest quality (slowest)
dio     = Fast (good for clean audio)
harvest = Balanced approach
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| GPU not detected | Install NVIDIA drivers + CUDA |
| Out of memory | Reduce batch size: `--batch-size 8` |
| Python 3.11+ | Downgrade to 3.8-3.10 |
| No audio files found | Check file format and location |
| Training too slow | Use GPU or reduce dataset |

## Configuration (.env)

```ini
# Increase quality
TRAINING_EPOCHS=200

# Reduce VRAM usage
BATCH_SIZE=8

# Change device
DEVICE=cpu  # or cuda
```

## Check Progress

```bash
# Status check
python -m src.main status

# Full report
python -m src.main report

# View logs
tail -f ./logs/voice_cloner.log
```

## Device Support

```
GPU (RTX 3060):    2-4 hours training
GPU (GTX 1060):    8-12 hours training
CPU-only:          24-48+ hours training
```

## Output Location

```
Output files saved to:
Voice-Cloner/
└── output/
    ├── voice_converted.wav
    └── [other converted files]
```

## Important Reminders

✅ **DO:**
- Record in quiet environment
- Use 44.1kHz sample rate
- Record 20-30 minutes of vocals
- Monitor training progress
- Save FL Studio project frequently

❌ **DON'T:**
- Close terminal during training
- Set volume to maximum
- Use heavily compressed audio
- Over-process with effects
- Forget to backup recordings

## Documentation

- **README.md** - Full overview
- **SETUP_GUIDE.md** - Installation help
- **USER_GUIDE.md** - Detailed guide
- **FL_STUDIO_GUIDE.md** - FL Studio help

## Support Commands

```bash
# Help for any command
python -m src.main COMMAND --help

# Show all commands
python -m src.main --help

# FL Studio guide
python -m src.main guide

# Interactive setup
python -m src.main quickstart
```

## Common Workflows

### Workflow 1: First Time Setup
```bash
python -m src.main quickstart
```

### Workflow 2: Just Test (No GPU)
```bash
# Edit .env: DEVICE=cpu
python -m src.main detect
python -m src.main setup
```

### Workflow 3: Advanced User
```bash
python -m src.main detect
python -m src.main setup
python -m src.main preprocess ./vocals
python -m src.main train --epochs 200 --batch-size 8
python -m src.main batch_infer ./input ./output --pitch-shift 2
```

---

**Print this card for quick reference! 🎤**

**Latest Version**: 0.1.0

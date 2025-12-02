# Voice Cloner - Quick Start Guide

## Installation

### Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA (recommended for speed, optional)
- ~8GB free disk space for models

### Setup (Windows)

```bash
# 1. Clone the repository
git clone https://github.com/PlumbMonkey/voice-cloner.git
cd voice-cloner

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# If you want GPU acceleration (NVIDIA):
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Setup (macOS/Linux)

```bash
git clone https://github.com/PlumbMonkey/voice-cloner.git
cd voice-cloner

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Step 1: Prepare Your Voice Samples

1. **Collect your voice recordings**
   - Record clear samples of YOUR voice
   - Format: WAV or MP3
   - Duration: 10-30 minutes total (minimum)
   - Quality: Minimal background noise, clear speech

2. **Place samples in `samples/` folder**
   ```
   samples/
   ├── sample1.wav
   ├── sample2.wav
   ├── sample3.wav
   └── sample4.wav
   ```

3. **Important: Verify it's YOUR voice**
   - Listen to each file
   - Make sure all samples are consistent (same person)
   - Remove any files with background noise or multiple speakers

---

## Step 2: Train Your Voice Model

```bash
python train.py
```

This will:
1. Resample your voice samples to 44.1kHz
2. Extract HuBERT voice features
3. Train the model (takes 30 mins - 2 hours depending on GPU)
4. Save the model to `checkpoints/`

**First time?** It will download pre-trained models (~500MB).

---

## Step 3: Convert Audio to Your Voice

```bash
# Simple conversion
python convert.py input/vocals.wav

# With custom settings
python convert.py input/vocals.wav \
  --output output/my_version.wav \
  --pitch-shift 0 \
  --index-rate 0.5

# List available models
python convert.py --list-models
```

### Output
Converted audio will appear in `output/` folder.

---

## Advanced Usage

### Parameters

```bash
python convert.py input/file.wav \
  --speaker-id 0              # Which speaker to use (if multiple)
  --pitch-shift 0             # Shift pitch in semitones (-12 to +12)
  --f0-method crepe           # F0 extraction: crepe, parselmouth, dio, harvest
  --index-rate 0.5            # Feature retrieval strength (0.0-1.0)
  --output output/custom.wav  # Output filename
```

### F0 Methods
- **crepe**: Most accurate, but slower (default)
- **parselmouth**: Fast, good quality
- **dio/harvest**: Very fast, lower quality

### Pitch Shift
- Negative values: Lower pitch (male voice)
- Positive values: Higher pitch (female voice)
- Example: `-5` semitones = lower by half a step

---

## FL Studio Workflow

1. **Export vocal stem** as WAV (16-bit, 44.1kHz)
2. **Place in `input/` folder**
3. **Run conversion**: `python convert.py input/vocal_stem.wav`
4. **Import result** back into FL Studio
5. **Blend with other stems** to create final mix

---

## Troubleshooting

### "Model not found"
- Train a model first: `python train.py`
- Or download a pre-trained model

### "CUDA out of memory"
- Reduce GPU usage: Use `--index-rate 0.3` for faster processing
- Or use CPU: Models are slower but work

### "Conversion sounds wrong"
- Check your voice samples are good quality
- Retrain with more/better data
- Adjust `--index-rate` (try 0.3 to 0.7)

### Poor audio quality
- Use high-quality input (WAV, 44.1kHz+)
- Train with more voice samples
- Adjust pitch shift if needed

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 8GB | 16GB |
| Disk | 5GB | 20GB |
| GPU | Optional | NVIDIA RTX 3060+ |

**Inference times** (on RTX 3070):
- 10 second audio: ~2-5 seconds
- 1 minute audio: ~30-60 seconds
- CPU: ~5-10x slower

---

## File Structure

```
voice-cloner/
├── samples/          # Put your voice recordings here
├── input/            # Audio files to convert
├── output/           # Converted audio
├── models/           # Pre-trained models
├── checkpoints/      # Your trained model
├── src/
│   ├── core/         # Voice conversion engine
│   └── utils/        # Audio utilities
├── convert.py        # Convert audio
├── train.py          # Train a model
└── README.md         # Full documentation
```

---

## Next Steps

- **Improve quality**: Collect more voice samples (20-30 min)
- **Fine-tune**: Experiment with `--index-rate` and `--pitch-shift`
- **Automate**: Create batch conversion scripts
- **Share**: Contribute improvements back to the community!

---

## Community & Support

- **GitHub**: https://github.com/PlumbMonkey/voice-cloner
- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share tips
- **License**: MIT (see LICENSE file)

---

## Credits

Built with [so-vits-svc-fork](https://github.com/voicepaw/so-vits-svc-fork) - a community fork of the Singing Voice Conversion project.

Happy cloning! 🎵

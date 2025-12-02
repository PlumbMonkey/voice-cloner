# Voice Cloner

Convert any vocal audio to sound like YOUR voice using AI. Perfect for musicians, producers, and content creators.

## What It Does

Transform vocals, singing, or speech into your voice while preserving the original performance, emotion, and timing. Great for:

- 🎵 **Music Production** - Replace vocals in song stems from FL Studio, Ableton, Logic Pro
- 🗣️ **Voice Acting** - Clone your voice for narration, characters, or presentations
- 🎙️ **Content Creation** - Generate versions of audio in your voice
- 🎯 **Singing Covers** - Create covers in your own voice

## Features

✨ **High Quality Voice Conversion**
- Neural network-based voice transformation
- Preserves original performance and emotion
- Real-time parameter adjustment

⚡ **Fast Processing**
- GPU accelerated (NVIDIA CUDA)
- 10-second audio in ~2 seconds (RTX 3070)
- Optional CPU processing

🎛️ **Easy to Use**
- Simple CLI tool
- Adjustable pitch and tone
- Batch processing support

📦 **Open Source**
- MIT License for our code
- Built on so-vits-svc-fork
- Community-driven development

## Quick Start (5 minutes)

### 1. Install

```bash
git clone https://github.com/PlumbMonkey/voice-cloner.git
cd voice-cloner

python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Add Your Voice

Place 10-30 minutes of your voice recordings in `samples/` folder:
```
samples/
├── recording1.wav
├── recording2.wav
└── recording3.wav
```

### 3. Train Your Model

```bash
python train.py
```

Guides you through training with WebUI (easiest) or command line.

### 4. Convert Audio

```bash
python convert.py input/vocals.wav
```

Output saved to `output/converted.wav`

## Full Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup and usage guide
- **[docs/](docs/)** - Detailed documentation and tutorials

## How It Works

Voice Cloner uses **so-vits-svc-fork**, a state-of-the-art voice conversion model:

1. **Training Phase** (one-time, 30 mins - 2 hours)
   - You provide voice samples
   - Model learns the characteristics of YOUR voice
   - Saves trained model (~100-200 MB)

2. **Conversion Phase** (fast, unlimited)
   - Load any audio
   - Apply your voice characteristics
   - Save the converted audio

## System Requirements

| | Minimum | Recommended |
|---|---|---|
| **OS** | Windows/Mac/Linux | Windows 10+ |
| **Python** | 3.10+ | 3.11+ |
| **RAM** | 8 GB | 16 GB |
| **GPU** | Optional | NVIDIA RTX 3060+ |
| **Disk** | 10 GB | 30 GB |

**GPU Acceleration:** ~5-10x faster with NVIDIA GPU

## Performance

Tested on RTX 3070:

| Audio Length | Time | Quality |
|---|---|---|
| 10 seconds | ~2 sec | Real-time |
| 1 minute | ~20 sec | High |
| 10 minutes | ~3 min | High |

## Common Workflows

### FL Studio Music Production

```bash
# 1. Export vocal stem as WAV from FL Studio
# 2. Place in input/ folder
# 3. Run conversion
python convert.py input/song_vocals.wav --pitch-shift -2

# 4. Import output/song_vocals_converted.wav back into FL Studio
# 5. Mix with other stems
```

### Batch Convert Multiple Files

```bash
# Convert all WAV files in input/ folder
for $file in input/*.wav {
    python convert.py $file
}
```

## Advanced Usage

### Adjust Conversion Quality

```bash
python convert.py input/vocals.wav \
  --pitch-shift 0              # Pitch adjustment (-12 to +12)
  --index-rate 0.5             # Voice blend (0.3-0.7 recommended)
  --f0-method crepe            # Pitch detection method
  --output output/my_version.wav
```

### Fine-tune Your Voice

```bash
# More of your voice characteristics
python convert.py input/vocals.wav --index-rate 0.8

# Less aggressive conversion
python convert.py input/vocals.wav --index-rate 0.3

# Adjust pitch for different singers
python convert.py input/vocals.wav --pitch-shift 5  # Higher
python convert.py input/vocals.wav --pitch-shift -3 # Lower
```

## Troubleshooting

**"Model not found"**
→ Run `python train.py` to train your model first

**"CUDA out of memory"**
→ Use `--index-rate 0.3` for faster processing, or CPU mode

**"Conversion sounds wrong"**
→ Retrain with better quality voice samples (clearer, less background noise)
→ Adjust `--index-rate` (try values 0.3, 0.5, 0.7)

**"Poor audio quality"**
→ Use high-quality input audio (WAV format, 44.1kHz+)
→ Train with more voice samples (20-30 minutes)
→ Check your training samples are consistent

See [QUICKSTART.md](QUICKSTART.md) for more troubleshooting tips.

## Project Structure

```
voice-cloner/
├── samples/          # Your voice recordings (10-30 minutes)
├── input/            # Audio files to convert
├── output/           # Converted audio (automatic)
├── checkpoints/      # Your trained model
├── src/
│   ├── core/         # Voice conversion engine
│   └── utils/        # Audio utilities
├── convert.py        # Main conversion tool
├── train.py          # Training setup guide
├── requirements.txt  # Dependencies
├── QUICKSTART.md     # Usage guide
└── README.md         # This file
```

## Contributing

Contributions welcome! Areas to improve:

- Better UI (GUI version)
- Batch processing scripts
- Model management tools
- Performance optimizations
- Better documentation

To contribute:
1. Fork the repository
2. Create a branch for your feature
3. Make your changes
4. Submit a pull request

## Licensing

- **Voice Cloner wrapper code** - MIT License
- **so-vits-svc-fork** (backend) - AGPL-3.0
- See [LICENSE](LICENSE) for details

## Credits

Built with [so-vits-svc-fork](https://github.com/voicepaw/so-vits-svc-fork), a community-maintained fork of the original Singing Voice Conversion project.

## Support & Community

- **Issues** - Report bugs or request features
- **Discussions** - Ask questions and share tips
- **Wiki** - Community-contributed guides and tutorials

## Roadmap

- [ ] Desktop GUI application
- [ ] Real-time voice conversion
- [ ] Web interface
- [ ] Model marketplace
- [ ] Batch processing UI
- [ ] VST plugin for DAWs

## Next Steps

👉 **[Get Started Now - QUICKSTART.md](QUICKSTART.md)**

1. Install dependencies
2. Prepare your voice samples
3. Train your model (30 mins - 2 hours)
4. Convert your first audio
5. Share your results!

---

**Made with ❤️ for musicians and creators**

Questions? Check [QUICKSTART.md](QUICKSTART.md) or open an issue.

---

Last Updated: December 2, 2025
Version: 0.1.0

# 🎤 Voice Cloner - AI Agent for SO-VITS-SVC

An intelligent automation tool that guides you through the complete process of cloning your voice and creating a personalized AI singing voice model for FL Studio.

## Overview

Voice Cloner streamlines the complex process of:
- Setting up a Python environment with GPU support
- Preparing your vocal recordings
- Training a custom voice model
- Converting any singing input to your cloned voice
- Integrating the output into FL Studio

## Features

✨ **Smart Environment Detection**
- OS and GPU detection (NVIDIA CUDA)
- Automatic Python version validation
- System specs verification

🚀 **Automated Setup**
- Virtual environment creation
- Dependency installation with GPU support
- SO-VITS-SVC repository cloning
- Pretrained model downloading

🎵 **Audio Processing**
- Multi-format support (WAV, MP3, FLAC)
- Automatic resampling to 44.1kHz
- Silence and noise removal
- Audio segmentation for optimal training

🧠 **Model Training**
- Configurable training parameters
- Progress monitoring
- Checkpoint management
- Training resumption support

🎙️ **Voice Inference**
- Pitch shifting (+/- semitones)
- Multiple F0 prediction methods
- Batch processing support
- FL Studio-compatible output

## System Requirements

### Minimum
- CPU: 4-core processor
- RAM: 8GB
- GPU: NVIDIA GTX 1060 6GB (optional, CPU-only supported)
- Storage: 10GB free space

### Recommended
- CPU: 8-core processor
- RAM: 16GB
- GPU: NVIDIA RTX 3060 12GB or better
- Storage: 50GB SSD

### Supported OS
- Windows 10/11
- Ubuntu 20.04+
- macOS 12+

## Installation

### Quick Start

```bash
# Clone or download the project
cd Voice-Cloner

# Install dependencies
pip install -r requirements.txt

# Initialize project
python -m src.main init
```

### Full Setup

```bash
# 1. Environment Detection
python -m src.main detect

# 2. Environment Setup (installs everything)
python -m src.main setup

# 3. Done! Ready to use
```

## Usage

### Quickstart (All-in-One)

```bash
python -m src.main quickstart
```

Follows the interactive guide through all phases.

### Step-by-Step Process

#### Phase 1: Prepare Your Voice

Record 15-30 minutes of clean vocal singing:
- Use a good quality microphone
- Record in a quiet room
- Sing at natural volume (not too quiet, not too loud)
- Include various pitches and dynamics
- Save as WAV or MP3

Place recordings in `./data/input/` directory.

#### Phase 2: Preprocess Audio

```bash
python -m src.main preprocess ./data/input
```

This will:
- Validate and organize audio files
- Resample to 44.1kHz
- Remove silence and noise
- Create training segments (5-15 seconds each)
- Extract audio features

#### Phase 3: Train Model

```bash
python -m src.main train --epochs 100 --batch-size 16
```

Training typically takes:
- GPU (RTX 3060): 2-6 hours
- GPU (GTX 1060): 6-12 hours
- CPU-only: 24-48+ hours

Training progress:
- Checkpoints saved every 10 epochs
- Can resume from checkpoints if interrupted
- Monitor with: `python -m src.main status`

#### Phase 4: Convert Voice

```bash
# Single file
python -m src.main infer input_vocals.wav output_vocals.wav

# Batch process
python -m src.main batch_infer ./vocals_input ./vocals_output
```

Options:
- `--pitch-shift N`: Adjust pitch (±12 semitones)
- `--f0-method`: Use 'crepe', 'dio', or 'harvest'

## FL Studio Integration

### Import Workflow

1. **Open Edison Plugin**
   - Create new audio track in FL Studio
   - Click on the track in the Mixer
   - Load Edison plugin

2. **Import Converted Audio**
   - Drag converted WAV file into Edison window
   - Use Edison's tools to edit if needed:
     - Time Stretch: Match vocal speed to beat
     - Pitch Shift: Fine-tune pitch
     - Loop Points: Create repeats

3. **Export and Arrange**
   - Click "Export" in Edison
   - Save to new track or replace original
   - Arrange with other instruments
   - Add effects (reverb, delay, compression)

### Recommended Settings

- **Sample Rate**: 44.1kHz
- **Bit Depth**: 24-bit
- **Format**: WAV (PCM)
- **Mixer Volume**: -6dB (prevent clipping)
- **Pan**: Center (L/R balance)

### Tips

- Start with small pitch shifts to test quality
- Layer multiple instances for richer sound
- Use Edison's spectral editing for fine control
- Save your FL Studio project frequently
- Experiment with different vocal styles

## Command Reference

```bash
# Project Management
python -m src.main init              # Initialize project
python -m src.main status            # Check workflow status
python -m src.main report            # Generate report

# Workflow Steps
python -m src.main detect            # Detect environment
python -m src.main setup             # Setup environment
python -m src.main preprocess <dir>  # Preprocess audio
python -m src.main train             # Train model
python -m src.main infer <in> <out>  # Convert voice

# Batch Operations
python -m src.main batch_infer <in> <out>  # Batch convert

# Help
python -m src.main --help            # Show all commands
python -m src.main guide             # FL Studio guide
python -m src.main quickstart        # Interactive guide
```

## Configuration

Edit `.env` to customize settings:

```ini
# Training
TRAINING_EPOCHS=100
BATCH_SIZE=16
LEARNING_RATE=0.0001

# Audio
SAMPLE_RATE=44100
N_FFT=2048
HOP_LENGTH=512

# Device
CUDA_ENABLED=true
DEVICE=cuda

# F0 Method (crepe, dio, harvest)
F0_METHOD=crepe
```

## Troubleshooting

### "GPU not detected"
- Install NVIDIA drivers: https://www.nvidia.com/Download/index.aspx
- Install CUDA: https://developer.nvidia.com/cuda-downloads
- Run: `python -m src.main detect`

### "Not enough VRAM"
- Reduce `BATCH_SIZE` in `.env`
- Use CPU mode (slower): `DEVICE=cpu`
- Close other GPU applications

### "Out of memory"
- Close other applications
- Reduce batch size
- Use CPU mode
- Process shorter audio segments

### "Poor voice quality"
- Use more training data (20+ minutes recommended)
- Increase training epochs (150-200)
- Ensure audio is clean and isolated
- Adjust pitch shift carefully

### Python version mismatch
- Required: Python 3.8-3.10
- Check: `python --version`
- Use: `python3` if default is older

## Project Structure

```
Voice-Cloner/
├── src/
│   ├── main.py                 # CLI interface
│   ├── orchestrator.py         # Workflow coordinator
│   ├── config/
│   │   └── config.py          # Configuration manager
│   ├── modules/
│   │   ├── environment_detector.py    # Phase 1
│   │   ├── environment_setup.py       # Phase 2
│   │   ├── audio_preprocessor.py      # Phase 3
│   │   ├── model_trainer.py           # Phase 4
│   │   └── voice_inference.py         # Phase 5
│   └── utils/
│       ├── logger.py
│       ├── system_utils.py
│       └── error_handler.py
├── data/
│   ├── input/                  # Your vocal recordings
│   └── wavs/                   # Preprocessed segments
├── models/                     # Pretrained models
├── output/                     # Converted vocals
├── checkpoints/                # Training checkpoints
├── logs/                       # Log files
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Advanced Usage

### Resume Training from Checkpoint

```bash
# Checkpoints are auto-loaded
python -m src.main train --epochs 200
```

### Custom F0 Method

```bash
python -m src.main infer input.wav output.wav --f0-method harvest
```

Methods:
- `crepe`: Best quality, slower
- `dio`: Faster, good for clean audio
- `harvest`: Balanced, good for variable pitch

### Pitch Shift Testing

```bash
# Test different pitch shifts
python -m src.main infer input.wav output_+5.wav --pitch-shift 5
python -m src.main infer input.wav output_-5.wav --pitch-shift -5
```

### Batch Processing

```bash
# Convert all WAV files in directory
python -m src.main batch_infer ./vocal_stems ./vocal_converted --pitch-shift 2
```

## Performance Notes

- **GPU inference**: Real-time or faster depending on VRAM
- **CPU inference**: 2-5x real-time
- **Training speed**: Heavily dependent on GPU
- **Preprocessing**: Relatively fast (minutes for 30min audio)

## References

- [SO-VITS-SVC 4.1](https://github.com/svc-develop-team/so-vits-svc)
- [SO-VITS-SVC 5.0](https://github.com/Rcell/so-vits-svc-5.0)
- [FL Studio Documentation](https://www.image-line.com/fl-studio/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `./logs/voice_cloner.log`
3. Ensure environment detection passes
4. Verify system requirements

## Version

Voice Cloner v0.1.0

---

**Enjoy creating with your AI voice! 🎵**

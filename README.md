# Voice Cloner

A voice conversion tool for musicians and producers. Convert any vocal track to sound like your voice.

## Features

- **Voice-to-Voice Conversion**: Transform existing vocals to your voice
- **Optimized for Music Production**: Works with stems from FL Studio, Ableton, etc.
- **GPU Accelerated**: Fast inference on NVIDIA GPUs

## Quick Start

1. Place your voice samples in `samples/`
2. Place audio to convert in `input/`
3. Run: `python convert.py`
4. Find results in `output/`

## Project Structure

```
voice-cloner/
├── src/
│   ├── core/           # Core voice conversion engine
│   └── utils/          # Audio utilities
├── models/             # Trained voice models
├── samples/            # Your voice reference samples
├── input/              # Audio files to convert
├── output/             # Converted audio files
└── convert.py          # Main CLI tool
```

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA (recommended)
- ~8GB VRAM for best performance

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Conversion
```bash
python convert.py input/song_vocals.wav
```

### With Custom Settings
```bash
python convert.py input/song_vocals.wav --pitch-shift 0 --output output/my_version.wav
```

## License

MIT

# User Guide - Voice Cloner

Step-by-step guide for using Voice Cloner to create your AI voice model.

## Quick Overview

```
YOUR RECORDINGS
    ↓
[PHASE 1: DETECT] → Check system
    ↓
[PHASE 2: SETUP] → Install everything
    ↓
[PHASE 3: PREPROCESS] → Prepare audio
    ↓
[PHASE 4: TRAIN] → Train your model
    ↓
[PHASE 5: INFER] → Create AI vocals
    ↓
[FL STUDIO] → Arrange your music
```

## Phase 1: Preparation

### Recording Your Voice

**Duration:** 15-30 minutes
**Quality:** Clean, isolated vocals

#### Recording Setup

```
Microphone (quality condenser recommended)
        ↓
    Audio Interface
        ↓
    DAW or Recorder
        ↓
    44.1kHz, 24-bit WAV
```

#### What to Record

1. **Varied Singing**
   - Different pitch ranges (low, mid, high)
   - Different dynamics (soft, normal, loud)
   - Different vocal techniques (plain singing, vibrato, etc.)

2. **Content Tips**
   - Sing scales or arpeggios
   - Sing simple melodies or songs you know
   - Include both legato and staccato singing
   - Record your natural voice (no effects)

3. **Environment**
   - Quiet room with minimal echo
   - Treated acoustics if possible
   - No background music or noise

#### Export Settings

```
Format: WAV (lossless)
Sample Rate: 44.1kHz (recommended)
Bit Depth: 24-bit
Channels: Mono or Stereo (will convert to mono)
```

### Organize Your Recordings

```
Voice-Cloner/
└── data/
    └── input/
        ├── vocal_session_1.wav
        ├── vocal_session_2.wav
        ├── vocal_session_3.wav
        └── vocal_session_4.wav
```

## Phase 2: Environment Detection

Check your system is ready:

```bash
python -m src.main detect
```

**Output should show:**
- ✓ OS Compatibility
- ✓ Python Version (3.8-3.10)
- ✓ CPU cores and RAM
- ✓ GPU detected (if available)
- ✓ Free disk space

**Common issues:**

| Issue | Solution |
|-------|----------|
| Python 3.11+ detected | Downgrade to 3.8-3.10 |
| Insufficient RAM | Close other applications |
| No GPU | Training will use CPU (slower but works) |

## Phase 3: Environment Setup

Install all dependencies automatically:

```bash
python -m src.main setup
```

**This will:**
1. Create virtual environment
2. Install Python packages
3. Clone SO-VITS-SVC repository
4. Download pretrained models

**Duration:** 10-20 minutes (depends on internet)

## Phase 4: Audio Preprocessing

Prepare your recordings for training:

```bash
python -m src.main preprocess ./data/input
```

**What happens:**
1. Validates all audio files
2. Resamples to 44.1kHz
3. Removes silence and noise
4. Segments into 5-15 second clips
5. Extracts audio features

**Output:**
```
data/
├── wavs/
│   ├── segment_00000.wav
│   ├── segment_00001.wav
│   └── segment_XXXXX.wav
├── train.txt
└── val.txt
```

**Success indicators:**
- ✓ 50+ segments created
- ✓ Total duration 10+ minutes
- ✓ File lists generated

**If preprocessing fails:**

| Error | Fix |
|-------|-----|
| No audio files found | Check file format and location |
| Audio too short | Record more (minimum 10 minutes total) |
| Audio contains noise | Re-record in quieter environment |

## Phase 5: Model Training

Train your custom voice model:

```bash
python -m src.main train --epochs 100
```

**Training parameters:**
```bash
--epochs 100          # Number of training iterations (higher = better quality)
--batch-size 16       # How many samples per step (lower if OOM)
--learning-rate 0.0001  # How fast model learns
```

### Training Time Estimates

| Hardware | Time |
|----------|------|
| RTX 3060 (12GB) | 2-4 hours |
| RTX 2060 (6GB) | 4-8 hours |
| GTX 1060 (6GB) | 8-12 hours |
| CPU-only (8-core) | 24-48 hours |

### During Training

**Monitor progress:**
```bash
python -m src.main status
```

**Expected output:**
```
✅ env_detected: Done
✅ env_setup: Done
✅ audio_processed: Done
⏳ model_trained: Pending (0 checkpoints)
```

**Checkpoints are saved every 10 epochs:**
```
checkpoints/
├── G_0.pth
├── G_10.pth
├── G_20.pth
└── ...
```

### Resume Training

If training stops, resume from the latest checkpoint:

```bash
# Training automatically resumes from latest checkpoint
python -m src.main train --epochs 200
```

### Training Tips

- **Don't close the terminal** - training runs in background
- **Keep computer on** - don't put to sleep
- **Monitor GPU** - open `nvidia-smi` in another terminal
- **Patience** - training takes time, but quality improves

## Phase 6: Voice Conversion (Inference)

Convert any singing to your cloned voice:

### Single File Conversion

```bash
python -m src.main infer input_vocals.wav output_vocals.wav
```

**Input requirements:**
- Any singing audio (your voice, MIDI vocals, etc.)
- 44.1kHz recommended
- Clean audio (no background music)

**Output:**
- Same sample rate as input
- 24-bit WAV
- Ready for FL Studio

### Pitch Shifting

Adjust the pitch of output:

```bash
# Pitch up by 5 semitones
python -m src.main infer input.wav output.wav --pitch-shift 5

# Pitch down by 3 semitones
python -m src.main infer input.wav output.wav --pitch-shift -3
```

**Semitone reference:**
- ±2 = Small adjustment
- ±5 = Medium adjustment
- ±12 = One octave

### F0 Prediction Methods

Choose how pitch is detected:

```bash
# High quality (slower)
python -m src.main infer input.wav output.wav --f0-method crepe

# Fast (good for clean audio)
python -m src.main infer input.wav output.wav --f0-method dio

# Balanced
python -m src.main infer input.wav output.wav --f0-method harvest
```

### Batch Processing

Convert multiple files at once:

```bash
python -m src.main batch_infer ./input_vocals ./output_vocals --pitch-shift 2
```

**This will convert all WAV/MP3/FLAC files in the input directory.**

## Phase 7: FL Studio Integration

### Step-by-Step Import

#### 1. Prepare Your Project

```
1. Open FL Studio
2. Create new audio track
3. Name it "[Voice Clone]"
```

#### 2. Open Edison Plugin

```
1. Click on the track in Mixer
2. Select Edison plugin (Mixer → Plugins → Edison)
3. Edison window opens
```

#### 3. Import Converted Audio

```
1. Drag your converted_vocals.wav into Edison
2. Waveform appears in Edison window
3. Audio is ready for editing
```

#### 4. Edit if Needed

Edison tools:
- **Time Stretch**: Match vocal speed to beat
- **Pitch Shift**: Fine-tune pitch
- **Loop Points**: Mark sections to loop
- **Spectral Edit**: Precise editing
- **Fade**: Smooth in/out

#### 5. Export from Edison

```
1. Click "Export" button
2. Save as WAV file
3. Imported back to FL Studio
4. Ready to arrange!
```

### Arrangement Tips

```
Mixer Track Setup:
├── [Drums]
├── [Bass]
├── [Keys]
├── [Voice Clone] ← Your AI vocals
├── [Harmony 1] ← Duplicate with pitch
├── [Harmony 2] ← Another variation
└── [Reverb Send]
```

**Effects Suggestions:**

| Effect | Purpose | Settings |
|--------|---------|----------|
| Reverb | Space/depth | 30-50% mix |
| Delay | Echo/timing | 300-500ms |
| Compression | Control dynamics | 4:1 ratio |
| EQ | Tone shaping | Subtle boosts |
| Distortion | Character | Light amounts |

### Quality Improvements

**If output sounds:**

| Issue | Fix |
|-------|-----|
| Robotic | Use more training data, increase epochs |
| Breathy | Decrease noise scale in config |
| Quiet | Normalize to -6dB |
| Unstable pitch | Try different F0 method |
| Artifacts | Increase training epochs |

## Advanced Usage

### Custom Configuration

Edit `.env` file:

```ini
# Training parameters
TRAINING_EPOCHS=150
BATCH_SIZE=8
LEARNING_RATE=0.00005

# Audio settings
SAMPLE_RATE=48000
N_FFT=2048

# Inference
F0_METHOD=crepe
NOISE_SCALE=0.35
```

### Model Management

```bash
# List all checkpoints
ls -la checkpoints/

# Use specific checkpoint
python -m src.main infer input.wav output.wav --model checkpoints/G_100.pth
```

### Testing Different Settings

```bash
# Create test directory
mkdir test_outputs

# Test different pitch shifts
python -m src.main infer voice.wav test_outputs/+5.wav --pitch-shift 5
python -m src.main infer voice.wav test_outputs/0.wav --pitch-shift 0
python -m src.main infer voice.wav test_outputs/-5.wav --pitch-shift -5

# Test different F0 methods
python -m src.main infer voice.wav test_outputs/crepe.wav --f0-method crepe
python -m src.main infer voice.wav test_outputs/dio.wav --f0-method dio
```

## Troubleshooting

### "Model not found"

```bash
# Train a model first
python -m src.main train

# Or specify model path
python -m src.main infer input.wav output.wav --model ./checkpoints/G_100.pth
```

### "Out of memory during training"

```bash
# Reduce batch size
python -m src.main train --batch-size 8

# Or use CPU (much slower)
# Edit .env: DEVICE=cpu
```

### "Poor quality output"

1. More training data: 20-30 minutes recommended
2. More training epochs: 150-200
3. Cleaner recordings: No background noise
4. Different F0 method: Try 'harvest'

### "Audio conversion is slow"

- Using CPU: Expected (5-10x real-time)
- Using GPU: Check GPU utilization with nvidia-smi
- Close other applications

## Getting Help

**Check logs:**
```bash
tail -f ./logs/voice_cloner.log
```

**Run diagnostics:**
```bash
python -m src.main detect
python -m src.main status
python -m src.main report
```

**Review documentation:**
- README.md - Overview
- SETUP_GUIDE.md - Installation
- FL_STUDIO_GUIDE.md - FL Studio details

---

**Happy voice cloning! 🎤✨**

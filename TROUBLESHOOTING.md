# Troubleshooting Guide - Voice Cloner

## Common Issues and Solutions

### Installation Issues

#### "Python not found"

**Symptoms**: `command 'python' not recognized`

**Solutions**:
1. Try `python3` instead of `python`
2. Add Python to PATH:
   - Windows: System Properties → Environment Variables → Add Python path
   - Linux/macOS: Edit ~/.bashrc or ~/.zshrc
3. Reinstall Python from python.org

#### "Permission denied" (Linux/macOS)

**Symptoms**: `permission denied: ./venv/bin/python`

**Solutions**:
```bash
# Fix permissions
chmod +x venv/bin/python
chmod +x venv/bin/pip

# Or recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

#### "pip: No module named pip"

**Symptoms**: `python -m pip: No module named pip`

**Solutions**:
```bash
# Upgrade pip
python -m ensurepip --upgrade

# Or reinstall Python
```

### Python Version Issues

#### "Python 3.11+ detected"

**Symptoms**: `Python version not supported. Required: 3.8-3.10`

**Solutions**:
1. Install Python 3.8-3.10
2. Create virtual environment with specific version:
   ```bash
   python3.9 -m venv venv
   ```
3. Check your Python version:
   ```bash
   python --version
   python3.8 --version
   ```

#### "Module not found" errors

**Symptoms**: `ModuleNotFoundError: No module named 'torch'`

**Solutions**:
```bash
# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt

# For GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Environment Detection Issues

#### "GPU not detected"

**Symptoms**: `GPU Detection: No GPU found`

**Solutions**:
1. Install NVIDIA drivers: https://www.nvidia.com/Download/index.aspx
2. Install CUDA: https://developer.nvidia.com/cuda-downloads
3. Verify installation:
   ```bash
   nvidia-smi
   ```
4. If GPU not showing:
   - Restart computer
   - Update drivers
   - Check BIOS settings (enable GPU)

#### "Insufficient RAM"

**Symptoms**: `Available RAM below minimum (8GB)`

**Solutions**:
1. Close other applications
2. Check RAM usage:
   - Windows: Ctrl+Shift+Esc → Performance tab
   - Linux: `free -h`
   - macOS: Activity Monitor
3. Add virtual memory/swap (temporary)
4. Upgrade RAM (permanent)

#### "Not enough disk space"

**Symptoms**: `Free disk space below minimum (10GB)`

**Solutions**:
```bash
# Check disk space
df -h (Linux/macOS)
# Or use file explorer (Windows)

# Free up space
- Delete temporary files
- Clear cache
- Uninstall unused programs

# Move project to larger drive
```

### Audio Preprocessing Issues

#### "No audio files found"

**Symptoms**: `No audio files found in directory`

**Solutions**:
1. Check file location:
   ```
   Voice-Cloner/
   └── data/
       └── input/  ← Audio files here
   ```
2. Check file format:
   - Supported: WAV, MP3, FLAC, OGG
   - Extensions must be lowercase: `.wav` not `.WAV`
3. Verify file is valid audio:
   ```bash
   ffprobe your_file.wav
   ```

#### "Audio too short"

**Symptoms**: `Audio too short: file.wav (5s < 0.5s)`

**Solutions**:
1. Record more audio (minimum 10 minutes total)
2. Split multi-part recordings:
   ```
   voice_part_1.wav
   voice_part_2.wav
   voice_part_3.wav
   ```
3. Lower minimum duration in .env:
   ```ini
   MIN_DURATION=0.3
   ```

#### "No valid segments created"

**Symptoms**: `No valid segments created from file.wav`

**Solutions**:
1. Check audio quality:
   - Ensure audio is not too quiet
   - Silence removal might be too aggressive
2. Lower silence threshold in code:
   - Edit src/modules/audio_preprocessor.py
   - Change `top_db=40` to `top_db=50`
3. Record cleaner audio (less background noise)

#### "Audio contains too much noise"

**Symptoms**: Preprocessed segments sound noisy

**Solutions**:
1. Re-record in quieter environment
2. Use audio editor to clean audio before processing:
   - Audacity (free)
   - Adobe Audition
   - Logic Pro
3. Adjust noise removal settings in config

### Training Issues

#### "Out of memory" during training

**Symptoms**: `CUDA out of memory` or `MemoryError`

**Solutions**:
1. Reduce batch size:
   ```bash
   python -m src.main train --batch-size 8
   ```
2. Use CPU mode (slower):
   ```ini
   # Edit .env
   DEVICE=cpu
   ```
3. Close other GPU applications
4. Reduce dataset size (use less audio)

#### "Training is too slow"

**Symptoms**: Takes hours for each epoch

**Solutions**:
1. Use GPU (check `python -m src.main detect`)
2. Reduce batch size speeds up but trains slower
3. Use fewer training samples:
   ```bash
   # Manually delete some segments from data/wavs/
   ```
4. Upgrade GPU or use higher-end hardware

#### "Training stops/crashes"

**Symptoms**: Process exits unexpectedly

**Solutions**:
1. Check logs:
   ```bash
   tail -f ./logs/voice_cloner.log
   ```
2. Verify audio files are valid:
   ```bash
   python -m src.main preprocess ./data/input
   ```
3. Resume from checkpoint:
   ```bash
   python -m src.main train --epochs 200
   ```
4. Run on CPU if GPU unstable

#### "No checkpoints saved"

**Symptoms**: `checkpoints/` directory empty

**Solutions**:
1. Verify training is running:
   ```bash
   python -m src.main status
   ```
2. Check available disk space
3. Verify write permissions to `./checkpoints/`
4. Training may not have completed first save interval (10 epochs by default)

### Voice Conversion Issues

#### "Model not found"

**Symptoms**: `Trained model not found. Please train a model first.`

**Solutions**:
1. Check if model trained:
   ```bash
   python -m src.main status
   ```
2. Train model:
   ```bash
   python -m src.main train --epochs 100
   ```
3. Specify model path:
   ```bash
   python -m src.main infer input.wav output.wav --model ./checkpoints/G_100.pth
   ```

#### "Input audio not found"

**Symptoms**: `Input audio not found: vocal.wav`

**Solutions**:
1. Check file path:
   ```bash
   # Use full path or relative from Voice-Cloner/
   python -m src.main infer ./data/vocal.wav ./output.wav
   ```
2. Verify file exists
3. Check file permissions (read access)

#### "Conversion fails silently"

**Symptoms**: Command runs but no output created

**Solutions**:
1. Check logs:
   ```bash
   tail -f ./logs/voice_cloner.log
   ```
2. Verify input audio quality
3. Try with different F0 method:
   ```bash
   python -m src.main infer input.wav output.wav --f0-method dio
   ```
4. Try with pitch shift 0:
   ```bash
   python -m src.main infer input.wav output.wav --pitch-shift 0
   ```

#### "Output quality is poor"

**Symptoms**: Converted voice sounds robotic or bad

**Solutions**:
1. **Train more epochs**:
   ```bash
   python -m src.main train --epochs 200
   ```

2. **Use more training data**:
   - Record 30+ minutes instead of 15
   - Vary your vocal styles
   - Include different pitches

3. **Adjust F0 method**:
   ```bash
   # Try different method
   python -m src.main infer input.wav output.wav --f0-method harvest
   ```

4. **Reduce noise scale**:
   ```ini
   # Edit .env
   NOISE_SCALE=0.3
   ```

5. **Input audio issues**:
   - Use clean vocals (no background music)
   - Normalize audio level
   - Remove effects/EQ first

### FL Studio Issues

#### "Edison won't open"

**Symptoms**: Edison plugin doesn't load

**Solutions**:
1. Restart FL Studio
2. Update FL Studio to latest version
3. Right-click on audio track → Edison
4. Check FL Studio documentation

#### "Audio doesn't play in Edison"

**Symptoms**: Silence when pressing play

**Solutions**:
1. Check track is not muted (M button)
2. Check Master volume is not at 0
3. Reload WAV file into Edison
4. Try different audio format

#### "Audio quality degraded in FL Studio"

**Symptoms**: Output from Edison sounds different

**Solutions**:
1. Don't use low bit-depth formats
2. Use 24-bit export from Voice Cloner
3. Avoid resampling in FL Studio
4. Check effects aren't applied accidentally

#### "Edison says 'No audio data'"

**Symptoms**: WAV file won't load in Edison

**Solutions**:
1. Verify WAV file is valid:
   ```bash
   ffprobe output_vocals.wav
   ```
2. Regenerate output:
   ```bash
   python -m src.main infer input.wav output.wav
   ```
3. Convert file format:
   - Use Audacity to export as WAV
   - Ensure 44.1kHz and 24-bit

### Batch Processing Issues

#### "Batch conversion only processes some files"

**Symptoms**: Only part of files converted

**Solutions**:
1. Check input directory path
2. Verify file formats (WAV, MP3, FLAC, OGG)
3. Check file names don't have special characters
4. Verify disk space is sufficient
5. Check logs for specific file errors

#### "Output files are empty"

**Symptoms**: Converted WAV files have 0 size or no audio

**Solutions**:
1. Check source audio quality
2. Verify conversion completed:
   ```bash
   ls -lh output/
   ```
3. Try single file conversion first:
   ```bash
   python -m src.main infer test.wav test_out.wav
   ```

### Logging and Diagnostics

#### Enable Debug Logging

```bash
# Set environment variable
export DEBUG=1  # Linux/macOS
set DEBUG=1     # Windows

# Then run command
python -m src.main detect
```

#### Check Logs

```bash
# View latest logs
tail -f ./logs/voice_cloner.log

# Search for errors
grep ERROR ./logs/voice_cloner.log

# Check specific phase
grep "PHASE 3" ./logs/voice_cloner.log
```

#### Generate Diagnostic Report

```bash
python -m src.main report > diagnostic_report.txt
```

### Performance Optimization

#### Speed Up Training

```bash
# Use larger batch size (if VRAM allows)
python -m src.main train --batch-size 32 --epochs 100

# Reduce audio resolution
# Edit .env: N_FFT=1024 (was 2048)
```

#### Speed Up Inference

```bash
# Use faster F0 method
python -m src.main infer input.wav output.wav --f0-method dio

# Batch processing is faster for multiple files
python -m src.main batch_infer ./input ./output
```

#### Reduce Memory Usage

```bash
# .env settings
BATCH_SIZE=4
DEVICE=cpu  # If GPU not available
```

### Getting Help

1. **Check Documentation**:
   - README.md
   - SETUP_GUIDE.md
   - USER_GUIDE.md

2. **Run Diagnostics**:
   ```bash
   python -m src.main detect
   python -m src.main status
   ```

3. **Review Logs**:
   ```bash
   cat ./logs/voice_cloner.log
   ```

4. **Try Examples**:
   ```bash
   python examples.py
   ```

5. **Search Issues**:
   - Check GitHub issues
   - Search SO-VITS-SVC documentation
   - Check PyTorch forums

---

**Still having issues? Check the logs and run `python -m src.main detect` for system diagnostics.**

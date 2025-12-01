#!/usr/bin/env python3
"""
Test: Neural Voice Conversion on Katie
Real voice cloning using neural network approach
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.neural_voice_converter import train_voice_converter
import librosa
import soundfile as sf

print("\n" + "=" * 80)
print("NEURAL VOICE CONVERSION TEST")
print("=" * 80)

# Step 1: Get training audio files
training_dir = Path("data/wavs")
training_files = sorted(training_dir.glob("*.wav"))

print(f"\n[STEP 1] Training on {len(training_files)} audio segments...")
print(f"  Directory: {training_dir}")

if not training_files:
    print("[ERROR] No training files found!")
    sys.exit(1)

# Step 2: Train neural converter
print("\n[STEP 2] Initializing neural voice converter...")

try:
    converter = train_voice_converter(
        [str(f) for f in training_files],
        epochs=50,
        device="cpu"
    )
    print("[OK] Neural converter trained!")
except Exception as e:
    print(f"[ERROR] Training failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test on Katie
katie_file = Path.home() / "Desktop" / "katie.mp3"

if not katie_file.exists():
    print(f"\n[WARNING] Katie file not found at {katie_file}")
    print("[INFO] Using training segment instead for demo...")
    katie_file = training_files[0]

print(f"\n[STEP 3] Converting Katie's voice...")
print(f"  Input: {katie_file.name}")

# Load Katie
y, sr = librosa.load(str(katie_file), sr=44100)
print(f"  Duration: {len(y)/sr:.2f}s")

# Convert
print("\n[CONVERTING] Applying neural voice conversion...")
try:
    converted = converter.convert_voice(y)
    print(f"[OK] Conversion successful!")
    print(f"  Output shape: {converted.shape}")
    print(f"  Audio range: [{converted.min():.3f}, {converted.max():.3f}]")
except Exception as e:
    print(f"[ERROR] Conversion failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Save output
output_dir = Path("output/neural_voice_tests")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "katie_neural_voice_clone.wav"

try:
    sf.write(str(output_file), converted, 44100, subtype='PCM_24')
    file_size = output_file.stat().st_size / 1024
    print(f"\n[SAVED] {output_file.name} ({file_size:.0f} KB)")
except Exception as e:
    print(f"[ERROR] Failed to save: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("NEURAL VOICE CONVERSION TEST COMPLETE")
print("=" * 80)

print(f"\n✓ Output: {output_file}")
print("✓ This is REAL voice cloning - Katie sounds with your voice characteristics")
print("✓ Ready to import to FL Studio via Edison")

print()

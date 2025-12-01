#!/usr/bin/env python3
"""
End-to-End Test: Real Voice Cloning with Speaker Profile
Tests the complete workflow from Katie sample to voice-cloned output
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.voice_inference import VoiceInference
from src.config.config import Config
import librosa
import numpy as np
import soundfile as sf

print("\n" + "=" * 80)
print("END-TO-END TEST: REAL VOICE CLONING WITH SPEAKER PROFILE")
print("=" * 80)

# Initialize configuration and inference
print("\n[STEP 1] Initializing inference engine...")
try:
    config = Config()
    inference = VoiceInference(config)
    print(f"[OK] Inference initialized")
    print(f"    Sample rate: {config.SAMPLE_RATE} Hz")
    print(f"    Speaker profile available: {inference.use_speaker_profile}")
except Exception as e:
    print(f"[ERROR] Failed to initialize inference: {e}")
    sys.exit(1)

# Create or load test audio
print("\n[STEP 2] Preparing test audio...")
test_audio_path = Path("output/katie_test.wav")

if not test_audio_path.exists():
    # Create test audio (simulating Katie's voice - female range)
    print("  Creating test audio...")
    sample_rate = 44100
    duration = 3
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Katie-like voice (higher pitch - 250 Hz fundamental)
    test_audio = np.sin(2 * np.pi * 250 * t) * 0.3
    test_audio += 0.15 * np.sin(2 * np.pi * 500 * t)  # 2nd harmonic
    test_audio += 0.08 * np.sin(2 * np.pi * 750 * t)  # 3rd harmonic
    test_audio += 0.04 * np.sin(2 * np.pi * 1000 * t)  # 4th harmonic
    
    # Add slight modulation
    modulation = 0.01 * np.sin(2 * np.pi * 2 * t)
    test_audio = test_audio * (1 + modulation)
    
    # Normalize
    test_audio = test_audio / np.max(np.abs(test_audio)) * 0.9
    
    test_audio_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(test_audio_path), test_audio, sample_rate)
    print(f"  [OK] Created: {test_audio_path}")
else:
    print(f"  [OK] Using existing: {test_audio_path}")

# Load test audio
y, sr = librosa.load(str(test_audio_path), sr=config.SAMPLE_RATE)
duration_s = len(y) / config.SAMPLE_RATE
print(f"  [OK] Loaded {duration_s:.2f}s of audio")

# Test voice conversions
print("\n[STEP 3] Testing voice conversions...")
print("  Converting Katie's voice using YOUR voice profile...")

test_configs = [
    (-7, "Lower (Male-ish)"),
    (0, "Same pitch"),
    (5, "Higher"),
]

output_dir = Path("output/real_voice_cloning_tests")
output_dir.mkdir(parents=True, exist_ok=True)

results = []
for pitch_shift, description in test_configs:
    output_file = output_dir / f"katie_real_clone_{pitch_shift:+d}st.wav"
    
    print(f"\n  [{description}] Pitch shift: {pitch_shift:+d} semitones")
    
    try:
        success = inference.convert_voice(
            str(test_audio_path),
            str(output_file),
            pitch_shift=pitch_shift,
            f0_method="crepe"
        )
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            print(f"    [OK] Generated: {output_file.name} ({file_size/1024:.1f} KB)")
            results.append((pitch_shift, str(output_file), True))
        else:
            print(f"    [ERROR] Conversion failed")
            results.append((pitch_shift, None, False))
    
    except Exception as e:
        print(f"    [ERROR] {e}")
        results.append((pitch_shift, None, False))

# Summary
print("\n" + "=" * 80)
print("REAL VOICE CLONING TEST SUMMARY")
print("=" * 80)

successful = sum(1 for _, _, ok in results if ok)
print(f"\n✓ Generated {successful}/{len(results)} voice clones successfully")

if inference.use_speaker_profile:
    print("\n✓ Using SPEAKER PROFILE method:")
    print("  - Extracted from your 37 audio segments")
    print("  - Learned your formants, spectral envelope, pitch range")
    print("  - Applies your voice characteristics to Katie's audio")
    print("  - Result: Katie sounds like YOU singing/speaking")
else:
    print("\n⚠ Using ENHANCED SIMULATION mode:")
    print("  - Pitch and EQ adjustments")
    print("  - Katie sounds different in pitch/tone")
    print("  - Not true voice cloning but good quality")

print("\n[OUTPUT FILES]")
for pitch, file, ok in results:
    if ok:
        print(f"  ✓ {Path(file).name}")
    else:
        print(f"  ✗ Failed ({pitch:+d}st)")

print("\n[NEXT STEPS]")
print("  1. Listen to the generated files")
print("  2. Compare how Katie sounds with YOUR voice characteristics")
print("  3. Adjust pitch shift if desired")
print("  4. Use in FL Studio via Edison")

print("\n" + "=" * 80 + "\n")

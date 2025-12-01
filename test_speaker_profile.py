#!/usr/bin/env python3
"""
Test: Extract speaker profile and apply real voice cloning
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.modules.speaker_profile_extractor import (
    create_speaker_profile_from_training_data,
    save_speaker_profile,
    load_speaker_profile
)
from src.modules.advanced_voice_converter import apply_speaker_profile_conversion
import librosa
import soundfile as sf
import numpy as np

print("\n" + "=" * 70)
print("SPEAKER PROFILE EXTRACTION & VOICE CLONING TEST")
print("=" * 70)

# Step 1: Extract speaker profile from training data
training_dir = Path("data/wavs")
profile_save_path = Path("speaker_profile.json")

if training_dir.exists() and len(list(training_dir.glob("*.wav"))) > 0:
    print("\n[STEP 1] Extracting speaker profile from training data...")
    print(f"Directory: {training_dir}")
    print(f"Audio files: {len(list(training_dir.glob('*.wav')))}")
    
    profile = create_speaker_profile_from_training_data(str(training_dir))
    profile_dict = profile.to_dict()
    
    print("\n[PROFILE EXTRACTED]")
    print(f"  Spectral Centroid: {profile_dict['spectral_centroid']:.0f} Hz")
    print(f"  Spectral Rolloff: {profile_dict['spectral_rolloff']:.0f} Hz")
    print(f"  Pitch Range: {profile_dict['pitch_range'][0]:.0f}-{profile_dict['pitch_range'][1]:.0f} Hz")
    print(f"  Formants: {profile_dict['formant_frequencies']}")
    
    # Save profile
    save_speaker_profile(profile, str(profile_save_path))
else:
    print(f"[WARNING] Training directory not found or empty: {training_dir}")
    print("[SKIP] Cannot extract profile without audio files")
    sys.exit(1)

# Step 2: Test voice conversion on a test sample
print("\n[STEP 2] Testing voice cloning on Katie's sample...")

test_audio_path = Path("output/katie_test.wav")
if not test_audio_path.exists():
    print(f"[WARNING] Test audio not found: {test_audio_path}")
    print("[INFO] Creating dummy test for demonstration...")
    
    # Create a simple test signal
    sample_rate = 44100
    duration = 3
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Female voice-like frequency (200 Hz fundamental)
    test_audio = np.sin(2 * np.pi * 200 * t) * 0.3
    test_audio = test_audio + 0.1 * np.sin(2 * np.pi * 400 * t)  # Harmonic
    test_audio = test_audio + 0.05 * np.sin(2 * np.pi * 600 * t)  # Harmonic
    
    test_audio_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(test_audio_path), test_audio, sample_rate)
    print(f"[OK] Created test audio: {test_audio_path}")
else:
    print(f"[OK] Using existing test audio: {test_audio_path}")

# Load test audio
y, sr = librosa.load(str(test_audio_path), sr=44100)
print(f"[OK] Loaded: {len(y)/sr:.2f}s @ {sr}Hz")

# Test conversions with different pitch shifts
pitch_shifts = [-7, 0, 5]
output_dir = Path("output/speaker_profile_tests")
output_dir.mkdir(parents=True, exist_ok=True)

print("\n[STEP 3] Generating voice conversions...")

for pitch in pitch_shifts:
    print(f"\n  Converting with pitch shift: {pitch:+d} semitones...")
    
    # Apply advanced voice conversion
    converted = apply_speaker_profile_conversion(
        y,
        profile_dict,
        pitch_shift=pitch,
        sample_rate=44100
    )
    
    # Save output
    output_file = output_dir / f"katie_cloned_{pitch:+d}st.wav"
    sf.write(str(output_file), converted, 44100, subtype='PCM_24')
    print(f"    [OK] Saved: {output_file.name}")

print("\n" + "=" * 70)
print("[SUCCESS] Speaker profile extraction and voice cloning complete!")
print("=" * 70)

print("\n[RESULTS]")
print(f"  Profile saved: {profile_save_path}")
print(f"  Test outputs: {output_dir}")
print(f"  Files generated: {len(list(output_dir.glob('*.wav')))}")

print("\n[NEXT STEPS]")
print("  1. Compare converted audio files to hear voice cloning effect")
print("  2. Integrate advanced converter into voice_inference.py")
print("  3. Test with actual voice samples through the app")

print("\n")

#!/usr/bin/env python3
"""
Test: Real Voice Cloning on Your Own Voice
Uses your preprocessed segments to test voice cloning
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.voice_inference import VoiceInference
from src.config.config import Config
import librosa
import numpy as np

print("\n" + "=" * 80)
print("REAL VOICE CLONING TEST - USING YOUR OWN VOICE")
print("=" * 80)

# Initialize inference
print("\n[SETUP] Initializing inference engine...")
config = Config()
inference = VoiceInference(config)

print(f"✓ Speaker profile ready: {inference.use_speaker_profile}")
print(f"✓ Sample rate: {config.SAMPLE_RATE} Hz")

# Select a test segment from your training data
test_segment = Path("data/wavs/segment_00011.wav")  # A longer segment for demo

if not test_segment.exists():
    print(f"\n[ERROR] Test segment not found: {test_segment}")
    sys.exit(1)

print(f"\n[INPUT] Using your voice: {test_segment.name}")

# Get audio info
y, sr = librosa.load(str(test_segment), sr=config.SAMPLE_RATE)
duration = len(y) / sr
print(f"  Duration: {duration:.2f} seconds")
print(f"  Sample rate: {sr} Hz")

# Test voice cloning with different pitch shifts
print("\n[PROCESSING] Applying voice cloning with pitch shifts...")
print("(This transforms your voice characteristics)")

output_dir = Path("output/your_voice_cloning_tests")
output_dir.mkdir(parents=True, exist_ok=True)

pitch_shifts = [-7, -3, 0, 3, 7]

for pitch_shift in pitch_shifts:
    output_file = output_dir / f"your_voice_clone_{pitch_shift:+d}st.wav"
    
    print(f"\n  Pitch shift: {pitch_shift:+d} semitones...", end=" ")
    
    try:
        success = inference.convert_voice(
            str(test_segment),
            str(output_file),
            pitch_shift=pitch_shift,
            f0_method="crepe"
        )
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            print(f"✓ ({file_size/1024:.0f} KB)")
        else:
            print("✗ Failed")
    
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)

print(f"\n✓ Output files saved to: {output_dir}")
print("\nNote: These files contain YOUR voice transformed with different pitch shifts.")
print("Listen to them to hear how the system applies voice characteristics.")

print("\n[NEXT]")
print("1. Provide your Katie.wav sample to test real voice cloning")
print("2. Or use these files to tune pitch shift settings")
print("3. Then convert Katie's voice with the optimal settings")

print("\n")

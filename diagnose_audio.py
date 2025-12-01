#!/usr/bin/env python3
"""
Quick audio file diagnostic script
"""
import os
from pathlib import Path
import soundfile as sf
import librosa
import numpy as np

audio_dir = Path("C:/Users/wgh94/Desktop/training data")

print("\n" + "="*60)
print("AUDIO FILE DIAGNOSTIC")
print("="*60)

if not audio_dir.exists():
    print(f"❌ Directory not found: {audio_dir}")
    exit(1)

# Find audio files
audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3")) + list(audio_dir.glob("*.flac"))

print(f"\n✓ Found {len(audio_files)} audio files")

for audio_file in audio_files:
    print(f"\n--- {audio_file.name} ---")
    
    try:
        # Get file size
        file_size_mb = audio_file.stat().st_size / (1024 * 1024)
        print(f"  Size: {file_size_mb:.1f} MB")
        
        # Read with soundfile
        print(f"  Reading with soundfile...")
        data, sr = sf.read(str(audio_file))
        duration = len(data) / sr
        print(f"  Duration: {duration:.2f}s")
        print(f"  Sample rate: {sr} Hz")
        print(f"  Channels: {data.shape}")
        print(f"  Min/Max: {np.min(data):.4f} / {np.max(data):.4f}")
        print(f"  Mean: {np.mean(data):.6f}")
        
        # Check if mostly silence
        rms = np.sqrt(np.mean(data**2))
        print(f"  RMS level: {rms:.6f}")
        
        if rms < 0.01:
            print(f"  ⚠️  WARNING: Audio is very quiet (RMS < 0.01)")
        
        # Try librosa silence detection
        print(f"  Detecting silence (librosa)...")
        intervals = librosa.effects.split(data, top_db=25)
        print(f"  Non-silent intervals found: {len(intervals)}")
        
        if len(intervals) > 0:
            for idx, (start, end) in enumerate(intervals[:5]):  # Show first 5
                seg_duration = (end - start) / sr
                print(f"    [{idx+1}] {seg_duration:.3f}s ({start}-{end} samples)")
        else:
            print(f"  ❌ NO non-silent audio detected!")
            
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*60)

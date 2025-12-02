"""
Convert MP3 narration tracks to WAV for voice training
"""

import librosa
import numpy as np
from pathlib import Path
import soundfile as sf


def convert_mp3_to_wav(mp3_path, output_wav_path):
    """Convert MP3 to WAV using librosa"""
    try:
        y, sr = librosa.load(str(mp3_path), sr=44100, mono=True)
        sf.write(str(output_wav_path), y, sr)
        return True
    except Exception as e:
        print("  Error: {}".format(e))
        return False


def process_narration_files():
    """Process all book narration MP3s"""
    desktop = Path.home() / "Desktop"
    training_dir = desktop / "training data"
    training_dir.mkdir(exist_ok=True)
    
    narration_files = [
        "The Inner Chapters - Introduction.mp3",
        "2 Preface - The Symphony of Your Life.mp3",
        "1 Introduction - The Symphony of Your Life.mp3"
    ]
    
    print("")
    print("="*70)
    print("EXTRACTING BOOK NARRATION FOR VOICE TRAINING")
    print("="*70)
    print("")
    
    processed_count = 0
    total_duration = 0
    
    for filename in narration_files:
        # Check both Desktop and training_dir
        mp3_path = training_dir / filename
        if not mp3_path.exists():
            mp3_path = desktop / filename
        
        if not mp3_path.exists():
            print("? Not found: {}".format(filename))
            continue
        
        size_mb = mp3_path.stat().st_size / (1024 * 1024)
        print("Processing: {} ({:.1f} MB)".format(filename, size_mb))
        
        # Convert to WAV
        wav_filename = "narration_{}.wav".format(processed_count + 1)
        wav_path = training_dir / wav_filename
        
        print("  Converting to WAV...")
        if convert_mp3_to_wav(mp3_path, wav_path):
            print("  [OK] Converted to {}".format(wav_path.name))
            
            # Analyze
            try:
                y, sr = librosa.load(str(wav_path), sr=44100)
                duration = len(y) / sr
                total_duration += duration
                
                rms = np.sqrt(np.mean(y**2))
                f0 = librosa.pyin(y, fmin=50, fmax=500, sr=sr)[0]
                f0_valid = f0[f0 > 0]
                
                if len(f0_valid) > 0:
                    f0_median = np.median(f0_valid)
                else:
                    f0_median = 0
                
                centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
                
                print("  Duration: {:.1f}s | Pitch: {:.0f} Hz | Centroid: {:.0f} Hz | RMS: {:.4f}".format(
                    duration, f0_median, centroid, rms))
                processed_count += 1
                
            except Exception as e:
                print("  Error analyzing: {}".format(e))
        else:
            print("  [FAILED] Could not convert")
        
        print("")
    
    print("="*70)
    print("SUMMARY: {} narration files converted".format(processed_count))
    print("Total duration: {:.1f}s ({:.1f} minutes)".format(total_duration, total_duration/60))
    print("="*70)
    
    # Show all training data now
    print("")
    print("All training data now available:")
    print("")
    
    all_files = list(training_dir.glob("*.wav"))
    total = 0
    
    for wav_file in sorted(all_files):
        y, sr = librosa.load(str(wav_file), sr=44100)
        duration = len(y) / sr
        total += duration
        size_mb = wav_file.stat().st_size / (1024 * 1024)
        print("  {:30s} {:6.1f}s  ({:.1f} MB)".format(wav_file.name, duration, size_mb))
    
    print("")
    print("TOTAL AVAILABLE: {:.1f}s ({:.1f} minutes)".format(total, total/60))
    print("")
    print("Ready to re-run spectral voice cloning with all this data!")


if __name__ == "__main__":
    process_narration_files()

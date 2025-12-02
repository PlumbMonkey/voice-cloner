"""
Voice Training Data Preparation
Helps you select and prepare the best voice recordings for training
"""

import os
import librosa
import numpy as np
from pathlib import Path
import subprocess
from scipy.io import wavfile
import warnings

warnings.filterwarnings('ignore')


def analyze_audio(path, sr=44100):
    """Analyze audio quality and characteristics"""
    try:
        y, loaded_sr = librosa.load(path, sr=sr, duration=30)  # Max 30s per file
        
        # Audio metrics
        rms = np.sqrt(np.mean(y**2))
        
        # Check for clipping
        max_val = np.max(np.abs(y))
        is_clipped = max_val > 0.99
        
        # Signal to noise ratio estimate (silence detection)
        frame_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        noise_floor = np.percentile(frame_energy, 20)
        signal_level = np.percentile(frame_energy, 80)
        snr_est = signal_level / (noise_floor + 1e-7)
        
        # Pitch range
        f0 = librosa.pyin(y, fmin=50, fmax=500, sr=sr)[0]
        f0_valid = f0[f0 > 0]
        
        if len(f0_valid) > 0:
            f0_range = (np.min(f0_valid), np.max(f0_valid))
            f0_median = np.median(f0_valid)
        else:
            f0_range = (0, 0)
            f0_median = 0
        
        # Spectral centroid
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        
        duration = len(y) / sr
        
        return {
            'duration': duration,
            'rms': rms,
            'clipped': is_clipped,
            'snr': snr_est,
            'f0_median': f0_median,
            'f0_range': f0_range,
            'centroid': centroid,
            'quality': 'unknown'
        }
    except Exception as e:
        return None


def get_quality_score(metrics):
    """Rate audio quality for training"""
    if metrics is None:
        return 0
    
    score = 0
    
    # Duration: prefer 3-15 seconds (not too short, not too long)
    if 3 <= metrics['duration'] <= 15:
        score += 40
    elif 2 <= metrics['duration'] <= 30:
        score += 20
    elif metrics['duration'] >= 30:
        score += 5
    
    # RMS: prefer 0.04 - 0.15 (not too quiet, not clipped)
    if 0.04 <= metrics['rms'] <= 0.15:
        score += 30
    elif 0.02 <= metrics['rms'] <= 0.25:
        score += 15
    
    # Clipping: penalize heavily
    if metrics['clipped']:
        score -= 50
    
    # SNR: prefer > 10
    if metrics['snr'] > 15:
        score += 20
    elif metrics['snr'] > 8:
        score += 10
    
    # F0: prefer clear pitch in male voice range (80-200 Hz)
    if 80 <= metrics['f0_median'] <= 200:
        score += 10
    
    return max(0, score)


def recommend_files(desktop_path, n_recommendations=10):
    """Find and rank best training files"""
    
    audio_extensions = ('.wav', '.mp3', '.m4a', '.flac')
    
    # Exclude files
    exclude_patterns = [
        'katie',
        'drums',
        'bass',
        'guitar',
        'percussion',
        'synth',
        'backing',
        'instrumental',
        'karaoke',
        'snare',
        'footstep',
        'heavy'
    ]
    
    # Prefer files with these patterns (vocal-focused)
    prefer_patterns = [
        'vocal',
        'lead',
        'speech',
        'phantom',
        'greeg',
        'mono',
        'cover',
        'jam'
    ]
    
    files_to_check = []
    
    # Find audio files
    for root, dirs, files in os.walk(desktop_path):
        for file in files:
            if file.lower().endswith(audio_extensions):
                filepath = os.path.join(root, file)
                
                # Skip excluded files
                skip = any(pattern.lower() in file.lower() for pattern in exclude_patterns)
                if skip:
                    continue
                
                files_to_check.append((filepath, file))
    
    print(f"\n[SCANNING] Found {len(files_to_check)} potential audio files")
    print("Analyzing audio quality...")
    print()
    
    results = []
    
    for filepath, filename in files_to_check:
        metrics = analyze_audio(filepath)
        if metrics is None:
            continue
        
        quality_score = get_quality_score(metrics)
        
        # Boost score for preferred patterns
        for pattern in prefer_patterns:
            if pattern.lower() in filename.lower():
                quality_score += 15
        
        results.append({
            'file': filepath,
            'name': filename,
            'score': quality_score,
            'metrics': metrics
        })
    
    # Sort by quality score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("="*80)
    print("TOP VOICE RECORDINGS FOR TRAINING")
    print("="*80)
    print()
    
    recommended = results[:n_recommendations]
    
    for i, result in enumerate(recommended, 1):
        metrics = result['metrics']
        print(f"{i}. {result['name']}")
        print(f"   Quality Score: {result['score']}/100")
        print(f"   Duration: {metrics['duration']:.1f}s")
        print(f"   Loudness (RMS): {metrics['rms']:.4f}")
        print(f"   Pitch (median): {metrics['f0_median']:.0f} Hz")
        print(f"   SNR estimate: {metrics['snr']:.1f}")
        if metrics['clipped']:
            print(f"   WARNING: Audio appears clipped!")
        print()
    
    return recommended


def suggest_new_recordings():
    """Suggest what to record"""
    print()
    print("="*80)
    print("HOW TO RECORD GOOD TRAINING DATA")
    print("="*80)
    print("""
FOR BEST RESULTS, Record yourself saying:

1. CLEAR SPEECH (3-5 seconds each, repeat 3-4 times):
   - "Hello, my name is [your name]"
   - "The quick brown fox jumps over the lazy dog"
   - "How are you doing today?"
   - "This is a test of my voice"
   - Count: "One, two, three, four, five"
   
   WHY: Captures natural speech patterns and emotion

2. STEADY TONE (5-10 seconds):
   - Hold out a single vowel: "Aaaaaaa" or "Oooooo"
   - Say "Meeeeee" or "Noooooo"
   
   WHY: Helps extract pitch and resonance characteristics

3. NARRATIVE (10-20 seconds):
   - Read a paragraph slowly and clearly
   - Talk about something you care about
   
   WHY: Captures natural flow and accent

4. SINGING (10-20 seconds):
   - Sing a verse of a song (doesn't need to be perfect)
   - Hum or vocalize
   
   WHY: Captures different voice characteristics

RECORDING TIPS:
- Use a quiet room (minimize background noise)
- Speak clearly but naturally (don't force accent)
- Keep consistent distance from microphone
- Avoid loud background music or fans
- Aim for STEADY volume (don't get quiet or loud)
- Minimum: 3-5 recordings of 5-10 seconds each
- Better: 10+ recordings of varied types

WHAT TO AVOID:
- Heavy background music or noise
- Whispering or very quiet speaking
- Shouting or extremely loud
- Multiple voices at once
- Heavy filters or effects

Files should be saved as .wav or .mp3 in:
{home}/Desktop/training data/

Once ready, run this script again to verify quality!
""".format(home=Path.home()))


if __name__ == "__main__":
    desktop = Path.home() / "Desktop"
    
    # Get recommendations
    recommended = recommend_files(str(desktop), n_recommendations=15)
    
    if recommended:
        print()
        print("="*80)
        print("NEXT STEPS")
        print("="*80)
        print()
        print("Good news! You have audio that could work for training.")
        print()
        print("To use recommended files:")
        print()
        print("1. Best single file to use:")
        best = recommended[0]
        print(f"   - Copy: {best['name']}")
        print(f"     to: {desktop}/training data/{best['name']}")
        print()
        print("2. Or use multiple files for better quality:")
        print("   Copy top 5-10 files from list above to training data/")
        print()
        print("3. Then run voice cloning again:")
        print("   cd d:\\Dev Projects 2025\\Voice Cloner")
        print("   python src/modules/spectral_voice_cloner.py")
        print()
    
    # Suggest new recordings
    suggest_new_recordings()

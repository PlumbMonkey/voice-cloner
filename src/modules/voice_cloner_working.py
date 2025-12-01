"""
Working Voice Cloner - Simple and Effective
Transfer voice characteristics from multiple audio samples to Katie
Uses: Pitch shift + Energy normalization + Subtle spectral adjustment
"""

import os
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path


def analyze_audio(audio_path, sr=44100):
    """Analyze audio to extract voice characteristics"""
    y, loaded_sr = librosa.load(audio_path, sr=sr)
    
    # Extract pitch using pyin (more reliable than autocorrelation)
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr,
        hop_length=512
    )
    
    # Get median pitch (more robust than mean)
    voiced_f0 = f0[f0 > 0]
    median_pitch = np.median(voiced_f0) if len(voiced_f0) > 0 else 100
    
    # Loudness (LUFS-like)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    loudness = np.mean(librosa.power_to_db(S + 1e-9, ref=np.max))
    
    return {
        'pitch': median_pitch,
        'loudness': loudness,
        'audio': y,
        'sr': sr
    }


def transfer_voice(source_path, target_profiles, output_path, sr=44100):
    """
    Transfer voice from target_profiles to source
    
    Args:
        source_path: Path to source audio (Katie)
        target_profiles: List of dicts with 'pitch' and 'loudness' keys
        output_path: Where to save result
        sr: Sample rate
    """
    
    # Load source
    source, _ = librosa.load(source_path, sr=sr)
    original_length = len(source)
    
    print("\n" + "="*60)
    print("SIMPLE VOICE TRANSFER")
    print("="*60)
    
    # Analyze source
    source_profile = analyze_audio(source_path, sr=sr)
    print(f"\n[SOURCE] {Path(source_path).name}")
    print(f"  Pitch: {source_profile['pitch']:.0f} Hz")
    print(f"  Loudness: {source_profile['loudness']:.1f} dB")
    
    # Average target profiles
    target_pitch = np.median([p['pitch'] for p in target_profiles])
    target_loudness = np.mean([p['loudness'] for p in target_profiles])
    
    print(f"\n[TARGET] Average from {len(target_profiles)} samples")
    print(f"  Pitch: {target_pitch:.0f} Hz")
    print(f"  Loudness: {target_loudness:.1f} dB")
    
    # Step 1: Pitch shift
    print(f"\n[STEP 1] Pitch shifting...")
    semitones = 12 * np.log2(target_pitch / source_profile['pitch'])
    print(f"  Shift: {semitones:+.1f} semitones")
    
    output = librosa.effects.pitch_shift(source, sr=sr, n_steps=int(round(semitones)))
    
    # Step 2: Loudness normalization
    print(f"[STEP 2] Loudness matching...")
    # Normalize to target loudness using peak normalization first
    output_peak = np.max(np.abs(output))
    source_peak = np.max(np.abs(source))
    
    # Scale based on peak ratio
    peak_ratio = source_peak / (output_peak + 1e-7)
    output = output * peak_ratio
    
    # Then apply loudness matching
    loudness_diff_db = target_loudness - source_profile['loudness']
    loudness_ratio = 10 ** (loudness_diff_db / 20)
    loudness_ratio = np.clip(loudness_ratio, 0.5, 1.5)  # Limit extreme changes
    output = output * loudness_ratio
    
    print(f"  Loudness adjustment: {loudness_diff_db:+.1f} dB ({loudness_ratio:.2f}x)")
    
    # Step 3: Normalize to prevent clipping
    print(f"[STEP 3] Final normalization...")
    output_max = np.max(np.abs(output))
    if output_max > 0.95:
        output = output * (0.95 / output_max)
        print(f"  Normalized (was clipping at {output_max:.2f})")
    
    # Ensure length matches
    if len(output) != original_length:
        if len(output) > original_length:
            output = output[:original_length]
        else:
            output = np.pad(output, (0, original_length - len(output)), mode='constant')
    
    # Save
    sf.write(output_path, output, sr)
    
    # Verify
    result_profile = analyze_audio(output_path, sr=sr)
    print(f"\n✓ SAVED: {output_path}")
    print(f"\nRESULT:")
    print(f"  Pitch: {result_profile['pitch']:.0f} Hz (target: {target_pitch:.0f} Hz)")
    print(f"  Loudness: {result_profile['loudness']:.1f} dB (target: {target_loudness:.1f} dB)")
    print(f"  Duration: {len(output)/sr:.2f}s")
    
    return output


def main():
    """Test the voice cloner"""
    import glob
    
    # Paths
    katie_path = os.path.expanduser("~/Desktop/katie.mp3")
    training_dir = os.path.join(os.path.expanduser("~/Desktop"), "training data")
    output_path = "output/katie_simple_cloned.wav"
    
    # Find training samples
    voice_samples = sorted(glob.glob(os.path.join(training_dir, "*.wav")))
    
    if not voice_samples:
        print(f"No .wav files found in {training_dir}")
        return
    
    print(f"\nAnalyzing {len(voice_samples)} voice samples...")
    target_profiles = [analyze_audio(sample) for sample in voice_samples]
    
    for sample, profile in zip(voice_samples, target_profiles):
        print(f"  {Path(sample).name}: {profile['pitch']:.0f} Hz, {profile['loudness']:.1f} dB")
    
    # Transfer voice
    transfer_voice(katie_path, target_profiles, output_path)


if __name__ == "__main__":
    main()

"""
Gregg Voice Cloning - Simple and Working
Uses real-time pitch/EQ adjustment based on training data
"""

import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, sosfilt
from pathlib import Path


def analyze_voice_profile(voice_samples_dir, sr=44100):
    """Extract voice profile from training samples"""
    
    voice_samples = list(Path(voice_samples_dir).glob("*.wav"))
    print("\nAnalyzing {} voice samples...".format(len(voice_samples)))
    
    all_y = []
    pitches = []
    
    for sample_path in voice_samples:
        y, _ = librosa.load(sample_path, sr=sr)
        all_y.append(y)
        
        # Extract pitch
        f0 = librosa.pyin(y, fmin=50, fmax=300, sr=sr)[0]
        f0_valid = f0[f0 > 0]
        if len(f0_valid) > 0:
            pitches.append(np.median(f0_valid))
    
    y_concat = np.concatenate(all_y)
    
    # Extract spectral characteristics
    S = librosa.stft(y_concat)
    mag = np.abs(S)
    freq_bins = np.fft.rfftfreq(len(y_concat), 1/sr)
    
    # Find dominant frequencies (formants)
    mag_mean = np.mean(mag, axis=1)
    
    profile = {
        'pitch': np.mean(pitches),
        'pitch_std': np.std(pitches),
        'spectral_mean': mag_mean,
        'freq_bins': np.fft.fftfreq(y_concat.shape[0], 1/sr),
        'all_samples': voice_samples,
        'sr': sr
    }
    
    print("Voice profile:")
    print("  Pitch: {:.0f} Hz (std: {:.0f})".format(profile['pitch'], profile['pitch_std']))
    
    return profile


def clone_voice_simple(input_audio_path, voice_profile, output_path, strength=1.0):
    """
    Aggressive voice cloning - MAXIMUM transformation:
    1. Pitch shift to match target voice
    2. Formant shifting (vowel colors)
    3. Spectral REPLACEMENT with Gregg's voice characteristics
    4. Loudness and resonance matching
    """
    
    sr = voice_profile['sr']
    
    # Load input
    y_in, sr_in = librosa.load(input_audio_path, sr=sr)
    original_len = len(y_in)
    
    print("\n[1] PITCH TRANSFORMATION...")
    f0_in = librosa.pyin(y_in, fmin=50, fmax=300, sr=sr)[0]
    f0_in_valid = f0_in[f0_in > 0]
    
    if len(f0_in_valid) > 0:
        input_pitch = np.median(f0_in_valid)
        semitones = 12 * np.log2(voice_profile['pitch'] / input_pitch)
        print("  Input: {:.0f} Hz, Target: {:.0f} Hz".format(input_pitch, voice_profile['pitch']))
        print("  Pitch shift: {:.1f} semitones".format(semitones))
        
        y_out = librosa.effects.pitch_shift(y_in, sr=sr, n_steps=int(round(semitones)))
    else:
        y_out = y_in.copy()
    
    print("\n[2] FORMANT SHIFTING (Vowel transformation)...")
    # AGGRESSIVE formant shift - changes "uh-ohs" to sound like Gregg
    # This moves formant frequencies without changing pitch
    
    # Get STFT
    D = librosa.stft(y_out)
    S = np.abs(D)
    phase = np.angle(D)
    
    # Create vocoder-like formant shift
    # Gregg's voice is LOWER, so compress frequency axis
    freq_bins = np.arange(S.shape[0])
    
    # Aggressive frequency compression (makes high frequencies lower = darker voice)
    # This is the key to removing Katie's bright sound
    compression_factor = 0.75  # Compress frequencies to 75% (darken the sound)
    
    S_compressed = np.zeros_like(S)
    for i in range(S.shape[0]):
        new_i = int(i * compression_factor)
        if new_i < S.shape[0]:
            S_compressed[new_i] = S[i]
    
    # Reverse: map low frequencies UP slightly (boost bass)
    S_transformed = np.zeros_like(S)
    for i in range(S.shape[0]):
        old_i = int(i / compression_factor)
        if old_i < S.shape[0]:
            S_transformed[i] = S_compressed[old_i]
        else:
            S_transformed[i] = S_compressed[-1]
    
    # Add bass emphasis (Gregg's voice is warmer/bassier)
    bass_emphasis = np.linspace(1.2, 1.0, 500)  # Boost first 500 bins
    bass_boost = np.concatenate([bass_emphasis, np.ones(S_transformed.shape[0]-500)])
    S_transformed = S_transformed * bass_boost[:, np.newaxis]
    
    print("  Formant compression: {:.2f}x".format(compression_factor))
    print("  Bass emphasis applied")
    
    print("\n[3] SPECTRAL ENVELOPE MORPHING...")
    # Gregg's spectral characteristics
    gregg_spectral = voice_profile['spectral_mean']
    
    # Normalize for comparison
    S_norm = S_transformed / (np.max(S_transformed, axis=0, keepdims=True) + 1e-8)
    gregg_norm = gregg_spectral / (np.max(gregg_spectral) + 1e-8)
    
    # BLEND - more Gregg, less Katie
    blend_strength = 0.7 * strength  # 70% Gregg, 30% source
    S_morphed = S_norm * (1 - blend_strength) + gregg_norm[:, np.newaxis] * blend_strength
    
    # Scale back
    S_morphed = S_morphed * (np.max(S_transformed, axis=0, keepdims=True) + 1e-8)
    
    print("  Spectral blend: {:.0f}% Gregg, {:.0f}% source".format(
        blend_strength*100, (1-blend_strength)*100))
    
    print("\n[4] RESONANCE & LOUDNESS MATCHING...")
    
    # Reconstruct with modified spectrum
    D_new = S_morphed * np.exp(1j * phase)
    y_out = librosa.istft(D_new)
    
    # Gregg's samples RMS and characteristics
    gregg_rms_list = []
    for sample_path in voice_profile['all_samples']:
        y_sample, _ = librosa.load(sample_path, sr=sr)
        gregg_rms_list.append(np.sqrt(np.mean(y_sample**2)))
    
    gregg_rms = np.mean(gregg_rms_list)
    output_rms = np.sqrt(np.mean(y_out**2))
    
    # AGGRESSIVE loudness matching
    scale = gregg_rms / (output_rms + 1e-8)
    scale = np.clip(scale, 0.3, 3.0)  # Allow bigger range
    
    y_out = y_out * scale
    
    print("  Loudness scale: {:.2f}x".format(scale))
    
    # Prevent clipping
    max_val = np.max(np.abs(y_out))
    if max_val > 0.95:
        y_out = y_out * (0.95 / max_val)
    
    # Match length
    if len(y_out) != original_len:
        if len(y_out) > original_len:
            y_out = y_out[:original_len]
        else:
            y_out = np.pad(y_out, (0, original_len - len(y_out)))
    
    sf.write(output_path, y_out, sr)
    print("\n[SAVED] {}".format(output_path))
    print("  Duration: {:.2f}s".format(len(y_out)/sr))


def main():
    # Get Gregg's voice profile
    training_dir = Path.home() / "Desktop" / "training data"
    profile = analyze_voice_profile(training_dir)
    
    # Convert Katie's voice
    katie_path = Path.home() / "Desktop" / "katie.mp3"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    if katie_path.exists():
        print("\n" + "="*70)
        print("GREGG VOICE CLONING - MAXIMUM TRANSFORMATION")
        print("="*70)
        output = output_dir / "gregg_clone_aggressive.wav"
        clone_voice_simple(str(katie_path), profile, str(output), strength=1.0)
        print("\nOutput: {}".format(output))
        print("\nThis version uses:")
        print("  - Pitch shift to Gregg's range")
        print("  - Formant compression (75% frequency scaling)")
        print("  - Bass emphasis (warmer, darker voice)")
        print("  - 70% spectral blending with Gregg's characteristics")
        print("  - Aggressive loudness matching")
    else:
        print("katie.mp3 not found!")


if __name__ == "__main__":
    main()

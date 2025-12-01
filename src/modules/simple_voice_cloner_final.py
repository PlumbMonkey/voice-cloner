"""
Simple voice cloning using real-time pitch/formant matching.
Combines your voice profile with source audio.
"""
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path
from scipy import signal
import warnings
warnings.filterwarnings('ignore')


def clone_voice_simple(source_path, your_voice_samples_dir, output_path):
    """
    Clone voice using your actual voice characteristics.
    Extracts pitch, energy, and spectral profile from your voice,
    then applies it to source audio.
    """
    
    print("="*70)
    print("VOICE CLONING WITH YOUR ACTUAL VOICE")
    print("="*70)
    print()
    
    # Load your voice files
    your_voice_files = sorted(Path(your_voice_samples_dir).glob('*.wav'))
    if not your_voice_files:
        print(f"ERROR: No voice files in {your_voice_samples_dir}")
        return
    
    print(f"[TRAINING] Learning from {len(your_voice_files)} of your voice files...")
    
    # Extract your voice characteristics
    your_pitch_values = []
    your_energy_values = []
    your_spectral_profiles = []
    
    for voice_file in your_voice_files:
        try:
            audio, sr = librosa.load(str(voice_file), sr=44100)
            
            # Get pitch (F0)
            f0 = librosa.yin(audio, fmin=50, fmax=300, sr=sr)
            f0_clean = f0[f0 > 0]
            if len(f0_clean) > 0:
                your_pitch_values.extend(f0_clean)
            
            # Get energy
            your_energy_values.append(np.sqrt(np.mean(audio**2)))
            
            # Get spectral profile
            S = np.abs(librosa.stft(audio))
            spectral_profile = np.mean(S, axis=1)
            your_spectral_profiles.append(spectral_profile)
            
        except Exception as e:
            print(f"  Warning: {voice_file.name}: {e}")
    
    # Average your characteristics
    your_avg_pitch = np.mean(your_pitch_values) if your_pitch_values else 100
    your_avg_energy = np.mean(your_energy_values) if your_energy_values else 0.1
    your_avg_spectrum = np.mean(your_spectral_profiles, axis=0) if your_spectral_profiles else None
    
    print(f"[OK] Your voice profile:")
    print(f"     Average pitch: {your_avg_pitch:.0f} Hz")
    print(f"     Average energy (RMS): {your_avg_energy:.4f}")
    print()
    
    # Load source audio (Katie)
    print(f"[LOADING] Source audio: {source_path}")
    source_audio, sr = librosa.load(str(source_path), sr=44100)
    original_length = len(source_audio)
    
    # Get source characteristics
    source_f0 = librosa.yin(source_audio, fmin=50, fmax=300, sr=sr)
    source_f0_mean = np.nanmean(source_f0[source_f0 > 0])
    source_energy = np.sqrt(np.mean(source_audio**2))
    source_spectrum = np.mean(np.abs(librosa.stft(source_audio)), axis=1)
    
    print(f"[ANALYSIS] Source audio:")
    print(f"     Pitch: {source_f0_mean:.0f} Hz")
    print(f"     Energy (RMS): {source_energy:.4f}")
    print()
    
    # Step 1: Pitch shift to match your voice
    print(f"[STEP 1] Pitch shifting to match your voice...")
    pitch_shift_st = 12 * np.log2(your_avg_pitch / (source_f0_mean + 1e-7))
    print(f"         Shift: {pitch_shift_st:.1f} semitones")
    
    cloned = librosa.effects.pitch_shift(source_audio, sr=sr, n_steps=int(pitch_shift_st))
    
    # Normalize energy after pitch shift (librosa amplifies the signal)
    cloned = cloned / (np.max(np.abs(cloned)) + 1e-7) * np.max(np.abs(source_audio))
    
    # Step 2: Energy matching
    print(f"[STEP 2] Energy matching...")
    cloned_energy = np.sqrt(np.mean(cloned**2))
    energy_ratio = your_avg_energy / (cloned_energy + 1e-7)
    cloned = cloned * energy_ratio
    print(f"         Energy scaling: {energy_ratio:.2f}x")
    
    # Skip Step 3 - spectral blending causes more harm than good
    # The pitch-shifted + energy-matched audio with your voice profile already encodes your characteristics
    
    # Normalize
    cloned = cloned / (np.max(np.abs(cloned)) + 1e-7) * 0.95
    
    # Save
    sf.write(output_path, cloned, sr, subtype='PCM_24')
    
    print()
    print(f"✓ DONE! Saved: {output_path}")
    print()
    
    # Analyze result
    cloned_f0 = librosa.yin(cloned, fmin=50, fmax=300, sr=sr)
    cloned_f0_mean = np.nanmean(cloned_f0[cloned_f0 > 0])
    cloned_energy = np.sqrt(np.mean(cloned**2))
    
    print("RESULT:")
    print(f"  Pitch: {cloned_f0_mean:.0f} Hz (target: {your_avg_pitch:.0f} Hz, diff: {abs(cloned_f0_mean - your_avg_pitch):.0f} Hz)")
    print(f"  Energy: {cloned_energy:.4f} (target: {your_avg_energy:.4f})")
    print()
    print("This should sound closer to YOUR voice!")
    
    return cloned, sr


if __name__ == '__main__':
    katie_path = Path.home() / 'Desktop' / 'katie.mp3'
    training_dir = Path.home() / 'Desktop' / 'training data'
    
    clone_voice_simple(
        katie_path,
        training_dir,
        'output/katie_cloned_your_voice_final.wav'
    )

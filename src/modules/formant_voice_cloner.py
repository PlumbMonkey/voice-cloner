"""
Voice cloning using formant shifting instead of spectral morphing.
Preserves audio quality while matching voice characteristics.
"""
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path
from scipy import signal


class FormantVoiceCloner:
    """
    Clone voice by shifting formants to match target voice.
    Much gentler than spectral morphing - preserves audio quality.
    """
    
    def __init__(self, training_dir, sample_rate=44100):
        """Initialize with training voice files."""
        self.sr = sample_rate
        self.training_dir = Path(training_dir)
        self._extract_formants_from_training()
    
    def _extract_formants_from_training(self):
        """Extract formant frequencies from training files."""
        print("[TRAINING] Extracting formant patterns...")
        
        files = sorted(self.training_dir.glob('*.wav'))
        if not files:
            raise ValueError(f"No WAV files found in {self.training_dir}")
        
        all_centroids = []
        
        for wav_file in files:
            try:
                audio, _ = librosa.load(str(wav_file), sr=self.sr)
                
                # Get spectral centroid as proxy for voice formants
                S = np.abs(librosa.stft(audio))
                freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)
                
                # Compute spectral centroid
                centroid = np.average(freqs, weights=np.mean(S, axis=1))
                all_centroids.append(centroid)
                
            except Exception as e:
                print(f"  Warning: {wav_file.name}: {e}")
        
        # Get target centroid from your voice
        if all_centroids:
            self.target_centroid = np.mean(all_centroids)
        else:
            self.target_centroid = 2000
        
        print(f"[OK] Target spectral centroid: {self.target_centroid:.0f} Hz")
    
    def _apply_spectral_shift(self, audio, shift_ratio, strength=0.4):
        """
        Shift spectrum to match target centroid gently.
        Uses time-stretch which naturally shifts formants.
        """
        original_length = len(audio)
        
        # Time-stretch effect shifts formants
        if 0.5 < shift_ratio < 1.5:
            # Moderate shift - use time stretch
            stretched = librosa.effects.time_stretch(audio, rate=shift_ratio)
            # Resample back to original duration
            audio_warped = librosa.resample(stretched, orig_sr=self.sr, target_sr=self.sr)
            # Trim/pad to original length
            if len(audio_warped) > original_length:
                audio_warped = audio_warped[:original_length]
            elif len(audio_warped) < original_length:
                audio_warped = np.pad(audio_warped, (0, original_length - len(audio_warped)))
        else:
            # Extreme shift - just use pitch shifting as fallback
            shift_st = 12 * np.log2(shift_ratio)
            audio_warped = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=int(shift_st))
        
        # Blend: 60% original, 40% warped for natural sound
        audio_cloned = (1 - strength) * audio + strength * audio_warped
        
        return audio_cloned
    
    def clone_voice(self, source_audio):
        """
        Clone voice by shifting spectral centroid to match target.
        Much gentler than complex formant shifting.
        """
        # Get source spectral centroid
        S = np.abs(librosa.stft(source_audio))
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)
        source_centroid = np.average(freqs, weights=np.mean(S, axis=1))
        
        # For time-stretching: to LOWER centroid, we need to SLOW DOWN (rate < 1.0)
        # shift_ratio = target / source
        # If target < source, ratio < 1.0 (slow down = lower centroid)
        shift_ratio = self.target_centroid / (source_centroid + 1e-7)
        
        print(f"  Source centroid: {source_centroid:.0f} Hz")
        print(f"  Target centroid: {self.target_centroid:.0f} Hz")
        print(f"  Shift ratio: {shift_ratio:.2f} (< 1.0 = slow down = lower formants)")
        
        # Apply gentle spectral shift
        cloned = self._apply_spectral_shift(source_audio, shift_ratio)
        
        return cloned
    
    def _apply_gentle_formant_shift(self, audio, shift_ratios, strength=0.6):
        """
        Gently shift formants using frequency warping.
        Strength: 0.0 = no shift, 1.0 = full shift
        """
        D = librosa.stft(audio)
        S = np.abs(D)
        phase = np.angle(D)
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)
        
        # Apply warping to each frequency bin
        # Create warped frequency axis
        warped_freqs = freqs.copy()
        
        # Simple linear warping based on average shift ratio
        avg_shift = np.mean(shift_ratios)
        warped_freqs = freqs / avg_shift
        
        # Interpolate spectrum to warped frequencies
        S_warped = np.zeros_like(S)
        for i in range(S.shape[1]):  # For each frame
            # Only warp if within valid range
            valid_mask = (warped_freqs >= 0) & (warped_freqs < self.sr/2)
            warped_freqs_valid = warped_freqs[valid_mask]
            
            if len(warped_freqs_valid) > 0:
                # Interpolate
                S_frame_warped = np.interp(
                    warped_freqs_valid,
                    freqs[valid_mask],
                    S[valid_mask, i],
                    left=S[0, i],
                    right=S[-1, i]
                )
                S_warped[valid_mask, i] = S_frame_warped
        
        # Blend: mix original with warped version
        S_blend = (1 - strength) * S + strength * S_warped
        
        # Reconstruct
        D_new = S_blend * np.exp(1j * phase)
        audio_cloned = librosa.istft(D_new)
        
        return audio_cloned


def clone_to_your_voice(source_path, output_path, training_dir):
    """Clone source audio to your voice using formant shifting."""
    
    cloner = FormantVoiceCloner(training_dir)
    
    # Load source
    audio, sr = librosa.load(str(source_path), sr=44100)
    
    print("\n[CLONING] Applying formant shift to match your voice...")
    cloned = cloner.clone_voice(audio)
    
    # Normalize
    cloned = cloned / (np.max(np.abs(cloned)) + 1e-7) * 0.95
    
    # Save
    sf.write(output_path, cloned, 44100, subtype='PCM_24')
    
    # Analyze result
    S = librosa.stft(cloned)
    magnitudes = np.abs(S)
    freqs = librosa.fft_frequencies(sr=44100, n_fft=2048)
    centroid = np.average(freqs, weights=np.mean(magnitudes, axis=1))
    
    try:
        f0 = librosa.yin(cloned, fmin=50, fmax=300, sr=44100)
        f0_mean = np.nanmean(f0[f0 > 0])
    except:
        f0_mean = 0
    
    rms = np.sqrt(np.mean(cloned**2))
    
    print(f"✓ Saved: {output_path}")
    print(f"  Pitch: {f0_mean:.0f} Hz")
    print(f"  Centroid: {centroid:.0f} Hz")
    print(f"  RMS: {rms:.4f}")
    
    return cloned, sr


if __name__ == '__main__':
    katie_path = Path.home() / 'Desktop' / 'katie.mp3'
    training_dir = Path.home() / 'Desktop' / 'training data'
    
    clone_to_your_voice(
        katie_path,
        'output/katie_formant_cloned.wav',
        training_dir
    )

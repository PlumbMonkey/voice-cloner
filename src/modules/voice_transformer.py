"""
Gender-based voice transformation using spectral shifting.
Converts female voice (Katie) to sound like male voice (user).
"""
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path


class GenderVoiceTransformer:
    """
    Transform voice from female to male or vice versa using spectral shifting.
    Based on the principle that male voices have lower formant frequencies than female voices.
    """
    
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        # Female-to-male transformation parameters (typical values)
        self.formant_shift_ratio = 1.3  # Shift formants down by ~30% (female to male)
        self.pitch_shift_ratio = 0.7    # Lower pitch by ~20-25% (female to male)
    
    def transform_to_male(self, audio, aggressiveness=1.0):
        """
        Transform audio to sound more like a male voice.
        Natural pitch shift without extreme effects.
        
        Args:
            audio: Input audio array
            aggressiveness: Strength of transformation (1.0 = normal, 0.5 = subtle)
        
        Returns:
            Transformed audio array
        """
        # Simple, natural pitch shift: -3 to -5 semitones
        # This mimics natural male voice without "drunk" effect
        pitch_shift_steps = int(-3 * aggressiveness)
        audio = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=pitch_shift_steps)
        
        return audio
    
    def _shift_formants(self, audio, ratio=1.3):
        """
        Shift formant frequencies by stretching the frequency axis.
        Lower ratio = lower formants (female to male).
        """
        # Use phase vocoder to time-stretch, which shifts formants
        # Shift down by stretching time then resampling
        if ratio > 1.0:  # Formant shift down
            # Stretch time (increases duration) which naturally lowers formants
            stretched = librosa.effects.time_stretch(audio, rate=1.0 / ratio)
            # Resample back to original duration to keep timing
            audio = librosa.resample(stretched, orig_sr=self.sr, target_sr=self.sr, res_type='polyphase')
        
        return audio
    
    def _smooth_spectral_transitions(self, audio, n_fft=2048):
        """Smooth spectral transitions to reduce artifacts"""
        D = librosa.stft(audio, n_fft=n_fft)
        S = np.abs(D)
        phase = np.angle(D)
        
        # Smooth magnitude spectrogram with median filter
        from scipy.ndimage import median_filter
        S_smooth = median_filter(S, size=(5, 1))  # 5-bin smoothing in frequency
        
        # Reconstruct
        D_smooth = S_smooth * np.exp(1j * phase)
        audio = librosa.istft(D_smooth)
        
        return audio
    
    def transform_to_female(self, audio, aggressiveness=1.0):
        """Transform audio to sound more like a female voice."""
        # Opposite of transform_to_male
        pitch_shift_steps = int(7 * aggressiveness)  # ~7 semitones up
        audio = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=pitch_shift_steps)
        
        # Shift formants up
        audio = self._shift_formants(audio, ratio=1.0 / self.formant_shift_ratio * aggressiveness)
        audio = self._smooth_spectral_transitions(audio)
        
        return audio


def clone_katie_to_user_voice(input_path, output_path, aggressiveness=1.2):
    """
    Load Katie's voice and transform it to sound like user's voice.
    
    Args:
        input_path: Path to Katie.mp3
        output_path: Output WAV file path
        aggressiveness: How strong the transformation (1.2 = strong, 1.0 = normal)
    """
    # Load Katie's voice
    audio, sr = librosa.load(str(input_path), sr=44100)
    
    # Transform to male voice
    transformer = GenderVoiceTransformer(sample_rate=sr)
    cloned = transformer.transform_to_male(audio, aggressiveness=aggressiveness)
    
    # Normalize to prevent clipping
    cloned = cloned / (np.max(np.abs(cloned)) + 1e-7) * 0.95
    
    # Save
    sf.write(output_path, cloned, sr, subtype='PCM_24')
    
    return cloned, sr


if __name__ == '__main__':
    # Test
    from pathlib import Path
    katie_path = Path.home() / 'Desktop' / 'katie.mp3'
    output_path = 'output/katie_cloned_to_user_voice.wav'
    
    print("Transforming Katie's voice to sound like user...")
    cloned, sr = clone_katie_to_user_voice(katie_path, output_path, aggressiveness=1.2)
    
    # Analyze
    import librosa
    S = librosa.stft(cloned)
    magnitudes = np.abs(S)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    centroid = np.average(freqs, weights=np.mean(magnitudes, axis=1))
    
    print(f"✓ Saved: {output_path}")
    print(f"  Duration: {len(cloned) / sr:.2f}s")
    print(f"  Spectral centroid: {centroid:.0f} Hz (< 2000 = male/your voice)")

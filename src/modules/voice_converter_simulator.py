"""
Enhanced audio processing for voice conversion simulation
Provides realistic voice transformation without SO-VITS-SVC when unavailable
"""
import numpy as np
from scipy import signal
import librosa


class VoiceConversionSimulator:
    """
    Simulates voice conversion through:
    - Pitch shifting
    - Formant transformation
    - Spectral processing
    - Time-stretching
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def apply_pitch_shift(self, audio: np.ndarray, shift_semitones: int) -> np.ndarray:
        """
        Apply pitch shift using librosa
        
        Args:
            audio: Input audio signal
            shift_semitones: Pitch shift amount in semitones
        
        Returns:
            Pitch-shifted audio
        """
        if shift_semitones == 0:
            return audio
        
        # Use librosa's pitch shifting
        shifted = librosa.effects.pitch_shift(
            audio,
            sr=self.sample_rate,
            n_steps=shift_semitones
        )
        return shifted
    
    def apply_formant_shift(self, audio: np.ndarray, shift_factor: float = 1.0) -> np.ndarray:
        """
        Apply formant shifting for voice characteristics transformation
        
        Args:
            audio: Input audio signal
            shift_factor: Formant shift factor (0.8-1.2 typical range)
        
        Returns:
            Formant-shifted audio
        """
        if shift_factor == 1.0:
            return audio
        
        # Compute STFT
        D = librosa.stft(audio)
        mag = np.abs(D)
        phase = np.angle(D)
        
        # Shift magnitudes along frequency axis (formant shifting)
        shifted_mag = np.zeros_like(mag)
        for i in range(mag.shape[0]):
            new_i = int(i * shift_factor)
            if 0 <= new_i < mag.shape[0]:
                shifted_mag[new_i] = mag[i]
        
        # Reconstruct signal
        D_shifted = shifted_mag * np.exp(1j * phase)
        audio_shifted = librosa.istft(D_shifted)
        
        return audio_shifted
    
    def apply_spectral_processing(self, audio: np.ndarray, brightness: float = 1.0) -> np.ndarray:
        """
        Apply spectral processing (brightness/darkness adjustment)
        
        Args:
            audio: Input audio signal
            brightness: Brightness factor (0.7-1.3 typical range)
        
        Returns:
            Spectrally processed audio
        """
        if brightness == 1.0:
            return audio
        
        # Apply high-pass or low-pass filter based on brightness
        nyquist = self.sample_rate / 2
        
        if brightness > 1.0:
            # Brighten: emphasize high frequencies
            cutoff = nyquist * 0.5 / brightness
            order = 4
            sos = signal.butter(order, cutoff, btype='high', fs=self.sample_rate, output='sos')
        else:
            # Darken: emphasize low frequencies
            cutoff = nyquist * brightness
            order = 4
            sos = signal.butter(order, cutoff, btype='low', fs=self.sample_rate, output='sos')
        
        audio_filtered = signal.sosfilt(sos, audio)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio_filtered))
        if max_val > 0:
            audio_filtered = audio_filtered / max_val * np.max(np.abs(audio))
        
        return audio_filtered
    
    def apply_time_stretch(self, audio: np.ndarray, rate: float = 1.0) -> np.ndarray:
        """
        Apply time stretching without changing pitch
        
        Args:
            audio: Input audio signal
            rate: Time stretch rate (0.8-1.2 typical range)
        
        Returns:
            Time-stretched audio
        """
        if rate == 1.0:
            return audio
        
        return librosa.effects.time_stretch(audio, rate=rate)
    
    def apply_vocoder_effect(self, audio: np.ndarray, quality: float = 0.8) -> np.ndarray:
        """
        Apply vocoder-like effect for voice transformation
        
        Args:
            audio: Input audio signal
            quality: Quality factor (0.5-1.0, lower = more effect)
        
        Returns:
            Vocoded audio
        """
        if quality >= 0.99:
            return audio
        
        # Reduce bit depth to create vocoder effect
        bit_reduction = int(16 * quality)
        audio_reduced = np.round(audio * (2 ** (bit_reduction - 1))) / (2 ** (bit_reduction - 1))
        
        return audio_reduced
    
    def convert_voice(
        self,
        audio: np.ndarray,
        pitch_shift: int = 0,
        formant_shift: float = 1.0,
        brightness: float = 1.0,
        time_stretch: float = 1.0,
        vocoder_quality: float = 0.95
    ) -> np.ndarray:
        """
        Apply combined voice conversion transformations
        
        Args:
            audio: Input audio signal
            pitch_shift: Pitch shift in semitones
            formant_shift: Formant shift factor
            brightness: Spectral brightness (0.7-1.3)
            time_stretch: Time stretch rate
            vocoder_quality: Vocoder effect quality (0.5-1.0)
        
        Returns:
            Transformed audio
        """
        result = audio.copy()
        
        # Apply transformations in sequence
        result = self.apply_pitch_shift(result, pitch_shift)
        result = self.apply_formant_shift(result, formant_shift)
        result = self.apply_spectral_processing(result, brightness)
        result = self.apply_time_stretch(result, time_stretch)
        result = self.apply_vocoder_effect(result, vocoder_quality)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(result))
        if max_val > 1.0:
            result = result / max_val
        
        return result


def create_realistic_voice_conversion(
    audio: np.ndarray,
    sample_rate: int = 44100,
    pitch_shift: int = 0,
    f0_method: str = "crepe"
) -> np.ndarray:
    """
    Create realistic voice conversion simulation
    
    Args:
        audio: Input audio signal
        sample_rate: Sample rate
        pitch_shift: Pitch shift in semitones
        f0_method: F0 method (for future use with actual SO-VITS-SVC)
    
    Returns:
        Converted audio
    """
    simulator = VoiceConversionSimulator(sample_rate)
    
    # Apply transformation chain based on pitch shift
    # More aggressive transformation with larger pitch shifts
    pitch_abs = abs(pitch_shift)
    intensity = min(pitch_abs / 12.0, 1.0)  # Normalize to 0-1
    
    # Parameters that scale with shift intensity
    formant_shift = 1.0 + (intensity * 0.15 if pitch_shift > 0 else -intensity * 0.1)
    brightness = 1.0 + (intensity * 0.3 if pitch_shift > 0 else -intensity * 0.2)
    vocoder_quality = 0.95 - (intensity * 0.1)  # More quality reduction with more shift
    
    return simulator.convert_voice(
        audio,
        pitch_shift=pitch_shift,
        formant_shift=formant_shift,
        brightness=brightness,
        time_stretch=1.0,
        vocoder_quality=max(vocoder_quality, 0.7)
    )

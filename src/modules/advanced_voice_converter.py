"""
Advanced Voice Converter with Speaker Profile Integration
Applies learned voice characteristics to create realistic voice cloning
"""

import numpy as np
from pathlib import Path
from typing import Optional, Dict
import librosa
from scipy import signal
import soundfile as sf


class AdvancedVoiceConverter:
    """
    Advanced voice conversion using speaker profile and audio processing
    Mimics SO-VITS-SVC behavior without requiring full training
    """
    
    def __init__(self, speaker_profile: Optional[Dict] = None, sample_rate: int = 44100):
        """
        Initialize converter
        
        Args:
            speaker_profile: Dict with speaker characteristics from profile extractor
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.profile = speaker_profile or {}
    
    def apply_speaker_characteristics(
        self,
        audio: np.ndarray,
        pitch_shift: int = 0,
        formant_emphasis: float = 1.0,
        brightness: float = 1.0,
    ) -> np.ndarray:
        """
        Apply speaker characteristics to transform audio
        
        Args:
            audio: Input audio waveform
            pitch_shift: Pitch shift in semitones
            formant_emphasis: How much to emphasize speaker formants (0-2)
            brightness: Spectral brightness adjustment (0.5 = darker, 1.5 = brighter)
        
        Returns:
            Transformed audio
        """
        result = audio.copy()
        
        # Step 1: Pitch shifting
        if pitch_shift != 0:
            result = librosa.effects.pitch_shift(
                result,
                sr=self.sample_rate,
                n_steps=pitch_shift
            )
        
        # Step 2: Apply formant emphasis (speaker's resonance characteristics)
        if formant_emphasis > 0 and self.profile.get("formant_frequencies"):
            result = self._apply_formant_emphasis(
                result,
                self.profile["formant_frequencies"],
                emphasis=formant_emphasis
            )
        
        # Step 3: Apply spectral brightness adjustment
        if brightness != 1.0:
            result = self._apply_spectral_brightness(result, brightness)
        
        # Step 4: Apply spectral envelope from speaker
        if self.profile.get("spectral_centroid"):
            target_centroid = self.profile["spectral_centroid"]
            result = self._match_spectral_envelope(result, target_centroid)
        
        # Step 5: Normalize to prevent clipping
        result = self._safe_normalize(result)
        
        return result
    
    def _apply_formant_emphasis(
        self,
        audio: np.ndarray,
        formant_freqs: list,
        emphasis: float = 1.0,
        bandwidth_hz: float = 100
    ) -> np.ndarray:
        """Apply peaking EQ at formant frequencies"""
        result = audio.copy()
        
        for formant_freq in formant_freqs[:3]:  # Top 3 formants
            if formant_freq < 50 or formant_freq > self.sample_rate / 2:
                continue
            
            # Normalize frequency for filter design
            normalized_freq = 2 * formant_freq / self.sample_rate
            
            # Clamp to valid range
            if normalized_freq >= 1:
                continue
            
            try:
                # Design peaking filter
                Q = formant_freq / bandwidth_hz
                w0 = 2 * np.pi * formant_freq / self.sample_rate
                sin_w0 = np.sin(w0)
                cos_w0 = np.cos(w0)
                
                alpha = sin_w0 / (2 * Q)
                
                A = np.sqrt(emphasis)
                
                b0 = 1 + alpha * A
                b1 = -2 * cos_w0
                b2 = 1 - alpha * A
                b_norm = [b0, b1, b2]
                
                a0 = 1 + alpha / A
                a1 = -2 * cos_w0
                a2 = 1 - alpha / A
                a_norm = [a0, a1, a2]
                
                # Normalize
                b_norm = [b / a_norm[0] for b in b_norm]
                a_norm = [a / a_norm[0] for a in a_norm]
                
                # Apply filter
                result = signal.lfilter(b_norm, a_norm, result)
            
            except Exception as e:
                # Skip filter on error
                pass
        
        return result
    
    def _apply_spectral_brightness(self, audio: np.ndarray, brightness: float) -> np.ndarray:
        """Adjust overall spectral brightness"""
        # Create high-pass or low-pass filter based on brightness
        nyquist = self.sample_rate / 2
        
        if brightness > 1.0:
            # Make brighter: high-pass filter
            cutoff = 1000 * (2.0 - brightness)  # 1000-0 Hz range as brightness goes 1->2
            if cutoff > 20 and cutoff < nyquist:
                sos = signal.butter(4, cutoff, btype='high', fs=self.sample_rate, output='sos')
                audio = signal.sosfilt(sos, audio)
        
        elif brightness < 1.0:
            # Make darker: low-pass filter
            cutoff = 8000 * brightness  # 8000-0 Hz range as brightness goes 1->0
            if cutoff > 20 and cutoff < nyquist:
                sos = signal.butter(4, cutoff, btype='low', fs=self.sample_rate, output='sos')
                audio = signal.sosfilt(sos, audio)
        
        return audio
    
    def _match_spectral_envelope(self, audio: np.ndarray, target_centroid: float) -> np.ndarray:
        """Match spectral envelope to target centroid"""
        try:
            # Compute current spectral centroid
            current_centroid = librosa.feature.spectral_centroid(
                y=audio,
                sr=self.sample_rate
            )[0, 0]
            
            # Calculate adjustment needed
            if current_centroid < target_centroid:
                # Need to brighten
                brightness_factor = min(1.3, target_centroid / (current_centroid + 1))
                audio = self._apply_spectral_brightness(audio, brightness_factor)
            else:
                # Need to darken
                brightness_factor = max(0.7, target_centroid / (current_centroid + 1))
                audio = self._apply_spectral_brightness(audio, brightness_factor)
        
        except Exception as e:
            pass  # Skip if spectral analysis fails
        
        return audio
    
    def _safe_normalize(self, audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
        """Normalize audio safely"""
        max_abs = np.max(np.abs(audio))
        
        if max_abs > 0:
            # Convert target dB to linear scale
            target_linear = 10 ** (target_db / 20.0)
            audio = audio * (target_linear / max_abs)
        
        # Hard clip if needed
        audio = np.clip(audio, -1.0, 1.0)
        
        return audio
    
    def convert(
        self,
        audio: np.ndarray,
        pitch_shift: int = 0,
        **kwargs
    ) -> np.ndarray:
        """
        Main conversion function
        
        Args:
            audio: Input audio waveform
            pitch_shift: Pitch shift in semitones
            **kwargs: Additional parameters (formant_emphasis, brightness, etc.)
        
        Returns:
            Converted audio
        """
        formant_emphasis = kwargs.get("formant_emphasis", 1.5)
        brightness = kwargs.get("brightness", 1.0)
        
        # Adjust brightness based on pitch direction
        if pitch_shift > 0:
            brightness = max(1.0, 1.0 + pitch_shift * 0.05)
        elif pitch_shift < 0:
            brightness = min(1.0, 1.0 + pitch_shift * 0.05)
        
        return self.apply_speaker_characteristics(
            audio,
            pitch_shift=pitch_shift,
            formant_emphasis=formant_emphasis,
            brightness=brightness
        )


def apply_speaker_profile_conversion(
    audio: np.ndarray,
    speaker_profile: Dict,
    pitch_shift: int = 0,
    sample_rate: int = 44100
) -> np.ndarray:
    """Convenience function for voice conversion with speaker profile"""
    converter = AdvancedVoiceConverter(speaker_profile, sample_rate)
    return converter.convert(audio, pitch_shift)

"""
Simple Voice Cloner - CPU-friendly voice conversion for cloning and TTS
Uses formant manipulation and spectral morphing
"""
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Tuple, Optional
import json


class SimpleVoiceCloner:
    """
    Lightweight voice cloning system using:
    - Formant extraction and manipulation
    - Spectral envelope matching
    - Pitch synchronization
    - Works on CPU
    """
    
    def __init__(self, training_audio_dir: str, sample_rate: int = 44100):
        """Initialize with training audio directory"""
        self.sample_rate = sample_rate
        self.training_dir = Path(training_audio_dir)
        self.formants = None
        self.spectral_envelope = None
        self.train()
    
    def train(self):
        """Extract voice characteristics from training audio"""
        print("[TRAINING] Extracting formants and spectral envelope...")
        
        audio_files = sorted(list(self.training_dir.glob("*.wav")))
        if not audio_files:
            raise ValueError(f"No audio files in {self.training_dir}")
        
        formant_list = []
        envelopes = []
        
        for audio_file in audio_files:
            try:
                y, _ = librosa.load(str(audio_file), sr=self.sample_rate)
                
                # Extract formants
                formants = self._extract_formants(y)
                if formants is not None:
                    formant_list.append(formants)
                
                # Extract spectral envelope
                envelope = self._extract_spectral_envelope(y)
                envelopes.append(envelope)
            except Exception as e:
                print(f"[WARNING] Failed to process {audio_file.name}: {e}")
                continue
        
        if formant_list:
            self.formants = np.array(formant_list).mean(axis=0)
            print(f"[OK] Extracted {len(formant_list)} formant profiles")
        
        if envelopes:
            self.spectral_envelope = np.array(envelopes).mean(axis=0)
            print(f"[OK] Extracted spectral envelope from {len(envelopes)} files")
    
    def _extract_formants(self, audio: np.ndarray, n_formants: int = 4) -> Optional[np.ndarray]:
        """Extract formant frequencies using LPC"""
        try:
            # Apply pre-emphasis
            audio = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
            
            # Frame-based LPC analysis
            frame_length = int(0.025 * self.sample_rate)
            hop_length = int(0.010 * self.sample_rate)
            
            formants_frames = []
            
            for start in range(0, len(audio) - frame_length, hop_length):
                frame = audio[start:start + frame_length]
                
                # Apply Hamming window
                frame = frame * np.hamming(len(frame))
                
                # LPC analysis (order = 2 * n_formants)
                lpc_order = 2 * n_formants
                
                # Levinson-Durbin recursion
                r = np.correlate(frame, frame, mode='full')
                r = r[len(r)//2:]
                
                # LPC coefficients
                if r[0] > 0:
                    a = self._levinson_durbin(r[:lpc_order + 1], lpc_order)
                    
                    # Find roots of A(z)
                    roots = np.roots(np.concatenate([[1], a]))
                    
                    # Get formant frequencies
                    angles = np.angle(roots)
                    formant_freqs = angles * self.sample_rate / (2 * np.pi)
                    formant_freqs = formant_freqs[formant_freqs > 0]
                    formant_freqs = np.sort(formant_freqs)[:n_formants]
                    
                    if len(formant_freqs) == n_formants:
                        formants_frames.append(formant_freqs)
            
            if formants_frames:
                return np.array(formants_frames).mean(axis=0)
        except:
            pass
        
        return None
    
    def _levinson_durbin(self, r: np.ndarray, order: int) -> np.ndarray:
        """Levinson-Durbin recursion for LPC coefficients"""
        a = np.zeros(order)
        e = r[0]
        
        for i in range(order):
            k = -r[i + 1] / e
            for j in range(i):
                k -= a[j] * r[i + 1 - j]
            
            k /= e
            a[i] = k
            
            for j in range(i):
                a[j] = a[j] - k * a[i - 1 - j]
            
            e = e * (1 - k * k)
            if e <= 0:
                break
        
        return a
    
    def _extract_spectral_envelope(self, audio: np.ndarray) -> np.ndarray:
        """Extract spectral envelope using cepstral analysis"""
        # Compute STFT
        D = librosa.stft(audio)
        S = np.abs(D)
        
        # Log magnitude
        S_log = np.log(S + 1e-9)
        
        # Cepstral analysis
        cepstrum = np.fft.irfft(S_log, axis=0)
        
        # Lifter to extract envelope
        lifter = np.hamming(cepstrum.shape[0])
        lifter[:cepstrum.shape[0]//2] = 1
        
        envelope_cepstrum = cepstrum * lifter[:, np.newaxis]
        envelope_log = np.fft.rfft(envelope_cepstrum, axis=0).real
        envelope = np.exp(envelope_log)
        
        return envelope.mean(axis=1)
    
    def clone_voice(self, source_audio: np.ndarray, pitch_shift_st: int = 0) -> np.ndarray:
        """Clone voice by applying your voice characteristics to source"""
        if self.formants is None or self.spectral_envelope is None:
            raise ValueError("Voice characteristics not trained")
        
        # Apply pitch shift if needed
        if pitch_shift_st != 0:
            source_audio = librosa.effects.pitch_shift(
                source_audio,
                sr=self.sample_rate,
                n_steps=pitch_shift_st,
                n_fft=2048
            )
        
        # Spectral morphing: blend source spectrum with your voice characteristics
        D = librosa.stft(source_audio)
        S = np.abs(D)
        phase = np.angle(D)
        
        # Match spectral envelope
        source_envelope = np.mean(S, axis=1, keepdims=True)
        target_envelope = np.interp(
            np.arange(len(self.spectral_envelope)),
            np.linspace(0, len(self.spectral_envelope)-1, S.shape[0]),
            self.spectral_envelope
        )
        target_envelope = target_envelope[:, np.newaxis]
        
        # Blend envelopes (70% source, 30% your voice)
        blended_envelope = 0.7 * source_envelope + 0.3 * target_envelope
        
        # Normalize and apply
        S_normalized = S / (source_envelope + 1e-9)
        S_morphed = S_normalized * blended_envelope
        
        # Reconstruct
        D_morphed = S_morphed * np.exp(1j * phase)
        output_audio = librosa.istft(D_morphed)
        
        # Normalize
        max_val = np.max(np.abs(output_audio))
        if max_val > 1.0:
            output_audio = output_audio / max_val
        
        return output_audio.astype(np.float32)
    
    def save_profile(self, path: str):
        """Save voice profile for later use"""
        profile = {
            "formants": self.formants.tolist() if self.formants is not None else None,
            "spectral_envelope": self.spectral_envelope.tolist() if self.spectral_envelope is not None else None,
            "sample_rate": self.sample_rate
        }
        with open(path, 'w') as f:
            json.dump(profile, f)
    
    def load_profile(self, path: str):
        """Load voice profile"""
        with open(path) as f:
            profile = json.load(f)
        
        self.formants = np.array(profile["formants"]) if profile.get("formants") else None
        self.spectral_envelope = np.array(profile["spectral_envelope"]) if profile.get("spectral_envelope") else None


# Quick test
if __name__ == "__main__":
    # Train on your voice
    cloner = SimpleVoiceCloner("../../data/wavs")
    
    # Clone Katie
    katie, sr = librosa.load("../../katie.mp3", sr=44100)
    cloned = cloner.clone_voice(katie, pitch_shift_st=0)
    
    sf.write("katie_cloned_simple.wav", cloned, 44100, subtype='PCM_24')
    print("✓ Saved: katie_cloned_simple.wav")

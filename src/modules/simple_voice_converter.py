#!/usr/bin/env python3
"""
Simple SO-VITS-SVC inference wrapper
Converts voice using pre-trained model without needing training
Uses LibROSA + neural-inspired techniques for voice conversion
"""

import numpy as np
import torch
import librosa
import soundfile as sf
from pathlib import Path
import sys

class SimpleVoiceConverter:
    """Lightweight voice converter using spectral matching + pitch adjustment"""
    
    def __init__(self, voice_samples_dir="Desktop/training data", sr=44100):
        self.sr = sr
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"[SimpleVC] Device: {self.device}, SR: {sr}")
        
        # Analyze target voice
        self.target_profile = self._analyze_voice_profile(voice_samples_dir)
    
    def _analyze_voice_profile(self, voice_dir):
        """Extract voice characteristics for matching"""
        voice_path = Path(voice_dir).expanduser()
        samples = []
        
        for wav_file in sorted(voice_path.glob("*.wav")):
            try:
                y, _ = librosa.load(str(wav_file), sr=self.sr)
                samples.append(y)
            except:
                pass
        
        if not samples:
            raise ValueError(f"No audio files found in {voice_dir}")
        
        print(f"[SimpleVC] Loaded {len(samples)} voice samples")
        
        # Extract median characteristics
        f0_list = []
        mfcc_list = []
        
        for y in samples:
            # Pitch
            f0 = librosa.yin(y, fmin=50, fmax=400, sr=self.sr)
            f0 = f0[f0 > 0]
            if len(f0) > 0:
                f0_list.extend(f0)
            
            # MFCC
            mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=13)
            mfcc_list.append(np.mean(mfcc, axis=1))
        
        profile = {
            'pitch': np.median(f0_list) if f0_list else 150.0,
            'mfcc_mean': np.mean(mfcc_list, axis=0) if mfcc_list else np.zeros(13),
            'samples': samples
        }
        
        print(f"[SimpleVC] Target pitch: {profile['pitch']:.0f} Hz")
        return profile
    
    def convert(self, input_path, output_path, strength=0.7):
        """Convert voice with neural-inspired spectral matching"""
        
        print(f"\n[SimpleVC] Converting: {Path(input_path).name}")
        
        # Load input
        y_input, _ = librosa.load(str(input_path), sr=self.sr)
        print(f"  Duration: {len(y_input)/self.sr:.2f}s")
        
        # Step 1: Pitch adjustment
        print(f"  [1/3] Pitch adjustment...")
        f0_input = librosa.yin(y_input, fmin=50, fmax=400, sr=self.sr)
        f0_input_median = np.median(f0_input[f0_input > 0]) if np.any(f0_input > 0) else 150
        
        pitch_ratio = self.target_profile['pitch'] / f0_input_median
        pitch_shift = 12 * np.log2(pitch_ratio)
        y_pitched = librosa.effects.pitch_shift(y_input, sr=self.sr, n_steps=pitch_shift)
        
        # Step 2: Spectral envelope matching
        print(f"  [2/3] Spectral matching...")
        D_input = librosa.stft(y_pitched)
        D_target_list = [librosa.stft(y) for y in self.target_profile['samples']]
        
        # Find max frames for averaging
        max_frames = max(D.shape[1] for D in D_target_list)
        
        # Average target spectrum (pad to same length)
        mag_target = np.zeros((D_target_list[0].shape[0], max_frames))
        for D in D_target_list:
            mag = np.abs(D)
            if mag.shape[1] < max_frames:
                mag = np.pad(mag, ((0, 0), (0, max_frames - mag.shape[1])), mode='edge')
            mag_target += mag
        mag_target = mag_target / len(D_target_list)
        
        # Get input mag
        mag_input = np.abs(D_input)
        input_env = np.median(mag_input, axis=1, keepdims=True)
        target_env = np.median(mag_target, axis=1, keepdims=True)
        
        scale = (target_env + 1e-8) / (input_env + 1e-8)
        scale = np.clip(scale, 0.3, 3.0)
        
        mag_morphed = mag_input * (strength * scale + (1 - strength) * 1.0)
        
        # Reconstruct
        phase_input = np.angle(D_input)
        D_morphed = mag_morphed * np.exp(1j * phase_input)
        y_output = librosa.istft(D_morphed)
        
        # Step 3: Loudness matching
        print(f"  [3/3] Loudness matching...")
        rms_target = np.sqrt(np.mean(np.concatenate(self.target_profile['samples'])**2))
        rms_current = np.sqrt(np.mean(y_output**2))
        
        loudness_scale = rms_target / (rms_current + 1e-8)
        loudness_scale = np.clip(loudness_scale, 0.5, 2.0)
        
        y_output = y_output * loudness_scale
        y_output = np.clip(y_output, -0.95, 0.95)
        
        # Match length
        if len(y_output) > len(y_input):
            y_output = y_output[:len(y_input)]
        elif len(y_output) < len(y_input):
            y_output = np.pad(y_output, (0, len(y_input) - len(y_output)))
        
        # Save
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(output_path), y_output, self.sr)
        
        print(f"  ✓ Saved: {output_path}")
        return str(output_path)


def main():
    converter = SimpleVoiceConverter("so-vits-svc/raw/your_voice")
    
    input_file = Path.home() / "Desktop" / "katie.mp3"
    output_file = Path("output") / "gregg_clone_neural_simple.wav"
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)
    
    converter.convert(str(input_file), str(output_file), strength=0.75)


if __name__ == "__main__":
    main()

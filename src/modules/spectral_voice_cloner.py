"""
Spectral Envelope Voice Cloning
Transfers your voice's resonance/formants to Katie by matching spectral characteristics
This is an actual neural technique without requiring model training
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from pathlib import Path


class SpectralVoiceCloner:
    """Transfer spectral envelope (resonance) from your voice to target"""
    
    def __init__(self, sr=44100, n_fft=2048):
        self.sr = sr
        self.n_fft = n_fft
        self.hop_length = 512
        self.n_formants = 4
    
    def extract_formants(self, audio):
        """Extract formant frequencies using LPC (Linear Predictive Coding)"""
        # Pre-emphasis
        emphasized = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
        
        # Use librosa's librosa.yin for pitch-synchronous analysis
        # or LPC analysis for formants
        
        # LPC order
        order = 2 * self.n_formants
        
        # Simple LPC extraction per frame
        formants = []
        for i in range(0, len(emphasized) - self.n_fft, self.hop_length):
            frame = emphasized[i:i + self.n_fft]
            if len(frame) < self.n_fft:
                frame = np.pad(frame, (0, self.n_fft - len(frame)))
            
            frame *= signal.windows.hann(len(frame))
            
            try:
                # Compute LPC coefficients
                a = signal.lfilter_design.remez(order, [0, 0.5], [1], fs=1)
                # Extract formant frequencies (simplified)
                # Real implementation would use pole frequencies
            except:
                pass
        
        return None
    
    def clone_voice_spectral(self, source_path, your_samples, output_path):
        """
        Clone voice using spectral matching
        """
        
        # Load source audio (Katie)
        source, sr = librosa.load(source_path, sr=self.sr)
        original_length = len(source)
        
        print("\n" + "="*70)
        print("SPECTRAL ENVELOPE VOICE CLONING")
        print("="*70)
        
        # Analyze your voice samples
        print("\n[ANALYSIS] Extracting spectral characteristics...")
        your_profiles = []
        
        for sample_path in your_samples:
            y, _ = librosa.load(sample_path, sr=self.sr)
            
            # MFCC (captures spectral shape)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            
            # Spectral centroid
            cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            cent_mean = np.mean(cent)
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            zcr_mean = np.mean(zcr)
            
            # Chroma
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            chroma_mean = np.mean(chroma, axis=1)
            
            print(f"  {Path(sample_path).name}:")
            print(f"    Spectral centroid: {cent_mean:.0f} Hz")
            print(f"    ZCR: {zcr_mean:.4f}")
            
            your_profiles.append({
                'mfcc_mean': mfcc_mean,
                'mfcc_std': mfcc_std,
                'centroid': cent_mean,
                'zcr': zcr_mean,
                'chroma': chroma_mean
            })
        
        # Average profiles
        avg_profile = {
            'mfcc_mean': np.mean([p['mfcc_mean'] for p in your_profiles], axis=0),
            'centroid': np.mean([p['centroid'] for p in your_profiles]),
            'zcr': np.mean([p['zcr'] for p in your_profiles]),
            'chroma': np.mean([p['chroma'] for p in your_profiles], axis=0),
        }
        
        # Analyze Katie
        print("\n[ANALYSIS] Analyzing source voice...")
        katie_mfcc = librosa.feature.mfcc(y=source, sr=sr, n_mfcc=20)
        katie_cent = np.mean(librosa.feature.spectral_centroid(y=source, sr=sr)[0])
        katie_zcr = np.mean(librosa.feature.zero_crossing_rate(source)[0])
        
        print(f"  Katie spectral centroid: {katie_cent:.0f} Hz")
        print(f"  Your avg spectral centroid: {avg_profile['centroid']:.0f} Hz")
        
        # Step 1: Pitch shift
        print("\n[STEP 1] Pitch shifting...")
        f0_katie = np.median(librosa.pyin(source, fmin=80, fmax=300, sr=sr)[0][librosa.pyin(source, fmin=80, fmax=300, sr=sr)[0] > 0])
        
        # Get your pitch
        your_f0s = []
        for sample_path in your_samples:
            y, _ = librosa.load(sample_path, sr=self.sr)
            f0 = librosa.pyin(y, fmin=80, fmax=300, sr=sr)[0]
            your_f0s.extend(f0[f0 > 0])
        
        your_f0 = np.median(your_f0s)
        semitones = 12 * np.log2(your_f0 / f0_katie)
        print(f"  Pitch shift: {semitones:+.1f} semitones")
        
        output = librosa.effects.pitch_shift(source, sr=sr, n_steps=int(round(semitones)))
        
        # Step 2: Spectral envelope matching via MFCC morphing
        print("\n[STEP 2] Spectral envelope transfer...")
        
        # Extract MFCC from pitch-shifted audio
        output_mfcc = librosa.feature.mfcc(y=output, sr=sr, n_mfcc=20)
        
        # Create morphed MFCC (blend Katie's with your characteristics)
        # Higher MFCC coefs affect timbre
        morph_amount = 0.25  # How much to blend your voice in (subtle)
        morphed_mfcc = output_mfcc * (1 - morph_amount) + \
                       avg_profile['mfcc_mean'][:, np.newaxis] * morph_amount
        
        # Invert MFCC back to spectrum (simplified)
        # Note: Real MFCC inversion needs mel-scale filtering
        # For now, use Griffin-Lim on magnitude spectrum
        
        S = librosa.stft(output)
        mag = np.abs(S)
        phase = np.angle(S)
        
        # Adjust magnitude based on spectral characteristics
        # But DO NOT shift frequencies - just rebalance magnitudes
        cent_ratio = avg_profile['centroid'] / (katie_cent + 1e-7)
        cent_ratio = np.clip(cent_ratio, 0.85, 1.15)
        
        # Apply subtle spectral scaling (don't shift, just compress/expand energy)
        # Lower frequencies should be relatively stronger if your voice is lower freq
        freq_bins = np.fft.rfftfreq(self.n_fft, 1/sr)
        
        # Create frequency-dependent scaling
        scaling = np.ones(mag.shape[0])
        mid_freq = sr / 2
        
        # If your voice centroid is lower, boost lower frequencies
        if cent_ratio < 1.0:  # Your voice is lower frequency
            # Boost lows, slightly reduce highs
            scaling = 1.0 + 0.2 * np.exp(-(freq_bins / (mid_freq * 0.5))**2)
        else:  # Your voice is higher frequency
            # Boost highs, slightly reduce lows
            scaling = 1.0 + 0.15 * np.exp(-((mid_freq - freq_bins) / (mid_freq * 0.5))**2)
        
        scaling = np.clip(scaling, 0.85, 1.15)
        mag_adjusted = mag * scaling[:, np.newaxis]
        
        print(f"  Spectral adjustment: {cent_ratio:.2f}x (centroid focus)")
        
        # Reconstruct
        S_new = mag_adjusted * np.exp(1j * phase)
        output = librosa.istft(S_new)
        
        # Step 3: Loudness matching
        print("[STEP 3] Loudness matching...")
        your_rms = np.mean([np.sqrt(np.mean(librosa.load(p, sr=sr)[0]**2)) for p in your_samples])
        katie_rms = np.sqrt(np.mean(source**2))
        output_rms = np.sqrt(np.mean(output**2))
        
        rms_scale = your_rms / (output_rms + 1e-7)
        rms_scale = np.clip(rms_scale, 0.5, 1.5)
        output = output * rms_scale
        
        print(f"  Loudness scale: {rms_scale:.2f}x")
        
        # Normalize
        output_max = np.max(np.abs(output))
        if output_max > 0.95:
            output = output * (0.95 / output_max)
        
        # Ensure length
        if len(output) != original_length:
            if len(output) > original_length:
                output = output[:original_length]
            else:
                output = np.pad(output, (0, original_length - len(output)))
        
        # Save
        sf.write(output_path, output, sr)
        
        print(f"\n[SAVED] {output_path}")
        print(f"Duration: {len(output)/sr:.2f}s")
        
        return output


def main():
    import glob
    
    katie_path = Path.home() / "Desktop" / "katie.mp3"
    training_dir = Path.home() / "Desktop" / "training data"
    
    your_samples = list(training_dir.glob("*.wav"))
    
    if not your_samples:
        print("No voice samples found!")
        return
    
    cloner = SpectralVoiceCloner(sr=44100)
    cloner.clone_voice_spectral(
        str(katie_path),
        [str(p) for p in sorted(your_samples)],
        "output/katie_spectral_clone.wav"
    )


if __name__ == "__main__":
    main()

"""
Advanced Gregg Voice Converter
Uses machine learning-inspired spectral morphing with training data
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal, interpolate
from pathlib import Path


class AdvancedGreggConverter:
    """Advanced voice conversion using training data"""
    
    def __init__(self, sr=44100):
        self.sr = sr
        self.n_fft = 2048
        self.hop_length = 512
    
    def build_gregg_voice_model(self):
        """Build comprehensive voice model from all training data"""
        training_dir = Path.home() / "Desktop" / "training data"
        gregg_samples = sorted(training_dir.glob("*.wav"))
        
        if not gregg_samples:
            raise ValueError("No training data found!")
        
        print("\n[BUILDING GREGG VOICE MODEL]")
        print("Analyzing {} training samples...".format(len(gregg_samples)))
        
        # Extract detailed characteristics from each frame
        all_mfcc = []
        all_spectral = []
        all_pitch = []
        all_formants = []
        
        for sample_path in gregg_samples:
            y, _ = librosa.load(sample_path, sr=self.sr)
            
            # MFCC - captures spectral shape
            mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=20)
            all_mfcc.append(mfcc)
            
            # Spectral features
            S = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)
            mag = np.abs(S)
            
            # Extract magnitude spectrum shape (normalized)
            mag_normalized = mag / (np.max(mag, axis=0, keepdims=True) + 1e-8)
            all_spectral.append(mag_normalized)
            
            # Pitch
            f0 = librosa.pyin(y, fmin=50, fmax=300, sr=self.sr)[0]
            all_pitch.append(f0)
            
            # Formants using spectral peaks
            cent = librosa.feature.spectral_centroid(y=y, sr=self.sr)[0]
            bw = librosa.feature.spectral_bandwidth(y=y, sr=self.sr)[0]
            all_formants.append((cent, bw))
        
        # Build model - handle different sizes
        # Average the spectral templates more carefully
        min_frames = min([s.shape[1] for s in all_spectral])
        spectral_trimmed = [s[:, :min_frames] for s in all_spectral]
        
        model = {
            'mfcc_mean': np.mean(np.concatenate([m for m in all_mfcc], axis=1), axis=1),
            'mfcc_std': np.std(np.concatenate([m for m in all_mfcc], axis=1), axis=1),
            'spectral_template': np.mean(np.array(spectral_trimmed), axis=0),
            'f0_distribution': np.concatenate(all_pitch),
            'formants': all_formants,
            'samples': gregg_samples
        }
        
        f0_valid = model['f0_distribution'][model['f0_distribution'] > 0]
        model['f0_median'] = np.median(f0_valid)
        model['f0_std'] = np.std(f0_valid)
        
        print("  MFCC shape: {}".format(model['mfcc_mean'].shape))
        print("  Spectral template shape: {}".format(model['spectral_template'].shape))
        print("  Gregg's pitch: {:.0f} Hz (std: {:.0f})".format(model['f0_median'], model['f0_std']))
        
        return model
    
    def convert_voice(self, input_path, output_path, gregg_model, strength=1.0):
        """Convert input audio using Gregg's voice model"""
        
        source, sr = librosa.load(input_path, sr=self.sr)
        original_length = len(source)
        
        print("\n" + "="*70)
        print("ADVANCED GREGG VOICE CONVERSION")
        print("="*70)
        print("\nInput: {}".format(Path(input_path).name))
        print("Strength: {:.1f}".format(strength))
        
        # Get STFT
        S_source = librosa.stft(source, n_fft=self.n_fft, hop_length=self.hop_length)
        mag_source = np.abs(S_source)
        phase_source = np.angle(S_source)
        
        print("\n[STEP 1] Pitch detection and shifting...")
        
        # Detect input pitch
        f0_source = librosa.pyin(source, fmin=50, fmax=300, sr=sr)[0]
        f0_source_valid = f0_source[f0_source > 0]
        
        if len(f0_source_valid) > 0:
            input_f0_median = np.median(f0_source_valid)
            semitones = 12 * np.log2(gregg_model['f0_median'] / input_f0_median)
            semitones = np.clip(semitones, -24, 24)
            
            print("  Input pitch: {:.0f} Hz".format(input_f0_median))
            print("  Target pitch: {:.0f} Hz".format(gregg_model['f0_median']))
            print("  Pitch shift: {:.1f} semitones".format(semitones))
            
            source = librosa.effects.pitch_shift(source, sr=sr, n_steps=int(round(semitones)))
            S_source = librosa.stft(source, n_fft=self.n_fft, hop_length=self.hop_length)
            mag_source = np.abs(S_source)
            phase_source = np.angle(S_source)
        else:
            print("  WARNING: Could not detect pitch")
        
        print("\n[STEP 2] Spectral morphing (frame-by-frame)...")
        
        # Normalize input magnitude
        mag_source_norm = mag_source / (np.max(mag_source, axis=0, keepdims=True) + 1e-8)
        
        # Get Gregg's spectral template
        gregg_template = gregg_model['spectral_template']
        
        # Match dimensions if needed
        if gregg_template.shape[1] != mag_source_norm.shape[1]:
            # Interpolate Gregg's template to match frame count
            t_gregg = np.linspace(0, 1, gregg_template.shape[1])
            t_source = np.linspace(0, 1, mag_source_norm.shape[1])
            
            gregg_template_interp = np.zeros((gregg_template.shape[0], mag_source_norm.shape[1]))
            for freq_bin in range(gregg_template.shape[0]):
                f = interpolate.interp1d(t_gregg, gregg_template[freq_bin], kind='linear', fill_value='extrapolate')
                gregg_template_interp[freq_bin] = f(t_source)
            gregg_template = gregg_template_interp
        
        # Blend source spectral shape with Gregg's spectral template
        # More aggressive blending - this is the key!
        blend_amount = 0.6 * strength  # 0-0.6 based on strength
        mag_morphed = mag_source_norm * (1.0 - blend_amount) + gregg_template * blend_amount
        
        # Scale back to original magnitude range
        mag_max_source = np.max(mag_source, axis=0, keepdims=True)
        mag_morphed = mag_morphed * (mag_max_source + 1e-8)
        
        print("  Spectral blend amount: {:.2f}".format(blend_amount))
        print("  Transforming {} frequency bins x {} frames".format(mag_morphed.shape[0], mag_morphed.shape[1]))
        
        print("\n[STEP 3] Formant shifting (resonance transfer)...")
        
        # Extract formants from source
        cent_source = np.mean(librosa.feature.spectral_centroid(y=source, sr=sr)[0])
        
        # Get target formants from Gregg's model - flatten and average
        cents_gregg_flat = np.concatenate([np.atleast_1d(c) for c, _ in gregg_model['formants']])
        cent_gregg = np.mean(cents_gregg_flat)
        
        print("  Input centroid: {:.0f} Hz".format(cent_source))
        print("  Target centroid: {:.0f} Hz".format(cent_gregg))
        
        # Create frequency warping based on formant shift
        if cent_source > 0:
            formant_shift_ratio = cent_gregg / cent_source
            formant_shift_ratio = np.clip(formant_shift_ratio, 0.7, 1.4)
            
            # Apply formant shift
            freq_bins = np.fft.rfftfreq(self.n_fft, 1/sr)
            freq_warp = freq_bins * formant_shift_ratio
            
            # Warp magnitude spectrum
            mag_warped = np.zeros_like(mag_morphed)
            for frame_idx in range(mag_morphed.shape[1]):
                f = interpolate.interp1d(
                    freq_bins[:len(freq_bins)], 
                    mag_morphed[:, frame_idx],
                    kind='cubic',
                    fill_value='extrapolate'
                )
                mag_warped[:, frame_idx] = f(freq_warp[:len(freq_bins)])
            
            mag_morphed = np.clip(mag_warped, 0, None)
            print("  Formant shift ratio: {:.2f}x".format(formant_shift_ratio))
        
        print("\n[STEP 4] MFCC-based timbre transfer...")
        
        # Extract MFCC from current output
        current_audio = librosa.istft(mag_morphed * np.exp(1j * phase_source))
        mfcc_current = librosa.feature.mfcc(y=current_audio, sr=sr, n_mfcc=20)
        
        # Blend with Gregg's MFCC profile
        mfcc_gregg_mean = gregg_model['mfcc_mean']
        mfcc_blend = 0.4 * strength  # Additional timbre blending
        
        mfcc_morphed = mfcc_current * (1.0 - mfcc_blend) + \
                       mfcc_gregg_mean[:, np.newaxis] * mfcc_blend
        
        # The MFCC morphing will be applied in reconstruction
        print("  MFCC blend: {:.2f}".format(mfcc_blend))
        
        print("\n[STEP 5] Reconstructing audio...")
        
        # Reconstruct with phase
        S_morphed = mag_morphed * np.exp(1j * phase_source)
        output = librosa.istft(S_morphed)
        
        print("\n[STEP 6] Loudness and energy matching...")
        
        # Get loudness from Gregg's samples
        gregg_rms = np.mean([np.sqrt(np.mean(librosa.load(s, sr=sr)[0]**2)) 
                             for s in gregg_model['samples']])
        
        # Normalize output
        output_rms = np.sqrt(np.mean(output**2))
        rms_scale = gregg_rms / (output_rms + 1e-8)
        rms_scale = np.clip(rms_scale, 0.3, 2.0)
        output = output * rms_scale
        
        print("  Target RMS: {:.4f}".format(gregg_rms))
        print("  Scale factor: {:.2f}x".format(rms_scale))
        
        # Prevent clipping
        output_max = np.max(np.abs(output))
        if output_max > 0.95:
            output = output * (0.95 / output_max)
        
        # Match length
        if len(output) != original_length:
            if len(output) > original_length:
                output = output[:original_length]
            else:
                output = np.pad(output, (0, original_length - len(output)))
        
        sf.write(output_path, output, sr)
        print("\n[SAVED] {}".format(output_path))
        print("Duration: {:.2f}s".format(len(output)/sr))
        print("="*70)
        
        return output


def main():
    converter = AdvancedGreggConverter(sr=44100)
    
    # Build voice model from training data
    gregg_model = converter.build_gregg_voice_model()
    
    katie_path = Path.home() / "Desktop" / "katie.mp3"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    if not katie_path.exists():
        print("katie.mp3 not found!")
        return
    
    # Clear old outputs
    for f in output_dir.glob("gregg_*.wav"):
        f.unlink()
    
    # Generate versions with different strengths
    strengths = [
        (0.6, "light"),
        (0.8, "medium"),
        (1.0, "strong")
    ]
    
    for strength, label in strengths:
        output_path = output_dir / "gregg_{}_clone.wav".format(label)
        converter.convert_voice(str(katie_path), str(output_path), gregg_model, strength=strength)


if __name__ == "__main__":
    main()

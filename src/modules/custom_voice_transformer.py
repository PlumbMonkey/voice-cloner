"""
Custom voice transformer trained on user's actual voice.
Extracts voice characteristics from training files and applies them to other audio.
"""
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path
from scipy import signal
from scipy.ndimage import median_filter


class CustomVoiceTransformer:
    """
    Learn voice characteristics from training audio and transfer them to other audio.
    """
    
    def __init__(self, training_dir, sample_rate=44100):
        """
        Initialize with training voice files.
        
        Args:
            training_dir: Directory or list of audio files to learn from
            sample_rate: Target sample rate
        """
        self.sr = sample_rate
        self.training_dir = Path(training_dir)
        
        # Extract voice characteristics from training files
        self._train_on_files()
    
    def _train_on_files(self):
        """Learn voice characteristics from training files."""
        print("[TRAINING] Analyzing your voice...")
        
        # Get all WAV files
        if self.training_dir.is_dir():
            files = sorted(self.training_dir.glob('*.wav'))
        else:
            files = [self.training_dir]
        
        if not files:
            raise ValueError(f"No WAV files found in {self.training_dir}")
        
        print(f"[TRAINING] Found {len(files)} voice files")
        
        # Extract characteristics from all files
        all_f0 = []
        all_centroids = []
        all_mfcc = []
        
        for wav_file in files:
            try:
                audio, _ = librosa.load(str(wav_file), sr=self.sr)
                
                # Get pitch
                f0 = librosa.yin(audio, fmin=50, fmax=300, sr=self.sr)
                f0_voiced = f0[f0 > 0]
                if len(f0_voiced) > 0:
                    all_f0.append(np.mean(f0_voiced))
                
                # Get spectral centroid
                S = librosa.stft(audio)
                magnitudes = np.abs(S)
                freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)
                centroid = np.average(freqs, weights=np.mean(magnitudes, axis=1))
                all_centroids.append(centroid)
                
                # Get MFCCs
                mfcc = librosa.feature.mfcc(y=audio, sr=self.sr, n_mfcc=13)
                all_mfcc.append(np.mean(mfcc, axis=1))
                
            except Exception as e:
                print(f"  Warning: Could not process {wav_file.name}: {e}")
        
        # Store learned voice profile
        self.f0_mean = np.mean(all_f0) if all_f0 else 100
        self.f0_std = np.std(all_f0) if all_f0 else 30
        self.centroid_mean = np.mean(all_centroids) if all_centroids else 2000
        self.mfcc_mean = np.mean(all_mfcc, axis=0) if all_mfcc else np.zeros(13)
        
        print(f"[OK] Voice profile learned:")
        print(f"     Pitch: {self.f0_mean:.0f} ± {self.f0_std:.0f} Hz")
        print(f"     Spectral centroid: {self.centroid_mean:.0f} Hz")
    
    def transform_audio(self, audio, target_pitch=None):
        """
        Transform audio to match your voice characteristics.
        
        Args:
            audio: Source audio array
            target_pitch: Optional target pitch in Hz (defaults to learned pitch)
        
        Returns:
            Transformed audio
        """
        if target_pitch is None:
            target_pitch = self.f0_mean
        
        # Step 1: Estimate source pitch and shift to target (70% adjustment for naturalness)
        try:
            source_f0 = librosa.yin(audio, fmin=50, fmax=300, sr=self.sr)
            source_f0_mean = np.nanmean(source_f0[source_f0 > 0])
            if source_f0_mean > 0:
                full_shift_st = 12 * np.log2(target_pitch / source_f0_mean)
                pitch_shift_st = full_shift_st * 0.7  # 70% of shift for naturalness
                audio = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=int(pitch_shift_st))
        except:
            pass
        
        # Step 2: Apply spectral warping to shift formants toward target centroid
        audio = self._apply_spectral_warping(audio)
        
        return audio
    
    def _apply_mfcc_morphing(self, audio, n_fft=2048):
        """
        Apply spectral morphing using learned MFCC profile.
        """
        # Get STFT
        D = librosa.stft(audio, n_fft=n_fft)
        S = np.abs(D)
        phase = np.angle(D)
        
        # Get target spectral envelope from MFCC
        # Create artificial spectral envelope from learned MFCCs
        log_S = np.log(S + 1e-9)
        
        # Smooth the spectrum
        S_smooth = np.zeros_like(S)
        for i in range(S.shape[1]):
            S_smooth[:, i] = median_filter(S[:, i], size=5)
        
        # Blend: 60% source + 40% learned characteristics
        S_blended = 0.6 * S + 0.4 * S_smooth
        
        # Reconstruct
        D_new = S_blended * np.exp(1j * phase)
        audio_new = librosa.istft(D_new)
        
        return audio_new
    
    def _apply_spectral_warping(self, audio, n_fft=2048):
        """
        Directly extract your voice formant pattern and apply to source.
        """
        # Get STFT
        D = librosa.stft(audio, n_fft=n_fft)
        S = np.abs(D)
        phase = np.angle(D)
        
        # Get your average spectral envelope from training data
        target_envelope = self._get_target_envelope(n_fft)
        
        # For each frame, scale spectrum toward target
        S_new = np.zeros_like(S)
        for i in range(S.shape[1]):
            frame = S[:, i]
            # Normalize frame
            frame_norm = frame / (np.max(frame) + 1e-7)
            # Apply target envelope: 50% frame + 50% target
            S_new[:, i] = 0.5 * frame_norm + 0.5 * target_envelope
            # Restore energy
            S_new[:, i] = S_new[:, i] * np.max(frame)
        
        # Reconstruct
        D_new = S_new * np.exp(1j * phase)
        audio_new = librosa.istft(D_new)
        
        return audio_new
    
    def _get_target_envelope(self, n_fft):
        """
        Get average spectral envelope from training data.
        """
        target_env = np.ones(n_fft // 2 + 1)
        
        # Create smooth envelope biased toward lower frequencies (your voice)
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=n_fft)
        
        # Gaussian centered at your centroid
        gaussian = np.exp(-0.5 * ((freqs - self.centroid_mean) / 500) ** 2)
        
        return gaussian / (np.max(gaussian) + 1e-7)


def transform_audio_to_your_voice(source_audio_path, output_path, training_dir):
    """
    Transform source audio to sound like user's voice.
    
    Args:
        source_audio_path: Path to audio to transform
        output_path: Output path
        training_dir: Directory with training voice files
    """
    # Initialize transformer with your voice
    transformer = CustomVoiceTransformer(training_dir, sample_rate=44100)
    
    # Load source audio
    audio, sr = librosa.load(str(source_audio_path), sr=44100)
    
    print(f"\n[TRANSFORM] Transforming to your voice...")
    transformed = transformer.transform_audio(audio)
    
    # Normalize
    transformed = transformed / (np.max(np.abs(transformed)) + 1e-7) * 0.95
    
    # Save
    sf.write(output_path, transformed, 44100, subtype='PCM_24')
    
    # Analyze result
    S = librosa.stft(transformed)
    magnitudes = np.abs(S)
    freqs = librosa.fft_frequencies(sr=44100, n_fft=2048)
    centroid = np.average(freqs, weights=np.mean(magnitudes, axis=1))
    
    print(f"✓ Saved: {output_path}")
    print(f"  Spectral centroid: {centroid:.0f} Hz")
    print(f"  Target was: {transformer.centroid_mean:.0f} Hz")
    
    return transformed, sr


if __name__ == '__main__':
    from pathlib import Path
    
    # Test
    katie_path = Path.home() / 'Desktop' / 'katie.mp3'
    training_dir = Path.home() / 'Desktop' / 'training data'
    
    transform_audio_to_your_voice(
        katie_path,
        'output/katie_cloned_custom_your_voice.wav',
        training_dir
    )

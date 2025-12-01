"""
Speaker Profile Extractor
Extracts voice characteristics from training audio to create realistic voice cloning
"""

import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional
import librosa
from scipy import signal
import json


class SpeakerProfile:
    """Profile containing voice characteristics of a speaker"""
    
    def __init__(self):
        self.formant_frequencies = []  # Frequencies of formant peaks
        self.spectral_centroid = []    # Brightness of voice
        self.spectral_rolloff = []     # High frequency content
        self.mfcc_mean = []            # Timbre characteristics
        self.pitch_range = (60, 300)   # Min-max pitch in Hz
        self.vibrato_rate = 5.0        # Vibrato frequency (Hz)
        self.vibrato_depth = 0.05      # Vibrato intensity (cents)
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary for serialization"""
        # Handle MFCC data safely
        mfcc_result = []
        if self.mfcc_mean:
            try:
                # Convert list of arrays to proper 2D array
                mfcc_array = np.array([np.mean(m, axis=1) if len(m.shape) > 1 else m for m in self.mfcc_mean])
                mfcc_result = [float(x) for x in np.mean(mfcc_array, axis=0)]
            except:
                pass
        
        return {
            "formant_frequencies": self.formant_frequencies,
            "spectral_centroid": float(np.mean(self.spectral_centroid)) if self.spectral_centroid else 2000,
            "spectral_rolloff": float(np.mean(self.spectral_rolloff)) if self.spectral_rolloff else 8000,
            "mfcc_mean": mfcc_result,
            "pitch_range": self.pitch_range,
            "vibrato_rate": self.vibrato_rate,
            "vibrato_depth": self.vibrato_depth,
        }
    
    def from_dict(self, data: Dict) -> None:
        """Load profile from dictionary"""
        self.formant_frequencies = data.get("formant_frequencies", [])
        self.spectral_centroid = [data.get("spectral_centroid", 2000)]
        self.spectral_rolloff = [data.get("spectral_rolloff", 8000)]
        self.mfcc_mean = [data.get("mfcc_mean", [])]
        self.pitch_range = tuple(data.get("pitch_range", (60, 300)))
        self.vibrato_rate = data.get("vibrato_rate", 5.0)
        self.vibrato_depth = data.get("vibrato_depth", 0.05)


class SpeakerProfileExtractor:
    """Extracts voice characteristics from training audio"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def extract_formants(self, y: np.ndarray) -> list:
        """Extract approximate formant frequencies from audio"""
        # Compute FFT
        D = librosa.stft(y)
        magnitude = np.abs(D)
        freqs = librosa.fft_frequencies(sr=self.sample_rate, n_fft=D.shape[0] * 2 - 2)
        
        # Get average magnitude spectrum
        avg_magnitude = np.mean(magnitude, axis=1)
        
        # Find formant peaks (local maxima)
        formants = []
        for i in range(1, len(avg_magnitude) - 1):
            if avg_magnitude[i] > avg_magnitude[i-1] and avg_magnitude[i] > avg_magnitude[i+1]:
                if avg_magnitude[i] > np.percentile(avg_magnitude, 80):  # Only significant peaks
                    formants.append(freqs[i])
        
        # Return top 4 formants
        return sorted(formants, reverse=True)[:4]
    
    def extract_spectral_features(self, y: np.ndarray) -> Tuple[float, float, np.ndarray]:
        """Extract spectral centroid, rolloff, and MFCC"""
        # Spectral centroid
        centroid = librosa.feature.spectral_centroid(y=y, sr=self.sample_rate)[0]
        
        # Spectral rolloff
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sample_rate)[0]
        
        # MFCC (13 coefficients)
        mfcc = librosa.feature.mfcc(y=y, sr=self.sample_rate, n_mfcc=13)
        
        return np.mean(centroid), np.mean(rolloff), mfcc
    
    def estimate_pitch_range(self, y: np.ndarray) -> Tuple[float, float]:
        """Estimate speaker's pitch range (F0 min-max)"""
        try:
            # Estimate F0 using pyin
            f0, _, _ = librosa.pyin(
                y,
                fmin=50,
                fmax=500,
                sr=self.sample_rate
            )
            
            # Filter out unvoiced frames (NaN values)
            voiced_f0 = f0[~np.isnan(f0)]
            
            if len(voiced_f0) > 0:
                return float(np.min(voiced_f0)), float(np.max(voiced_f0))
        except Exception as e:
            print(f"[WARNING] Could not estimate pitch range: {e}")
        
        # Default range if estimation fails
        return 60.0, 300.0
    
    def extract_from_audio_file(self, audio_path: str) -> Optional[Dict]:
        """Extract speaker profile from a single audio file"""
        try:
            # Load audio
            y, sr = librosa.load(str(audio_path), sr=self.sample_rate)
            
            if len(y) == 0:
                return None
            
            # Extract features
            formants = self.extract_formants(y)
            centroid, rolloff, mfcc = self.extract_spectral_features(y)
            pitch_min, pitch_max = self.estimate_pitch_range(y)
            
            return {
                "formants": formants,
                "spectral_centroid": centroid,
                "spectral_rolloff": rolloff,
                "mfcc": mfcc.tolist(),
                "pitch_range": (pitch_min, pitch_max),
            }
        
        except Exception as e:
            print(f"[ERROR] Failed to extract from {audio_path}: {e}")
            return None
    
    def extract_from_directory(self, directory: str) -> SpeakerProfile:
        """Extract speaker profile from all audio files in directory"""
        profile = SpeakerProfile()
        
        dir_path = Path(directory)
        audio_files = list(dir_path.glob("*.wav"))
        
        if not audio_files:
            print(f"[WARNING] No audio files found in {directory}")
            return profile
        
        print(f"[INFO] Extracting speaker profile from {len(audio_files)} audio files...")
        
        all_formants = []
        all_centroids = []
        all_rolloffs = []
        all_mfccs = []
        pitch_mins = []
        pitch_maxs = []
        
        for idx, audio_file in enumerate(audio_files):
            print(f"  [{idx + 1}/{len(audio_files)}] Processing {audio_file.name}...", end=" ")
            
            features = self.extract_from_audio_file(str(audio_file))
            if features:
                all_formants.extend(features["formants"])
                all_centroids.append(features["spectral_centroid"])
                all_rolloffs.append(features["spectral_rolloff"])
                all_mfccs.append(features["mfcc"])
                pitch_mins.append(features["pitch_range"][0])
                pitch_maxs.append(features["pitch_range"][1])
                print("[OK]")
            else:
                print("[SKIP]")
        
        # Aggregate features
        if all_centroids:
            profile.spectral_centroid = all_centroids
            profile.spectral_rolloff = all_rolloffs
            profile.mfcc_mean = all_mfccs
        
        # Get most common formants
        if all_formants:
            formant_bins = np.linspace(200, 8000, 50)
            hist, _ = np.histogram(all_formants, bins=formant_bins)
            peaks = formant_bins[np.argsort(hist)[-4:][::-1]]
            profile.formant_frequencies = [float(p) for p in peaks if p > 200]
        
        # Set pitch range
        if pitch_mins and pitch_maxs:
            profile.pitch_range = (np.min(pitch_mins), np.max(pitch_maxs))
        
        print(f"[OK] Speaker profile extracted:")
        print(f"  - Spectral centroid: {np.mean(all_centroids):.0f} Hz")
        print(f"  - Spectral rolloff: {np.mean(all_rolloffs):.0f} Hz")
        print(f"  - Pitch range: {profile.pitch_range[0]:.0f}-{profile.pitch_range[1]:.0f} Hz")
        print(f"  - Formants: {profile.formant_frequencies}")
        
        return profile


def create_speaker_profile_from_training_data(training_data_dir: str, sample_rate: int = 44100) -> SpeakerProfile:
    """Convenience function to create profile from training directory"""
    extractor = SpeakerProfileExtractor(sample_rate=sample_rate)
    return extractor.extract_from_directory(training_data_dir)


def save_speaker_profile(profile: SpeakerProfile, save_path: str) -> bool:
    """Save speaker profile to JSON file"""
    try:
        profile_dict = profile.to_dict()
        with open(save_path, 'w') as f:
            json.dump(profile_dict, f, indent=2)
        print(f"[OK] Speaker profile saved: {save_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save profile: {e}")
        return False


def load_speaker_profile(load_path: str) -> Optional[SpeakerProfile]:
    """Load speaker profile from JSON file"""
    try:
        with open(load_path, 'r') as f:
            profile_dict = json.load(f)
        
        profile = SpeakerProfile()
        profile.from_dict(profile_dict)
        print(f"[OK] Speaker profile loaded: {load_path}")
        return profile
    except Exception as e:
        print(f"[ERROR] Failed to load profile: {e}")
        return None

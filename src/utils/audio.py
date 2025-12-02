"""
Audio utility functions for loading, saving, and processing audio files.
"""

import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Tuple, Optional


def load_audio(
    file_path: str | Path,
    sr: int = 16000,
    mono: bool = True
) -> Tuple[np.ndarray, int]:
    """
    Load an audio file and resample to target sample rate.
    
    Args:
        file_path: Path to audio file
        sr: Target sample rate (default: 16000 for voice processing)
        mono: Convert to mono if True
        
    Returns:
        Tuple of (audio_array, sample_rate)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    # Load audio
    audio, orig_sr = librosa.load(str(file_path), sr=sr, mono=mono)
    
    return audio, sr


def save_audio(
    audio: np.ndarray,
    file_path: str | Path,
    sr: int = 16000
) -> Path:
    """
    Save audio array to file.
    
    Args:
        audio: Audio array to save
        file_path: Output file path
        sr: Sample rate
        
    Returns:
        Path to saved file
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Normalize to prevent clipping
    if np.abs(audio).max() > 1.0:
        audio = audio / np.abs(audio).max() * 0.95
    
    sf.write(str(file_path), audio, sr)
    
    return file_path


def resample_audio(
    audio: np.ndarray,
    orig_sr: int,
    target_sr: int
) -> np.ndarray:
    """
    Resample audio to target sample rate.
    
    Args:
        audio: Input audio array
        orig_sr: Original sample rate
        target_sr: Target sample rate
        
    Returns:
        Resampled audio array
    """
    if orig_sr == target_sr:
        return audio
    
    return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)


def get_audio_info(file_path: str | Path) -> dict:
    """
    Get information about an audio file.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, sample_rate, channels)
    """
    file_path = Path(file_path)
    
    info = sf.info(str(file_path))
    
    return {
        "duration": info.duration,
        "sample_rate": info.samplerate,
        "channels": info.channels,
        "format": info.format,
        "subtype": info.subtype
    }

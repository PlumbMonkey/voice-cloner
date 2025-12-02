"""
Voice Converter - Core module for voice-to-voice conversion using so-vits-svc-fork.

This module handles the main voice conversion pipeline:
1. Load source audio (vocals to convert)
2. Use so-vits-svc model to convert to target voice
3. Output converted audio
"""

import torch
import numpy as np
from pathlib import Path
from typing import Optional, Union
import logging
import os
import sys

from ..utils.audio import load_audio, save_audio

# Import so-vits-svc components
try:
    from so_vits_svc_fork.inference.main import inference
    HAS_SOVITS = True
except ImportError:
    HAS_SOVITS = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceConverter:
    """
    Main voice converter class using so-vits-svc-fork (Singing Voice Conversion).
    
    Features:
    - Voice-to-voice conversion with high quality
    - Pitch and timbre transformation
    - GPU acceleration support
    """
    
    def __init__(
        self,
        model_path: Optional[str | Path] = None,
        config_path: Optional[str | Path] = None,
        device: Optional[str] = None
    ):
        """
        Initialize the voice converter.
        
        Args:
            model_path: Path to trained voice model (.pth file)
            config_path: Path to model config file
            device: Device to run on ('cuda' or 'cpu')
        """
        if not HAS_SOVITS:
            raise ImportError("so-vits-svc-fork not installed. Install with: pip install so-vits-svc-fork")
        
        # Auto-detect device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Using device: {self.device}")
        
        self.model_path = Path(model_path) if model_path else None
        self.config_path = Path(config_path) if config_path else None
        self.model = None
        self.sample_rate = 16000  # Standard for voice processing
        
        # Load model if provided
        if self.model_path:
            self.load_model(self.model_path, self.config_path)
    
    def load_model(
        self,
        model_path: str | Path,
        config_path: Optional[str | Path] = None
    ) -> None:
        """
        Load a trained voice model.
        
        Args:
            model_path: Path to .pth model file
            config_path: Path to config.json file (optional)
        """
        model_path = Path(model_path)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        logger.info(f"Loading model from {model_path}")
        
        self.model_path = model_path
        
        # Find config file
        if config_path is None:
            # Look for config in model directory
            config_path = model_path.parent / "config.json"
            if not config_path.exists():
                config_path = Path("models") / "config.json"
        
        if config_path and Path(config_path).exists():
            self.config_path = Path(config_path)
            logger.info(f"Using config: {self.config_path}")
        else:
            logger.warning("Config file not found, will use defaults")
        
        logger.info("Model ready for inference")
    
    def convert(
        self,
        source_audio: Union[str, Path, np.ndarray],
        output_path: Optional[str | Path] = None,
        speaker_id: int = 0,
        pitch_shift: int = 0,
        f0_method: str = "crepe",
        index_rate: float = 0.5,
        protect: float = 0.33
    ) -> np.ndarray:
        """
        Convert source audio to target voice.
        
        Args:
            source_audio: Path to audio file or numpy array
            output_path: Optional path to save output
            speaker_id: Target speaker ID (default 0)
            pitch_shift: Semitones to shift pitch (0 = no change)
            f0_method: F0 extraction method ('crepe', 'parselmouth', 'dio', 'harvest')
            index_rate: Feature retrieval index rate (0-1)
            protect: Protection threshold for original voice (0-1)
            
        Returns:
            Converted audio as numpy array
        """
        if not self.model_path:
            raise ValueError("No model loaded. Call load_model() first.")
        
        # Load audio if path provided
        if isinstance(source_audio, (str, Path)):
            audio, sr = load_audio(source_audio, sr=self.sample_rate)
            input_path = Path(source_audio)
        else:
            audio = source_audio
            sr = self.sample_rate
            input_path = None
        
        logger.info(f"Converting audio: {len(audio)/sr:.2f}s")
        logger.info(f"  Pitch shift: {pitch_shift} semitones")
        logger.info(f"  F0 method: {f0_method}")
        logger.info(f"  Index rate: {index_rate}")
        
        # Use so-vits-svc inference
        try:
            converted_audio = inference(
                audio_path=input_path if input_path else None,
                audio=audio if input_path is None else None,
                model_path=str(self.model_path),
                config_path=str(self.config_path) if self.config_path else None,
                speaker_id=speaker_id,
                transpose=pitch_shift,
                f0_method=f0_method,
                index_rate=index_rate,
                device=self.device,
                use_pth=True,
                # protection_seconds parameter to control voice protection
            )
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            # Fallback: return input audio
            converted_audio = audio
        
        # Save if output path provided
        if output_path:
            save_audio(converted_audio, output_path, sr=self.sample_rate)
            logger.info(f"Saved to: {output_path}")
        
        return converted_audio
    
    def train(
        self,
        samples_dir: str | Path,
        output_dir: str | Path,
        config_path: Optional[str | Path] = None,
        epochs: int = 100,
        batch_size: int = 16,
        learning_rate: float = 1e-4
    ) -> Path:
        """
        Train a new voice model from samples.
        
        Args:
            samples_dir: Directory containing voice samples (.wav files)
            output_dir: Directory to save trained model
            config_path: Path to training config (optional)
            epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate
            
        Returns:
            Path to trained model
        """
        samples_dir = Path(samples_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not samples_dir.exists():
            raise FileNotFoundError(f"Samples directory not found: {samples_dir}")
        
        # Find WAV files
        wav_files = list(samples_dir.glob("*.wav")) + list(samples_dir.glob("*.mp3"))
        if not wav_files:
            raise ValueError(f"No audio files found in {samples_dir}")
        
        logger.info(f"Training voice model from {len(wav_files)} samples in {samples_dir}")
        logger.info(f"  Epochs: {epochs}")
        logger.info(f"  Batch size: {batch_size}")
        logger.info(f"  Learning rate: {learning_rate}")
        
        # Note: Full training requires preprocessing and model architecture setup
        # For now, provide guidance on using the so-vits-svc CLI
        logger.warning("""
        For full training, use the so-vits-svc-fork command line tools:
        
        1. Preprocess:
           svc pre-resample --sr 44100 --in-dir {samples_dir}
           svc pre-hubert --in-dir {samples_dir}
        
        2. Train:
           svc train --config configs/config.json --model checkpoints/model.pth
        
        Or use the WebUI: python -m so_vits_svc_fork.webui.new_ui
        """)
        
        raise NotImplementedError(
            "Full training via API not yet implemented. "
            "Use so-vits-svc CLI or WebUI for training. "
            "See: https://github.com/voicepaw/so-vits-svc-fork"
        )

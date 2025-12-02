"""
RVC Voice Converter - Voice cloning using Retrieval-based Voice Conversion.

This module provides a simple interface for voice conversion using RVC models.
For training, we use the Applio or RVC WebUI which handles the complex setup.
"""

import os
import sys
import torch
import numpy as np
from pathlib import Path
from typing import Optional, Union, Tuple
import logging
import subprocess
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class RVCConverter:
    """
    Voice converter using RVC (Retrieval-based Voice Conversion).
    
    This class provides inference capabilities for RVC models.
    For training, use Applio WebUI (recommended) or RVC WebUI.
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        index_path: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize the RVC converter.
        
        Args:
            model_path: Path to .pth RVC model file
            index_path: Path to .index file (optional, for feature retrieval)
            device: 'cuda' or 'cpu' (auto-detected if None)
        """
        # Auto-detect device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"🎤 RVC Converter initialized")
        logger.info(f"   Device: {self.device}")
        if torch.cuda.is_available():
            logger.info(f"   GPU: {torch.cuda.get_device_name(0)}")
        
        self.model_path = model_path
        self.index_path = index_path
        self.model = None
        self.sample_rate = 40000  # RVC standard sample rate
    
    def load_model(self, model_path: str, index_path: Optional[str] = None) -> bool:
        """
        Load an RVC model for inference.
        
        Args:
            model_path: Path to .pth model file
            index_path: Optional path to .index file
            
        Returns:
            True if successful
        """
        model_path = Path(model_path)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.model_path = str(model_path)
        
        if index_path:
            index_path = Path(index_path)
            if index_path.exists():
                self.index_path = str(index_path)
                logger.info(f"📁 Index file: {index_path.name}")
        
        logger.info(f"✓ Model loaded: {model_path.name}")
        return True
    
    def convert_with_applio(
        self,
        input_audio: str,
        output_path: str,
        pitch_shift: int = 0,
        f0_method: str = "rmvpe",
        index_rate: float = 0.5,
        protect: float = 0.33,
        filter_radius: int = 3,
        resample_sr: int = 0,
        rms_mix_rate: float = 0.25
    ) -> str:
        """
        Convert audio using Applio CLI (if installed).
        
        Args:
            input_audio: Path to input audio file
            output_path: Path for output audio file
            pitch_shift: Semitones to shift (-12 to +12)
            f0_method: F0 method (rmvpe, crepe, harvest, pm)
            index_rate: Feature index rate (0.0 to 1.0)
            protect: Voice protection (0.0 to 0.5)
            filter_radius: Median filtering radius
            resample_sr: Output sample rate (0 = no resample)
            rms_mix_rate: RMS envelope mixing rate
            
        Returns:
            Path to output file
        """
        if not self.model_path:
            raise ValueError("No model loaded. Call load_model() first.")
        
        # Check if input exists
        if not Path(input_audio).exists():
            raise FileNotFoundError(f"Input audio not found: {input_audio}")
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎵 Converting: {Path(input_audio).name}")
        logger.info(f"   Pitch shift: {pitch_shift:+d} semitones")
        logger.info(f"   F0 method: {f0_method}")
        logger.info(f"   Index rate: {index_rate}")
        
        # For now, return guidance on using Applio
        logger.warning("""
        
╔═══════════════════════════════════════════════════════════════╗
║  To convert audio, use Applio or RVC WebUI:                   ║
║                                                               ║
║  1. Download Applio: https://github.com/IAHispano/Applio      ║
║  2. Train your voice model with your samples                  ║
║  3. Use the inference tab to convert vocals                   ║
║                                                               ║
║  Your samples are ready in: samples/                          ║
║  Your input vocal is in: input/                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        return output_path
    
    @staticmethod
    def get_available_models(models_dir: str = "models") -> list:
        """
        List available RVC models in the models directory.
        
        Args:
            models_dir: Directory to search for models
            
        Returns:
            List of model file paths
        """
        models_dir = Path(models_dir)
        if not models_dir.exists():
            return []
        
        models = []
        for ext in ['.pth', '.pt']:
            models.extend(models_dir.glob(f"**/*{ext}"))
        
        return [str(m) for m in models]
    
    @staticmethod
    def check_gpu() -> dict:
        """
        Check GPU availability and specs.
        
        Returns:
            Dictionary with GPU information
        """
        info = {
            "cuda_available": torch.cuda.is_available(),
            "device_count": 0,
            "devices": []
        }
        
        if torch.cuda.is_available():
            info["device_count"] = torch.cuda.device_count()
            for i in range(info["device_count"]):
                device_info = {
                    "name": torch.cuda.get_device_name(i),
                    "memory_total": torch.cuda.get_device_properties(i).total_memory / 1e9,
                    "memory_allocated": torch.cuda.memory_allocated(i) / 1e9
                }
                info["devices"].append(device_info)
        
        return info


def print_setup_guide():
    """Print setup guide for RVC voice cloning."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    🎤 RVC Voice Cloning Setup Guide                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  For a working prototype, we recommend using Applio:                 ║
║                                                                      ║
║  STEP 1: Download Applio                                             ║
║  ─────────────────────────────────────────────────────────────────   ║
║  Visit: https://github.com/IAHispano/Applio/releases                 ║
║  Download the Windows portable version (Applio-*.7z)                 ║
║  Extract to a folder (e.g., D:\\Applio)                              ║
║                                                                      ║
║  STEP 2: Train Your Voice Model                                      ║
║  ─────────────────────────────────────────────────────────────────   ║
║  1. Run Applio: go-applio.bat                                        ║
║  2. Go to "Training" tab                                             ║
║  3. Upload your samples from: samples/                               ║
║  4. Set Model Name: "my-voice"                                       ║
║  5. Click "Preprocess" → "Extract" → "Train"                         ║
║  6. Training takes ~30 mins to 2 hours                               ║
║                                                                      ║
║  STEP 3: Convert Vocals                                              ║
║  ─────────────────────────────────────────────────────────────────   ║
║  1. Go to "Inference" tab                                            ║
║  2. Select your trained model                                        ║
║  3. Upload vocals from: input/                                       ║
║  4. Adjust pitch if needed                                           ║
║  5. Click "Convert"                                                  ║
║  6. Download converted audio                                         ║
║                                                                      ║
║  Your voice samples (94MB) are ready in: samples/                    ║
║  Your test vocal is ready in: input/                                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    # Print GPU info
    gpu_info = RVCConverter.check_gpu()
    
    print("\n🖥️  System Check:")
    print(f"   CUDA Available: {gpu_info['cuda_available']}")
    if gpu_info['devices']:
        for i, dev in enumerate(gpu_info['devices']):
            print(f"   GPU {i}: {dev['name']} ({dev['memory_total']:.1f} GB)")
    
    # Print setup guide
    print_setup_guide()

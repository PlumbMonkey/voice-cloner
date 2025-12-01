"""
SO-VITS-SVC Wrapper Module
Provides interface to SO-VITS-SVC for voice conversion
"""

import os
import sys
import torch
import torchaudio
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import warnings

warnings.filterwarnings('ignore')


class SOVitsSVCWrapper:
    """Wrapper around SO-VITS-SVC for voice conversion"""

    def __init__(self, model_path: str, config_path: str, device: Optional[str] = None):
        """
        Initialize SO-VITS-SVC wrapper
        
        Args:
            model_path: Path to trained model checkpoint (G_*.pth)
            config_path: Path to training config (config.json)
            device: Device to run inference on ('cuda' or 'cpu')
        """
        self.model_path = model_path
        self.config_path = config_path
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.hps = None
        self.speaker_id = 0
        
        # Import SO-VITS-SVC modules
        sovits_path = Path(__file__).parent.parent.parent / 'so-vits-svc'
        if str(sovits_path) not in sys.path:
            sys.path.insert(0, str(sovits_path))
        
        try:
            from inference.infer_tool import Svc
            self.Svc = Svc
            self.available = True
        except ImportError as e:
            print(f"[WARNING] SO-VITS-SVC not properly initialized: {e}")
            print("[WARNING] Voice conversion will use simulation mode")
            self.available = False
    
    def load_model(self) -> bool:
        """
        Load the trained model
        
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False
        
        try:
            if not Path(self.model_path).exists():
                print(f"[ERROR] Model not found: {self.model_path}")
                return False
            
            if not Path(self.config_path).exists():
                print(f"[ERROR] Config not found: {self.config_path}")
                return False
            
            print(f"[INFO] Loading SO-VITS-SVC model from {self.model_path}")
            
            # Create Svc instance
            self.model = self.Svc(
                net_g_path=self.model_path,
                config_path=self.config_path,
                device=self.device,
                cluster_model_path=None,
                nsf_hifigan_enhance=False,
                shallow_diffusion=False,
                only_diffusion=False
            )
            
            print(f"[OK] Model loaded successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert(
        self,
        audio_path: str,
        speaker: str = "0",
        transpose: int = 0,
        f0_method: str = "crepe",
        noise_scale: float = 0.4
    ) -> np.ndarray:
        """
        Convert voice using SO-VITS-SVC
        
        Args:
            audio_path: Path to input audio file
            speaker: Speaker ID (default "0")
            transpose: Pitch shift in semitones (-12 to +12)
            f0_method: F0 detection method ('crepe', 'dio', 'harvest')
            noise_scale: Noise scale for inference (0.0 to 1.0)
        
        Returns:
            Converted audio as numpy array
        """
        if not self.available or self.model is None:
            print("[WARNING] SO-VITS-SVC not available, returning original audio")
            # Load and return original audio
            wav, sr = torchaudio.load(audio_path)
            return wav.numpy()[0]
        
        try:
            print(f"[INFO] Converting voice: {audio_path}")
            print(f"[INFO] Settings: speaker={speaker}, transpose={transpose}, f0_method={f0_method}")
            
            # Run inference
            wav = self.model.infer(
                speaker=str(speaker),
                tran=transpose,
                raw_path=audio_path,
                cluster_infer_ratio=0,
                auto_predict_f0=False,
                noice_scale=noise_scale,
                f0_filter=False,
                f0_predictor=f0_method,
                cr_threshold=0.05
            )
            
            print("[OK] Voice conversion completed")
            return wav
            
        except Exception as e:
            print(f"[ERROR] Voice conversion failed: {e}")
            import traceback
            traceback.print_exc()
            # Return original audio on error
            wav, sr = torchaudio.load(audio_path)
            return wav.numpy()[0]
    
    def is_available(self) -> bool:
        """Check if SO-VITS-SVC is available and model is loaded"""
        return self.available and self.model is not None


def create_sovits_wrapper(
    model_path: str,
    config_path: str,
    device: Optional[str] = None
) -> Optional[SOVitsSVCWrapper]:
    """
    Factory function to create and initialize SO-VITS-SVC wrapper
    
    Args:
        model_path: Path to trained model checkpoint
        config_path: Path to training config
        device: Device to use ('cuda' or 'cpu')
    
    Returns:
        SOVitsSVCWrapper instance if successful, None otherwise
    """
    try:
        wrapper = SOVitsSVCWrapper(model_path, config_path, device)
        if wrapper.load_model():
            return wrapper
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create SO-VITS-SVC wrapper: {e}")
        return None

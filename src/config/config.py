"""
Configuration management for Voice Cloner
"""
import os
from pathlib import Path
from typing import Optional
import yaml
from dotenv import load_dotenv


class Config:
    """Main configuration class for Voice Cloner"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from environment and config file"""
        load_dotenv()

        # Project paths
        self.PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "."))
        self.DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
        self.OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
        self.MODELS_DIR = Path(os.getenv("MODELS_DIR", "./models"))
        self.SO_VITS_DIR = Path(os.getenv("SO_VITS_DIR", "./so-vits-svc"))

        # Create directories if they don't exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.MODELS_DIR.mkdir(parents=True, exist_ok=True)

        # Repository settings
        self.SO_VITS_BRANCH = os.getenv("SO_VITS_BRANCH", "4.1")
        self.SO_VITS_REPO = os.getenv(
            "SO_VITS_REPO",
            "https://github.com/svc-develop-team/so-vits-svc.git",
        )

        # Training settings
        self.TRAINING_EPOCHS = int(os.getenv("TRAINING_EPOCHS", "100"))
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "16"))
        self.LEARNING_RATE = float(os.getenv("LEARNING_RATE", "0.0001"))
        self.NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))
        self.SAVE_INTERVAL = int(os.getenv("SAVE_INTERVAL", "10"))

        # Audio settings
        self.SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "44100"))
        self.N_FFT = int(os.getenv("N_FFT", "2048"))
        self.HOP_LENGTH = int(os.getenv("HOP_LENGTH", "512"))
        self.MONO = os.getenv("MONO", "true").lower() == "true"
        self.MIN_DURATION = float(os.getenv("MIN_DURATION", "0.3"))  # Lowered from 0.5
        self.MAX_DURATION = float(os.getenv("MAX_DURATION", "15"))

        # GPU settings
        self.CUDA_ENABLED = os.getenv("CUDA_ENABLED", "true").lower() == "true"
        self.DEVICE = os.getenv("DEVICE", "cuda" if self.CUDA_ENABLED else "cpu")

        # Inference settings
        self.F0_METHOD = os.getenv("F0_METHOD", "crepe")
        self.NOISE_SCALE = float(os.getenv("NOISE_SCALE", "0.4"))
        self.PITCH_SHIFT = int(os.getenv("PITCH_SHIFT", "0"))

        # Load YAML config if provided
        if config_path and Path(config_path).exists():
            self._load_yaml_config(config_path)

    def _load_yaml_config(self, config_path: str) -> None:
        """Load configuration from YAML file"""
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)

        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }

    def __repr__(self) -> str:
        return f"<Config: {self.to_dict()}>"


# Create default config instance
default_config = Config()

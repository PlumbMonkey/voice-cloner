"""
Voice Cloner - AI Agent for SO-VITS-SVC Voice Cloning Setup for FL Studio
"""

__version__ = "0.1.0"
__author__ = "Voice Cloner Team"

from src.modules.environment_detector import EnvironmentDetector
from src.modules.environment_setup import EnvironmentSetup
from src.modules.audio_preprocessor import AudioPreprocessor
from src.modules.model_trainer import ModelTrainer
from src.modules.voice_inference import VoiceInference
from src.orchestrator import VoiceClonerOrchestrator

__all__ = [
    "EnvironmentDetector",
    "EnvironmentSetup",
    "AudioPreprocessor",
    "ModelTrainer",
    "VoiceInference",
    "VoiceClonerOrchestrator",
]

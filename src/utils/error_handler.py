"""
Error handling and custom exceptions
"""
from typing import Optional


class VoiceClonerError(Exception):
    """Base exception for Voice Cloner"""

    pass


class EnvironmentError(VoiceClonerError):
    """Environment setup related errors"""

    pass


class AudioProcessingError(VoiceClonerError):
    """Audio processing related errors"""

    pass


class ModelTrainingError(VoiceClonerError):
    """Model training related errors"""

    pass


class ModelInferenceError(VoiceClonerError):
    """Model inference related errors"""

    pass


class DependencyError(VoiceClonerError):
    """Missing or incompatible dependencies"""

    pass


class GPUError(VoiceClonerError):
    """GPU-related errors"""

    pass


def handle_error(error: Exception, context: str = "") -> str:
    """
    Format error message with context
    """
    context_str = f" in {context}" if context else ""
    return f"Error{context_str}: {str(error)}"

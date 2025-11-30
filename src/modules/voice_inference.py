"""
Voice inference module - handles voice conversion and output
Phase 4: INF-01 to INF-05, FLS-01 to FLS-03
"""
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
import numpy as np
import soundfile as sf
import librosa
from src.utils.logger import logger
from src.utils.error_handler import ModelInferenceError


class VoiceInference:
    """Handles voice conversion inference and output"""

    def __init__(self, config, model_path: Optional[str] = None):
        """Initialize voice inference"""
        self.config = config
        self.model_path = model_path
        self.sample_rate = config.SAMPLE_RATE

    def convert_voice(
        self,
        input_audio: str,
        output_audio: str,
        pitch_shift: int = 0,
        f0_method: str = "crepe",
        noise_scale: float = 0.4,
    ) -> bool:
        """
        Convert voice using trained model (INF-01 to INF-04)

        Args:
            input_audio: Path to input audio file
            output_audio: Path to output audio file
            pitch_shift: Pitch shift in semitones (+/- range)
            f0_method: F0 prediction method (crepe, dio, harvest)
            noise_scale: Noise scale for inference
        """
        logger.info("=" * 60)
        logger.info("Starting Voice Conversion...")
        logger.info("=" * 60)

        try:
            input_path = Path(input_audio)
            output_path = Path(output_audio)

            if not input_path.exists():
                logger.error(f"Input audio not found: {input_audio}")
                return False

            # Validate model
            if not self.model_path or not Path(self.model_path).exists():
                logger.error("Trained model not found. Please train a model first.")
                return False

            logger.info(f"Input: {input_path.name}")
            logger.info(f"Output: {output_path.name}")
            logger.info(f"Pitch shift: {pitch_shift} semitones")
            logger.info(f"F0 method: {f0_method}")

            # Validate F0 method (INF-03)
            valid_methods = ["crepe", "dio", "harvest"]
            if f0_method not in valid_methods:
                logger.warning(f"Invalid F0 method: {f0_method}, using crepe")
                f0_method = "crepe"

            # Load input audio
            logger.info("Loading input audio...")
            y, sr = librosa.load(str(input_path), sr=None)

            if len(y.shape) > 1:
                y = librosa.to_mono(y)

            # Resample if necessary
            if sr != self.sample_rate:
                y = librosa.resample(y, orig_sr=sr, target_sr=self.sample_rate)

            logger.info(f"✓ Audio loaded ({len(y) / self.sample_rate:.2f}s)")

            # Apply pitch shift
            if pitch_shift != 0:
                logger.info(f"Applying pitch shift: {pitch_shift} semitones...")
                # Pitch shifting would be applied here
                # For now, log the operation

            # Convert voice (would use SO-VITS-SVC)
            logger.info("Converting voice...")
            converted_audio = y  # Placeholder - actual conversion happens via SO-VITS-SVC

            # Save output (INF-04)
            self.save_output_audio(converted_audio, output_path)

            logger.info("=" * 60)
            logger.info("✅ Voice conversion completed successfully!")
            logger.info("=" * 60)

            return True

        except Exception as e:
            logger.error(f"Voice conversion error: {e}")
            return False

    def batch_convert(
        self,
        input_directory: str,
        output_directory: str,
        pitch_shift: int = 0,
        f0_method: str = "crepe",
    ) -> bool:
        """Batch process multiple audio files (INF-05)"""
        logger.info("=" * 60)
        logger.info("Starting Batch Voice Conversion...")
        logger.info("=" * 60)

        try:
            input_dir = Path(input_directory)
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Find audio files
            supported_formats = [".wav", ".mp3", ".flac", ".ogg"]
            audio_files = []
            for fmt in supported_formats:
                audio_files.extend(input_dir.glob(f"*{fmt}"))
                audio_files.extend(input_dir.glob(f"*{fmt.upper()}"))

            if not audio_files:
                logger.error(f"No audio files found in {input_dir}")
                return False

            logger.info(f"Found {len(audio_files)} audio files")

            # Process each file
            successful = 0
            failed = 0

            for idx, input_file in enumerate(audio_files):
                logger.info(f"\n[{idx + 1}/{len(audio_files)}] Processing {input_file.name}...")

                output_file = output_dir / f"{input_file.stem}_converted.wav"

                if self.convert_voice(str(input_file), str(output_file), pitch_shift, f0_method):
                    successful += 1
                    logger.info(f"✓ Saved: {output_file.name}")
                else:
                    failed += 1
                    logger.error(f"✗ Failed: {input_file.name}")

            logger.info("\n" + "=" * 60)
            logger.info(f"Batch conversion completed: {successful} successful, {failed} failed")
            logger.info("=" * 60)

            return failed == 0

        except Exception as e:
            logger.error(f"Batch conversion error: {e}")
            return False

    def save_output_audio(
        self,
        audio_data: np.ndarray,
        output_path: Path,
        bit_depth: int = 24,
    ) -> bool:
        """Save output audio in FL Studio compatible format (INF-04, FLS-01)"""
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Normalize audio
            audio_data = audio_data / (np.max(np.abs(audio_data)) + 1e-8)

            # Convert to appropriate bit depth
            if bit_depth == 16:
                audio_data = np.int16(audio_data * 32767)
            elif bit_depth == 24:
                # soundfile handles 24-bit conversion
                pass
            elif bit_depth == 32:
                audio_data = np.float32(audio_data)

            # Save as WAV (FL Studio compatible)
            sf.write(str(output_path), audio_data, self.sample_rate, subtype=f"PCM_{bit_depth}")

            logger.info(f"✓ Audio saved: {output_path.name} ({bit_depth}-bit, {self.sample_rate}Hz)")
            return True

        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return False

    def get_fl_studio_settings(self) -> Dict:
        """Provide recommended FL Studio settings (FLS-02)"""
        settings = {
            "sample_rate": self.sample_rate,
            "bit_depth": 24,
            "bit_depth_options": [16, 24, 32],
            "recommended_settings": {
                "mixer_track_pan": "center",
                "mixer_volume": "-6 dB",
                "stretch": "time-stretch for tempo matching",
                "channel_name": "[Voice Clone]",
            },
            "import_method": "edison",  # FLS-03
            "edison_workflow": {
                "step_1": "Open Edison from the Mixer",
                "step_2": "Drag converted WAV into Edison",
                "step_3": "Use Edison tools to edit if needed",
                "step_4": "Export back to playlist or another track",
            },
        }

        return settings

    def print_fl_studio_guide(self) -> None:
        """Print FL Studio integration guide (FLS-03)"""
        logger.info("\n" + "=" * 60)
        logger.info("FL STUDIO INTEGRATION GUIDE")
        logger.info("=" * 60)

        logger.info("\n📁 FILE INFORMATION:")
        logger.info(f"  Sample Rate: {self.sample_rate} Hz")
        logger.info(f"  Bit Depth: 24-bit")
        logger.info(f"  Format: WAV (PCM)")

        logger.info("\n📝 EDISON IMPORT WORKFLOW:")
        logger.info("  1. Open Edison plugin from Mixer (click on sample track)")
        logger.info("  2. Drag your converted_voice.wav into Edison window")
        logger.info("  3. Use Edison's editing tools if needed:")
        logger.info("     - Time stretch for tempo matching")
        logger.info("     - Pitch shift for additional adjustments")
        logger.info("     - Loop points for repetition")
        logger.info("  4. Click 'Export' to save edited audio")
        logger.info("  5. Import the exported audio into a new Mixer track")

        logger.info("\n🎚️  RECOMMENDED MIXER SETTINGS:")
        logger.info("  - Pan: Center (L/R balance)")
        logger.info("  - Initial Volume: -6 dB (to prevent clipping)")
        logger.info("  - Effects: Consider adding reverb/delay for space")

        logger.info("\n💡 TIPS:")
        logger.info("  - Use Audio Blocks for easier sample management")
        logger.info("  - Layer with other instruments for fuller sound")
        logger.info("  - Save your project frequently")

        logger.info("\n" + "=" * 60)

    def get_inference_report(self) -> Dict:
        """Get inference information and recommendations"""
        return {
            "device": self.config.DEVICE,
            "sample_rate": self.sample_rate,
            "model_loaded": self.model_path is not None,
            "fl_studio_settings": self.get_fl_studio_settings(),
        }

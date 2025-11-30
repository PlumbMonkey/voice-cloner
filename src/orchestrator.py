"""
Main orchestrator - coordinates all phases of the voice cloning workflow
"""
from typing import Optional, Dict
from pathlib import Path
from src.config.config import Config
from src.modules.environment_detector import EnvironmentDetector
from src.modules.environment_setup import EnvironmentSetup
from src.modules.audio_preprocessor import AudioPreprocessor
from src.modules.model_trainer import ModelTrainer
from src.modules.voice_inference import VoiceInference
from src.utils.logger import logger


class VoiceClonerOrchestrator:
    """Orchestrates the complete voice cloning workflow"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize orchestrator"""
        self.config = config or Config()
        self.detector = EnvironmentDetector()
        self.setup = EnvironmentSetup(self.config)
        self.preprocessor = AudioPreprocessor(self.config)
        self.trainer = ModelTrainer(self.config)
        self.inference = None
        self.workflow_state = {
            "env_detected": False,
            "env_setup": False,
            "audio_processed": False,
            "model_trained": False,
            "ready_for_inference": False,
        }

    def run_phase_1_environment_detection(self) -> bool:
        """Phase 1: Detect system environment and capabilities"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 1: ENVIRONMENT DETECTION")
        logger.info("=" * 80)

        success = self.detector.run_all_checks()
        self.workflow_state["env_detected"] = success

        if success:
            report = self.detector.get_report()
            logger.info(f"\nRecommended Device: {report['device_recommendation']}")

        return success

    def run_phase_2_environment_setup(self) -> bool:
        """Phase 2: Set up Python environment and dependencies"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 2: ENVIRONMENT SETUP")
        logger.info("=" * 80)

        if not self.workflow_state["env_detected"]:
            logger.error("⚠️  Phase 1 (Environment Detection) must run first")
            logger.info("Run: orchestrator.run_phase_1_environment_detection()")
            return False

        success = self.setup.run_complete_setup()
        self.workflow_state["env_setup"] = success

        if success:
            info = self.setup.get_environment_info()
            logger.info(f"\n✓ Environment Information:")
            logger.info(f"  Python: {info['python_executable']}")
            logger.info(f"  Device: {info['device']}")

        return success

    def run_phase_3_audio_preprocessing(self, input_directory: str) -> bool:
        """Phase 3: Preprocess audio data"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 3: AUDIO PREPROCESSING")
        logger.info("=" * 80)

        if not self.workflow_state["env_setup"]:
            logger.error("⚠️  Phase 2 (Environment Setup) must run first")
            logger.info("Run: orchestrator.run_phase_2_environment_setup()")
            return False

        success = self.preprocessor.run_preprocessing_pipeline(input_directory)
        self.workflow_state["audio_processed"] = success

        if success:
            stats = self.preprocessor.get_preprocessing_stats()
            logger.info(f"\n✓ Preprocessing Statistics:")
            logger.info(f"  Segments: {stats.get('segments', 0)}")
            logger.info(f"  Total Duration: {stats.get('total_duration', 0) / 60:.1f} minutes")

        return success

    def run_phase_4_model_training(
        self,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        learning_rate: Optional[float] = None,
    ) -> bool:
        """Phase 4: Train voice model"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 4: MODEL TRAINING")
        logger.info("=" * 80)

        if not self.workflow_state["audio_processed"]:
            logger.error("⚠️  Phase 3 (Audio Preprocessing) must run first")
            logger.info("Run: orchestrator.run_phase_3_audio_preprocessing(input_dir)")
            return False

        # Generate training config
        if not self.trainer.generate_training_config(epochs, batch_size, learning_rate):
            return False

        # Estimate training time
        stats = self.preprocessor.get_preprocessing_stats()
        time_estimate = self.trainer.estimate_training_time(stats.get("segments", 1))

        logger.info(f"\n⏱️  Estimated Training Time: {int(time_estimate.get('estimated_hours', 0))}h {int(time_estimate.get('estimated_minutes', 0))}m")

        # Start training
        success = self.trainer.start_training()
        self.workflow_state["model_trained"] = success
        self.workflow_state["ready_for_inference"] = success

        return success

    def run_phase_5_voice_inference(
        self,
        input_audio: str,
        output_audio: str,
        model_path: Optional[str] = None,
        pitch_shift: int = 0,
        f0_method: str = "crepe",
    ) -> bool:
        """Phase 5: Convert voice with trained model"""
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 5: VOICE INFERENCE")
        logger.info("=" * 80)

        if not self.workflow_state["ready_for_inference"]:
            logger.error("⚠️  A trained model is required for inference")
            logger.info("Run phases 1-4 to train a model first")
            return False

        # Initialize inference
        self.inference = VoiceInference(self.config, model_path)

        # Perform conversion
        success = self.inference.convert_voice(
            input_audio,
            output_audio,
            pitch_shift=pitch_shift,
            f0_method=f0_method,
        )

        if success:
            self.inference.print_fl_studio_guide()

        return success

    def batch_inference(
        self,
        input_directory: str,
        output_directory: str,
        model_path: Optional[str] = None,
        pitch_shift: int = 0,
    ) -> bool:
        """Batch convert multiple audio files"""
        logger.info("\n" + "=" * 80)
        logger.info("BATCH INFERENCE")
        logger.info("=" * 80)

        if not self.workflow_state["ready_for_inference"]:
            logger.error("⚠️  A trained model is required for inference")
            return False

        # Initialize inference
        self.inference = VoiceInference(self.config, model_path)

        # Perform batch conversion
        return self.inference.batch_convert(
            input_directory,
            output_directory,
            pitch_shift=pitch_shift,
        )

    def check_status(self) -> Dict:
        """Check current workflow status"""
        logger.info("\n" + "=" * 80)
        logger.info("WORKFLOW STATUS")
        logger.info("=" * 80)

        status_symbols = {"True": "✅", "False": "❌"}

        for phase, completed in self.workflow_state.items():
            symbol = status_symbols.get(str(completed), "⏳")
            logger.info(f"  {symbol} {phase}: {'Done' if completed else 'Pending'}")

        # Check for available resources
        if self.workflow_state["env_detected"]:
            report = self.detector.get_report()
            device = report.get("device_recommendation")
            logger.info(f"\n  Device: {device}")

        return self.workflow_state

    def get_complete_report(self) -> Dict:
        """Get comprehensive workflow report"""
        return {
            "workflow_state": self.workflow_state,
            "environment": self.detector.get_report() if self.workflow_state["env_detected"] else {},
            "preprocessing": (
                self.preprocessor.get_preprocessing_stats()
                if self.workflow_state["audio_processed"]
                else {}
            ),
            "training": (
                self.trainer.get_training_report()
                if self.workflow_state["model_trained"]
                else {}
            ),
            "inference": (
                self.inference.get_inference_report()
                if self.inference
                else {}
            ),
        }

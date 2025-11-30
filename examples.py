"""
Example usage of Voice Cloner
"""
from src.config.config import Config
from src.orchestrator import VoiceClonerOrchestrator
from src.utils.logger import logger


def example_1_detect_environment():
    """Example 1: Detect system environment"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 1: Detect Environment")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()
    success = orchestrator.run_phase_1_environment_detection()

    if success:
        report = orchestrator.detector.get_report()
        logger.info(f"\nEnvironment Report:")
        logger.info(f"  Device: {report['device_recommendation']}")
        logger.info(f"  Warnings: {len(report['warnings'])}")
        logger.info(f"  Errors: {len(report['errors'])}")


def example_2_setup_environment():
    """Example 2: Setup complete environment"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 2: Setup Environment")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    # First detect
    if not orchestrator.run_phase_1_environment_detection():
        logger.error("Detection failed")
        return False

    # Then setup
    if not orchestrator.run_phase_2_environment_setup():
        logger.error("Setup failed")
        return False

    logger.info("\n✅ Environment setup complete!")
    return True


def example_3_preprocess_audio():
    """Example 3: Preprocess audio files"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 3: Preprocess Audio")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    # Input directory with WAV files
    input_dir = "./data/input"

    if not orchestrator.run_phase_3_audio_preprocessing(input_dir):
        logger.error("Preprocessing failed")
        return False

    stats = orchestrator.preprocessor.get_preprocessing_stats()
    logger.info(f"\n✅ Preprocessing complete!")
    logger.info(f"  Segments: {stats.get('segments', 0)}")
    logger.info(f"  Duration: {stats.get('total_duration', 0) / 60:.1f} minutes")

    return True


def example_4_train_model():
    """Example 4: Train voice model"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 4: Train Model")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    # Train with custom parameters
    if not orchestrator.run_phase_4_model_training(
        epochs=50,  # Reduced for testing
        batch_size=16,
        learning_rate=0.0001,
    ):
        logger.error("Training failed")
        return False

    logger.info("\n✅ Training started!")

    # Check training status
    progress = orchestrator.trainer.check_training_progress()
    logger.info(f"\nTraining Status:")
    logger.info(f"  Status: {progress.get('status')}")
    logger.info(f"  Checkpoints: {progress.get('checkpoints', 0)}")

    return True


def example_5_voice_inference():
    """Example 5: Convert voice"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 5: Voice Inference")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    input_audio = "./data/input_vocals.wav"
    output_audio = "./data/output_vocals.wav"

    # Single conversion
    if not orchestrator.run_phase_5_voice_inference(
        input_audio,
        output_audio,
        pitch_shift=0,
        f0_method="crepe",
    ):
        logger.error("Inference failed")
        return False

    logger.info("\n✅ Voice conversion complete!")
    logger.info(f"Output saved to: {output_audio}")

    return True


def example_6_batch_inference():
    """Example 6: Batch convert multiple files"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 6: Batch Inference")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    input_dir = "./data/input_vocals"
    output_dir = "./data/output_vocals"

    if not orchestrator.batch_inference(
        input_dir,
        output_dir,
        pitch_shift=2,
    ):
        logger.error("Batch inference failed")
        return False

    logger.info("\n✅ Batch conversion complete!")

    return True


def example_7_workflow_status():
    """Example 7: Check workflow status"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 7: Workflow Status")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    # Check status
    status = orchestrator.check_status()

    # Get full report
    report = orchestrator.get_complete_report()
    logger.info(f"\nFull Report Sections:")
    logger.info(f"  - Workflow State: {list(report['workflow_state'].keys())}")
    logger.info(f"  - Environment: {len(report.get('environment', {}))} items")
    logger.info(f"  - Preprocessing: {len(report.get('preprocessing', {}))} items")
    logger.info(f"  - Training: {len(report.get('training', {}))} items")


def example_8_complete_workflow():
    """Example 8: Complete workflow from start to finish"""
    logger.info("\n" + "=" * 60)
    logger.info("EXAMPLE 8: Complete Workflow")
    logger.info("=" * 60)

    orchestrator = VoiceClonerOrchestrator()

    steps = [
        ("Environment Detection", lambda: orchestrator.run_phase_1_environment_detection()),
        ("Environment Setup", lambda: orchestrator.run_phase_2_environment_setup()),
        ("Audio Preprocessing", lambda: orchestrator.run_phase_3_audio_preprocessing("./data/input")),
        ("Model Training", lambda: orchestrator.run_phase_4_model_training(epochs=100)),
    ]

    for step_name, step_func in steps:
        logger.info(f"\n▶️  {step_name}...")
        try:
            if not step_func():
                logger.error(f"✗ {step_name} failed")
                return False
            logger.info(f"✓ {step_name} completed")
        except KeyboardInterrupt:
            logger.warning("Workflow interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Error in {step_name}: {e}")
            return False

    logger.info("\n" + "=" * 60)
    logger.info("✅ COMPLETE WORKFLOW FINISHED!")
    logger.info("=" * 60)

    return True


if __name__ == "__main__":
    logger.info("Voice Cloner - Usage Examples")

    # Uncomment the example you want to run:

    # example_1_detect_environment()
    # example_2_setup_environment()
    # example_3_preprocess_audio()
    # example_4_train_model()
    # example_5_voice_inference()
    # example_6_batch_inference()
    # example_7_workflow_status()
    # example_8_complete_workflow()

    logger.info("\nTo run an example, uncomment it in __main__ section")

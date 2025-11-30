"""
Main CLI interface for Voice Cloner
"""
import sys
import click
from pathlib import Path
from typing import Optional
from src.config.config import Config
from src.orchestrator import VoiceClonerOrchestrator
from src.utils.logger import logger


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    🎤 Voice Cloner - AI Agent for SO-VITS-SVC Voice Cloning Setup for FL Studio

    An intelligent automation tool that guides you through the complete process of
    cloning your voice and creating a personalized AI singing voice model.

    For detailed help: voice-cloner COMMAND --help
    """
    pass


@cli.command()
def init():
    """Initialize a new Voice Cloner project"""
    logger.info("=" * 60)
    logger.info("Voice Cloner Project Initialization")
    logger.info("=" * 60)

    try:
        config = Config()

        logger.info("\n📁 Creating project directories...")
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        config.MODELS_DIR.mkdir(parents=True, exist_ok=True)

        logger.info("✓ Project initialized successfully")
        logger.info(f"\nProject paths:")
        logger.info(f"  Data: {config.DATA_DIR}")
        logger.info(f"  Output: {config.OUTPUT_DIR}")
        logger.info(f"  Models: {config.MODELS_DIR}")

    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)


@cli.command()
def detect():
    """Detect system environment and capabilities"""
    try:
        orchestrator = VoiceClonerOrchestrator()
        success = orchestrator.run_phase_1_environment_detection()

        if success:
            logger.info("\n✅ Environment detection passed!")
        else:
            logger.error("\n❌ Environment detection failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Detection error: {e}")
        sys.exit(1)


@cli.command()
def setup():
    """Set up environment and install dependencies"""
    try:
        orchestrator = VoiceClonerOrchestrator()

        # Check environment first
        logger.info("Checking system requirements...")
        if not orchestrator.run_phase_1_environment_detection():
            logger.error("Environment detection failed")
            sys.exit(1)

        # Run setup
        if not orchestrator.run_phase_2_environment_setup():
            logger.error("Environment setup failed")
            sys.exit(1)

        logger.info("\n✅ Environment setup completed!")

    except Exception as e:
        logger.error(f"Setup error: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_directory", type=click.Path(exists=True))
def preprocess(input_directory):
    """Preprocess audio files for training"""
    try:
        orchestrator = VoiceClonerOrchestrator()

        logger.info(f"Preprocessing audio from: {input_directory}")

        if not orchestrator.run_phase_3_audio_preprocessing(input_directory):
            logger.error("Audio preprocessing failed")
            sys.exit(1)

        logger.info("\n✅ Audio preprocessing completed!")

    except Exception as e:
        logger.error(f"Preprocessing error: {e}")
        sys.exit(1)


@cli.command()
@click.option("--epochs", default=100, help="Number of training epochs")
@click.option("--batch-size", default=16, help="Batch size for training")
@click.option("--learning-rate", default=0.0001, help="Learning rate")
def train(epochs, batch_size, learning_rate):
    """Train voice model"""
    try:
        orchestrator = VoiceClonerOrchestrator()

        logger.info("Starting model training...")

        if not orchestrator.run_phase_4_model_training(epochs, batch_size, learning_rate):
            logger.error("Model training failed")
            sys.exit(1)

        logger.info("\n✅ Model training setup completed!")

    except Exception as e:
        logger.error(f"Training error: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_audio", type=click.Path(exists=True))
@click.argument("output_audio", type=click.Path())
@click.option("--model", default=None, help="Path to trained model")
@click.option("--pitch-shift", default=0, help="Pitch shift in semitones")
@click.option("--f0-method", default="crepe", help="F0 prediction method")
def infer(input_audio, output_audio, model, pitch_shift, f0_method):
    """Convert voice using trained model"""
    try:
        orchestrator = VoiceClonerOrchestrator()

        logger.info("Starting voice inference...")

        if not orchestrator.run_phase_5_voice_inference(
            input_audio,
            output_audio,
            model_path=model,
            pitch_shift=int(pitch_shift),
            f0_method=f0_method,
        ):
            logger.error("Voice inference failed")
            sys.exit(1)

        logger.info("\n✅ Voice inference completed!")

    except Exception as e:
        logger.error(f"Inference error: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_directory", type=click.Path(exists=True))
@click.argument("output_directory", type=click.Path())
@click.option("--model", default=None, help="Path to trained model")
@click.option("--pitch-shift", default=0, help="Pitch shift in semitones")
def batch_infer(input_directory, output_directory, model, pitch_shift):
    """Batch convert multiple audio files"""
    try:
        orchestrator = VoiceClonerOrchestrator()

        logger.info("Starting batch voice inference...")

        if not orchestrator.batch_inference(
            input_directory,
            output_directory,
            model_path=model,
            pitch_shift=int(pitch_shift),
        ):
            logger.error("Batch inference failed")
            sys.exit(1)

        logger.info("\n✅ Batch inference completed!")

    except Exception as e:
        logger.error(f"Batch inference error: {e}")
        sys.exit(1)


@cli.command()
def status():
    """Check workflow status"""
    try:
        orchestrator = VoiceClonerOrchestrator()
        orchestrator.check_status()

    except Exception as e:
        logger.error(f"Status check error: {e}")
        sys.exit(1)


@cli.command()
def report():
    """Generate comprehensive workflow report"""
    try:
        orchestrator = VoiceClonerOrchestrator()
        report = orchestrator.get_complete_report()

        logger.info("=" * 60)
        logger.info("COMPREHENSIVE WORKFLOW REPORT")
        logger.info("=" * 60)

        import json
        logger.info(json.dumps(report, indent=2, default=str))

    except Exception as e:
        logger.error(f"Report generation error: {e}")
        sys.exit(1)


@cli.command()
def quickstart():
    """Run complete voice cloning workflow from start to finish"""
    logger.info("=" * 80)
    logger.info("🎤 VOICE CLONER - QUICKSTART")
    logger.info("=" * 80)

    try:
        # Get user input
        input_dir = click.prompt("Enter path to your vocal recordings", type=click.Path(exists=True))

        click.confirm(
            "\nThis will run the complete setup process. Continue?",
            abort=True,
        )

        orchestrator = VoiceClonerOrchestrator()

        # Phase 1
        logger.info("\n[PHASE 1/4] Detecting environment...")
        if not orchestrator.run_phase_1_environment_detection():
            logger.error("Environment detection failed")
            return

        # Phase 2
        logger.info("\n[PHASE 2/4] Setting up environment...")
        if not orchestrator.run_phase_2_environment_setup():
            logger.error("Environment setup failed")
            return

        # Phase 3
        logger.info("\n[PHASE 3/4] Preprocessing audio...")
        if not orchestrator.run_phase_3_audio_preprocessing(input_dir):
            logger.error("Audio preprocessing failed")
            return

        # Phase 4
        logger.info("\n[PHASE 4/4] Training model...")
        epochs = click.prompt("Number of training epochs", default=100, type=int)

        if not orchestrator.run_phase_4_model_training(epochs=epochs):
            logger.error("Model training failed")
            return

        logger.info("\n" + "=" * 80)
        logger.info("✅ QUICKSTART WORKFLOW COMPLETED!")
        logger.info("=" * 80)
        logger.info("\nNext steps:")
        logger.info("1. Wait for training to complete")
        logger.info("2. Use 'voice-cloner infer' to convert voice")
        logger.info("3. Import output WAV into FL Studio")

    except click.Abort:
        logger.info("\nQuickstart cancelled")
    except Exception as e:
        logger.error(f"Quickstart error: {e}")
        sys.exit(1)


@cli.command()
def guide():
    """Show FL Studio integration guide"""
    logger.info("=" * 80)
    logger.info("FL STUDIO INTEGRATION GUIDE")
    logger.info("=" * 80)

    logger.info("\n📋 PREPARATION:")
    logger.info("  1. Record 15-30 minutes of your clean vocal singing")
    logger.info("  2. Place WAV files in ./data/input directory")
    logger.info("  3. Run: voice-cloner quickstart")

    logger.info("\n🎓 TRAINING:")
    logger.info("  1. Training typically takes 2-12 hours")
    logger.info("  2. Model checkpoints are saved every 10 epochs")
    logger.info("  3. You can resume from checkpoints if interrupted")

    logger.info("\n🎵 VOICE CONVERSION:")
    logger.info("  1. Prepare input singing (any voice, any MIDI vocal)")
    logger.info("  2. Run: voice-cloner infer input.wav output.wav")
    logger.info("  3. Adjust --pitch-shift if needed (+/- semitones)")

    logger.info("\n🎚️ FL STUDIO WORKFLOW:")
    logger.info("  1. Create new audio track in FL Studio")
    logger.info("  2. Open Edison plugin on the track")
    logger.info("  3. Drag converted WAV into Edison window")
    logger.info("  4. Use Edison tools to edit timing/pitch if needed")
    logger.info("  5. Export back to playlist")
    logger.info("  6. Layer with other instruments")

    logger.info("\n💡 TIPS:")
    logger.info("  - Use 44.1kHz sample rate for compatibility")
    logger.info("  - Normalize audio to -6dB to prevent clipping")
    logger.info("  - Start with small pitch shifts to test model quality")
    logger.info("  - Experiment with F0 methods (crepe, dio, harvest)")

    logger.info("\n" + "=" * 80)


if __name__ == "__main__":
    cli()

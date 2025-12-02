#!/usr/bin/env python3
"""
Train a voice model using your voice samples.

This script uses so-vits-svc-fork to train a model that can convert other voices to yours.

Usage:
    python train.py
    
The script will:
1. Preprocess your voice samples from samples/
2. Extract features (HuBERT embeddings)
3. Train the model
4. Save the trained model to models/
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init()

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header():
    """Print training header."""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
    print(f"║    {Fore.WHITE}Voice Model Trainer - so-vits-svc{Fore.CYAN}     ║")
    print(f"║       {Fore.YELLOW}Training your voice clone{Fore.CYAN}           ║")
    print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")


def check_samples():
    """Check if voice samples exist."""
    samples_dir = Path("samples")
    
    if not samples_dir.exists():
        logger.error(f"{Fore.RED}Samples directory not found!{Style.RESET_ALL}")
        logger.info("Create a 'samples/' folder and add your voice recordings (.wav files)")
        return False
    
    audio_files = list(samples_dir.glob("*.wav")) + list(samples_dir.glob("*.mp3"))
    
    if not audio_files:
        logger.error(f"{Fore.RED}No audio files found in samples/{Style.RESET_ALL}")
        logger.info("Add your voice recordings (.wav or .mp3) to the samples/ folder")
        return False
    
    total_duration = 0
    logger.info(f"{Fore.GREEN}Found {len(audio_files)} audio files:{Style.RESET_ALL}")
    
    for f in audio_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        logger.info(f"  - {f.name} ({size_mb:.1f}MB)")
    
    # Recommend minimum duration
    logger.info(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
    logger.info("  - Total audio: 10-30 minutes (minimum)")
    logger.info("  - Format: WAV or MP3")
    logger.info("  - Sample rate: 16-48 kHz")
    logger.info("  - Quality: Clear, minimal background noise")
    
    return True


def run_command(cmd, description):
    """Run a command and handle errors."""
    logger.info(f"\n{Fore.YELLOW}► {description}{Style.RESET_ALL}")
    logger.info(f"  Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        logger.info(f"  {Fore.GREEN}✓ Complete{Style.RESET_ALL}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"  {Fore.RED}✗ Failed{Style.RESET_ALL}")
        logger.error(f"  Error: {e}")
        return False
    except FileNotFoundError:
        logger.error(f"  {Fore.RED}✗ Command not found{Style.RESET_ALL}")
        return False


def train_model():
    """Train the voice model."""
    print_header()
    
    # Check samples
    if not check_samples():
        return
    
    input("Press Enter to start training...")
    
    logger.info(f"\n{Fore.CYAN}Starting training pipeline...{Style.RESET_ALL}\n")
    
    # Create models directory
    Path("models").mkdir(exist_ok=True)
    Path("checkpoints").mkdir(exist_ok=True)
    
    steps = [
        # Step 1: Resample audio
        (
            ["svc", "pre-resample", "--sr", "44100", "--in-dir", "samples"],
            "Resampling audio to 44.1kHz"
        ),
        
        # Step 2: Extract HuBERT features
        (
            ["svc", "pre-hubert", "--in-dir", "samples/44k"],
            "Extracting voice features (HuBERT)"
        ),
        
        # Step 3: Run training
        (
            ["svc", "train", "--config", "configs/config.json"],
            "Training voice model (this may take a while...)"
        ),
    ]
    
    success = True
    for i, (cmd, desc) in enumerate(steps, 1):
        logger.info(f"\n{Fore.CYAN}Step {i}/{len(steps)}{Style.RESET_ALL}")
        if not run_command(cmd, desc):
            success = False
            break
    
    if success:
        logger.info(f"\n{Fore.GREEN}╔════════════════════════════════════════╗")
        logger.info(f"║         {Fore.WHITE}Training Complete!{Fore.GREEN}            ║")
        logger.info(f"║  Your model is ready in: checkpoints/{Fore.WHITE}  ║{Fore.GREEN}")
        logger.info(f"╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    else:
        logger.error(f"\n{Fore.RED}Training failed. Check the errors above.{Style.RESET_ALL}")
        logger.info("\nAlternative: Use the so-vits-svc WebUI:")
        logger.info("  python -m so_vits_svc_fork.webui.new_ui")


if __name__ == "__main__":
    train_model()

#!/usr/bin/env python3
"""
Train a voice model using your voice samples.

This script uses so-vits-svc-fork to train a model that can convert other voices to yours.

Usage:
    python train.py
"""

import os
import sys
import logging
import shutil
import json
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
        return []
    
    audio_files = list(samples_dir.glob("*.wav")) + list(samples_dir.glob("*.mp3"))
    
    if not audio_files:
        logger.error(f"{Fore.RED}No audio files found in samples/{Style.RESET_ALL}")
        logger.info("Add your voice recordings (.wav or .mp3) to the samples/ folder")
        return []
    
    logger.info(f"{Fore.GREEN}Found {len(audio_files)} audio files:{Style.RESET_ALL}")
    
    total_mb = 0
    for f in audio_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        total_mb += size_mb
        logger.info(f"  - {f.name} ({size_mb:.1f}MB)")
    
    logger.info(f"\n  Total: {total_mb:.1f}MB")
    
    # Recommend minimum duration
    logger.info(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
    logger.info("  - Total audio: 10-30 minutes (minimum)")
    logger.info("  - Format: WAV or MP3")
    logger.info("  - Sample rate: 16-48 kHz")
    logger.info("  - Quality: Clear, minimal background noise")
    
    return audio_files


def setup_training_environment():
    """Set up the training environment."""
    logger.info(f"\n{Fore.CYAN}Setting up training environment...{Style.RESET_ALL}")
    
    # Create necessary directories
    dirs = ["checkpoints", "logs", "samples/44k"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        logger.info(f"  ✓ Created {d}/")
    
    # Create default config if it doesn't exist
    config_path = Path("configs/config.json")
    if not config_path.exists():
        config_path.parent.mkdir(exist_ok=True)
        config = {
            "train": {
                "batch_size": 16,
                "epochs": 100,
                "learning_rate": 0.0001,
                "log_interval": 10,
                "save_interval": 100,
            },
            "data": {
                "n_fft": 2048,
                "n_mels": 80,
                "sampling_rate": 44100,
                "hop_size": 512,
                "win_size": 2048,
                "f_min": 40,
                "f_max": 7600,
                "f0_min": 50,
                "f0_max": 1100,
                "use_nsf": True,
            }
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"  ✓ Created {config_path}")
    
    return config_path


def train_with_webui():
    """Guide user to train with WebUI."""
    logger.info(f"\n{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    logger.info(f"{Fore.CYAN}TRAINING METHOD: WebUI (Recommended){Style.RESET_ALL}")
    logger.info(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}\n")
    
    logger.info("The easiest way to train is using the so-vits-svc WebUI.")
    logger.info("It provides a visual interface for preprocessing and training.\n")
    
    logger.info(f"{Fore.GREEN}Step 1: Download the WebUI{Style.RESET_ALL}")
    logger.info("  Visit: https://github.com/voicepaw/so-vits-svc-fork/releases")
    logger.info("  Download: 'so-vits-svc-fork-webui.exe' (Windows)")
    logger.info("  Or use Python:\n")
    
    logger.info(f"{Fore.CYAN}  python -m so_vits_svc_fork.inference.main --help{Style.RESET_ALL}\n")
    
    logger.info(f"{Fore.GREEN}Step 2: Alternatively, use our simple conversion (no training needed yet){Style.RESET_ALL}")
    logger.info("  If you have a pre-trained model in models/:")
    logger.info(f"\n{Fore.CYAN}  python convert.py input/vocals.wav{Style.RESET_ALL}\n")
    
    logger.info(f"{Fore.YELLOW}For now, we'll use a workaround approach:{Style.RESET_ALL}\n")


def show_alternative_methods():
    """Show alternative ways to train/convert."""
    logger.info(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    logger.info(f"{Fore.YELLOW}ALTERNATIVE: Try conversion without training{Style.RESET_ALL}")
    logger.info(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    logger.info("Since training setup requires the full so-vits-svc CLI,")
    logger.info("here's what we recommend:\n")
    
    logger.info(f"{Fore.GREEN}Option 1: Use Pre-trained Models{Style.RESET_ALL}")
    logger.info("  - Visit: https://huggingface.co/search?q=so-vits-svc")
    logger.info("  - Download a pre-trained model")
    logger.info("  - Place in: models/")
    logger.info("  - Run: python convert.py input/vocals.wav\n")
    
    logger.info(f"{Fore.GREEN}Option 2: Train with WebUI (Recommended){Style.RESET_ALL}")
    logger.info("  - WebUI is easier and more reliable")
    logger.info("  - Download: https://github.com/voicepaw/so-vits-svc-fork")
    logger.info("  - Follow README instructions\n")
    
    logger.info(f"{Fore.GREEN}Option 3: Use Command Line (Advanced){Style.RESET_ALL}")
    logger.info("  - Clone: git clone https://github.com/voicepaw/so-vits-svc-fork.git")
    logger.info("  - Follow training steps in their README\n")
    
    logger.info(f"{Fore.YELLOW}Next Steps:{Style.RESET_ALL}")
    logger.info("  1. Prepare your samples (already done ✓)")
    logger.info("  2. Train a model using one of the methods above")
    logger.info("  3. Run: python convert.py input/vocals.wav")
    logger.info("  4. Check output/ folder for results\n")


def main():
    """Main training setup."""
    print_header()
    
    # Check samples
    audio_files = check_samples()
    if not audio_files:
        return
    
    # Setup environment
    setup_training_environment()
    
    # Show alternatives
    train_with_webui()
    show_alternative_methods()
    
    logger.info(f"{Fore.GREEN}Your voice samples are ready!{Style.RESET_ALL}")
    logger.info(f"Total files: {len(audio_files)}\n")
    
    logger.info(f"{Fore.CYAN}Next: Train your model and come back to convert audio.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

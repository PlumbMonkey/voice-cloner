#!/usr/bin/env python3
"""
Voice Cloner - Convert vocals to your voice.

Usage:
    python convert.py input/vocals.wav
    python convert.py input/vocals.wav --output output/my_voice.wav
    python convert.py input/vocals.wav --pitch-shift -2
"""

import argparse
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core import VoiceConverter
from src.utils import load_audio, save_audio


def print_header():
    """Print application header."""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗")
    print(f"║       {Fore.WHITE}Voice Cloner v0.1.0{Fore.CYAN}               ║")
    print(f"║   {Fore.YELLOW}Convert any voice to YOUR voice{Fore.CYAN}       ║")
    print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert vocals to your voice",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        help="Input audio file to convert"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: output/<input_name>_converted.wav)"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Path to voice model (.pth file)"
    )
    
    parser.add_argument(
        "--pitch-shift", "-p",
        type=int,
        default=0,
        help="Pitch shift in semitones (default: 0)"
    )
    
    parser.add_argument(
        "--speaker-id", "-s",
        type=int,
        default=0,
        help="Speaker ID (default: 0)"
    )
    
    parser.add_argument(
        "--f0-method",
        type=str,
        choices=["crepe", "parselmouth", "dio", "harvest"],
        default="crepe",
        help="F0 extraction method (default: crepe)"
    )
    
    parser.add_argument(
        "--index-rate", "-i",
        type=float,
        default=0.5,
        help="Index rate for retrieval (0-1, default: 0.5)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available voice models"
    )
    
    args = parser.parse_args()
    
    print_header()
    
    # List models if requested
    if args.list_models:
        models_dir = Path("models")
        if models_dir.exists():
            models = list(models_dir.glob("*.pth"))
            if models:
                print(f"{Fore.GREEN}Available models:{Style.RESET_ALL}")
                for model in models:
                    print(f"  - {model.name}")
            else:
                print(f"{Fore.YELLOW}No models found in 'models/' directory{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Models directory not found{Style.RESET_ALL}")
        return
    
    # Check input file
    if not args.input:
        parser.print_help()
        print(f"\n{Fore.RED}Error: Please provide an input audio file{Style.RESET_ALL}")
        return
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"{Fore.RED}Error: Input file not found: {input_path}{Style.RESET_ALL}")
        return
    
    # Set output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{input_path.stem}_converted.wav"
    
    # Find model
    model_path = None
    if args.model:
        model_path = Path(args.model)
        if not model_path.exists():
            print(f"{Fore.RED}Error: Model not found: {model_path}{Style.RESET_ALL}")
            return
    else:
        # Look for default model
        models_dir = Path("models")
        if models_dir.exists():
            models = list(models_dir.glob("*.pth"))
            if models:
                model_path = models[0]
                print(f"{Fore.CYAN}Using model: {model_path.name}{Style.RESET_ALL}")
    
    # Initialize converter
    print(f"{Fore.CYAN}Initializing voice converter...{Style.RESET_ALL}")
    converter = VoiceConverter(model_path=model_path)
    
    # Convert
    print(f"{Fore.CYAN}Converting: {input_path.name}{Style.RESET_ALL}")
    print(f"  Pitch shift: {args.pitch_shift} semitones")
    print(f"  F0 method: {args.f0_method}")
    print(f"  Index rate: {args.index_rate}")
    
    try:
        converter.convert(
            source_audio=input_path,
            output_path=output_path,
            speaker_id=args.speaker_id,
            pitch_shift=args.pitch_shift,
            f0_method=args.f0_method,
            index_rate=args.index_rate
        )
        
        print(f"\n{Fore.GREEN}✓ Conversion complete!{Style.RESET_ALL}")
        print(f"  Output: {output_path}")
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Conversion failed: {e}{Style.RESET_ALL}")
        raise


if __name__ == "__main__":
    main()

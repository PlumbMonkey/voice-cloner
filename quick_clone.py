#!/usr/bin/env python3
"""
Quick Voice Cloning Helper
Simple tool to clone any voice using your speaker profile
"""

import sys
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.voice_inference import VoiceInference
from src.config.config import Config

def main():
    parser = argparse.ArgumentParser(
        description="Clone a voice using your speaker profile",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clone Katie with -7 semitone lower pitch
  python quick_clone.py katie.wav -7
  
  # Clone with no pitch shift
  python quick_clone.py katie.wav 0
  
  # Clone with +5 semitone higher pitch
  python quick_clone.py katie.wav 5
"""
    )
    
    parser.add_argument(
        "input_audio",
        help="Path to input audio file (WAV, MP3, etc.)"
    )
    
    parser.add_argument(
        "pitch_shift",
        type=int,
        nargs="?",
        default=0,
        help="Pitch shift in semitones (default: 0)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: auto-generated)"
    )
    
    parser.add_argument(
        "-f", "--f0-method",
        default="crepe",
        choices=["crepe", "dio", "harvest"],
        help="F0 detection method (default: crepe)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input_audio)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)
    
    # Auto-generate output path if not provided
    if args.output:
        output_path = Path(args.output)
    else:
        stem = input_path.stem
        suffix = f"_{args.pitch_shift:+d}st" if args.pitch_shift != 0 else "_cloned"
        output_path = input_path.parent / f"{stem}{suffix}.wav"
    
    print("\n" + "=" * 70)
    print("QUICK VOICE CLONING")
    print("=" * 70)
    
    print(f"\n[INPUT]  {input_path.name}")
    print(f"[PITCH]  {args.pitch_shift:+d} semitones")
    print(f"[METHOD] {args.f0_method}")
    print(f"[OUTPUT] {output_path.name}")
    
    # Initialize and convert
    print("\n[PROCESSING] Cloning voice...")
    config = Config()
    inference = VoiceInference(config)
    
    if not inference.use_speaker_profile:
        print("[WARNING] Speaker profile not available!")
        print("[WARNING] Will use basic simulation mode instead")
    
    success = inference.convert_voice(
        str(input_path),
        str(output_path),
        pitch_shift=args.pitch_shift,
        f0_method=args.f0_method
    )
    
    if success:
        file_size = output_path.stat().st_size / 1024
        print(f"\n[SUCCESS] Voice cloned!")
        print(f"[FILE]   {output_path.name} ({file_size:.0f} KB)")
        print(f"[READY]  Use in FL Studio via Edison plugin")
    else:
        print(f"\n[ERROR] Voice cloning failed!")
        sys.exit(1)
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()

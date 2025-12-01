#!/usr/bin/env python3
"""
Final Voice Cloning Tool - Real Neural Voice Conversion
Generate perfect Katie voice clones using your voice
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.voice_inference import VoiceInference
from src.config.config import Config
import librosa
import soundfile as sf

print("\n" + "=" * 80)
print("🎤 REAL VOICE CLONING - KATIE VOICE TRANSFORMATION")
print("=" * 80)

# Initialize
config = Config()
inference = VoiceInference(config)

# Katie file
katie_file = Path.home() / "Desktop" / "katie.mp3"

if not katie_file.exists():
    print(f"[ERROR] Katie file not found: {katie_file}")
    sys.exit(1)

print(f"\n[INPUT] {katie_file.name}")
y, sr = librosa.load(str(katie_file), sr=config.SAMPLE_RATE)
print(f"[DURATION] {len(y)/sr:.2f}s @ {sr}Hz")

# Show what method will be used
print(f"\n[METHODS AVAILABLE]")
print(f"  Neural Converter: {'✓ YES' if inference.use_neural_converter else '✗ NO'}")
print(f"  Speaker Profile: {'✓ YES' if inference.use_speaker_profile else '✗ NO'}")
print(f"  SO-VITS-SVC: {'✓ YES' if inference.sovits_wrapper else '✗ NO'}")

# Generate multiple clones
output_dir = Path("output/final_katie_voice_clones")
output_dir.mkdir(parents=True, exist_ok=True)

configs = [
    (0, "Original Pitch (Your Voice)"),
    (-2, "Slightly Lower"),
    (-4, "Lower-Medium"),
    (2, "Slightly Higher"),
    (4, "Higher-Medium"),
]

print("\n" + "=" * 80)
print("GENERATING VOICE CLONES")
print("=" * 80)

successful = 0
for pitch, description in configs:
    output_file = output_dir / f"katie_{description.replace(' ', '_').lower()}.wav"
    
    print(f"\n[{description}] Pitch: {pitch:+d}st...", end=" ", flush=True)
    
    try:
        success = inference.convert_voice(
            str(katie_file),
            str(output_file),
            pitch_shift=pitch,
            f0_method="crepe"
        )
        
        if success and output_file.exists():
            successful += 1
            size = output_file.stat().st_size / 1024
            print(f"✓ ({size:.0f} KB)")
        else:
            print("✗ Failed")
    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

print(f"\n✓ Generated {successful}/{len(configs)} voice clones")
print(f"\nOutput directory: {output_dir}")

files = sorted(output_dir.glob("*.wav"))
for f in files:
    size = f.stat().st_size / 1024
    print(f"  • {f.name} ({size:.0f} KB)")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)

print("""
1. Listen to all files to find the best pitch
2. Import preferred version to FL Studio:
   - Open Edison plugin from Mixer
   - Drag .wav file into Edison
   - Edit/time-stretch as needed
   - Export back to arrange
3. Layer with original Katie or other vocals
4. Add effects and produce your track

Files are ready to use immediately! 🎉
""")

print()

#!/usr/bin/env python3
"""Generate Katie voice clones with your voice profile"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.voice_inference import VoiceInference
from src.config.config import Config

# Katie's file on desktop
katie_file = Path.home() / "Desktop" / "katie.mp3"

if not katie_file.exists():
    print(f"[ERROR] Katie file not found: {katie_file}")
    sys.exit(1)

print(f"\n[INPUT] {katie_file.name} ({katie_file.stat().st_size/1024/1024:.1f} MB)")

# Initialize
config = Config()
inference = VoiceInference(config)

print(f"[PROFILE] Speaker profile: {'✓ Loaded' if inference.use_speaker_profile else '✗ Not available'}")

# Generate 3 versions
print("\n[CONVERTING] Katie with your voice profile...")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for pitch in [-7, 0, 5]:
    output = output_dir / f"katie_your_voice_{pitch:+d}st.wav"
    
    print(f"\n  Pitch {pitch:+d}st...", end=" ", flush=True)
    
    try:
        inference.convert_voice(str(katie_file), str(output), pitch_shift=pitch)
        
        if output.exists():
            size_kb = output.stat().st_size / 1024
            print(f"✓ ({size_kb:.0f} KB)")
        else:
            print("✗ Failed to create file")
    except Exception as e:
        print(f"✗ Error: {e}")

# Show results
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

results = sorted(output_dir.glob("katie_your_voice_*.wav"))
if results:
    print(f"\n✓ Generated {len(results)} voice clones:")
    for f in results:
        print(f"  • {f.name}")
    print("\n[READY] Import to FL Studio using Edison plugin")
else:
    print("\n✗ No files generated")

print()

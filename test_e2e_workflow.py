#!/usr/bin/env python3
"""
End-to-end workflow test for Voice Cloner with SO-VITS-SVC integration
"""
import sys
from pathlib import Path
import shutil

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config.config import default_config
from src.modules.voice_inference import VoiceInference
from src.utils.logger import logger

def test_e2e_workflow():
    """Test complete end-to-end voice conversion workflow"""
    logger.info("=" * 70)
    logger.info("END-TO-END VOICE CONVERSION WORKFLOW TEST")
    logger.info("=" * 70)
    
    # Step 1: Find checkpoint
    logger.info("\n[STEP 1] Finding trained model checkpoint...")
    checkpoints_dir = project_root / "checkpoints"
    checkpoint_files = sorted(checkpoints_dir.glob("*.pth"), reverse=True)
    
    if not checkpoint_files:
        logger.error("[ERROR] No checkpoint files found!")
        return False
    
    latest_checkpoint = checkpoint_files[0]
    logger.info(f"[OK] Using checkpoint: {latest_checkpoint.name}")
    
    # Step 2: Initialize inference engine
    logger.info("\n[STEP 2] Initializing voice inference engine...")
    try:
        inference = VoiceInference(default_config, str(latest_checkpoint))
        logger.info("[OK] Inference engine initialized")
    except Exception as e:
        logger.error(f"[ERROR] Failed to initialize: {e}")
        return False
    
    # Step 3: Find input audio
    logger.info("\n[STEP 3] Locating input audio file...")
    audio_dir = project_root / "data" / "wavs"
    audio_files = list(audio_dir.glob("*.wav"))
    
    if not audio_files:
        logger.error("[ERROR] No preprocessed audio files found!")
        return False
    
    input_audio = audio_files[0]
    logger.info(f"[OK] Using input: {input_audio.name}")
    
    # Step 4: Prepare output path
    logger.info("\n[STEP 4] Preparing output location...")
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_audio = output_dir / f"{input_audio.stem}_cloned.wav"
    
    # Remove existing output if it exists
    if output_audio.exists():
        output_audio.unlink()
    
    logger.info(f"[OK] Output will be saved to: {output_audio.name}")
    
    # Step 5: Run voice conversion
    logger.info("\n[STEP 5] Running voice conversion...")
    logger.info("-" * 70)
    
    try:
        success = inference.convert_voice(
            input_audio=str(input_audio),
            output_audio=str(output_audio),
            pitch_shift=0,
            f0_method="crepe",
            noise_scale=0.4
        )
        logger.info("-" * 70)
        
        if not success:
            logger.error("[ERROR] Voice conversion failed!")
            return False
        
    except Exception as e:
        logger.error(f"[ERROR] Conversion exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 6: Verify output
    logger.info("\n[STEP 6] Verifying output file...")
    if not output_audio.exists():
        logger.error(f"[ERROR] Output file not created: {output_audio}")
        return False
    
    file_size_mb = output_audio.stat().st_size / (1024 * 1024)
    logger.info(f"[OK] Output file created: {output_audio.name}")
    logger.info(f"[OK] File size: {file_size_mb:.2f} MB")
    
    # Step 7: Print summary
    logger.info("\n" + "=" * 70)
    logger.info("WORKFLOW TEST COMPLETED SUCCESSFULLY!")
    logger.info("=" * 70)
    logger.info(f"\nSummary:")
    logger.info(f"  Input:  {input_audio.name} ({input_audio.stat().st_size / (1024 * 1024):.2f} MB)")
    logger.info(f"  Output: {output_audio.name} ({file_size_mb:.2f} MB)")
    logger.info(f"  Checkpoint: {latest_checkpoint.name}")
    logger.info(f"\nNext steps:")
    logger.info(f"  1. Play {output_audio.name} to listen to the converted voice")
    logger.info(f"  2. Import into FL Studio or your DAW")
    logger.info(f"  3. Fine-tune parameters if needed (pitch_shift, f0_method, noise_scale)")
    logger.info(f"\n" + "=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = test_e2e_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"\n[FATAL] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

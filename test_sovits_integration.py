"""
Test script for SO-VITS-SVC integration
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.modules.sovits_wrapper import SOVitsSVCWrapper, create_sovits_wrapper
from src.utils.logger import logger

def test_sovits_wrapper():
    """Test SO-VITS-SVC wrapper initialization"""
    logger.info("=" * 60)
    logger.info("Testing SO-VITS-SVC Wrapper")
    logger.info("=" * 60)
    
    # Test 1: Check if SO-VITS-SVC is available
    logger.info("\n[TEST 1] Checking SO-VITS-SVC availability...")
    sovits_path = project_root / 'so-vits-svc'
    if sovits_path.exists():
        logger.info(f"[OK] SO-VITS-SVC directory found: {sovits_path}")
    else:
        logger.error(f"[ERROR] SO-VITS-SVC directory not found: {sovits_path}")
        return False
    
    # Test 2: Check for inference tools
    logger.info("\n[TEST 2] Checking inference tools...")
    infer_tool = sovits_path / 'inference' / 'infer_tool.py'
    if infer_tool.exists():
        logger.info(f"[OK] Inference tool found: {infer_tool}")
    else:
        logger.error(f"[ERROR] Inference tool not found: {infer_tool}")
    
    # Test 3: Try importing SO-VITS-SVC modules
    logger.info("\n[TEST 3] Attempting to import SO-VITS-SVC modules...")
    try:
        sys.path.insert(0, str(sovits_path))
        from inference.infer_tool import Svc
        logger.info("[OK] Successfully imported Svc from SO-VITS-SVC")
    except ImportError as e:
        logger.warning(f"[WARNING] Could not import Svc: {e}")
        logger.info("[INFO] This is expected if dependencies aren't fully installed")
    
    # Test 4: Create wrapper (will fail gracefully without models)
    logger.info("\n[TEST 4] Creating SO-VITS-SVC wrapper...")
    dummy_model = project_root / "checkpoints" / "G_20251130_175603.pth"
    dummy_config = project_root / "config.json"
    
    wrapper = SOVitsSVCWrapper(str(dummy_model), str(dummy_config))
    logger.info(f"[OK] Wrapper created (available={wrapper.available})")
    
    # Test 5: Check loaded models
    logger.info("\n[TEST 5] Checking preprocessed audio...")
    data_dir = project_root / 'data' / 'wavs'
    if data_dir.exists():
        audio_files = list(data_dir.glob('*.wav'))
        logger.info(f"[OK] Found {len(audio_files)} preprocessed audio files")
    else:
        logger.warning(f"[WARNING] Preprocessed audio directory not found: {data_dir}")
    
    # Test 6: Check checkpoint
    logger.info("\n[TEST 6] Checking model checkpoint...")
    checkpoints_dir = project_root / 'checkpoints'
    if checkpoints_dir.exists():
        checkpoints = list(checkpoints_dir.glob('*.pth'))
        logger.info(f"[OK] Found {len(checkpoints)} checkpoint files")
        for ckpt in checkpoints:
            logger.info(f"      - {ckpt.name}")
    else:
        logger.warning(f"[WARNING] Checkpoints directory not found: {checkpoints_dir}")
    
    logger.info("\n" + "=" * 60)
    logger.info("SO-VITS-SVC Wrapper Test Complete")
    logger.info("=" * 60)
    
    return True

if __name__ == "__main__":
    test_sovits_wrapper()

#!/usr/bin/env python3
"""
Test enhanced voice conversion simulator
"""
import sys
from pathlib import Path
import numpy as np

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.modules.voice_converter_simulator import VoiceConversionSimulator, create_realistic_voice_conversion
from src.utils.logger import logger
import librosa
import soundfile as sf


def test_voice_converter_simulator():
    """Test voice conversion simulator with various parameters"""
    logger.info("=" * 70)
    logger.info("TESTING ENHANCED VOICE CONVERTER SIMULATOR")
    logger.info("=" * 70)
    
    # Load a test audio file
    logger.info("\n[TEST 1] Loading test audio...")
    audio_dir = project_root / "data" / "wavs"
    audio_files = list(audio_dir.glob("*.wav"))
    
    if not audio_files:
        logger.error("[ERROR] No audio files found!")
        return False
    
    input_audio_path = audio_files[0]
    logger.info(f"[OK] Using audio: {input_audio_path.name}")
    
    # Load audio
    audio, sr = librosa.load(str(input_audio_path), sr=44100)
    logger.info(f"[OK] Audio loaded: {len(audio) / sr:.2f}s at {sr}Hz")
    
    # Test 2: Initialize simulator
    logger.info("\n[TEST 2] Initializing VoiceConversionSimulator...")
    simulator = VoiceConversionSimulator(sample_rate=sr)
    logger.info("[OK] Simulator initialized")
    
    # Test 3: Test individual transformations
    logger.info("\n[TEST 3] Testing individual transformations...")
    
    logger.info("  - Testing pitch shift (+5 semitones)...")
    pitch_shifted = simulator.apply_pitch_shift(audio, 5)
    logger.info(f"    [OK] Output: {len(pitch_shifted) / sr:.2f}s")
    
    logger.info("  - Testing formant shift (1.1x)...")
    formant_shifted = simulator.apply_formant_shift(audio, 1.1)
    logger.info(f"    [OK] Output: {len(formant_shifted) / sr:.2f}s")
    
    logger.info("  - Testing spectral processing (brightness=1.2)...")
    spectral = simulator.apply_spectral_processing(audio, 1.2)
    logger.info(f"    [OK] Output: {len(spectral) / sr:.2f}s")
    
    logger.info("  - Testing vocoder effect...")
    vocoded = simulator.apply_vocoder_effect(audio, 0.8)
    logger.info(f"    [OK] Output: {len(vocoded) / sr:.2f}s")
    
    # Test 4: Test combined voice conversion
    logger.info("\n[TEST 4] Testing combined voice conversion...")
    
    test_cases = [
        {"pitch_shift": 0, "label": "No shift (baseline)"},
        {"pitch_shift": 5, "label": "Female shift (+5 semitones)"},
        {"pitch_shift": -5, "label": "Male shift (-5 semitones)"},
        {"pitch_shift": 12, "label": "Octave up (+12 semitones)"},
    ]
    
    output_dir = project_root / "output" / "simulation_tests"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, test_case in enumerate(test_cases, 1):
        pitch_shift = test_case["pitch_shift"]
        label = test_case["label"]
        
        logger.info(f"  [{i}] {label}...")
        
        converted = simulator.convert_voice(
            audio,
            pitch_shift=pitch_shift,
            formant_shift=1.0 + (pitch_shift / 60.0),
            brightness=1.0 + (pitch_shift / 40.0),
            time_stretch=1.0,
            vocoder_quality=0.95
        )
        
        # Verify output
        if len(converted) == 0:
            logger.error(f"    [ERROR] Empty output!")
            continue
        
        max_val = np.max(np.abs(converted))
        if max_val > 1.5:
            logger.warning(f"    [WARNING] Clipping detected (max={max_val:.2f}), normalizing...")
            converted = converted / max_val
        
        # Save output
        output_path = output_dir / f"test_{i:02d}_{pitch_shift:+d}semitones.wav"
        sf.write(str(output_path), converted, sr, subtype="PCM_24")
        logger.info(f"    [OK] Saved: {output_path.name}")
    
    # Test 5: Test using the convenience function
    logger.info("\n[TEST 5] Testing convenience function...")
    converted_easy = create_realistic_voice_conversion(audio, sr, pitch_shift=5)
    logger.info(f"[OK] Converted using convenience function: {len(converted_easy) / sr:.2f}s")
    
    # Save test output
    test_output = output_dir / "convenience_function_test.wav"
    sf.write(str(test_output), converted_easy, sr, subtype="PCM_24")
    logger.info(f"[OK] Saved: {test_output.name}")
    
    logger.info("\n" + "=" * 70)
    logger.info("VOICE CONVERTER SIMULATOR TEST COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"\nTest outputs saved to: {output_dir}")
    logger.info("You can now compare different voice transformations!")
    
    return True


if __name__ == "__main__":
    try:
        success = test_voice_converter_simulator()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"\n[FATAL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

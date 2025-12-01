"""
Text-to-Speech with Voice Cloning
Uses edge-tts for base TTS + SimpleVoiceCloner for voice transformation
"""
import asyncio
import edge_tts
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np
from simple_voice_cloner import SimpleVoiceCloner


async def text_to_speech_cloned(
    text: str,
    output_file: str,
    voice_profile_path: str = "voice_profile_simple.json",
    pitch_shift_st: int = 0,
    sample_rate: int = 44100,
    training_dir: str = "data/wavs"
) -> bool:
    """
    Convert text to speech using your cloned voice
    
    Args:
        text: Text to convert
        output_file: Output WAV file path
        voice_profile_path: Path to voice profile JSON
        pitch_shift_st: Pitch shift in semitones
        sample_rate: Sample rate
        training_dir: Directory with training audio files
    
    Returns:
        True if successful
    """
    try:
        # Generate TTS with neutral voice
        print("[TTS] Generating base speech...")
        communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural", rate="+0%")
        
        # Save temp TTS
        temp_tts = "temp_tts.wav"
        await communicate.save(temp_tts)
        
        # Load and resample
        tts_audio, tts_sr = librosa.load(temp_tts, sr=sample_rate, mono=True)
        
        # Remove temp file
        Path(temp_tts).unlink()
        
        # Load voice cloner with your profile
        print("[CLONING] Applying your voice characteristics...")
        cloner = SimpleVoiceCloner(training_dir)
        
        # Try to load profile, fall back to training if not found
        profile_path = Path(voice_profile_path)
        if not profile_path.exists():
            profile_path = Path(training_dir).parent / voice_profile_path
        
        if profile_path.exists():
            cloner.load_profile(str(profile_path))
        else:
            print(f"[WARNING] Profile not found at {profile_path}, using trained characteristics")
        
        # Apply voice transformation
        cloned_audio = cloner.clone_voice(tts_audio, pitch_shift_st=pitch_shift_st)
        
        # Save
        sf.write(output_file, cloned_audio, sample_rate, subtype='PCM_24')
        print(f"[OK] Saved: {output_file}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")
        return False


def sync_text_to_speech_cloned(
    text: str,
    output_file: str,
    voice_profile_path: str = "voice_profile_simple.json",
    pitch_shift_st: int = 0,
    sample_rate: int = 44100,
    training_dir: str = "data/wavs"
) -> bool:
    """Synchronous wrapper for text-to-speech"""
    return asyncio.run(text_to_speech_cloned(
        text,
        output_file,
        voice_profile_path,
        pitch_shift_st,
        sample_rate,
        training_dir
    ))


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("TEXT-TO-SPEECH WITH YOUR VOICE CLONE")
    print("=" * 70)
    
    text = "Hello, this is a test of text to speech using my cloned voice. It sounds like me!"
    
    print(f"\nConverting: '{text}'")
    success = sync_text_to_speech_cloned(
        text,
        "../../output/test_tts_cloned.wav",
        training_dir="../../data/wavs",
        pitch_shift_st=0
    )
    
    if success:
        print("\n✓ TTS successful!")

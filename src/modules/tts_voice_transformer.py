"""
Text-to-speech with voice transformation (female to male).
Generates speech and transforms it to sound like user's voice.
"""
import asyncio
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from edge_tts import Communicate


async def text_to_speech_transformed(text, output_path, aggressiveness=2.0):
    """
    Convert text to speech using female voice, then transform to male voice.
    
    Args:
        text: Text to synthesize
        output_path: Output WAV file path
        aggressiveness: How strong the gender transformation (2.0 = very strong)
    """
    from src.modules.voice_transformer import GenderVoiceTransformer
    
    # Generate speech using edge-tts (default female voice)
    print(f"[TTS] Generating speech: '{text}'")
    temp_path = "output/temp_tts.wav"
    communicate = Communicate(text, voice="en-US-AriaNeural", rate="+0%")
    
    # Save to temp file
    await communicate.save(temp_path)
    
    # Load the generated speech
    audio, sr = librosa.load(temp_path, sr=44100)
    print(f"[TTS] Generated: {len(audio)/sr:.2f}s of speech")
    
    # Transform to male voice
    print(f"[TTS] Transforming to your male voice (aggressiveness={aggressiveness})...")
    transformer = GenderVoiceTransformer(sample_rate=sr)
    transformed = transformer.transform_to_male(audio, aggressiveness=aggressiveness)
    
    # Normalize
    transformed = transformed / (np.max(np.abs(transformed)) + 1e-7) * 0.95
    
    # Save
    sf.write(output_path, transformed, sr, subtype='PCM_24')
    print(f"✓ Saved: {output_path}")
    
    # Verify
    S = librosa.stft(transformed)
    magnitudes = np.abs(S)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    centroid = np.average(freqs, weights=np.mean(magnitudes, axis=1))
    print(f"  Spectral centroid: {centroid:.0f} Hz (male voice)")
    
    return transformed, sr


def sync_text_to_speech_transformed(text, output_path, aggressiveness=2.0):
    """Synchronous wrapper for text_to_speech_transformed."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(text_to_speech_transformed(text, output_path, aggressiveness))
    loop.close()
    return result


if __name__ == '__main__':
    # Test
    print("Test: Converting text to speech in your voice...")
    sync_text_to_speech_transformed(
        "Hello! This is text to speech using your voice. It should sound like a male speaking.",
        "output/tts_your_voice.wav",
        aggressiveness=2.0
    )
    print("Done!")

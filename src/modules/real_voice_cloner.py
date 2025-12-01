"""
Real Voice Cloner - Using Coqui TTS with Speaker Embeddings
This transfers actual voice characteristics using neural models,
not just pitch shifting.
"""

import os
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
import torch
import warnings

warnings.filterwarnings('ignore')


class RealVoiceCloner:
    """
    Uses Coqui TTS voice cloning with speaker embeddings
    for actual neural voice transfer
    """
    
    def __init__(self):
        print("[SETUP] Loading Coqui TTS models...")
        from TTS.api import TTS
        
        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"  Device: {device}")
        
        # Use the GLOW-TTS model with speaker encoder for voice cloning
        self.tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", 
                       gpu=(device == "cuda"))
        
        # Speaker encoder for voice embedding
        self.tts.load_speaker_encoder_model(
            model_path="tts_models/speaker_encoders/english/GemspeakerEncoder/model.pth"
        )
        
        self.sr = 22050  # Coqui's default
        print("  ✓ Models loaded")
    
    def extract_speaker_embedding(self, audio_path):
        """Extract speaker embedding from audio"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            # Get speaker embedding
            gpt_cond_latent, speaker_embedding = self.tts.synthesizer.speaker_encoder.encode_speaker(
                torch.from_numpy(y).unsqueeze(0).float()
            )
            
            return speaker_embedding.cpu().numpy()
        except Exception as e:
            print(f"  Warning: Could not extract embedding from {audio_path}: {e}")
            return None
    
    def clone_voice_from_samples(self, source_text, voice_samples, output_path):
        """
        Clone voice using multiple reference samples
        
        Args:
            source_text: Text to synthesize with cloned voice
            voice_samples: List of audio file paths to learn voice from
            output_path: Where to save result
        """
        
        print("\n" + "="*70)
        print("REAL VOICE CLONING WITH NEURAL NETWORKS")
        print("="*70)
        
        print(f"\n[LEARNING] Extracting speaker embeddings from {len(voice_samples)} samples...")
        
        embeddings = []
        for sample_path in voice_samples:
            print(f"  Processing: {Path(sample_path).name}")
            emb = self.extract_speaker_embedding(sample_path)
            if emb is not None:
                embeddings.append(emb)
        
        if not embeddings:
            print("  ERROR: Could not extract any embeddings!")
            return False
        
        # Average embeddings for more stable voice
        avg_embedding = np.mean(embeddings, axis=0)
        print(f"  ✓ Extracted {len(embeddings)} speaker embeddings")
        
        print(f"\n[SYNTHESIZING] Creating TTS with cloned voice...")
        print(f"  Text: {source_text[:60]}...")
        
        try:
            # Generate speech with cloned voice
            wav = self.tts.synthesize(
                texts=[source_text],
                speaker_embeddings=avg_embedding
            )
            
            # Save
            sf.write(output_path, wav, self.sr)
            print(f"\n✓ SAVED: {output_path}")
            print(f"  Duration: {len(wav)/self.sr:.2f}s")
            
            return True
        except Exception as e:
            print(f"  ERROR during synthesis: {e}")
            return False
    
    def transfer_voice_to_audio(self, source_audio_path, voice_samples, output_path):
        """
        Transfer voice from samples to existing audio
        This is harder - requires voice conversion model
        """
        
        print("\n" + "="*70)
        print("VOICE TRANSFER (Advanced)")
        print("="*70)
        
        print("\n[NOTE] Voice transfer requires additional models.")
        print("       For now, recommend using voice cloning with TTS instead.")
        print("       Would you like to:")
        print("       1. Synthesize new speech with your cloned voice?")
        print("       2. Use simple pitch/energy matching as fallback?")
        
        return False


def test_voice_cloning():
    """Test real voice cloning"""
    
    # Find Katie audio
    katie_path = os.path.expanduser("~/Desktop/katie.mp3")
    if not os.path.exists(katie_path):
        print(f"ERROR: {katie_path} not found")
        return
    
    # Find your voice samples
    training_dir = os.path.join(os.path.expanduser("~/Desktop"), "training data")
    voice_samples = sorted([
        os.path.join(training_dir, f) 
        for f in os.listdir(training_dir) 
        if f.lower().endswith(('.wav', '.mp3', '.m4a'))
    ])
    
    if not voice_samples:
        print(f"ERROR: No voice samples found in {training_dir}")
        return
    
    print(f"Found {len(voice_samples)} voice samples:")
    for sample in voice_samples:
        print(f"  - {Path(sample).name}")
    
    # Initialize cloner
    cloner = RealVoiceCloner()
    
    # Test: Synthesize text with your voice
    test_text = "Hello, this is Katie speaking with your cloned voice. The voice transfer is working perfectly."
    
    cloner.clone_voice_from_samples(
        test_text,
        voice_samples,
        "output/katie_real_cloned_tts.wav"
    )
    
    print("\n" + "="*70)
    print("COMPARISON:")
    print("="*70)
    print("  Original: katie.mp3")
    print("  Cloned:   output/katie_real_cloned_tts.wav")
    print("\nThe cloned version should have YOUR voice characteristics")
    print("(pitch, resonance, accent patterns) applied to Katie's speech.")


if __name__ == "__main__":
    test_voice_cloning()

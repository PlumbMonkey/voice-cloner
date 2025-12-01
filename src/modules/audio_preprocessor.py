"""
Audio preprocessing module - handles audio validation, processing, and feature extraction
Phase 2: PRE-01 to PRE-08
"""
import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import numpy as np
import soundfile as sf
import librosa
from src.utils.logger import logger
from src.utils.error_handler import AudioProcessingError


class AudioPreprocessor:
    """Handles audio preprocessing, validation, and feature extraction"""

    SUPPORTED_FORMATS = [".wav", ".mp3", ".flac", ".ogg"]
    MIN_AUDIO_LENGTH = 0.5  # seconds
    MAX_AUDIO_DURATION = 15  # seconds for single segment

    def __init__(self, config):
        """Initialize audio preprocessor"""
        self.config = config
        self.sample_rate = config.SAMPLE_RATE
        self.n_fft = config.N_FFT
        self.hop_length = config.HOP_LENGTH

    def run_preprocessing_pipeline(self, input_dir: str) -> bool:
        """Execute complete preprocessing pipeline (PRE-01 to PRE-08)"""
        logger.info("=" * 60)
        logger.info("Starting Audio Preprocessing Pipeline...")
        logger.info("=" * 60)

        input_path = Path(input_dir)

        try:
            # Step 1: Validate audio files (PRE-01, PRE-02)
            audio_files = self.validate_audio_files(input_path)
            if not audio_files:
                logger.error("No valid audio files found")
                return False

            logger.info(f"✓ Found {len(audio_files)} valid audio files")

            # Step 2: Prepare output directories
            output_wavs_dir = self.config.DATA_DIR / "wavs"
            output_wavs_dir.mkdir(parents=True, exist_ok=True)

            # Step 3: Process each audio file
            all_segments = []
            for idx, audio_file in enumerate(audio_files):
                logger.info(f"\n[{idx + 1}/{len(audio_files)}] Processing {audio_file.name}...")

                # Convert to WAV and resample (PRE-03)
                wav_data, sr = self.load_and_preprocess_audio(audio_file)
                if wav_data is None:
                    logger.warning(f"Skipping {audio_file.name}")
                    continue

                # Split into segments (PRE-04, PRE-05)
                segments = self.segment_and_denoise_audio(wav_data, sr)
                if not segments:
                    logger.warning(f"No valid segments from {audio_file.name}")
                    continue

                logger.info(f"Created {len(segments)} audio segments")

                # Save segments
                for seg_idx, segment_data in enumerate(segments):
                    segment_file = output_wavs_dir / f"segment_{len(all_segments):05d}.wav"
                    sf.write(str(segment_file), segment_data, self.sample_rate)
                    all_segments.append(segment_file)

            if not all_segments:
                logger.error("No valid audio segments created")
                return False

            logger.info(f"\n✓ Created {len(all_segments)} total segments")

            # Step 4: Generate file lists (PRE-06)
            self.generate_file_lists(all_segments)

            # Step 5: Extract features (PRE-07, PRE-08)
            logger.info("\nExtracting audio features...")
            if not self.extract_features(all_segments):
                logger.error("Feature extraction failed")
                return False

            logger.info("\n" + "=" * 60)
            logger.info("✅ Audio preprocessing completed successfully!")
            logger.info(f"Total segments: {len(all_segments)}")
            logger.info("=" * 60)

            return True

        except Exception as e:
            logger.error(f"Preprocessing pipeline error: {e}")
            return False

    def validate_audio_files(self, input_dir: Path) -> List[Path]:
        """Validate and collect audio files (PRE-01, PRE-02)"""
        logger.info(f"Scanning for audio files in {input_dir}...")

        audio_files = []

        # Find all supported audio files
        for format in self.SUPPORTED_FORMATS:
            audio_files.extend(input_dir.glob(f"**/*{format}"))
            audio_files.extend(input_dir.glob(f"**/*{format.upper()}"))

        audio_files = list(set(audio_files))  # Remove duplicates

        if not audio_files:
            logger.error("No audio files found")
            return []

        # Validate file sizes and durations
        valid_files = []
        for audio_file in audio_files:
            try:
                # Check file size (at least 1 MB for meaningful audio)
                file_size_mb = audio_file.stat().st_size / (1024 * 1024)
                if file_size_mb < 1:
                    logger.warning(f"File too small: {audio_file.name} ({file_size_mb:.2f} MB)")
                    continue

                # Check duration
                try:
                    info = sf.info(str(audio_file))
                    audio_data = sf.read(str(audio_file))[0]
                    duration = len(audio_data) / info.samplerate
                except Exception as e:
                    logger.error(f"Failed to read {audio_file.name}: {e}")
                    continue
                
                if duration < self.MIN_AUDIO_LENGTH:
                    logger.warning(f"Audio too short: {audio_file.name} ({duration:.2f}s < {self.MIN_AUDIO_LENGTH}s)")
                    continue

                valid_files.append(audio_file)
                logger.info(f"✓ Valid audio: {audio_file.name} ({duration:.2f}s, {file_size_mb:.2f}MB)")

            except Exception as e:
                logger.warning(f"Error validating {audio_file.name}: {e}")
                continue

        # Warn if total duration is less than 10 minutes
        total_duration = 0
        for audio_file in valid_files:
            try:
                info = sf.info(str(audio_file))
                audio_data = sf.read(str(audio_file))[0]
                total_duration += len(audio_data) / info.samplerate
            except:
                pass

        if total_duration < 600:  # 10 minutes
            logger.warning(f"⚠ Total audio duration ({total_duration/60:.1f}m) below recommended (10m)")
            logger.warning("More audio data will improve model quality")

        logger.info(f"Validation complete: {len(valid_files)} valid files out of {len(audio_files)}")
        return valid_files

    def load_and_preprocess_audio(self, audio_file: Path) -> Tuple[Optional[np.ndarray], int]:
        """Load audio file and resample to target sample rate (PRE-03)"""
        try:
            logger.info(f"Loading {audio_file.name}...")

            # Read audio
            y, sr = librosa.load(str(audio_file), sr=None, mono=False)
            logger.info(f"  Loaded: shape={y.shape}, sr={sr}")

            # Convert to mono if stereo
            if len(y.shape) > 1:
                logger.info(f"  Converting from stereo to mono...")
                y = librosa.to_mono(y)
                logger.info(f"  Now mono: shape={y.shape}")
            
            # Resample if necessary
            if sr != self.sample_rate:
                logger.info(f"Resampling from {sr} Hz to {self.sample_rate} Hz...")
                y = librosa.resample(y, orig_sr=sr, target_sr=self.sample_rate)

            # Normalize audio
            y = y / (np.max(np.abs(y)) + 1e-8)

            logger.info(f"✓ Audio loaded and preprocessed ({len(y) / self.sample_rate:.2f}s)")
            return y, self.sample_rate

        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None, None

    def segment_and_denoise_audio(self, audio_data: np.ndarray, sr: int) -> List[np.ndarray]:
        """Segment long audio and remove silence/noise (PRE-04, PRE-05)"""
        segments = []

        try:
            logger.info(f"Total audio length: {len(audio_data) / sr:.2f}s at {sr} Hz")
            
            # Detect and remove silence
            logger.info(f"Removing silence (top_db={25})...")
            intervals = librosa.effects.split(
                audio_data,
                top_db=25,  # Lowered from 40 to be less aggressive (captures more audio)
                frame_length=self.n_fft,
                hop_length=self.hop_length,
            )

            logger.info(f"Found {len(intervals)} non-silent intervals")
            if len(intervals) == 0:
                logger.warning("⚠️  No non-silent audio detected! Audio may be all silence.")
                logger.warning("Try recording with higher volume or clearer audio")
                return []

            # Create segments from non-silent intervals
            kept = 0
            skipped_too_short = 0
            total_kept_duration = 0
            
            for idx, (start, end) in enumerate(intervals):
                segment = audio_data[start:end]
                duration = len(segment) / sr
                
                logger.debug(f"  Interval {idx+1}: {duration:.3f}s ({start}-{end} samples)")

                # Filter by duration
                if duration < self.config.MIN_DURATION:
                    logger.debug(f"    → Skipped: too short ({duration:.3f}s < {self.config.MIN_DURATION}s)")
                    skipped_too_short += 1
                    continue

                if duration > self.config.MAX_DURATION:
                    logger.debug(f"    → Splitting: too long ({duration:.3f}s > {self.config.MAX_DURATION}s)")
                    # Split long segments
                    max_samples = int(self.config.MAX_DURATION * sr)
                    for i in range(0, len(segment), max_samples):
                        sub_segment = segment[i:i + max_samples]
                        sub_duration = len(sub_segment) / sr
                        if sub_duration >= self.config.MIN_DURATION:
                            segments.append(sub_segment)
                            total_kept_duration += sub_duration
                            kept += 1
                else:
                    segments.append(segment)
                    total_kept_duration += duration
                    kept += 1
                    logger.debug(f"    ✓ Kept: {duration:.3f}s")

            logger.info(f"Segmentation complete:")
            logger.info(f"  Total kept: {kept} segments ({total_kept_duration:.2f}s)")
            logger.info(f"  Total skipped: {skipped_too_short} segments")
            
            if len(segments) == 0:
                logger.error("❌ No valid segments after filtering!")
                logger.error(f"   MIN_DURATION: {self.config.MIN_DURATION}s")
                logger.error(f"   MAX_DURATION: {self.config.MAX_DURATION}s")
            
            return segments

        except Exception as e:
            logger.error(f"Error segmenting audio: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []

    def generate_file_lists(self, segment_files: List[Path]) -> bool:
        """Generate file lists for training (PRE-06)"""
        try:
            logger.info("Generating file lists...")

            # Training list
            train_list_path = self.config.DATA_DIR / "train.txt"
            with open(train_list_path, "w") as f:
                for seg_file in segment_files:
                    f.write(f"{seg_file.relative_to(self.config.DATA_DIR)}\n")

            logger.info(f"✓ Created train list: {train_list_path}")

            # Val list (10% of data)
            val_count = max(1, len(segment_files) // 10)
            val_list_path = self.config.DATA_DIR / "val.txt"
            with open(val_list_path, "w") as f:
                for seg_file in segment_files[:val_count]:
                    f.write(f"{seg_file.relative_to(self.config.DATA_DIR)}\n")

            logger.info(f"✓ Created validation list: {val_list_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating file lists: {e}")
            return False

    def extract_features(self, segment_files: List[Path]) -> bool:
        """Extract F0 and HuBERT features (PRE-07, PRE-08)"""
        try:
            logger.info("Extracting audio features...")

            # This would typically use SO-VITS-SVC's feature extraction
            # For now, we'll create placeholder feature files
            features_dir = self.config.DATA_DIR / "features"
            features_dir.mkdir(parents=True, exist_ok=True)

            f0_dir = features_dir / "f0"
            hubert_dir = features_dir / "hubert"
            f0_dir.mkdir(parents=True, exist_ok=True)
            hubert_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"✓ Feature directories created")

            # Note: Actual feature extraction happens in SO-VITS-SVC pipeline
            logger.info("✓ Feature extraction paths prepared (will be computed during training)")

            return True

        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return False

    def get_preprocessing_stats(self) -> Dict:
        """Get preprocessing statistics"""
        try:
            wavs_dir = self.config.DATA_DIR / "wavs"
            if not wavs_dir.exists():
                return {"segments": 0, "total_duration": 0}

            wav_files = list(wavs_dir.glob("*.wav"))
            total_duration = 0

            for wav_file in wav_files:
                try:
                    data, sr = librosa.load(str(wav_file), sr=None)
                    total_duration += len(data) / sr
                except:
                    pass

            return {
                "segments": len(wav_files),
                "total_duration": total_duration,
                "average_segment_duration": total_duration / len(wav_files) if wav_files else 0,
            }

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

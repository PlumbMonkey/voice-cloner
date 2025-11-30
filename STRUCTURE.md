# Voice Cloner Project Structure

## Directory Overview

```
Voice-Cloner/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   ├── orchestrator.py           # Workflow orchestration
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py             # Configuration management
│   ├── modules/                  # Core processing modules
│   │   ├── __init__.py
│   │   ├── environment_detector.py    # Phase 1
│   │   ├── environment_setup.py       # Phase 2
│   │   ├── audio_preprocessor.py      # Phase 3
│   │   ├── model_trainer.py           # Phase 4
│   │   └── voice_inference.py         # Phase 5
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── logger.py             # Logging system
│       ├── system_utils.py       # System detection
│       └── error_handler.py      # Error handling
│
├── docs/                         # Documentation
│   ├── SETUP_GUIDE.md            # Installation guide
│   ├── USER_GUIDE.md             # Usage guide
│   └── FL_STUDIO_GUIDE.md        # FL Studio integration
│
├── data/                         # Data directory (gitignored)
│   ├── input/                    # Your vocal recordings
│   └── wavs/                     # Preprocessed segments
│
├── output/                       # Output files (gitignored)
│   └── *.wav                     # Converted vocals
│
├── models/                       # Pretrained models (gitignored)
│
├── checkpoints/                  # Training checkpoints (gitignored)
│
├── logs/                         # Log files (gitignored)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_voice_cloner.py      # Unit tests
│
├── examples.py                   # Usage examples
│
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project metadata
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
└── STRUCTURE.md                 # This file
```

## Module Descriptions

### Core Modules (src/modules/)

#### 1. environment_detector.py (Phase 1)
- Detects OS type (Windows/Linux/macOS)
- Checks Python version compatibility (3.8-3.10)
- Detects GPU availability (NVIDIA CUDA)
- Validates system specifications (CPU, RAM, disk space)
- Provides device recommendations

#### 2. environment_setup.py (Phase 2)
- Creates virtual environment
- Installs Python dependencies
- Clones SO-VITS-SVC repository
- Downloads pretrained models
- Configures GPU/CUDA support

#### 3. audio_preprocessor.py (Phase 3)
- Validates audio files (WAV, MP3, FLAC)
- Resamples audio to 44.1kHz
- Removes silence and noise
- Segments long audio into training chunks
- Generates training/validation file lists
- Prepares feature extraction

#### 4. model_trainer.py (Phase 4)
- Generates training configuration
- Configures training parameters
- Manages training execution
- Handles checkpoint saves
- Tracks training progress
- Estimates training time
- Supports checkpoint resumption

#### 5. voice_inference.py (Phase 5)
- Performs voice conversion
- Implements pitch shifting
- Supports multiple F0 methods (crepe, dio, harvest)
- Batch processing for multiple files
- Exports FL Studio compatible WAV
- Provides FL Studio integration guide

### Utility Modules (src/utils/)

#### logger.py
- Rich formatted logging
- Console and file output
- Debug level logging
- Color-coded message types

#### system_utils.py
- OS detection
- GPU/CUDA detection
- CPU information
- Memory and disk information
- System capability checks

#### error_handler.py
- Custom exception classes
- Error formatting and context
- Exception hierarchy
- Error message utilities

### Configuration (src/config/)

#### config.py
- Environment variable loading
- Configuration file management
- Path management
- Training parameter configuration
- Audio processing settings
- Device selection

## Data Flow

```
USER INPUT
    ↓
PHASE 1: DETECTION
  ├─ OS Check
  ├─ Python Version
  ├─ GPU Detection
  └─ System Specs
    ↓
PHASE 2: SETUP
  ├─ Virtual Env
  ├─ Dependencies
  ├─ Repository
  └─ Models
    ↓
PHASE 3: PREPROCESSING
  ├─ Audio Validation
  ├─ Resampling
  ├─ Segmentation
  ├─ Noise Removal
  └─ Feature Extraction
    ↓
PHASE 4: TRAINING
  ├─ Config Generation
  ├─ Training Execution
  ├─ Checkpoint Saves
  └─ Progress Tracking
    ↓
PHASE 5: INFERENCE
  ├─ Model Loading
  ├─ Voice Conversion
  ├─ Pitch Shifting
  └─ Output Export
    ↓
FL STUDIO INTEGRATION
  ├─ Edison Import
  ├─ Audio Editing
  ├─ Arrangement
  └─ Export/Release
```

## CLI Commands

### Project Management
- `python -m src.main init` - Initialize project
- `python -m src.main status` - Check workflow status
- `python -m src.main report` - Generate comprehensive report

### Workflow Phases
- `python -m src.main detect` - Phase 1: Detect environment
- `python -m src.main setup` - Phase 2: Setup environment
- `python -m src.main preprocess <dir>` - Phase 3: Preprocess audio
- `python -m src.main train` - Phase 4: Train model
- `python -m src.main infer <in> <out>` - Phase 5: Convert voice

### Batch Operations
- `python -m src.main batch_infer <in> <out>` - Batch convert files

### Guided Workflows
- `python -m src.main quickstart` - Interactive all-in-one setup
- `python -m src.main guide` - FL Studio integration guide

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_voice_cloner.py::TestSystemUtils::test_os_detection -v
```

### Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

## Configuration Files

### .env
Local environment variables (created from .env.example)
- Training parameters
- Audio settings
- Device selection
- F0 method configuration

### pyproject.toml
Project metadata and dependencies
- Package information
- Dependency definitions
- Optional dev dependencies
- Script entry points

### requirements.txt
Python package dependencies
- Core ML packages (torch, torchaudio)
- Audio processing (librosa, soundfile)
- Utilities (click, rich, pyyaml)

## Output Structure

```
output/
├── training/
│   ├── config.yaml
│   ├── log.txt
│   └── metrics.json
├── inference/
│   ├── voice_converted.wav
│   ├── voice_+5.wav
│   └── voice_-3.wav
└── fl_studio/
    ├── README.md
    └── integration_guide.txt
```

## Key Features

✅ **Cross-Platform**: Windows, Linux, macOS
✅ **GPU Support**: NVIDIA CUDA acceleration
✅ **Automated**: Complete workflow automation
✅ **User-Friendly**: CLI with clear feedback
✅ **Modular**: Each phase independent
✅ **Extensible**: Easy to add new modules
✅ **Well-Documented**: Comprehensive guides
✅ **Tested**: Unit tests included

---

**Voice Cloner Project Structure v0.1.0**

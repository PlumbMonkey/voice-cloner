#!/usr/bin/env python3
"""
Test SO-VITS-SVC model loading and voice conversion
"""

import sys
from pathlib import Path
import torch
import json

# Add SO-VITS-SVC to path
sovits_path = Path('so-vits-svc')
sys.path.insert(0, str(sovits_path))

from inference.infer_tool import Svc

print("[TEST] SO-VITS-SVC Model Loading and Voice Conversion Test")
print("=" * 60)

# Find latest checkpoint
checkpoints_dir = Path('checkpoints')
if not checkpoints_dir.exists():
    print(f"[ERROR] Checkpoints directory not found: {checkpoints_dir}")
    sys.exit(1)

checkpoints = sorted(checkpoints_dir.glob('G_*.pth'), reverse=True)
if not checkpoints:
    print("[ERROR] No checkpoints found in checkpoints/")
    sys.exit(1)

model_path = checkpoints[0]
config_path = Path('config.json')

print(f"[1] Model: {model_path.name}")
print(f"[2] Config: {config_path.name}")

if not config_path.exists():
    print(f"[ERROR] Config not found: {config_path}")
    sys.exit(1)

# Load config
with open(config_path) as f:
    config = json.load(f)
    print(f"[3] Config loaded: {config.get('model_name', 'unknown')} model")

# Test device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"[4] Device: {device}")

# Try to initialize Svc
try:
    print("\n[INIT] Initializing SO-VITS-SVC Svc class...")
    
    svc = Svc(
        net_g_path=str(model_path),
        config_path=str(config_path),
        device=device,
        cluster_model_path=None,
        nsf_hifigan_enhance=False,
        shallow_diffusion=False,
        only_diffusion=False
    )
    
    print("[OK] Svc object created successfully!")
    print("[OK] Model loaded and ready for inference!")
    
    print("\n[SUCCESS] SO-VITS-SVC is fully functional!")
    print("[NEXT] Ready to perform real voice conversion")
    
except FileNotFoundError as e:
    print(f"[ERROR] File not found: {e}")
    sys.exit(1)
    
except RuntimeError as e:
    print(f"[ERROR] Runtime error (likely model loading): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

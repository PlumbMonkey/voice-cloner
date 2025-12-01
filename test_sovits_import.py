#!/usr/bin/env python3
"""Test SO-VITS-SVC imports after numpy downgrade"""

import sys
from pathlib import Path

# Add SO-VITS-SVC to path
sovits_path = Path('so-vits-svc')
sys.path.insert(0, str(sovits_path))

print("[TEST] Testing SO-VITS-SVC imports with numpy 1.23.5...")

try:
    print("[1] Importing inference.infer_tool...")
    from inference.infer_tool import Svc
    print("[OK] Svc class imported successfully!")
    
    print("[2] Checking Svc initialization parameters...")
    import inspect
    sig = inspect.signature(Svc.__init__)
    print(f"[OK] Svc.__init__ signature: {sig}")
    
    print("\n[SUCCESS] SO-VITS-SVC is now importable!")
    print("[NEXT] Ready to test model loading and voice conversion")
    
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

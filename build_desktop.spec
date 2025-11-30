"""
PyInstaller build configuration for Voice Cloner Desktop App
Generates standalone executable with all dependencies bundled
"""
# Build with: pyinstaller build_desktop.spec

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

a = Analysis(
    [str(PROJECT_ROOT / 'src' / 'desktop_app.py')],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        (str(PROJECT_ROOT / 'docs'), 'docs'),
        (str(PROJECT_ROOT / 'assets'), 'assets'),
    ],
    hiddenimports=[
        'PyQt6',
        'torch',
        'librosa',
        'soundfile',
        'numpy',
        'scipy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoiceCloner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJECT_ROOT / 'assets' / 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VoiceCloner',
)

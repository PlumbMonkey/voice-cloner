# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Voice Cloner Desktop Application

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys

block_cipher = None

# Collect all PyQt5 modules
qt_submodules = collect_submodules('PyQt5')

# Data files needed
datas = [
    ('assets', 'assets'),
    ('src/config', 'src/config'),
    ('src/branding.py', 'src'),
]

# Hidden imports for audio processing
hidden_imports = [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui', 
    'PyQt5.QtWidgets',
    'soundfile',
    'librosa',
    'librosa.core',
    'librosa.util',
    'scipy',
    'numpy',
    'torch',
] + qt_submodules

a = Analysis(
    ['src/desktop_app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    icon='assets/logo.ico' if Path('assets/logo.ico').exists() else None,
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

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hidden_imports = [
    'Flask',
    'PyQt5',
    'sklearn',
    'whisper',
    'pytest',
    'pytestqt',
    'speech_recognition',
]

a = Analysis(
    ['css_editor/editor.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('css_editor/themes/*.css', 'css_editor/themes'),
        ('css_editor/assets/*', 'css_editor/assets'),
        ('static/css/*.css', 'static/css'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_editor',
)

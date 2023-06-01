block_cipher = None
app_icon = 'assets/chess.icns'

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('*', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas'],
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
    name='Xadrez',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    icon=app_icon,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='Xadrez.app',
    icon=app_icon,
    bundle_identifier='com.abel.xadrez',
)
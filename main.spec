# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/Administrator/Desktop/pfe/YouDow-desk/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Program Files/Python311/Lib/site-packages/psutil', 'psutil/'), ('C:/Program Files/Python311/Lib/site-packages/customtkinter', 'customtkinter/'), ('C:/Program Files/Python311/Lib/site-packages/googleapiclient', 'googleapiclient/')],
    hiddenimports=['googleapiclient.discovery'],
    hookspath=[],
    hooksconfig={},
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Administrator\\Downloads\\logo (2).ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

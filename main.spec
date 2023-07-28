# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

hiddenimports = [
    "PyQt6.QtCore.QPropertyAnimation",
    "PyQt6.QtCore.QRect",
    "PyQt6.QtCore.QTimer",
    "PyQt6.QtWidgets.QApplication",
    "PyQt6.QtWidgets.QMainWindow",
    "PyQt6.QtGui.QMovie",
    "PyQt6.QtGui.QIcon",
    "PyQt6.QtTest.QTest",
    "PyQt6.uic.loadUi",
    "afk_resources",
    "PyQt6.QtCore",
    "keyboard",
    "psutil",
    "sys",
    "os"
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[ ('./resources/', 'resources'),
            ('Anti-AFK.ui', '.')
    ],
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Anti AFK',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./resources/icon.ico',
)

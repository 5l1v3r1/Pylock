# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['pylock.py'],
             pathex=['/Users/lvoerman/Documents/directories/programmeren/python/PyLock'],
             binaries=[],
             datas=[('images/bg.jpg', 'images')],
             hiddenimports=['tkinter', 'tkinter.ttk', 'ttkthemes', 'pymsgbox', 'pycrypto'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pylock',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
app = BUNDLE(exe,
             name='pylock.app',
             icon='icon.ico',
             bundle_identifier=None)

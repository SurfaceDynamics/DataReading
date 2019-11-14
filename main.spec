# -*- mode: python -*-

block_cipher = None


a = Analysis(['Scripts\\main.py'],
             pathex=['C:\\Users\\Bruker\\Google Drive\\Interne Data\\Coding\\Database Reader'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
	  Tree('Database Reader', prefix=''),
          Tree('GUI', prefix=''),
          a.zipfiles,
          a.datas,
          name='Database Reader',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False, icon='res\\sd.ico')

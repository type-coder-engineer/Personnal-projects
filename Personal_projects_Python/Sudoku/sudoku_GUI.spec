# -*- mode: python -*-

block_cipher = None


a = Analysis(['sudoku_GUI.py'],
             pathex=['C:\\Users\\czhang\\Desktop\\test\\Sudoku'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('bg3.png', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\bg3.png', 'DATA'),
            ('left.png', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\left.png', 'DATA'),
            ('right.png', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\right.png', 'DATA'),
            ('down1.png', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\down1.png', 'DATA'),
            ('down2.png', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\down2.png', 'DATA'),
            ('sudokuIco.ico', 'C:\\Users\\czhang\\Desktop\\test\\Sudoku\\sudokuIco.ico', 'DATA')]
            
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sudoku_GUI',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='C:\\Users\\czhang\\Desktop\\test\\Sudoku\\sudokuIco.ico')
          
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='sudoku_GUI')
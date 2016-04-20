import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = 'ScumInvaders', 
      version='1.0.', 
      description='Stop scums',
      options = {'build_exe': {'include_files': ['Fonts\comic.ttf', 'Fonts\nasalization-rg.ttf', 'Fonts\Gtek Technology free promo.ttf']}},
      executables = [Executable(script = 'ScumInvaders.py', base = base)])

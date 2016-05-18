import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = 'ScumInvaders', 
      version='1.0.', 
      description='Stop scums',
      executables = [Executable(script = 'ScumInvaders.py', base = base)])
#test for limey

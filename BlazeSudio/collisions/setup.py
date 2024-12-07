from setuptools import setup, Extension
from Cython.Build import cythonize
import os, sys, shutil, re

extensions = [
    Extension("collisions", ["lib/collisions.py"]),
]

# Build pyi stub file automatically
os.system("stubgen lib/collisions.py --include-docstrings")
shutil.copy('./out/BlazeSudio/collisions/lib/collisions.pyi', './generated/collisions.pyi')

if '--no-build' not in sys.argv:
    if sys.platform == 'win32':
        platform = 'win_amd64'
        fname = f'collisions.cp{sys.version_info.major}{sys.version_info.minor}-{platform}.pyd'
    else:
        platform = 'x86_64-linux-gnu'
        fname = f'collisions.cpython-{sys.version_info.major}{sys.version_info.minor}-{platform}.so'
    setup(
        name="collisions",
        ext_modules=cythonize(
            extensions,
            nthreads=6,
            language_level="3",
        ),
    )
    shutil.move('./'+fname, './generated/'+fname)

from setuptools import setup, Extension
from Cython.Build import cythonize
import os, sys, shutil, re

extensions = [
    Extension("collisions", ["lib/collisions.py"]),
]

# Build pyi stub file automatically
os.system("stubgen lib/collisions.py --include-docstrings")
shutil.copy('./out/BlazeSudio/collisions/lib/collisions.pyi', './collisions.pyi')

if '--no-build' not in sys.argv:
    setup(
        name="collisions",
        ext_modules=cythonize(extensions),
    )

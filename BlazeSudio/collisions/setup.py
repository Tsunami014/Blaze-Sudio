from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import shutil

extensions = [
Extension("collisions", ["lib/collisions.py"]),
]

# Build pyi stub file automatically
os.system("stubgen lib/collisions.py")
shutil.copy('./out/collisions/lib/collisions.pyi', './collisions.pyi')

setup(
   name="collisions",
   ext_modules=cythonize(extensions),
)
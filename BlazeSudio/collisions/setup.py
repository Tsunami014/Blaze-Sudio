from setuptools import setup, Extension
from Cython.Build import cythonize
import os, sys, shutil, re

extensions = [
    Extension("collisions", ["lib/collisions.py"]),
]

# Build pyi stub file automatically
os.system("stubgen lib/collisions.py --include-docstrings")
shutil.copy('./out/BlazeSudio/collisions/lib/collisions.pyi', './collisions.pyi')

oldfs = os.listdir('./')

if '--no-build' not in sys.argv:
    setup(
        name="collisions",
        ext_modules=cythonize(extensions),
    )

newfs = [i for i in os.listdir('./') if i not in oldfs]
for f in newfs:
    newname = re.sub('collisions\.cpython-\\d+-', '', f)
    if os.path.exists(newname):
        os.remove(newname)
    os.rename(f, newname)

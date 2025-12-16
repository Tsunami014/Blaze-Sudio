"""
python -m pip install cython setuptools
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import shutil
import sys
import os

os.chdir(os.path.dirname(__file__))

extensions = [
    Extension(
        "collisions",
        ["lib/collisions.py"],
        define_macros=[("Py_LIMITED_API", "0x030B0000")],
        py_limited_api=True
    ),
]

# Build pyi stub file automatically
if os.system("stubgen lib/collisions.py --include-docstrings") == 0:
    shutil.copy('./out/BlazeSudio/collisions/lib/collisions.pyi', './generated/collisions.pyi')
else:
    print("Failed to generate stub file!")

if len(sys.argv) == 1:
    sys.argv = [sys.argv[0], "build_ext", "--inplace"]
if '--no-build' not in sys.argv:
    setup(
        name="collisions",
        ext_modules=cythonize(
            extensions,
            nthreads=6,
            language_level="3",
            compiler_directives={'binding': False} # Often required for Limited API
        ),
        options={
            'bdist_wheel': {'py_limited_api': 'cp310'}
        }
    )
    if sys.platform == 'win32':
        ext = '.pyd'
    else:
        ext = '.abi3.so'
    shutil.move('./collisions'+ext, './generated/collisions'+ext)


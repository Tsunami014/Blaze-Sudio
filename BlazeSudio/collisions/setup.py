from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
Extension("collisions", ["lib/collisions.py"]),
]
setup(
    name="collisions",
    ext_modules=cythonize(extensions),
)
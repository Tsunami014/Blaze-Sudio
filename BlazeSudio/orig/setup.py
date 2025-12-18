"""
python -m pip install cython setuptools mypy
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import shutil
import sys
import os

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" <folder> [--no-stub] [--no-copy] [--no-build] [-h/--help]")
    exit()

os.chdir(os.path.abspath(__file__+"/../../../"))

folder = sys.argv[1]
NAME = folder
if '/' in NAME:
    NAME = NAME[NAME.rindex('/')+1:]

print("Running with folder", folder)

orig = f"BlazeSudio/orig/{folder}"
out = f"BlazeSudio/{folder}"
pack = f"BlazeSudio.{folder.replace('/', '.')}"
if not os.path.exists(out):
    os.mkdir(out)

ALLMODULES = [f[:-3] for f in os.listdir(orig) if f[-3:] == '.py']
MODULES = [f for f in ALLMODULES if f[0] != '_' or f == '__init__']
NOCOMPILES = [f for f in ALLMODULES if f not in MODULES]

print(f"Found modules: {MODULES}, no-compile: {NOCOMPILES}")

extensions = [
    Extension(
        f"{pack}.{name}", [f"{orig}/{name}.py"],
        define_macros=[("Py_LIMITED_API", "0x030B0000")],
        py_limited_api=True
    )
    for name in MODULES
]

if '--no-stub' not in sys.argv:
    print("Generating stub files...")
    # Ensure that if the file was modified after the stub, the file must be newer so regenerate the stub, otherwise don't touch it
    def needs_stub(src, dst):
        if not os.path.exists(dst):
            return True
        return os.path.getmtime(src) > os.path.getmtime(dst)
    # Build pyi stub file automatically
    for name in MODULES:
        src = f"{orig}/{name}.py"
        dst = f"{out}/{name}.pyi"
        if not needs_stub(src, dst):
            print(f"Stub up-to-date: {name}")
            continue

        print(f"Stubgening {name}...")
        if os.system(f"stubgen {src} --include-docstrings") != 0:
            raise RuntimeError(
                f"Problem with stubgen on file `{src}`!"
            )
        shutil.move(
            f"./out/{src}i",
            f"{dst}.pyi"
        )

if '--no-copy' not in sys.argv:
    if len(NOCOMPILES) > 0:
        print("Copying non-compile modules...")
        for name in NOCOMPILES:
            shutil.copy(
                f"{orig}/{name}.py",
                f"{out}/{name}.py"
            )
            print(f"Copied {name}!")

if '--no-build' not in sys.argv:
    print("Compiling files...")
    sys.argv = [sys.argv[0], "build_ext", "--inplace"]
    setup(
        name=NAME,
        ext_modules=cythonize(
            extensions,
            nthreads=6,
            language_level="3",
            compiler_directives={'binding': False}
        ),
        options={
            'bdist_wheel': {'py_limited_api': 'cp311'}
        }
    )

print("Finished all operations for "+folder+"!")


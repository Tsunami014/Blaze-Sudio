def Compile(folder, main = None):
    """
    python -m pip install cython setuptools mypy
    """
    from setuptools import setup, Extension
    from Cython.Build import cythonize
    import shutil
    import sys
    import os

    NAME = folder
    if '/' in NAME:
        NAME = NAME[NAME.rindex('/')+1:]

    DEFAULT = ("build_ext", "--inplace")
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: "+sys.argv[0]+" [--no-stub] [--no-main-stub] [--no-build] [-h/--help] [..setuptools args]")
        print("If no setuptools args specified, will use `"+" ".join(DEFAULT)+"`")
        exit()

    init = f"BlazeSudio/{folder}/lib"
    gen = f"./out/BlazeSudio/{folder}/lib"
    out = f"./BlazeSudio/{folder}/generated"
    pack = f"BlazeSudio.{folder.replace('/', '.')}.generated"
    if not os.path.exists(out):
        os.mkdir(out)

    def test_file(fname):
        with open(f'{init}/{fname}') as f:
            return f.readline() != '# NO-COMPILE'

    MODULES = [f[:-3] for f in os.listdir(init) if f[-3:] == '.py' and f != '__init__.py' and test_file(f)]

    print("Found modules:", MODULES)

    extensions = [
        Extension(
            f"{pack}.{name}", [f"{init}/{name}.py"],
            define_macros=[("Py_LIMITED_API", "0x030B0000")],
            py_limited_api=True
        )
        for name in MODULES
    ]

    if '--no-stub' in sys.argv:
        sys.argv.remove('--no-stub')
    else:
        print("Generating stub files...")
        # Build pyi stub file automatically
        if os.system("stubgen") != 0:
            raise ValueError(
                "Stubgen command does not exist!"
            )
        for name in MODULES:
            print(f"Stubgening {name}...")
            if os.system(f"stubgen {init}/{name}.py --include-docstrings") != 0:
                raise RuntimeError(
                    f"Problem with stubgen on file `{init}/{name}.py`!"
                )
            shutil.copy(
                f"{gen}/{name}.pyi",
                f"{out}/{name}.pyi"
            )

    if '--no-main-stub' in sys.argv:
        sys.argv.remove('--no-main-stub')
    else:
        print("Generating main stub...")
        with open(f"./BlazeSudio/{folder}/__init__.pyi", "w+") as f:
            f.write(
                ""
            )

    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], *DEFAULT]
    if '--no-build' not in sys.argv:
        print("Compiling files...")
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

def _InitSetup(file, name, main=None):
    import sys
    import importlib
    import os

    MODULES = [f[:-3] for f in os.listdir(os.path.dirname(file)+'/lib') if f[-3:] == '.py' and f != '__init__.py']
    FAILEDS = []
    for nam in MODULES:
        mod = None
        if os.environ.get('BSdebugGraphicsCore', '0') != '1':
            try:
                mod = importlib.import_module(f".generated.{nam}", name)
            except ImportError: # If the file has no-compile, it won't be generated
                FAILEDS.append(mod) # It's still a good idea to keep a list of these in case it wasn't purposefully failing
        if mod is None:
            mod = importlib.import_module(f".lib.{nam}", name)
        sys.modules[f"{name}.{nam}"] = mod
        globals()[nam] = mod

    if main is not None:
        mainmod = sys.modules[f"{name}.{main}"]
        globals().update({
            i: getattr(mainmod, i) for i in mainmod.__all__
        })

    return FAILEDS


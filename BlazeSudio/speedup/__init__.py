try:
    import numba
    from numba.pycc import CC
except ImportError:
    numba = None
    CC = None
from importlib import import_module
from inspect import getfile
import os
import sys
import json

def requireNumba():
    if numba is None:
        raise ImportError(
            'This requires numba to be present, but it failed to import!'
        )

__all__ = ['setSpeedupType', 'jitrix']

SPEEDUP_TYP = 0

def setSpeedupType(newTyp: int):
    """
    Set the speedup type.

    Speedup types:
        0: No speed up. Uses cached compiled func if exists, otherwise use regular Python. Does not require numbita; if not present, will not use.
        1: JIT. Caches and runs the just in time compilation. First run will be slow, but all subsequent runs will be fast. Will require numbita.
    """
    global SPEEDUP_TYP
    newTyp = int(newTyp)
    if newTyp < 0 or newTyp > 1:
        raise ValueError(
            f'Speedup type must be between 0-1, found {newTyp}!'
        )
    if newTyp == 1:
        requireNumba()
    SPEEDUP_TYP = newTyp

# MODULES maps module_name -> {'funcs': [(func, sig, wrapped_func, test_case)], 'compiled': None or module}
MODULES = {}


def _compile_module(module_name):
    # Lazy load for efficiency (this function won't be called every run)
    import glob
    if 'BlazeSudio.speedup.cache' not in sys.modules:
        sys.modules['BlazeSudio.speedup.cache'] = import_module('BlazeSudio.speedup.cache')

    # Purge existing files
    cpth = os.path.abspath(__file__+'/../cache/')+'/'
    for m in glob.glob(cpth+module_name+'*'):
        os.remove(m)
    
    cc = CC(module_name, 'BlazeSudio.speedup.cache')
    INFO = {}
    for func, sig, _, __ in MODULES[module_name]['funcs']:
        cc.export(func.__name__, sig)(func)
        pth = getfile(func)
        if pth not in INFO:
            stat = os.stat(pth)
            INFO[pth] = [stat.st_size, stat.st_mtime]
    cc.compile()

    with open(cpth+module_name+'.info', 'w+') as f:
        json.dump(INFO, f)

def _get_module(module_name, error_on_modif=False):
    """
    Attempt to get the module and json and return it, otherwise will return None.

    keyword argument `error_on_modif`, if True, will error if it finds a function modified from the original file, whereas False (the default) will just return None
    """
    pth = os.path.abspath(__file__+f'/../cache/{module_name}.info')
    if os.path.exists(pth):
        with open(pth) as f:
            j = json.load(f)
    else:
        return None
    
    try:
        for pth, stat1 in j.items():
            fullstat2 = os.stat(pth)
            stat2 = [fullstat2.st_size, fullstat2.st_mtime]
            if stat1 != stat2:
                if error_on_modif:
                    raise ValueError(
                        f'File {pth} differs from compiled version!\n(size, modification time)\nOld stat: {stat1}\nNew stat: {stat2}'
                    )
                return None
    except FileNotFoundError as e:
        if error_on_modif:
            raise e
        return None

    modpath = f'BlazeSudio.speedup.cache.{module_name}'
    try:
        mod = import_module(modpath)
        return (mod, j)
    except ImportError:
        return None

def _get_compiled_module(module_name):
    """
    Attempt to import the compiled module. If not found, compile it and import again.
    """
    mod = _get_module(module_name)
    if mod is None:
        _compile_module(module_name)
        mod = _get_module(module_name)
        if mod is None:
            raise ValueError(
                f'Could not get just compiled mod! Compiled module exists: {mod[0] is not None}, JSON info exists: {mod[1] is not None}'
            )
    MODULES[module_name]['compiled'] = mod
    return mod

def jitrix(module: str, sig: str, test: str):
    """
    Runs the JIT compilation depending on the speedup type set.

    This is a function wrapper. Use it as `@jitrix(*args)`.

    Args:
        module: The module (set of functions) this one belongs to. All module funcs will be compiled at the same time (not one individually), so keep separate modules separate.
        sig: The function signature (see https://numba.pydata.org/numba-doc/dev/reference/types.html)
        test: The args to run when testing this func
    """
    def decorator(func):
        # Register the function for this module
        if module not in MODULES:
            MODULES[module] = {'funcs': [], 'compiled': None}

            mod = _get_module(module)
            if mod is not None:
                MODULES[module]['compiled'] = mod

        wrapper = None
        if SPEEDUP_TYP == 0:
            compiled_mod = MODULES[module]['compiled']
            if compiled_mod is not None:
                try:
                    wrapper = getattr(compiled_mod[0], func.__name__)
                except AttributeError:
                    pass
            if wrapper is None:
                wrapper = func
        else:
            def wrapper(*args, **kwargs):
                compiled_mod = MODULES[module]['compiled']
                if compiled_mod is None:
                    compiled_mod = _get_compiled_module(module)
                    MODULES[module]['compiled'] = compiled_mod
                getattr(compiled_mod[0], func.__name__)(*args, **kwargs)
        MODULES[module]['funcs'].append((func, sig, wrapper, test))
        return wrapper
    return decorator


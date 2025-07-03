try:
    import numba
    from numba.pycc import CC
except ImportError:
    numba = None
    CC = None
from importlib import import_module
import sys

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
    if 'BlazeSudio.speedup.cache' not in sys.modules:
        sys.modules['BlazeSudio.speedup.cache'] = import_module('BlazeSudio.speedup.cache')
    
    cc = CC(module_name, 'BlazeSudio.speedup.cache')
    for func, sig, _, __ in MODULES[module_name]['funcs']:
        cc.export(func.__name__, sig)(func)
    cc.compile()

def _get_compiled_module(module_name):
    """
    Attempt to import the compiled module. If not found, compile it and import again.
    """
    modpath = f'BlazeSudio.speedup.cache.{module_name}'
    try:
        mod = import_module(modpath)
    except ImportError:
        _compile_module(module_name)
        mod = import_module(modpath)
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

        def wrapper(*args, **kwargs):
            # SPEEDUP_TYP logic
            if SPEEDUP_TYP == 0:
                compiled_mod = MODULES[module]['compiled']
                if compiled_mod is not None:
                    # Try to get compiled version
                    try:
                        compiled_func = getattr(compiled_mod, func.__name__)
                        return compiled_func(*args, **kwargs)
                    except AttributeError:
                        pass
                # Fallback to Python version
                return func(*args, **kwargs)
            else:
                # JIT/AOT case: ensure compiled module exists
                compiled_mod = MODULES[module]['compiled']
                if compiled_mod is None:
                    compiled_mod = _get_compiled_module(module)
                compiled_func = getattr(compiled_mod, func.__name__)
                return compiled_func(*args, **kwargs)
        MODULES[module]['funcs'].append((func, sig, wrapper, test))
        return wrapper
    return decorator


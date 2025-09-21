try:
    import numba
    from numba.pycc import CC
except ImportError:
    numba = None
    CC = None
try:
    import numpy as np
except ImportError:
    np = None
from importlib import import_module
import typing
import inspect
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
        cc.export(func.__name__, sig)(func) # If this errors, your signature is wrong or something
        pth = inspect.getfile(func)
        if pth not in INFO:
            stat = os.stat(pth)
            INFO[pth] = [stat.st_size, stat.st_mtime]
    cc.compile() # If this errors, your code failed to compile (could be signature?)

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


def _check_arg(arg):
    if isinstance(arg, type):
        try:
            return numba.from_dtype(arg)
        except Exception:
            pass
    return arg

def _handle_param(p, func):
    if p.kind not in (inspect._ParameterKind.POSITIONAL_ONLY, inspect._ParameterKind.POSITIONAL_OR_KEYWORD):
        raise ValueError(
            f'Param kind must be positional, found {p.kind._name_}! (file {inspect.getfile(func)}, function {func.__name__}, param {p.name})'
        )
    if p.annotation is inspect._empty:
        raise ValueError(
            f'Type hint must be present! (file {inspect.getfile(func)}, function {func.__name__}, param {p.name})'
        )
    ann = p.annotation
    if isinstance(ann, str):
        return eval(ann, {'typing': typing, 'numba': numba, 'np': numba, 'numpy': numba}, {})
    if hasattr(ann, '__args__'):
        ann.__args__ = tuple(_check_arg(i) for i in ann.__args__)
    else:
        ann = _check_arg(ann)
    return numba.extending.as_numba_type(ann)

def _convert_arg(typ, given):
    etyp = type(typ)
    if type(given) is np.ndarray and etyp is numba.types.Array:
        reqdtyp = np.dtype(typ.dtype.name)
        if given.dtype != reqdtyp:
            arr = given.astype(reqdtyp)
        else:
            arr = given
        nord = typ.layout
        if nord == 'C':
            if not arr.flags['C_CONTIGUOUS']:
                arr = np.ascontiguousarray(arr)
        elif nord == 'F':
            if not arr.flags['F_CONTIGUOUS']:
                arr = np.asfortranarray(arr)
        if len(arr.shape) != typ.ndim:
            raise ValueError(
                f"Given array is incorrect! Expected {arr.ndim} dimensions, found {len(arr.shape)}!"
            )
        return arr
    # Check for other special types
    if etyp is numba.types.Array:
        arr = np.array(given, dtype=np.dtype(typ.dtype.name), order=typ.layout)
        if len(arr.shape) != typ.ndim:
            raise ValueError(
                f"Given array is incorrect! Expected {arr.ndim} dimensions, found {len(arr.shape)}!"
            )
        return arr
    if etyp is numba.types.UniTuple:
        if len(given) != typ.count:
            raise ValueError(
                f'Argument must be of length {typ.count}, found {len(given)}!'
            )
        return tuple(
            np.dtype(t.name).type(g) for t, g in zip(typ.types, given)
        )
    # Attempt to convert to a numpy type
    try:
        dtyp = np.dtype(typ.name).type
    except TypeError: # Raise a more descriptive error
        raise ValueError(
            f'Unable to convert numba type {type(typ)}!'
        )
    if given is dtyp: # Don't convert if don't need to
        return given
    return dtyp(given) # Try converting to the required numpy type


def jitrix(module: str, test: str):
    """
    Runs the JIT compilation depending on the speedup type set.

    This is a function wrapper. Use it as `@jitrix(*args)`.

    Args:
        module: The module (set of functions) this one belongs to. All module funcs will be compiled at the same time (not one individually), so keep separate modules separate.
        test: The args to run when testing this func

    You are required to have type annotations to use this wrapper. The type annotations can be:
    - typing annotations (e.g. `typing.List`)
    - basic python types (e.g. `int`)
    - numpy types (e.g. `np.uint32`)
    - strings which handle other scenarios, such as arrays (`"np.uint32[:]"`) (notice in strings, only typing and numba are avaliable to use; 'numpy' and 'np' both redirect to numba)
    I'm sure you'll be fine. If not, well... good luck
    """
    def decorator(func):
        # If numba is not present, either stick with python or error (depending on speedup type)
        if numba is None:
            if SPEEDUP_TYP == 0:
                return func
            requireNumba() # Should raise an error

        # Get all the arguments and their type annotations
        sig = inspect.signature(func)
        retAnn = sig.return_annotation
        if retAnn is inspect._empty:
            retSig = 'void'
        else:
            retSig = numba.extending.as_numba_type(retAnn)
        params = sig.parameters.values()
        paramsSigs = [_handle_param(p, func) for p in params]
        sig = f'{retSig}({", ".join(repr(i) for i in paramsSigs)})'

        # Register the function for this module
        if module not in MODULES:
            MODULES[module] = {'funcs': [], 'compiled': None}

            mod = _get_module(module)
            if mod is not None:
                MODULES[module]['compiled'] = mod

        def wrapper(*args, **kwargs):
            compiled_mod = MODULES[module]['compiled']
            if SPEEDUP_TYP == 0:
                run = None
                if compiled_mod is not None:
                    try:
                        run = getattr(compiled_mod[0], func.__name__)
                    except AttributeError:
                        pass
                if run is None:
                    run = func
            else:
                if compiled_mod is None:
                    compiled_mod = _get_compiled_module(module)
                    MODULES[module]['compiled'] = compiled_mod
                run = getattr(compiled_mod[0], func.__name__)

            if kwargs != {}:
                raise TypeError(
                    'Compiled functions cannot have keyword arguments!'
                )

            if len(args) != len(paramsSigs):
                raise TypeError(
                    f'Expected {len(paramsSigs)} arguments, found {len(args)}!'
                )
            args = [_convert_arg(p, a) for p, a in zip(paramsSigs, args)]

            return run(*args)
        MODULES[module]['funcs'].append((func, sig, wrapper, test))
        return wrapper
    return decorator


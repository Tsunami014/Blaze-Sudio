from typing import Iterable
from BlazeSudio.speedup import _compile_module, _get_module
from importlib import import_module

__all__ = ['sects', 'compile', 'isCached']

sects = {
    # import path, module name
    0: ('graphicsCore', 'draw')
}

def compile(sections: Iterable[int] = None):
    """
    Compile BlazeSudio's internal functions to make them faster!

    Args:
        sections: The specific sections to compile, defaults to all of them

    Sections:
        0: The graphics core
    """
    if sections is None:
        sections = list(sects.keys())

    for s in sections:
        impModuleName, moduleName = sects[s]
        import_module('BlazeSudio.'+impModuleName) # To ensure the funcs exist
        _compile_module(moduleName)

def isCached(module: str):
    """
    Check if a module is cached

    Args:
        module: The module to check
    """
    return _get_module(module) is not None


import re
import sys
import os.path
import importlib.util
from enum import Enum
from importlib.resources import files

import BlazeSudio.elementGen.types as Ts

def allCategories():
    cats = [i.name for i in (files('BlazeSudio') / 'data/nodes').iterdir() if i.is_file() and i.name != 'types.json']
    cats.sort()
    return cats

def getCategoryNodes(category):
    filepath = os.path.abspath((files('BlazeSudio') / ('data/nodes/'+category)).joinpath())
    module_name = '0GameIO'
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return [Node(getattr(module, i)) for i in dir(module) if not i.startswith('_')]

def getAllNodes():
    ns = []
    for cat in allCategories():
        ns.extend(getCategoryNodes(cat))
    return ns

class Mods(Enum):
    """Modifiers for inputs and outputs!"""
    NoShow = 0
    """Do not show this input/output on the node, only in the sidebar"""

class InOut:
    def __init__(self, parent, isinput, name, type, desc, default=None, mods=[]):
        self.parent = parent
        self.isinput = isinput
        self.name = name.strip()
        self.type = Ts.types[type.strip().lower()]
        self.strtype = Ts.strtypes[self.type]
        self.desc = desc.strip()
        self.mods = mods
        if default is None:
            default = Ts.defaults[self.strtype]
        self.value = default
    
    def canAccept(self, otherinout):
        return self.isinput != otherinout.isinput and self.parent != otherinout.parent
    
    def __str__(self):
        return f'<{"Input" if self.isinput else "Output"} "{self.name}", of type {type(self.type)} with value {self.value}>'
    def __repr__(self): return str(self)

class Node:
    NEXTUID = [0]
    def __init__(self, func):
        self.uid = self.NEXTUID[0]
        self.NEXTUID[0] += 1
        self.func = func
        doc = [i.strip() for i in func.__doc__.split('\n') if i.strip()]
        self.name = doc[0]
        self.desc = '\n'.join(doc[1:doc.index('Args:')])
        # inspect.signature(func).parameters
        checkMods = ['@'+i[0] for i in Mods.__members__.items()]
        # Isn't she beautiful? 🥹
        checkRegex = '^(.+?)[ \t]*?(?:\\((.*?)\\))?(?::[ \t]*?([^ ].*?))?[ \t]*$'
        self.inputs = []
        for i in doc[doc.index('Args:')+1:doc.index('Returns:')]:
            mods = []
            for m in checkMods:
                if m in i:
                    mods.append(getattr(Mods, m[1:]))
                    i = i.replace(m, '')
            self.inputs.append(InOut(self, True, *re.findall(checkRegex, i)[0], None, mods)) # TODO: Default values (i.e. where the None is)
        self.outputs = []
        for i in doc[doc.index('Returns:')+1:]:
            mods = []
            for m in checkMods:
                if m in i:
                    mods.append(getattr(Mods, m[1:]))
                    i = i.replace(m, '')
            self.outputs.append(InOut(self, False, *re.findall(checkRegex, i)[0], None, mods))
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def copy(self):
        return Node(self.func)
    
    def __str__(self):
        return f'<Node {self.name} with {len(self.inputs)} inputs and {len(self.outputs)} outputs>'
    def __repr__(self): return str(self)
    
    def __hash__(self):
        return hash((self.uid, self.name, self.desc, self.func))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return hash(self) != hash(other)

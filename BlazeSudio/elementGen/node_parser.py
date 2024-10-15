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
    NoNode = 0
    """Do not show this input/output on the node, only in the sidebar"""
    NoSidebar = 1
    """Do not show this input/output in the sidebar, only on the node"""
    LeaveName = 2
    """Do not replace the name of the output node with it's actual output"""
    ShowEqual = 3
    """Instead of replacing the name of the output node with it's output, include it
This would look like `Val: abc` instead of just replacing the node name (`Val`) with it's value (`abc`)"""

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

    def __hash__(self):
        return hash((self.parent, self.isinput, self.name))

    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return hash(self) != hash(other)

class Node:
    NEXTUID = [0]
    def __init__(self, func):
        self.uid = self.NEXTUID[0]
        self.NEXTUID[0] += 1
        self.func = func
        doc = [i.strip() for i in func.__doc__.split('\n') if i.strip()]
        self.name = doc[0]
        if 'Args:' in doc:
            docUpTo = doc.index('Args:')
        elif 'Returns:' in doc:
            docUpTo = doc.index('Returns:')
        else:
            docUpTo = len(doc)
        self.desc = '\n'.join(doc[1:docUpTo])
        # inspect.signature(func).parameters
        checkMods = ['@'+i[0] for i in Mods.__members__.items()]
        # Isn't she beautiful? 🥹
        checkRegex = '^(.+?)[ \t]*?(?:\\((.*?)\\))?(?::[ \t]*?([^ ].*?))?[ \t]*$'
        if 'Returns:' in doc:
            retIdx = doc.index('Returns:')
        else:
            retIdx = len(doc)
        self.inputs = []
        if 'Args:' in doc:
            for i in doc[doc.index('Args:')+1:retIdx]:
                mods = []
                for m in checkMods:
                    if m in i:
                        mods.append(getattr(Mods, m[1:]))
                        i = i.replace(m, '')
                self.inputs.append(InOut(self, True, *re.findall(checkRegex, i)[0], None, mods)) # TODO: Default values (i.e. where the None is)
        self.outputs = []
        if retIdx != len(doc):
            for i in doc[retIdx+1:]:
                mods = []
                for m in checkMods:
                    if m in i:
                        mods.append(getattr(Mods, m[1:]))
                        i = i.replace(m, '')
                self.outputs.append(InOut(self, False, *re.findall(checkRegex, i)[0], None, mods))
    
    def run(self, conns):
        ret = self.func(*[
            i.value if (self, i) not in conns else (
                conns[(self, i)][0].run(conns)[conns[(self, i)][0].outputs.index(conns[(self, i)][1])]
            ) for i in self.inputs
        ])
        if not isinstance(ret, list):
            return [ret]
        return ret
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def copy(self):
        return Node(self.func)
    
    def __str__(self):
        return f'<Node {self.name} with {len(self.inputs)} inputs and {len(self.outputs)} outputs>'
    def __repr__(self): return str(self)
    
    def __hash__(self):
        return hash((self.uid, self.name, self.desc, self.func))
    
    def TypeHash(self):
        return sum(ord(i) for i in self.name)*sum(ord(i) for i in self.desc)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return hash(self) != hash(other)

import os
from random import random
from copy import deepcopy
import elementGen.types as Ts

def allCategories():
    return [i.name for i in os.scandir('data/nodes') if i.is_file()]

class FakeDict(dict):
    def __init__(self, func=lambda: None, clearfunc=lambda: None):
        self.func = func
        self.clearfunc = clearfunc
    def __setitem__(self, __key, __value):
        try:
            self.func(__key, __value)
        except AttributeError: pass
        return super().__setitem__(__key, __value)
    def reset(self):
        for i in self:
            self.clearfunc(i, None)
        self.clear()

class Connector:
    def __init__(self, parent, isinp, name, typ='any'):
        self.num = random()
        self.parent = parent
        self.isinp = isinp
        self.name = name
        self.type = Ts.types[typ]
        self.rect = None
        self.value = Ts.defaults[typ]
        self.connectedto = None # Relying on externs to generate
    def isntsimilar(self, other):
        try:
            return self.parent != other.parent and self.isinp != other.isinp
        except: return False
    def copy(self):
        c = deepcopy(self)
        c.num = random()
        return c
    def __eq__(self, other):
        return hash(self) == hash(other)
        try:
            A = lambda a: getattr(self, a) == getattr(other, a)
            return A('isinp') and A('name') and A('type')# and A('parent') # We comment out this as it's annoying as hell to work with
        except: return False # Didn't have one of the attributes
    def __str__(self): return f'<Node "{self.name}" ({self.type}), parent: {str(self.parent)}, is an {"input" if self.isinp else "output"}>'
    def __repr__(self): return str(self)
    def __hash__(self): return hash(self.parent) + hash(self.num)

class Names:
    def __init__(self, data):
        self.num = random()
        self.rdata = data.strip(' \n')
        spl = self.rdata.split(' ')
        self.name = spl[0]
        self.inputs = []
        self.outputs = []
        self.cirs = FakeDict(self.setter, self.setter) # Relying on externals to generate
        self.func = None # Also relying on externals to generate, tho this time the 'externals' is the Parse class
        input = True
        for i in spl[1:]:
            if i == '|':
                input = False
                continue
            if input:
                s = i.split('@')
                self.inputs.append(Connector(self, True, s[1], s[0]))
            else:
                self.outputs.append(Connector(self, False, i))
    def setter(self, key, value):
        for i in range(len(self.inputs)):
            if self.inputs[i] == key:
                self.inputs[i].rect = value
                return
        for i in range(len(self.outputs)):
            if self.outputs[i] == key:
                self.outputs[i].rect = value
                return
        raise IndexError(
            'Could not find key in list!!'
        )
    def copy(self):
        c = deepcopy(self)
        c.num = random()
        """c.cirs = FakeDict(self.setter, self.setter)
        iis = []
        for i in c.inputs:
            iis.append(i.copy())
        c.inputs = iis
        oos = []
        for i in c.outputs:
            oos.append(i.copy())
        c.outputs = oos"""
        return c
    def get(self):
        ins = []
        for i in self.inputs:
            try:
                ins.append(i.connectedto.parent.get()[i.connectedto.name])
            except:
                ins.append(i.value)
        try:
            return self(*ins)
        except:
            return {}
    def __call__(self, *args):
        exec(self.func)
        return eval('node(*args)')
    
    def __str__(self):
        try:
            return self.name
        except AttributeError: return 'A Name object'
    def __repr__(self): return str(self)
    def __hash__(self):
        try:
            return hash(self.num)
        except AttributeError: return hash(str(self))

class Parse:
    def __init__(self, category):
        if not category.endswith('.py'): category += '.py'
        self.category = category
        self.rdata = open('data/nodes/'+category).read()
        self.data = {}
        pattern = 0
        spl = self.rdata.split('#')[1:]
        self.names = {}
        for i in spl:
            i = i.strip(' \n')
            if pattern == 0:
                i = Names(i)
                pattern = i
                self.names[str(i)] = i
            else:
                self.data[pattern] = i
                pattern.func = i
                pattern = 0
    def __call__(self, funcname, *args):
        exec(self.data[self.names[funcname]])
        return eval('node(*args)')
    
    def __str__(self): return self.category[:-3]
    def __repr__(self): return str(self)
    
    def getall(self):
        return list(self.data.keys())

def allNodes(category):
    return Parse(category).getall()

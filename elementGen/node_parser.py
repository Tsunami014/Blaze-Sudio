import os
from random import random
from copy import deepcopy
import elementGen.types as Ts
import re, inspect
from typing import Any
import ast

def allCategories():
    l = [i.name for i in os.scandir('data/nodes') if i.is_file()]
    l.sort()
    return l

def parse_func(funcstr):
    return dict(zip(re.findall(r'(?<=\@).+?(?=\()', funcstr), \
                    [ast.literal_eval(i) for i in re.findall(r"@.+?\((.+?)\)\n", funcstr)])), \
           re.findall(r'(@.+\n)*(((.+)\n?)+)', funcstr)[0][1]

class FakeDict():
    def __init__(self, func=lambda: None, clearfunc=lambda: None):
        self.func = func
        self.clearfunc = clearfunc
        self.d = {}
    def __setitem__(self, __key, __value):
        try:
            self.func(__key, __value)
        except AttributeError: pass
        self.d[__key] = __value
    
    def __getitem__(self, __key):
        return self.d[__key]
    
    def __str__(self): return str(self.d)
    def __repr__(self): return str(self.d)

    def reset(self):
        for i in self.d:
            self.clearfunc(i, None)
        self.d = {}

class Connector:
    def __init__(self, parentHASH, parentNAME, isinp, name, typ='any'):
        self.pHASH = parentHASH
        self.pNAME = parentNAME
        self.num = random()
        self.isinp = isinp
        self.name = name
        self.type = Ts.types[typ]
        self.rect = None
        self.value = Ts.defaults[typ]
        self.connectedto = None # Relying on externs to generate
    def get_CT(self, nodeL):
        '''Get the connected Connector object'''
        if self.connectedto is None: return None
        if self.connectedto[1]: return nodeL[self.connectedto[0]][1].inputs[self.connectedto[2]]
        else: return nodeL[self.connectedto[0]][1].outputs[self.connectedto[2]]
    def gen_CT(self, nodeL):
        '''Make a list compatible with being put in anothers' connectedto'''
        if self.isinp: idx = self.get_P(nodeL).inputs.index(self)
        else: idx = self.get_P(nodeL).outputs.index(self)
        return [[i[1] for i in nodeL].index(self.get_P(nodeL)), self.isinp, idx]
    def get_P(self, nodeL):
        return nodeL[[i[1].num for i in nodeL].index(self.pHASH)][1]
    def isntsimilar(self, other):
        try:
            return self.pHASH != other.pHASH and self.isinp != other.isinp
        except: return False
    def copy(self):
        c = deepcopy(self)
        c.num = random()
        return c
    def __eq__(self, other):
        return hash(self) == hash(other)
        try:
            A = lambda a: getattr(self, a) == getattr(other, a)
            return A('isinp') and A('name') and A('type')# and A(.get_P(') # We comment out this as it's annoying as hell to work with
        except: return False # Didn't have one of the attributes
    def __str__(self): return f'<Node "{self.name}" ({self.type}), parent: {str(self.pNAME)}, is an {"input" if self.isinp else "output"}>'
    def __repr__(self): return str(self)
    def __hash__(self): return hash(self.pHASH) + hash(self.num)

class Names:
    def __init__(self, func, data, nodeL):
        self.num = random()
        self.rfunc = func.strip(' \n')
        self.data = data
        self.name = data['Name']
        self.inputs = []
        self.outputs = []
        self.cirs = FakeDict(self.setter, self.setter) # Relying on externals to generate
        self.func = func
        exec(self.func)
        self.node = eval('node')
        self.doc = self.node.__doc__
        for i in inspect.signature(self.node).parameters.items():
            self.inputs.append(Connector(self.num, str(self), True, i[1].name, Ts.strtypes[i[1].annotation]))
            if i[1].default != inspect._empty:
                self.inputs[-1].value = i[1].default
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
        for i in c.inputs + c.outputs:
            i.pHASH = c.num
        return c
    def get(self, nodeL):
        ins = []
        for i in self.inputs:
            try:
                ins.append(i.get_CT(nodeL).get_P(nodeL).get(nodeL)[i.get_CT(nodeL).name])
            except:
                ins.append(i.value)
        try:
            outs = self(*ins)
            outnames = [i.name for i in self.outputs]
            inouts = [i for i in outs.keys() if i in outnames]
            notinouts = [i for i in outs.keys() if i not in outnames]
            dels = []
            for i in self.outputs:
                if i.name not in inouts: dels.append(i)
            for i in dels: self.outputs.remove(i)
            for i in notinouts:
                self.outputs.append(Connector(self.num, str(self), False, i, Ts.getType(outs[i])))
                self.outputs[-1].value = outs[i]
            return outs
        except:
            return {}
    def __call__(self, *args):
        return self.node(*args)
    
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
    def __init__(self, category, nodeL):
        if not category.endswith('.py'): category += '.py'
        self.category = category
        self.rfunc = open('data/nodes/'+category).read()
        self.data = {}
        spl = self.rfunc.split('\n#======#\n')[1:]
        self.names = {}
        for i in spl:
            i = i.strip(' \n')
            name = re.findall('(?<=def ).+?(?=\\()', i)[0]
            i = i.replace(name, 'node', 1)
            vals, func = parse_func(i)
            vals['Name'] = name
            i = Names(func, vals, nodeL)
            nodeL.append(i)
            self.names[vals['Name']] = i
            self.data[i] = func
    def __call__(self, funcname, *args):
        exec(self.data[self.names[funcname]])
        return eval('node(*args)')
    
    def __str__(self): return self.category[:-3].strip('0123456789')
    def __repr__(self): return str(self)
    
    def getall(self):
        return list(self.data.keys())

def allNodes(category):
    return Parse(category, []).getall()

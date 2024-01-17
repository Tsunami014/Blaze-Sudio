import os
from random import random
from copy import deepcopy
import elementGen.types as Ts
import re, inspect
from typing import Any

def allCategories():
    return [i.name for i in os.scandir('data/nodes') if i.is_file()]

def parse_func(funcstr):
    return dict(zip(re.findall(r'(?<=\@).+?(?=\()', funcstr), \
                    re.findall(r"@.+?\('(.+?)'\)\n", funcstr))), \
           re.findall(r'(@.+\n)+(((.+)\n?)+)', funcstr)[0][1]

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
    def __init__(self, func, data):
        self.num = random()
        self.rdata = func.strip(' \n')
        self.name = data['Name']
        self.inputs = []
        self.outputs = []
        self.cirs = FakeDict(self.setter, self.setter) # Relying on externals to generate
        self.func = func
        exec(self.func)
        self.node = eval('node')
        for i in inspect.signature(self.node).parameters.items():
            self.inputs.append(Connector(self, True, i[1].name, Ts.strtypes[i[1].annotation]))
            if i[1].default != inspect._empty:
                self.inputs[-1].value = i[1].default
        """input = True
        for i in spl[1:]:
            if i == '|':
                input = False
                continue
            if input:
                s = i.split('@')
                self.inputs.append(Connector(self, True, s[1], s[0]))
            else:
                self.outputs.append(Connector(self, False, i))"""
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
            outs = self(*ins)
            outnames = [i.name for i in self.outputs]
            inouts = [i for i in outs.keys() if i in outnames]
            notinouts = [i for i in outs.keys() if i not in outnames]
            dels = []
            for i in self.outputs:
                if i.name not in inouts: dels.append(i)
            for i in dels: self.outputs.remove(i)
            for i in notinouts:
                self.outputs.append(Connector(self, False, i))
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
    def __init__(self, category):
        if not category.endswith('.py'): category += '.py'
        self.category = category
        self.rdata = open('data/nodes/'+category).read()
        self.data = {}
        spl = self.rdata.split('\n#======#\n')[1:]
        untitleds = 0
        self.names = {}
        for i in spl:
            i = i.strip(' \n')
            vals, func = parse_func(i)
            if 'Name' not in vals:
                untitleds += 1
                vals['Name'] = f'Untitled{untitleds}'
            i = Names(func, vals)
            self.names[vals['Name']] = i
            self.data[i] = func
    def __call__(self, funcname, *args):
        exec(self.data[self.names[funcname]])
        return eval('node(*args)')
    
    def __str__(self): return self.category[:-3]
    def __repr__(self): return str(self)
    
    def getall(self):
        return list(self.data.keys())

def allNodes(category):
    return Parse(category).getall()

import pygame

# A Thing is a singular object
# A Stuff is a bunch of Things
# A Collection is a collection of layers of Stuff

class Container:
    pass

def handle_events():
    evs = pygame.event.get()
    cont = True
    for ev in evs:
        if ev.type == pygame.QUIT:
            cont = False
            break
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            cont = False
            break
    return evs, cont

class Thing:
    def __init__(self, obj):
        self.obj = obj
    
    def update(self, mousePos, events):
        return {self.obj: self.obj.update(mousePos, events)}

class Stuff:
    def __init__(self, categories=None):
        if categories is not None:
            self.categories = categories
        else:
            self.categories = {}
    
    def clear(self, ignores=[]):
        self.categories = {i: ([] if i not in ignores else self.categories[i]) for i in self.categories}

    def copy(self):
        return Stuff(self.categories.copy())
    
    def get(self):
        li = []
        for i in self.categories:
            li.extend(self.categories[i])
        return li
    
    def update(self, mousePos, events):
        returns = {}
        for i in self.categories:
            for j in self.categories[i]:
                returns[j] = j.update(mousePos, events)
        return returns
    
    def add(self, _name):
        self.categories[_name] = []
    
    def add_many(self, _names):
        self.categories.update({i: [] for i in _names if i not in self.categories})
    
    def remove(self, obj):
        for i in self.categories:
            if obj in self.categories[i]:
                self.categories[i].remove(obj)
    
    def __iter__(self):
        outl = []
        for i in self.categories.values():
            outl.extend(i)
        return iter(outl)
    
    def __len__(self):
        return len(self.get())
    
    def __getitem__(self, _key):
        return self.categories[_key]
    
    def __setitem__(self, _key, _value):
        self.categories[_key] = _value
        self.sync()
    
    def __str__(self):
        return '<Stuff with %i objects>'%len(self)
    def __repr__(self): return str(self)

class Collection:
    def __init__(self, layers=None):
        if layers is None:
            self.layers = [Stuff()]
        else:
            self.layers = layers
    
    def getall(self):
        alls = []
        for i in self.layers:
            alls.extend(i.get())
        return alls
    
    def remove(self, obj):
        for i in self.layers:
            if obj in i:
                i.remove(obj)
    
    def clear(self, ignores=[]):
        for i in self.layers:
            i.clear(ignores)
    
    def copy(self):
        return Collection([i.copy() for i in self.layers])
    
    def update(self, mousePos, events):
        outs = {}
        for i in self.layers:
            outs.update(i.update(mousePos, events))
        return outs
    
    def insert_layer(self, pos=-1):
        s = Stuff()
        self.layers.insert(pos, s)
        return s
    
    def __len__(self):
        return len(self.watch) + len(self.sprites)
    
    def __getitem__(self, _name):
        for i in self.layers:
            try:
                return i[_name]
            except KeyError:
                pass
        raise KeyError(
            f'Item {_name} does not exist in any layer!'
        )
    
    def __str__(self):
        return f'<Collection {self.layers}>'
    def __repr__(self): return str(self)

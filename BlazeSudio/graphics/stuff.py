import pygame

__all__ = [
    'Things',
    'Stuff',
    'Layers',
    'Collection',
]

# Stuff is an organisated dictionary of Things
# A Layer is a list that can be filled with Stuff
# A Collection is a collection of Layers of Stuff

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

class Things(list):
    def __init__(self, parent, data=()):
        self.parent = parent
        super().__init__((self._checkIt(i) for i in data))
    
    def _checkIt(self, it):
        if not it._init2Ran:
            it.G = self.parent
            it._init2()
            it._init2Ran = True
        return it
    
    def append(self, it):
        super().append(self._checkIt(it))
    
    def appendRaw(self, it):
        super().append(it)
    
    def extend(self, its):
        super().extend((self._checkIt(i) for i in its))
    
    def extendRaw(self, its):
        super().extend(its)
    
    def insert(self, index, it):
        super().insert(index, self._checkIt(it))
    
    def insertRaw(self, index, it):
        super().insert(index, it)
    
    def __iadd__(self, its):
        self.extend(its)
        return self

    def iaddRaw(self, its):
        self.extendRaw(its)
        return self
    
    def __add__(self, its):
        new_data = list(self)
        extra = [self._checkIt(i) for i in its]
        new_data.extend(extra)
        return Things(self.parent, new_data)
    
    def addRaw(self, its):
        new_data = list(self)
        new_data.extend(its)
        return Things(self.parent, new_data)
    
    def __getitem__(self, key):
        result = super().__getitem__(key)
        if isinstance(key, slice):
            return Things(self.parent, result)
        return result
    
    def __setitem__(self, key, value):
        if isinstance(key, slice):
            transformed = [self._checkIt(v) for v in value]
            super().__setitem__(key, transformed)
        else:
            super().__setitem__(key, value(self.parent))
    
    def setitemRaw(self, key, value):
        super().__setitem__(key, value)

class Stuff:
    def __init__(self, parent, categories=None):
        self.parent = parent
        if categories is not None:
            self.categories = categories
        else:
            self.categories = {}
    
    def clear(self, ignores=[]):
        self.categories = {i: (Things(self.parent) if i not in ignores else self.categories[i]) for i in self.categories}

    def copy(self):
        return Stuff(self.parent, self.categories.copy())
    
    def get(self):
        li = []
        for i in self.categories:
            li.extend(self.categories[i])
        return li
    
    def update(self, mousePos, events):
        returns = {}
        for i in self.categories:
            for j in self.categories[i]:
                returns[j] = j.UpdateDraw(mousePos.copy(), events)
                if returns[j] and -1 in returns[j]:
                    return
        return returns
    
    def add(self, _name):
        if _name not in self.categories:
            self.categories[_name] = Things(self.parent)
    
    def add_many(self, _names):
        self.categories.update({i: Things(self.parent) for i in _names if i not in self.categories})
    
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
        ln = 0
        for i in self.categories:
            ln += len(self.categories[i])
        return ln
    
    def __getitem__(self, _key):
        return self.categories[_key]
    
    def __setitem__(self, _key, _value):
        if _key not in self.categories:
            raise KeyError(
                f'Category {_key} does not exist!'
            )
        if not isinstance(_value, Things):
            self.categories[_key] = Things(self.parent, _value)
        else:
            self.categories[_key] = _value
    
    def __str__(self):
        return '<Stuff with %i objects>'%len(self)
    def __repr__(self): return str(self)

class Layers(list):
    def __init__(self, parent, data=()):
        self.parent = parent
        super().__init__(data)
    
    def __getitem__(self, _idx):
        if not isinstance(_idx, int):
            raise TypeError(
                'Index must be an integer!'
            )
        if _idx >= len(self):
            self.extend([Stuff(self.parent) for _ in range(_idx - len(self) + 1)])
        
        return super().__getitem__(_idx)

    def copy(self):
        return Layers(self.parent, iter(self))

    def __str__(self):
        return f'<Layers {super().__str__()}>'
    def __repr__(self):
        return f'<Layers {super().__repr__()}>'

class Collection:
    def __init__(self, parent, layers=None):
        self.parent = parent
        if layers is None:
            self.layers = Layers(self.parent, [Stuff(self.parent)])
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
        return Collection(self.parent, Layers(self.parent, [i.copy() for i in self.layers]))
    
    def insert_layer(self, pos=None) -> Stuff:
        if pos is None:
            pos = len(self.layers)
        s = Stuff(self.parent)
        self.layers.insert(pos, s)
        return s
    
    def __len__(self):
        return sum(len(i) for i in self.layers)

    def __iter__(self):
        for i in self.layers:
            for j in i.get():
                yield j
    
    def __getitem__(self, _name):
        for i in self.layers:
            try:
                return i[_name]
            except KeyError:
                pass
        raise KeyError(
            f'Item {_name} does not exist in any layer!'
        )
    
    def __setitem__(self, _name, _value):
        for i in self.layers:
            try:
                i[_name] = _value
                return
            except KeyError:
                pass
        raise KeyError(
            f'Item {_name} does not exist in any layer!'
        )
    
    def __str__(self):
        return f'<Collection {self.layers}>'
    def __repr__(self): return str(self)

class Container:
    pass

class Stuff:
    NAMES = []

    def __init__(self, overrideCategories=None):
        if overrideCategories is None:
            self.setup()
        else:
            self.categories = overrideCategories
            self.watch = self.categories.copy()
            self.sync()
    
    def setup(self):
        self.categories = {}
        for i in self.NAMES:
            self.categories[i] = []
        self.watch = self.categories.copy()
    
    def clear(self):
        self.setup()
    
    def diff(self):
        if self.watch != self.categories:
            self.watch = self.categories.copy()
            self.sync()
            return True
        return False

    def copy(self):
        return Stuff(self.categories.copy())
    
    def get(self):
        l = []
        for i in self.categories:
            l.extend(self.categories[i])
        return l
    
    def update_all(self, mousePos, events, G):
        for i in self.categories:
            for j in self.categories[i]:
                j.update(G.WIN, G.pause, mousePos, events, G)
    
    def add(self, _name):
        self.categories[_name] = []
        self.sync()
    
    def add_many(self, _names):
        self.categories.update({i: [] for i in _names if i not in self.categories})
        self.sync()
    
    def sync(self):
        for i in self.categories:
            if i not in self.NAMES:
                self.NAMES.append(i)
    
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
    def __init__(self, watch=None, sprites=None):
        if watch is None: self.watch = Stuff()
        else: self.watch = watch

        if sprites is None: self.sprites = Stuff()
        else: self.sprites = sprites
    
    def getall(self):
        return self.watch.get() + self.sprites.get()
    
    def clear(self):
        self.watch.clear()
        self.sprites.clear()
    
    def diff(self):
        return self.watch.diff()
    
    def copy(self):
        return Collection(self.watch.copy(), self.sprites.copy())
    
    def update_all(self, mousePos, events, G):
        self.watch.update_all(mousePos, events, G)
        self.sprites.update_all(mousePos, events, G)
    
    def __len__(self):
        return len(self.watch) + len(self.sprites)
    
    def __getitem__(self, _name):
        try:
            return self.watch[_name]
        except KeyError:
            return self.sprites[_name]
    
    def __str__(self):
        return f'<Collection watch={self.watch}, sprites={self.sprites}>'
    def __repr__(self): return str(self)

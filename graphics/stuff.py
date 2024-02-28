class Container:
    pass

class Stuff:
    NAMES = []
    CALLBACK = lambda: None

    def __init__(self):
        self.setup()
    
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
    
    def get(self):
        l = []
        for i in self.categories.items():
            l.extend(i)
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
        self.NAMES = list(self.categories.keys())
    
    def __getitem__(self, _key):
        return self.categories[_key]
    
    def __setitem__(self, _key, _value):
        self.categories[_key] = _value
        self.sync()
    
    def __str__(self):
        return '<Stuff with %i objects>'%len(self.get())
    def __repr__(self): return str(self)

class Collection:
    def __init__(self):
        self.watch = Stuff()
        self.sprites = Stuff()
    
    def getall(self):
        return self.watch.get() + self.sprites.get()
    
    def clear(self):
        self.watch.clear()
        self.sprites.clear()
    
    def diff(self):
        return self.watch.diff()
    
    def update_all(self, mousePos, events, G):
        self.watch.update_all(mousePos, events, G)
        self.sprites.update_all(mousePos, events, G)
    
    def __getitem__(self, _name):
        try:
            return self.watch[_name]
        except KeyError:
            return self.sprites[_name]
    
    def __str__(self):
        return f'<Collection watch={self.watch}, sprites={self.sprites}>'
    def __repr__(self): return str(self)

class StackPart:
    NEXT_UID = [0]
    def __init__(self, parent, stack, category, size, winSze):
        self.parent = parent
        self.stack = stack
        self.category = category
        self.stack.add(category, self)
        self.size = size
        self.winSze = winSze
        self.uid = self.NEXT_UID[0]
        self.NEXT_UID[0] += 1
    
    @property
    def position(self):
        return self.stack[self.category].index(self)

    def remove(self):
        self.stack[self.category].remove(self)
    
    def setSize(self, newSze):
        self.size = newSze
    
    def get(self):
        return self.category(self.winSze, self.size, [i.size for i in self.stack.alls[self.category]], self.stack.alls[self.category].index(self))

    def __call__(self): return self.get() # Another method for calling the same function
    
    def __hash__(self):
        return self.uid

class Stack:
    def __init__(self):
        self.alls = {}
    
    def clear(self):
        self.alls = {}
    
    def add(self, category, obj):
        if category not in self.alls:
            self.alls[category] = []
        self.alls[category].append(obj)
    
    def makeNew(self, category, size):
        return StackPart(self, category, size)
    
    def upTo(self, category, obj):
        """Get all objects in the specified category up until the object specified"""
        return self.alls[category][:self.alls[category].index(obj)]
    
    def __getitem__(self, item):
        return self.alls[item]
    
    def __setitem__(self, item, new):
        self.alls[item] = new
    
    def replaceWith(self, toReplace):
        self.alls = toReplace.alls
    
    def copy(self):
        s = Stack()
        s.alls = self.alls.copy()
        return s

import os

def allCategories():
    return [i.name for i in os.scandir('data/nodes') if i.is_file()]

class Names:
    def __init__(self, data):
        self.rdata = data.strip(' \n')
        spl = self.rdata.split(' ')
        self.name = spl[0]
        self.args = []
        for i in spl[1:]:
            s = i.split('@')
            self.args.append((s[1], s[0]))
    def __str__(self): return self.name
    def __repr__(self): return str(self)

class Parse:
    def __init__(self, category):
        if not category.endswith('.py'): category += '.py'
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
                pattern = 0
    def __call__(self, funcname, *args):
        exec(self.data[self.names[funcname]])
        return eval('node(*args)')
    def getall(self):
        return list(self.data.keys())

def allNodes(category):
    return Parse(category).getall()

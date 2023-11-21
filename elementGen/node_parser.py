import os

def allCategories():
    return [i.name for i in os.scandir('data/nodes') if i.is_file()]

class Parse:
    def __init__(self, category):
        self.rdata = open('data/nodes/'+category).read()
        self.data = {}
        pattern = 0
        spl = self.rdata.split('#')[1:-1]
        if spl[-1] == ' END ': spl = spl[:-1] # The END is for making it look nice, not actually needed
        for i in spl:
            i = i.strip(' \n')
            if pattern == 0:
                pattern = i
            else:
                self.data[pattern] = i
                pattern = 0
    def __call__(self, funcname, *args, **kwargs):
        exec(self.data[funcname])
        return eval('node(*args, **kwargs)', locals=locals())
    def getall(self):
        return list(self.data.keys())

def allNodes(category):
    return Parse(category).getall()

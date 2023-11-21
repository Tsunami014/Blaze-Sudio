import os

def allCategories():
    return [i.name for i in os.scandir('data/nodes') if i.is_file()]

def allNodes(category):
    pass

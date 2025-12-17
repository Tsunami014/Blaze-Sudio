import os, sys
base = os.path.abspath(__file__+"/../../../")
sys.path.append(base)
os.chdir(base)
from BlazeSudio.speedup import Compile
Compile("collisions")

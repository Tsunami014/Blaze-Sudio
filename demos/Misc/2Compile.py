"""Compile [debug]"""
def main():
    from BlazeSudio import speedup
    from BlazeSudio.speedup import compile
    from importlib import import_module
    import os
    import sys
    import time
    # Used in test funcs
    import numpy as np
    import random as rng
    speedup.setSpeedupType(1)
    sectsL = max(len(compile.sects), 3)
    print('ctrl+c to go back/exit')
    print("\n"*(sectsL+2))
    last_res = ""
    while True:
        print(f"\033[{sectsL+2}A"+"\n".join(f'{i}: {j[1]} ({j[0]})\033[J' for i, j in compile.sects.items()))
        print("\033[J\n"*(sectsL - len(compile.sects)), end="")
        print(last_res+"\033[J")
        try:
            inp = input("Select section > \033[J")
        except KeyboardInterrupt:
            print("Exiting.")
            return
        
        nxt = False
        try:
            inp = int(inp)
            if inp < 0 or inp >= len(compile.sects):
                last_res = "Number must be present in list"
            else:
                nxt = True
        except ValueError:
            last_res = "Input must be a number"

        if nxt:
            last_res = ""
            sect = inp
            chosen = compile.sects[sect]
            while True:
                print(f"\033[{sectsL+3}A" + f"Chosen: {chosen[1]} ({chosen[0]})\033[J")
                print("\n\033[J"*(sectsL-3))
                print(last_res+"\033[J")
                nt = ""
                if not compile.isCached(chosen[1]):
                    nt = " not"
                print(f"Compiled version does{nt} exist\033[J")
                print("p = purge compiled, c = compile, r = time regular, t = time compiled\033[J")
                try:
                    inp = input("What do you want to do? > \033[J")
                except KeyboardInterrupt:
                    last_res = ""
                    break
                inp = inp.lower().strip()
                if inp == 'p':
                    pth = os.path.abspath(__file__)
                    basepth = pth[:pth.rindex('/')]+'/BlazeSudio/speedup/cache/'
                    for i in os.listdir(basepth):
                        if i.startswith(chosen[1]):
                            os.remove(basepth+i)
                    if chosen[1] in speedup.MODULES:
                        speedup.MODULES[chosen[1]]['compiled'] = None
                    modulepth = 'BlazeSudio.speedup.cache.'+chosen[1]
                    if modulepth in sys.modules:
                        del sys.modules[modulepth]
                    last_res = "Purged!"
                elif inp == 'c':
                    compile.compile([sect])
                    last_res = "Compiled!"
                elif inp == 'r' or inp == 't':
                    if inp == 't' and not compile.isCached(chosen[1]):
                        last_res = "Not compiled, so cannot time!"
                        continue
                    totT = 0
                    eachRuns = 100
                    import_module('BlazeSudio.'+chosen[0])
                    if inp == 'r':
                        speedup.setSpeedupType(0)
                    for reg, _, comp, test in speedup.MODULES[chosen[1]]['funcs']:
                        for _ in range(eachRuns):
                            t = time.time()
                            comp(*eval(test, {'np': np, 'rng': rng}))
                            t2 = time.time()
                            totT += t2-t
                    speedup.setSpeedupType(1)
                    totRs = eachRuns*len(speedup.MODULES[chosen[1]]['funcs'])

                    lbl = {'r': 'Regular', 't': 'Compiled'}[inp]
                    last_res = f"{lbl} functions took a total of {round(totT/totRs, 8):.10f} seconds per run on average (over {totRs} runs)"
                else:
                    last_res = f'Input "{inp}" not recognised!'

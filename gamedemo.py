import os
import json
import importlib

allGames = os.listdir('demogames')
allGames.remove('data.json')

with open('demogames/data.json') as f:
    gameData = json.load(f)

print('Type a number to play that demo game!')
idx = 0
for i in allGames:
    if i in gameData:
        print(f'{idx}: {gameData[i]["Name"]}. {gameData[i]["Description"]}')
    else:
        print(f'{idx}: {i}. UNKNOWN - NOT IN GAMEDATA')
    idx += 1

i = input("> ")
if i.isdecimal():
    i = int(i)
    if 0 <= i < len(allGames):
        if allGames[i] in gameData:
            print(f'Starting demo game {i}: {gameData[allGames[i]]["Name"]}...')
        else:
            print(f'Starting demo game {i}: {allGames[i]}...')
        # os.chdir(os.path.join(os.getcwd(), 'demogames', allGames[i]))
        importlib.import_module('demogames.'+allGames[i]+'.main')
    else:
        print('Number out of range! Exiting...')
else:
    print('Is not a number! Exiting...')

import json, os
try:
    from utils.bot.AIs import AI
except ImportError:
    try:
        from bot.AIs import AI
    except ImportError:
        from AIs import AI

import os, re
bef = re.findall(r'((utils\/?)?(bot)?\n)', os.getcwd().replace('\\','/')+'\n')[0][0][:-1] # inp ends in newline
bef = '/'.join([i for i in ['utils', 'bot'] if i not in bef.split('/')])
if bef != '': bef += '/'

def get_all_ais():
    return AI().AIs

def get_all_ai_names():
    return [str(i) for i in AI().AIs]

def set_preferences(prefs):
    eprefs = get_preferences()
    eprefs.update(prefs)
    with open(f'{bef}preferences.json', 'w') as f:
        d = json.load(f)
        d['models'].update(eprefs)
        json.dump(d, f, indent=4)

def get_preferences(specifics=None):
    with open(f'{bef}preferences.json', 'r') as f:
        prefs = json.load(f)['models']
    if specifics:
        try: return prefs[specifics]
        except: return 5
    return prefs

async def rate_all(resps=None):
    out = {}
    if resps == None:
        ais = AI()
        resps, times = await ais.get_all_model_responses(times_too=True)
    prevs = get_preferences()
    print('Rate these responses out of 10! (nothing is 5)')
    i = 0
    for name, output in resps:
        if output == False: continue
        add = ''
        if name in prevs: add = ' (previous: ' + str(prevs[name]) + ')'
        try:
            rating = input(name + add + f' (time taken: {round(times[i])} secs): ' + output + '\n')
        except KeyboardInterrupt:
            await rate_all(resps)
            return
        if rating == '': continue
        else: out[name] = int(rating)
        i += 1
    set_preferences(out)

if __name__ == '__main__':
    import asyncio
    asyncio.run(rate_all())

import json, os
try:
    from utils.bot.AIs import AI
except ImportError:
    try:
        from bot.AIs import AI
    except ImportError:
        from AIs import AI
incwd = lambda txt: (txt+'/' if txt not in os.getcwd() else '')
bef = incwd('utils') + incwd('bot') # if you put this file in a directory called utils or bt this won't like you

def get_all_ais():
    return AI().AIs

def get_all_ai_names():
    return [str(i) for i in AI().AIs]

def set_preferences(prefs):
    eprefs = get_preferences()
    eprefs.update(prefs)
    with open(f'{bef}preferences.json', 'w') as f:
        json.dump(eprefs, f, indent=4)

def get_preferences(specifics=None):
    with open(f'{bef}preferences.json', 'r') as f:
        prefs = json.load(f)
    if specifics:
        try: return prefs[specifics]
        except: return 5
    return prefs

async def rate_all(resps=None):
    out = {}
    if resps == None:
        ais = AI()
        resps = await ais.get_all_model_responses()
    prevs = get_preferences()
    print('Rate these responses out of 10! (nothing is 5)')
    for name, output in resps:
        if output == False: continue
        add = ''
        if name in prevs: add = ' (previous: ' + str(prevs[name]) + ')'
        try:
            rating = input(name + add + ': ' + output + '\n')
        except KeyboardInterrupt:
            await rate_all(resps)
            return
        if rating == '': continue
        else: out[name] = int(rating)
    set_preferences(out)

if __name__ == '__main__':
    import asyncio
    asyncio.run(rate_all())
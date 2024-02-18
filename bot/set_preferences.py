import json, os
from bot.AIs import AI

def get_all_ais():
    return AI().AIs

def get_all_ai_names():
    return [str(i) for i in AI().AIs]

def set_preferences(prefs):
    eprefs = get_preferences()
    eprefs.update(prefs)
    if not os.path.exists('bot/preferences.json'):
        with open('bot/preferences.json', 'w+') as f:
            f.write(open('bot/preferencesDefault.json', 'r').read())
    with open('bot/preferences.json', 'w') as f:
        d = json.load(f)
        d['models'].update(eprefs)
        json.dump(d, f, indent=4)

def get_preferences(specifics=None):
    if not os.path.exists('bot/preferences.json'):
        with open('bot/preferences.json', 'w+') as f:
            f.write(open('bot/preferencesDefault.json', 'r').read())
    with open('preferences.json', 'r') as f:
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

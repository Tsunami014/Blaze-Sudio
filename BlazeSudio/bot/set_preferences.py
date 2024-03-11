import json
from importlib.resources import files

from BlazeSudio.bot.AIs import AI

def get_pref_file(mode='r', ensure_existance=True):
    file = files('BlazeSudio') / 'bot/preferences.json'
    if ensure_existance:
        if not file.exists():
            default = (files('BlazeSudio') / 'bot/preferencesDefault.json').read_text()
            o = file.open('w+')
            o.write(default)
            o.flush()
    return file.open(mode)

def set_preferences(prefs):
    eprefs = get_preferences()
    eprefs.update(prefs)
    # We know it exists as we called get_preferences() which should make it if it doesn't exist, so we don't need extra checks
    with get_pref_file('w', ensure_existance=False) as f:
        d = json.load(get_pref_file(ensure_existance=False))
        d['models'].update(eprefs)
        json.dump(d, f, indent=4)
        f.flush()

def get_preferences(specifics=None):
    with get_pref_file() as f:
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

import os, sys, time
import g4f

import asyncio, aiohttp
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import nest_asyncio
nest_asyncio.apply()

if os.getcwd().endswith('bot'): # set path 2 folders above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../../'))
    os.chdir(newpath)
elif os.getcwd().endswith('utils'): # set folder to one above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)

# now current folder should be '\AIHub' and not '\AIHub\utils' or '\AIHub\utils\bot' anymore!

sys.path.append(os.getcwd())

from utils.conversation_parse import PARSE
from utils.characters import *
from api_keys import loadAPIkeys
from utils.bot.gpt4real import G4A
from utils.bot.basebots import *

class ChatGPTBot(NetBaseBot):
    speed = 1 # don't need the other as it is the same
    async def _call_ai(self, cnvrs): # TODO: redo this func to work
        async with aiohttp.ClientSession() as session:
            #api_url = "https://chatgpt-api.shn.hk/v1/"
            api_url = "https://free.churchless.tech/v1/chat/completions"
            todo = {
            "model": "gpt-3.5-turbo",
            "messages": cnvrs
            }
            async with session.post(api_url, data=todo) as response:
                data = await response.json()
                return data['choices'][0]['message']

class UserBot(BaseBot):
    def __init__(self):
        """
        A way for the user to look like a bot in the computer's eyes and be treated the same. Kinda.
        Basically, instead of querying any AIs, it prompts the user for a response.
        Will need to be updated to work with a UI
        """
        super().__init__()
    def _call_ai(self, *args):
        return input('User : ')
    async def interrupt(self, *args): return ''
    def __call__(self, *args): return self._call_ai()
    async def is_online(self):
        return True

class G4FBot(CacheBaseBot):
    def __init__(self, provider, model):
        """
        An AI chatbot, a vessel for responses.

        Parameters
        ----------
        provider : str / g4f.Provider
            The provider of the model, e.g. 'EleutherAI'
        model : str / g4f.models
            The model name, e.g. 'gpt-neo-2.7B'
        """
        self.resp = ''
        self.out = ''
        self.thread = None
        self.stop = False
        if isinstance(provider, str):
            self.provider = getattr(g4f.Provider, provider)
        else:
            self.provider = provider
        if isinstance(model, str):
            self.model = getattr(g4f.models, model)
        else:
            self.model = model
    
    def __str__(self): return f'<{self.provider.params[self.provider.params.index("r.")+2:self.provider.params.index(" supports")]}: {self.model.name}>'

    async def __call__(self, cnvrs, change=True):
        if self.model.name in [] or not change: # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = PARSE([(3, 0), 2], '', inp, 'Bot') # TODO: CHANGE PARAMS
        else:
            inp = cnvrs
        if isinstance(inp, str):
            inp = [{'role': 'user', 'content': inp}]
        return await self._call_ai(inp)
    
    async def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        try:
            await self('Q: How are you?\nA: ')
            self.stop = True
            return bool(self.out) # if it is None or '' or [] etc. then false, else True
        except:
            return False
    
    async def _call_ai(self, cnvrs):
        return await self.provider.create_async(
                    model=self.model.name,
                    messages=cnvrs,
                )
    def copy(self):
        return G4FBot(self.provider, self.model)

class AI:
    def __init__(self, use_gpt4real=True, loadgpt4real=False):
        """
        A combo of MANY AI Chatbots!
        # NOTE: REMEMBER TO CALL `await AI.find_current()` BEFORE USING THE AI OR ELSE IT WILL ERROR WITH `None has no attribute X`
        AIs supported:
        - ChatGPT (who knows whether or not it works, there just in case...)
        - ALL THE AIS (providers & models) FROM g4f!!!!!! (including ChatGPT XD)
        - GPT4All (offline :) )
        
        Features:
        #TODO:
        - Can switch between AIs
        - Detects when offline, and switches to another AI
        - Autoswitch
        - Preferences as to which AIs are best

        Parameters
        ----------
        use_gpt4real : bool or list, optional
            Whether or not to use the GPT4Real AI, by default True
            If given a list will use all the files in the `utils/bot/model` folder with the names in the list
        loadgpt4real : bool, optional
            Whether or not to load the GPT4Real AI, by default False
            If this is False, it will only load the model when it uses the model.
            This is useful if you don't want to load the model if you don't need it, but bad if you want all the loading to happen at the same time.
        """
        print('HINT WITH LOADING: If you get less things to run (e.g. maybe close down those open browsers) it will lag your computer less (if at all!)')
        self.AIs = []
        all_ais = [ChatGPTBot]

        if use_gpt4real == True or isinstance(use_gpt4real, list):
            if isinstance(use_gpt4real, list):
                for i in use_gpt4real:
                    self.AIs.append(G4A(i, 'utils/bot/model/', loadgpt4real))
            else:
                for i in os.listdir('utils/bot/model'):
                    self.AIs.append(G4A(i, 'utils/bot/model/', loadgpt4real))
        
        provs = [i for i in dir(g4f.Provider) if not i.startswith('__') and i != 'annotations' and \
                 i.lower() != 'base_provider' and getattr(g4f.Provider,i).working and \
                 (not getattr(g4f.Provider,i).needs_auth)]

        def get_models(name):
            l = []
            #p = getattr(g4f.Provider,name.replace(re.findall(" .*", name)[0], "")).__name__
            p = getattr(g4f.Provider,name).__name__
            for i in [i for i in dir(g4f.models) if i.lower() != 'base_provider' and not i.startswith('__') and i.lower() == i]:
                try:
                    if (not i.startswith('__')) and i.lower() == i:
                        ms = getattr(g4f.models, i).best_provider
                        if not isinstance(ms, (tuple, list)): ms = [ms]
                        ms = [_.__name__ for _ in ms]
                        if p in ms:
                            append = G4FBot(name, i)
                            l.append(append)
                except: pass
            return l
        prov_models = {i: get_models(i) for i in provs}
        self.allthings = []
        for i in provs: self.allthings.extend([(i, j) for j in prov_models[i]])

        provs.remove('ChatBase') # IT SUCKS
        for i in provs: self.AIs.extend(get_models(i))
        for i in all_ais:
            self.AIs.append(i())
    
    async def reevaluate(self):
        responses = [
            i.reevaluate() for i in [_ for _ in self.AIs if isinstance(_, CacheBaseBot)]
        ]
        await asyncio.gather(*responses)
    
    async def get_all_model_responses(self, use_gpt4real=False, use_gpt4real_if_all_else_fails=True, times_too=False):
        async def test_gpt4real():
            modelsl2 = [_ for _ in self.AIs if isinstance(_, G4A)]
            async def trial2(i):
                await i('Q: hi\nA: ', change=False)
                while i.still_generating():
                    await asyncio.sleep(0.1)
                return (str(i), i.resp), time.time()
            responses = [trial2(i) for i in modelsl2]
            return (await asyncio.gather(*responses)), modelsl2
        async def test(i):
            try:
                return (str(i), await i('Q: How are you?\nA: ')), time.time()
            except: return None, time.time()
        l = [i for i in self.AIs if not isinstance(i, G4A)]
        n = time.time()
        resp = [test(i) for i in l]
        resps = await asyncio.gather(*resp)
        responses = [i[0] for i in resps]
        times = [i[1] - n for i in resps]
        if use_gpt4real or (use_gpt4real_if_all_else_fails and not any([i != None for i in responses])):
            n = time.time()
            res = await test_gpt4real()
            responses.extend([i[0] for i in res[0]])
            times.extend([i[1] - n for i in res[0]])
            l.extend(res[1])
        
        times = [times[i] for i in range(len(times)) if responses[i] != None]
        responses = [i for i in responses if i != None]
        if times_too: return responses, times
        return responses # all the working AIs' resopnses

    def __getattribute__(self, name): # so whenever anything wants to get self.AIs it responds with the sorted list
        if name == 'AIs':
            from utils.bot.set_preferences import get_preferences # it is here to avoid circular imports
            object.__getattribute__(self, 'AIs').sort(key=lambda x: get_preferences([str(x)]))
            return object.__getattribute__(self, 'AIs')
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if 'cur' not in dir(self):
            raise AttributeError(
                f'\
NO AI INITIATED and attribute {name} does not exist on this object!!!!\n\
Please use `await AI.find_current()` to find the current AI.'
            )
        try:
            return getattr(self.cur, name)
        except:
            raise AttributeError(
                f'Attribute {name} does not exist on this object or the current AI!'
            )
    
    async def list_all(self, use_gpt4real=False):
        self.cur = None
        if not use_gpt4real: l = [i for i in self.AIs if not isinstance(i, G4A)]
        else: l = self.AIs
        resp = [(i.is_online()) for i in l]
        return l, resp

    async def results(self, l, responses, used_gpt4real=False, use_gpt4real_if_all_else_fails=True):
        outs = [l[i] for i in range(len(l)) if responses[i]]
        responses = [l[i] for i in range(len(l)) if responses[i]]
        if outs == []:
            if use_gpt4real_if_all_else_fails:
                try:
                    self.cur = [i for i in self.AIs if isinstance(i, G4A)][0]
                except IndexError:
                    raise ValueError(
                        'No working AI model found! (including GPT4All :O)'
                    )
            else:
                raise ValueError(
                    'No working AI model found! (%s GPT4All%s)' % (('excluding' if not used_gpt4real else 'including')(', but you specified to not have them included, so :P' if not used_gpt4real else ' :O'))
                )
        self.cur = outs[0]
    
    async def find_current(self, use_gpt4real=False, use_gpt4real_if_all_else_fails=True):
        self.cur = None
        if not use_gpt4real: l = [i for i in self.AIs if not isinstance(i, G4A)]
        else: l = self.AIs
        resp = [(i.is_online()) for i in l]
        responses = await asyncio.gather(*resp)
        outs = [l[i] for i in range(len(l)) if responses[i]]
        responses = [l[i].out for i in range(len(l)) if responses[i]]
        if outs == []:
            if use_gpt4real_if_all_else_fails:
                try:
                    self.cur = [i for i in self.AIs if isinstance(i, G4A)][0]
                except IndexError:
                    raise ValueError(
                        'No working AI model found! (including GPT4All :O)'
                    )
            else:
                raise ValueError(
                    'No working AI model found! (%s GPT4All%s)' % (('excluding' if not use_gpt4real else 'including')(', but you specified to not have them included, so :P' if not use_gpt4real else ' :O'))
                )
        self.cur = outs[0]
        return l # all the working AIs

    async def __call__(self, *args, **kwargs):
        if self.cur.shorten or kwargs.get('change', True):
            args = list(args)
            args[0] = PARSE([(3, 0), 2], '', args[0], 'Bot') # TODO: change params
        await self.cur(*args, **kwargs)

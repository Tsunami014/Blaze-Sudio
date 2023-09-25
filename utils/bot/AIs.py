import os, sys, time
from threading import Thread
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

from utils.conversion_parse import PARSE
PARSE = PARSE
from utils.characters import *
from api_keys import loadAPIkeys
try:
    from utils.bot.gpt4real import G4A
except ImportError:
    try:
        from bot.gpt4real import G4A
    except ImportError:
        from gpt4real import G4A

def tokenize_text(text, token_length=2): # ChatGPTed func
    tokens = [text[i:i+token_length] for i in range(0, len(text), token_length)]
    return tokens

class BaseBot:
    shorten = False # Whether or not the length of the input affects the speed of response
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
        self.resp = ''
        self.out = ''
        self.thread = None
        self.stop = False
    
    async def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return out
    
    def _stream_ai(self, tostream):
        self.resp = ''
        ts = tokenize_text(tostream)
        for i in ts:
            self.resp += i
            time.sleep(0.25 if ' .,/?!' in i else 0.15)
            if self.stop: break
    
    def still_generating(self):
        if self.thread == None: return False
        return self.thread.is_alive()

    async def __call__(self, cnvrs):
        if isinstance(self, (ChatGPTBot,)): # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = cnvrs
        else:
            inp = PARSE(cnvrs, 0, 0) # TOCHANGE
        out = await self._call_ai(inp)
        self.out = out
        if self.thread != None:
            self.stop = True
            self.thread.join()
        self.stop = False
        self.thread = Thread(target=self._stream_ai, args=(out['content'],), daemon=True)
        self.thread.start()
    
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
            return True
        except:
            return False
    
    def __str__(self): return f'<{type(self).__name__}>'
    def __repr__(self): return self.__str__()

class NetBaseBot(BaseBot):
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        This AI uses the network, so it checks for wifi connection before checking whether or not it is online.
        """
        super().__init__()
    async def is_online(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://8.8.8.8', timeout=0.1):
                    pass
        except asyncio.exceptions.TimeoutError:
            pass # timeout, nothing to worry about
        except:
            return False # Offline, or bug.
        return await super().is_online()

class CacheBaseBot(BaseBot):
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        This AI stores it's avaliability in a cache, so it doesn't need to check every time. It can reevaluate if needed.
        """
        super().__init__()
        self.cache = None
    
    async def reevaluate(self):
        self.cache = await super().is_online()
        return self.cache
    
    async def is_online(self):
        try:
            if self.cache == None:
                await self.reevaluate()
        except: await self.reevaluate()
        return self.cache

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
    def _call_ai(self, cnvrs):
        return input('User : ')
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
    def __repr__(self): return self.__str__()

    async def __call__(self, cnvrs):
        if self.model.name in []: # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = PARSE(cnvrs, 0, 0) # TOCHANGE VALUES OF PARSE FUNC
        else:
            inp = cnvrs
        if isinstance(inp, str):
            inp = [{'role': 'user', 'content': inp}]
        out = await self._call_ai(inp)
        self.out = out
        if self.thread != None:
            self.stop = True
            self.thread.join()
        self.stop = False
        self.thread = Thread(target=self._stream_ai, args=(out,), daemon=True)
        self.thread.start()
    
    async def _call_ai(self, cnvrs):
        return await self.provider.create_async(
                    model=self.model.name,
                    messages=cnvrs,
                )

class AI():
    def __init__(self):
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
        """
        print('Loading AI please wait...\nHINT WITH LOADING: If you get less things to run (e.g. maybe close down those open browsers) it will lag your computer less (if at all!)')
        self.AIs = []
        all_ais = [ChatGPTBot]

        #for i in os.listdir('utils/bot/model'):
        #    all_ais.append(G4A(i, 'utils/bot/model/'))
        
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

        for i in provs: self.AIs.extend(get_models(i))
        for i in all_ais:
            try:
                self.AIs.append(i())
            except:
                pass
        from utils.bot.set_preferences import get_preferences
        self.AIs.sort(key=lambda x: get_preferences([str(x)]))
    
    async def reevaluate(self):
        responses = [
            i.reevaluate() for i in [_ for _ in self.AIs if isinstance(_, CacheBaseBot)]
        ]
        await asyncio.gather(*responses)
    
    async def get_all_model_responses(self):
        modelsl = [_ for _ in self.AIs if isinstance(_, CacheBaseBot)]
        responses = [
            i.reevaluate() for i in modelsl
        ]
        onlines = await asyncio.gather(*responses)
        return [[str(modelsl[i]), (False if onlines[i] == False else modelsl[i].out)] for i in range(len(onlines))]

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
    
    async def find_current(self):
        self.cur = None
        resp = [(i.is_online()) for i in self.AIs]
        responses = await asyncio.gather(*resp)
        l = []
        for i in range(len(responses)):
            if responses[i]:
                l.append(self.AIs[i])
        self.cur = l[0]
        return l # all the working AIs

    async def __call__(self, *args, **kwargs):
        await self.cur(*args, **kwargs)

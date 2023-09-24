import requests, os, sys, time
from threading import Thread
import g4f
import asyncio
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

# TODO: more AIs
# TODO: threading

def tokenize_text(text, token_length=2): # ChatGPTed func
    tokens = [text[i:i+token_length] for i in range(0, len(text), token_length)]
    return tokens

class BaseBot:
    speed = 0 # 0 = instant, 1 = fast, 2 = kinda fast, 3 = medium, 4 = medium-slow, 5 = slow, 6 = xtra slow
    shorten = False # Whether or not the length of the input affects the speed of response
    usesasync = False
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
        self.resp = ''
        self.thread = None
        self.stop = False
        self.asked_for_resp = 0
        self._init()
    
    def _init(self): # placeholder for other bots to fill if they need
        pass
    
    def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}
    
    def _stream_ai(self, tostream):
        self.resp = ''
        self.asked_for_resp = 0
        ts = tokenize_text(tostream)
        for i in ts:
            self.resp += i
            time.sleep(0.25 if ' .,/?!' in i else 0.15)
            if self.stop: break
    
    def still_generating(self):
        if self.thread == None: return False
        return self.thread.is_alive()
    
    def any_more(self):
        out = self.resp[self.asked_for_resp:]
        self.asked_for_resp = len(self.resp)
        return out

    def __call__(self, cnvrs):
        if isinstance(self, (ChatGPTBot,)): # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = cnvrs
        else:
            inp = PARSE(cnvrs, 0, 0) # TOCHANGE
        out = self._call_ai(inp)
        out = out['choices'][0]['message']
        if self.thread != None:
            self.stop = True
            self.thread.join()
        self.stop = False
        self.thread = Thread(target=self._stream_ai, args=(out['content'],), daemon=True)
        self.thread.start()
    
    def should_interrupt(self, cnvrs):
        pass
    
    def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        try:
            if self.usesasync:
                asyncio.run(self('1+1 = '))
            else:
                self('1+1 = ')
            self.stop = True
            return True
        except:
            return False

class NetBaseBot(BaseBot):
    def is_online(self):
        try:
            requests.get('https://8.8.8.8', timeout=0.1)
        except requests.exceptions.ReadTimeout:
            pass
        except:
            return False # Offline, or bug.
        return super().is_online()

class CacheBaseBot(BaseBot):
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
        self.resp = ''
        self.thread = None
        self.stop = False
        self.asked_for_resp = 0
        self.cache = None
        self._init()
    
    def reevaluate(self):
        self.cache = super().is_online()
        return self.cache
    
    def is_online(self):
        if self.usesasync:
            try:
                if self.cache == None:
                    asyncio.run(self.reevaluate())
            except: asyncio.run(self.reevaluate())
        else:
            try:
                if self.cache == None:
                    self.reevaluate()
            except: self.reevaluate()
        return self.cache

class ChatGPTBot(NetBaseBot):
    speed = 1 # don't need the other as it is the same
    def _call_ai(self, cnvrs): # TODO: redo this func to work
        #api_url = "https://chatgpt-api.shn.hk/v1/"
        api_url = "https://free.churchless.tech/v1/chat/completions"
        todo = {
        "model": "gpt-3.5-turbo",
        "messages": cnvrs
        }
        response = requests.post(api_url, json=todo)
        return response.json()

class UserBot(BaseBot):
    def _call_ai(self, cnvrs):
        return {'choices': [{'message': {'role': 'user', 'content': input('User : ')}}]}
    def is_online(self):
        return True

class G4FBot(CacheBaseBot):
    speed = 1 # don't need the other as it is the same
    usesasync = True
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
        self.thread = None
        self.stop = False
        self.asked_for_resp = 0
        if isinstance(provider, str):
            self.provider = getattr(g4f.Provider, provider)
        else:
            self.provider = provider
        if isinstance(model, str):
            self.model = getattr(g4f.models, model)
        else:
            self.model = model
    
    def __str__(self): return f'<{self.provider.__name__}: {self.model.__name__}>'
    def __repr__(self): return self.__str__()

    async def __call__(self, cnvrs):
        if self.model.name in []: # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = {'role': 'user', 'content': PARSE(cnvrs, 0, 0)} # TOCHANGE VALUES OF PARSE FUNC
        else:
            inp = cnvrs
        if isinstance(inp, str):
            inp = [{'role': 'user', 'content': inp}]
        out = await self._call_ai(inp)
        #out = out['choices'][0]['message']
        if self.thread != None:
            self.stop = True
            self.thread.join()
        self.stop = False
        self.thread = Thread(target=self._stream_ai, args=(out,), daemon=True)
        self.thread.start()
    
    async def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        try:
            if self.cache == None:
                await self.reevaluate()
        except: await self.reevaluate()
        return self.cache
    
    async def reevaluate(self):
        try:
            await self([{'role': 'user', 'content': 'Hi'}])
            self.cache = True
        except Exception as e:
            #print(e)
            self.cache = False
        return self.cache
    
    async def _call_ai(self, cnvrs):
        return await self.provider.create_async(
                    model=self.model.name,
                    messages=cnvrs,
                )

class AI():
    # Defining values that can be yoinked from other AIs
    speed = None
    shorten = None

    def __init__(self):
        """
        A combo of MANY AI Chatbots!
        AIs supported:
        - ChatGPT (who knows whether or not it works, there just in case...)
        - ALL THE AIS (providers & models) FROM g4f!!!!!!
        - GPT4All (offline :) )
        
        Features:
        #TODO:
        - Can switch between AIs
        - Detects when offline, and switches to another AI
        - Autoswitch
        - Preferences as to which AIs are best
        """
        self.AIs = []
        all_ais = [G4A, ChatGPTBot]
        
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
    
    def still_generating(self):
        return self.cur.still_generating()
    
    async def reevaluate(self):
        responses = [
            i.reevaluate()
            for i in [_ for _ in self.AIs if _.usesasync and isinstance(_, CacheBaseBot)]
        ]
        responses = await asyncio.gather(*responses) 

    def __getattr__(self, __name):
        return getattr(self.cur,__name)
    
    async def find_current(self):
        self.cur = None
        async def run(i): return i.is_online()
        resp = [(run(i) if not i.usesasync else i.is_online()) for i in self.AIs]
        responses = await asyncio.gather(*resp)
        l = []
        for i in range(len(responses)):
            if responses[i]:
                l.append(self.AIs[i])
        self.cur = l[0]
        return l # all the working AIs

    async def __call__(self, *args, **kwargs):
        await self.find_current()
        if self.cur.usesasync:
            await self.cur(*args, **kwargs)
        else:
            self.cur(*args, **kwargs)
    
    def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        self.find_current()
        return self.cur != None

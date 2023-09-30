import time, asyncio, aiohttp
import os, sys

if os.getcwd().endswith('bot'): # set path 2 folders above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../../'))
    os.chdir(newpath)
elif os.getcwd().endswith('utils'): # set folder to one above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)

# now current folder should be '\AIHub' and not '\AIHub\utils' or '\AIHub\utils\bot' anymore!

sys.path.append(os.getcwd())

from utils.conversation_parse import PARSE

class BaseBot:
    shorten = True # Whether or not the length of the input affects the speed of response
    # As a rule of thumb, this should always be True
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
        self.resp = ''
        self.thread = None
        self.stop = False
    
    async def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return out
    
    def still_generating(self):
        if self.thread == None: return False
        return self.thread.is_alive()

    async def __call__(self, cnvrs, description='', change=True):
        if not self.shorten or not change: # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = cnvrs
        else:
            inp = PARSE([(3, 0), 2], description, cnvrs, 'Bot') #TODO: change params
        out = await self._call_ai(inp)
        self.out = out
        self.stop_generating()
        
    
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
    
    def stop_generating(self):
        if self.thread != None:
            self.stop = True
            self.thread.join()
    
    def __str__(self): return f'<{type(self).__name__}>'
    def __repr__(self): return self.__str__()

    def copy(self):
        return self.__class__()

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

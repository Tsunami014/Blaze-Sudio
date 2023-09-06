import requests, os, sys, time
from threading import Thread

if os.getcwd().endswith('bot'): # set path 2 folders above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../../'))
    os.chdir(newpath)
elif os.getcwd().endswith('utils'): # set folder to one above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)

# now current folder should be '\AIHub' and not '\AIHub\utils' or '\AIHub\utils\bot' anymore!

sys.path.append(os.getcwd())

from utils.conversation_parser import PARSE
PARSE = PARSE
from utils.characters import *
from api_keys import loadAPIkeys
from utils.bot.gpt4real import GPT4All

# TODO: more AIs
# TODO: threading

def tokenize_text(text, token_length=2): # ChatGPTed func
    tokens = [text[i:i+token_length] for i in range(0, len(text), token_length)]
    return tokens

class BaseBot:
    speed = 0 # 0 = instant, 1 = fast, 2 = kinda fast, 3 = medium, 4 = medium-slow, 5 = slow, 6 = xtra slow
    shorten = False # Whether or not the length of the input affects the speed of response
    def __init__(self, printfunc=print):
        """
        An AI chatbot, a vessel for responses.

        Parameters
        ----------
        printfunc : function
            The function to use when streaming the tokens, defaults to print.
            Must have 2 optional params: the text to print, defaults to '', and "end", defaults to '\n'
        """
        self.resp = ''
        self.thread = None
        self.stop = False
        self.asked_for_resp = 0
        self.prf = printfunc
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
            self.prf(i, end='')
            time.sleep(0.25 if ' .,/?!' in i else 0.15)
            if self.stop: break
        self.prf()
    
    def any_more(self):
        out = self.resp[self.asked_for_resp:]
        self.asked_for_resp = len(self.resp)
        return out

    def __call__(self, cnvrs):
        if isinstance(self, (ChatGPTBot,)): # add all the AIs that need a conversation LIST to work (and don't need summarisation)
            inp = cnvrs
        else:
            inp = PARSE(cnvrs, 0, 0)
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

class AI():
    # Defining values that can be yoinked from other AIs
    speed = None
    shorten = None

    def __init__(self, printfunc=print):
        """
        A combo of MANY AI Chatbots!
        AIs supported:
        - ChatGPT
        
        Features:
        #TODO:
        - Can switch between AIs
        - Detects when offline, and switches to another AI
        - Autoswitch
        - Preferences as to which AIs are best

        Parameters
        ----------
        printfunc : function
            The function to use when streaming the tokens, defaults to print.
            Must have 2 optional params: the text to print, defaults to '', and "end", defaults to '\n'
        """
        self.AIs = []
        all_ais = [GPT4All, ChatGPTBot] # PUT IN ORDER OF HOW GOOD THEY ARE, best at front of list
        self.prf = printfunc
        for i in all_ais:
            try:
                self.AIs.append(i())
                self.AIs[-1].prf = self.prf
            except:
                pass
        self.resp = ''
        self.find_current()

    def __getattr__(self, __name):
        self.find_current()
        return self.cur.__getattr__(__name)
    
    def find_current(self):
        self.cur = None
        for i in self.AIs:
            if i.is_online():
                self.cur = i
                return

    def __call__(self, *args, **kwargs):
        self.find_current()
        ret = self.cur(*args, **kwargs)
        self.resp = self.cur.resp
        return ret
    
    def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        self.find_current()
        return self.cur != None

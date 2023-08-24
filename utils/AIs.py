import requests, os, sys
from bardapi import Bard

sys.path.append(os.getcwd()) # dunno why but it needs this

try:
    from utils.characters import *
except ImportError:
    from characters import *
    # Then set the path to the folder above, to import a file from the above folder
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)

from api_keys import loadAPIkeys

# TODO: more AIs
# TODO: threading

class BaseBot:
    speed = 0 # 0 = instant, 1 = fast, 2 = kinda fast, 3 = medium, 4 = medium-slow, 5 = slow, 6 = xtra slow
    shorten = False # Whether or not the length of the input affects the speed of response
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
        self._init()
    
    def _init(self): # placeholder for other bots to fill if they need
        pass
    
    def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}

    def __call__(self, message, cnvrs=[]):
        out = self._call_ai(cnvrs)['choices'][0]['message']
        return out['content']
    
    def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        try:
            self.__call__('what\'s 1+1?\n')
            return True
        except:
            return False

class ChatGPTBot(BaseBot):
    speed = 1 # don't need the other as it is the same
    def _call_ai(self, cnvrs):
        #api_url = "https://chatgpt-api.shn.hk/v1/"
        api_url = "https://free.churchless.tech/v1/chat/completions"
        todo = {
        "model": "gpt-3.5-turbo",
        "messages": cnvrs.tolist()
        }
        response = requests.post(api_url, json=todo)
        return response.json()

class BardAIBot(BaseBot): #TODO: check if this works
    speed = '???' # TODO: change this to a good value
    def _init(self):
        self.bard = Bard(token=loadAPIkeys()[0])
        # OR os.environ['_BARD_API_KEY']=loadAPIkeys()[0]
    def _call_ai(self, cnvrs):
        return self.bard.get_answer(str(cnvrs))['content']
        # OR return Bard().get_answer(str(cnvrs))['content']

class AI():
    # Defining values that can be yoinked from other AIs
    speed = None
    shorten = None

    def __init__(self):
        """
        A combo of MANY AI Chatbots!
        AIs supported:
        - ChatGPT
        - Bard AI
        
        Features:
        #TODO:
        - Can switch between AIs
        - Detects when offline, and switches to another AI
        - Autoswitch
        - Preferences as to which AIs are best
        """
        self.AIs = []
        all_ais = [ChatGPTBot, BardAIBot] # PUT IN ORDER OF HOW GOOD THEY ARE, best at front of list
        for i in all_ais:
            try:
                self.AIs.append(i())
            except:
                pass
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
        return self.cur(*args, **kwargs)
    
    def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently
        """
        self.find_current()
        return self.cur != None

if __name__ == '__main__':
    bot = ChatGPTBot()
    AI = Character(bot, 'AI', 'An AI assistant for the user.')
    you = Character(None, 'User', '')
    while True:
        you(input('You: '), AI)

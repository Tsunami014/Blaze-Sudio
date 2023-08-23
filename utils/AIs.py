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
    def _init(self):
        self.bard = Bard(token=loadAPIkeys()[0])
        # OR os.environ['_BARD_API_KEY']=loadAPIkeys()[0]
    def _call_ai(self, cnvrs):
        return self.bard.get_answer(str(cnvrs))['content']
        # OR return Bard().get_answer(str(cnvrs))['content']

class AI(BaseBot):
    def __init__(self):
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
        """

if __name__ == '__main__':
    bot = ChatGPTBot()
    AI = Character(bot, 'AI', 'An AI assistant for the user.')
    you = Character(None, 'User', '')
    while True:
        you(input('You: '), AI)

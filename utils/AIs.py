import requests

try:
    from utils.converse import *
    from utils.characters import *
except ImportError:
    from converse import *
    from characters import *

# TODO: more AIs
# TODO: threading

class BaseBot:
    def __init__(self):
        """
        An AI chatbot, a vessel for responses.
        """
    
    def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}

    def __call__(self, message, cnvrs=[], ignore_prev=False):
        cnvrs.append('user', message)
        out = self._call_ai(cnvrs)['choices'][0]['message']
        cnvrs.append(out['role'], out['content'])
        return out['content']

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
    #while True:
    #    print('bot : ' + bot(input('user : ')))
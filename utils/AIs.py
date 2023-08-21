import requests

try:
    from utils.converse import *
except ImportError:
    from converse import *

# TODO: more AIs
# TODO: threading

class BaseBot:
    def __init__(self, ic=None):
        """
        An AI chatbot

        Parameters
        ----------
        ic : converse, optional
            the initial conversation, by default nothing (new conversation)
        """
        self.cnvrs = ic if isinstance(ic, converse) else converse()

    def reset(self):
        """
        Reset (or start a new) conversation.
        """
        self.cnvrs.new()
    
    def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}

    def __call__(self, message, ignore_prev=False):
        cnvrs = [] if ignore_prev else self.cnvrs
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
    def __init__(self, ic=None):
        """
        A combo of ALL AI Chatbots that I have coded in!
        AIs supported:
        - ChatGPT
        
        Features:
        - Can switch between AIs
        - Detects when offline, and switches to another AI
        - Autoswitch
        - Preferences as to which AIs are best

        Parameters
        ----------
        ic : converse, optional
            the initial conversation, by default nothing (new conversation)
        """
        self.cnvrs = ic if isinstance(ic, converse) else converse()

if __name__ == '__main__':
    bot = ChatGPTBot()
    while True:
        print('bot : ' + bot(input('user : ')))

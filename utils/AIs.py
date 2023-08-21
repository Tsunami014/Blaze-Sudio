import requests
try:
    from utils.base import *
except ImportError:
    from base import *

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

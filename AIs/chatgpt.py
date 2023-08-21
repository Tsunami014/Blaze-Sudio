import requests
try:
    from AIs.base import BaseBot
except ImportError:
    from base import BaseBot

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

if __name__ == '__main__':
    bot = ChatGPTBot()
    while True:
        print('bot : ' + bot(input('user : ')))

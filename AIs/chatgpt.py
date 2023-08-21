import requests

# cnvrs = CoNVeRSation/CoNVeRSe

class ChatGPTBot:
    def __init__(self):
        self.cnvrs = []
    
    def reset(self):
        self.cnvrs = []
    
    def _call_ai(self, cnvrs):
        #api_url = "https://chatgpt-api.shn.hk/v1/"
        api_url = "https://free.churchless.tech/v1/chat/completions"
        todo = {
        "model": "gpt-3.5-turbo",
        "messages": cnvrs
        }
        response = requests.post(api_url, json=todo)
        return response.json()
    
    def __call__(self, message, ignore_prev=False):
        cnvrs = [] if ignore_prev else self.cnvrs
        cnvrs.append({'role': 'user', 'content': message})
        out = self._call_ai(cnvrs)['choices'][0]['message']
        cnvrs.append(out)
        return out['content']

if __name__ == '__main__':
    bot = ChatGPTBot()
    while True:
        print('bot : ' + bot(input('user : ')))

from gpt4all import GPT4All
from threading import Thread

try:
    from utils.bot.AIs import PARSE
except:
    try:
        from bot.AIs import PARSE
    except:
        from AIs import PARSE

BASICS = ['user: ', '### prompt'] # lower case for ease

class G4A:
    speed = 5 # 5 = slow, 6 = xtra slow
    shorten = True
    def __init__(self, printfunc=print):
        """
        A GPT4All AI chatbot, a vessel for responses. This runs offline!

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
        print('Loading AI please wait...\nHINT WITH LOADING: If you get less things to run (e.g. maybe close down those open browsers) it will lag your computer less (if at all!)')
        try:
            #Popular models:
            #ggml-gpt4all-j-v1.3-groovyy - gptj
            #gpt4all-lora-quantized-ggml - llama
            self.gptj = GPT4All("ggml-gpt4all-j-v1.3-groovyy", 'utils/bot/model/', \
                model_type='gptj') #gptj, llama, mpt
        except Exception as e:
            input('ERROR SERRING UP. Try restarting this or cleaning up some disc space. If this error persists, report it or something. Press enter to quit.')
            raise e
    
    @staticmethod # dunno why, it had this in the original so I'm including it here
    def _response_callback(self, token_id, response):
        self.resp += response.decode('utf-8')
        if self.stop == False: return False
        self.prf(response.decode('utf-8'), end='')
        for i in BASICS:
            if i in self.resp.lower():
                self.resp[:self.resp.index(i):] # override the end result to remove the part, and stop generating
                return False
        return True
    
    @staticmethod
    def _prompt_callback(self, token_id):
        return self.stop
    
    def _start(self, inp, after):
        print('generating...')
        self.gptj.generate(inp)
        print('finished!')
        self.prf()
        after(self.resp)
        self.stop = False
    
    def __call__(self, inp, after=lambda end: None):
        """
        Make the bot generate a response! Can be confusing, so make sure to look at the parameters below!

        Parameters
        ----------
        inp : str
            The string to input into the AI
        after : function, optional but recommended
            What to do after the bot finishes its stuff. The function needs to have one required parameter for the bot's final output, by default nothing
        personality : function, optional
            The personality of the AI. If you need examples/defaults look in utils/bot/personalities.py, by default AIP (AI's default faster personality)
        method : function, optional
            Basically what to do with every new token the bot produces. If you need examples/defaults look in utils/bot/methods.py, by default infinite generation
        cont : bool, optional
            Whether or not to continue off the last thing you inputted. Note this will continue what IT WROTE, to get it to write more off the same prompt, by default False (it will not continue)
        wait : bool, optional
            Whether to wait for the thing to finish or leave it as a thread, by default False (leave as a thread)
        params : dict, optional
            The parameters (how much it generates, etc.) of the bot. If you need examples/defaults look in utils/bot/params.py, by default NORMAL
        """
        self.stop = True
        self.asked_for_resp = 0
        self.resp = ''
        self.stop = False
        self.gptj.model._response_callback = lambda tok_id, resp: self._response_callback(self, tok_id, resp)
        self.gptj.model._prompt_callback = lambda tok_id: self._prompt_callback(self, tok_id)
        t = Thread(target=self._start, args=(inp, after), daemon=True)
        t.start()
    
    def wait_for_stop_generating(self):
        while not self.stop:
            pass
    
    def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}
    
    def any_more(self):
        out = self.resp[self.asked_for_resp:]
        self.asked_for_resp = len(self.resp)
        return out

    def __call__(self, cnvrs):
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
            Whether or not the bot can be questioned currently.
            For this bot, always is True.
        """
        return True

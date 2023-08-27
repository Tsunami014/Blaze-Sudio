from gpt4all import GPT4All
from threading import Thread
try:
    from utils.bot.methods import *
    from utils.bot.personalities import *
    from utils.bot.params import *
except ModuleNotFoundError:
    from methods import *
    from personalities import *
    from params import *

class Bot:
    def _init(self):
        self.gptj = GPT4All("ggml-gpt4all-j-v1.3-groovyy", 'utils/bot/model/', \
                model_type='gptj') #gptj, llama, mpt
        self.setup = True
    
    def __init__(self, thread=True):
        """
        A GPT4All bot that is super cool! This bot is v2.0!
        """
        self.setup = False
        print('Loading please wait...\nHINT WITH LOADING: If you get less things to run (e.g. maybe close down those open browsers) it will lag your computer less (if at all!)')
        try:
            #Popular models:
            #ggml-gpt4all-j-v1.3-groovyy - gptj
            #gpt4all-lora-quantized-ggml - llama
            if thread:
                Thread(target=lambda: self._init(), daemon=True).start()
            else:
                self._init()
        except Exception as e:
            input('ERROR SERRING UP. Try restarting this or cleaning up some disc space. If this error persists, report it or something. Press enter to quit.')
            raise e
        self.response = ''
        self._prevValues = [AIP, infinite]
        self.run = False
        self.generating = False
    
    @staticmethod # dunno why, it had this in the original so I'm including it here
    def _response_callback(self, token_id, response, method, customs):
        self.response += response.decode('utf-8')
        if self.run == False:
            return False
        cont = method(response.decode('utf-8'), self.response, **customs)
        if isinstance(cont, bool): return cont
        if isinstance(cont, str):
            self.response = cont
            return False
        return True
    
    @staticmethod
    def _prompt_callback(self, token_id):
        return self.run
    
    def _start(self, inp, after, personality, method, customs, params, override=''):
        if not self.setup:
            print('You need to wait for it to finish setting up!')
            return
        print('generating...')
        self.generating = True
        self.gptj.model._response_callback = lambda tok_id, resp: self._response_callback(self, tok_id, resp, method, customs)
        self.gptj.model._prompt_callback = lambda tok_id: self._prompt_callback(self, tok_id)
        self.gptj.generate((personality(inp) if override == '' else override), **params)
        print('finished!')
        after(self.response)
        self.run = False
        self.generating = False
    
    def __call__(self, inp, after=lambda end: None, personality=AIP, method=infinite, cont=False, wait=False, params=NORMAL, **customisations):
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
        if not cont:
            self.response = ''
        else:
            personality, method = self._prevValues
        self.run = True
        t = Thread(target=self._start, args=(inp, after, personality, method, customisations, params, ('' if not cont else self.response)), daemon=True)
        t.start()
        self._prevValues = [personality, method]
        if wait:
            t.join()
    
    def wait_for_load(self):
        while not self.setup:
            pass
    def wait_for_stop_generating(self):
        while self.generating:
            pass

if __name__ == '__main__':
    from tkinter.constants import END
    from tkinter import Button, Text, Label, Scale
    
    def set_out(txt, delete=True):
        out.configure(state='normal')
        if delete: out.delete('1.0', END)
        out.insert(END, txt)
        out.configure(state='disabled')
    
    def generate(cont):
        status.config(text=('Status: Generating...' if not cont else 'Status: Continuing...'))
        set_out('' if not cont else (bot.response))
        
        def fin(output):
            set_out(output + '\n\nfinished!')
            status.config(text='Status: Done!')
        
        bot(
            text.get('1.0', END), 
            fin, 
            [GFP, AIP, RAWP][int(s.get()) - 1], 
            untilNext, 
            cont,
            printfunc=lambda tok: set_out(tok, False)
        )
    
    def stop():
        bot.run = False
    
    bot = Bot()
    
    text = Text(bg='white', height=10)
    l = Label(text='Input:')
    l.pack()
    text.pack()
    text.insert(END, '')
    l1 = Label(text='personality \
(1=grapefruit, 2=normal AI (faster), 3=raw (do not use unless you know what you are doing))')
    l1.pack()
    s = Scale(text._root(), from_=1, to=3, orient='horizontal')
    s.pack()
    s.set(2)
    btn = Button(text._root(), text='Generate!', command=lambda: generate(False))
    btn.pack()
    btn2 = Button(text._root(), text='Keep going!', command=lambda: generate(True))
    btn2.pack()
    btn2 = Button(text._root(), text='Stop generating!', command=stop)
    btn2.pack()
    status = Label(text='Status: OK')
    status.pack()
    out = Text(text._root())
    set_out("This is where the bot's generation output will be!")
    out.pack(fill="both", expand=True)
    out.configure(bg=text._root().cget('bg'))
    out.configure(state="disabled")
    text.mainloop()
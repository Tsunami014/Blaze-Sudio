from gpt4all import GPT4All
from threading import Thread

BASICS = ['user: ', '### prompt'] # lower case for ease

class G4A:
    def __init__(self, model, typ, loadmodel):
        """
        A GPT4All AI chatbot, a vessel for responses. This runs offline!

        Parameters
        ----------
        model : str
            The name of the file to use for the model. This is the name of a file in utils/bot/model/ that contains the model.
        typ : str
            The type of model to use. Options are: gptj, llama, mpt
        loadmodel : bool
            Whether or not to load the model. If False, it will load the model on it's first __call__.
        """
        self.resp = ''
        self.thread = None
        self.stop = False
        self.model = model
        self.typ = typ
        if loadmodel: self.load_model()
        else: self.gptj = None
    
    def load_model(self):
        try:
            self.gptj = GPT4All(self.model, 'utils/bot/model/', \
                model_type=self.typ, allow_download=False) # we download them earlier, that's why we're here
        except Exception as e:
            input('ERROR SERRING UP. Try restarting this or cleaning up some disc space. If this error persists, report it or something. Press enter to quit.')
            raise e
    
    @staticmethod # dunno why, it had this in the original so I'm including it here
    def _response_callback(self, token_id, response):
        self.resp += response.decode('utf-8')
        if self.stop: return True
        for i in BASICS:
            if i in self.resp.lower():
                self.resp = self.resp[:self.resp.index(i):] # override the end result to remove the part, and stop generating
                return False
        return True
    
    @staticmethod
    def _prompt_callback(self, token_id):
        return not self.stop
    
    def _call_ai(self, inp):
        self.stop = False
        self.resp = ''
        self.resp = self.gptj.generate(inp)
    
    async def __call__(self, inp, change=None):
        """
        Make the bot generate a response!

        Parameters
        ----------
        inp : str
            The string to input into the AI
        params : dict, optional
            The parameters (how much it generates, etc.) of the bot. TODO: get a list of avaliable inputs
        """
        if self.gptj == None: self.load_model()
        self.gptj.model._response_callback = lambda tok_id, resp: self._response_callback(self, tok_id, resp)
        self.gptj.model._prompt_callback = lambda tok_id: self._prompt_callback(self, tok_id)
        self.thread = Thread(target=self._call_ai, args=(inp,), daemon=True)
        self.thread.start()
    
    async def is_online(self):
        """
        Returns
        -------
        Bool
            Whether or not the bot can be questioned currently.
            For this bot, always is True.
            I think...
        """
        return True
    
    def still_generating(self):
        if self.thread == None: return False
        return self.thread.is_alive()
    
    def stop_generating(self):
        if self.thread != None:
            self.stop = True
            self.thread.join()
    
    def __str__(self): return f'<GPT4All: {self.model}>'
    def __repr__(self): return self.__str__()

    def copy(self):
        new = G4A(self.model, self.typ, False)
        new.gptj = self.gptj
        return new

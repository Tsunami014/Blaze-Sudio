import languagemodels as lm
from threading import Thread
import time
try:
    from utils.bot.install_tinyllm import installed
except:
    try:
        from bot.install_tinyllm import installed
    except:
        from install_tinyllm import installed

def classify(doc: str, *labels: list[str]):

    results = lm.rank_instruct(
        f"Classify as {'or'.join(labels)}: {doc}\n\nClassification:", labels
    )

    return results[0]

optionsd = {
    "ask 'what?'": "q",
    "interrupt": "i",
    "say yes": "y",
    "say no": "n",
    "say OK": "o"
}

def tokenize_text(text, token_length=2): # ChatGPTed func
    tokens = [text[i:i+token_length] for i in range(0, len(text), token_length)]
    return tokens

class TinyLLM:
    def __init__(self):
        self.rams = installed()
        self.stop = False
        self.resp = ''
        self.thread = None
    
    def _stream_ai(self, tostream):
        self.resp = ''
        ts = tokenize_text(tostream)
        for i in ts:
            self.resp += i
            time.sleep((0.5 if '.' in i else 0.25) if ' ,/?!' in i else 0.15)
            if self.stop: break
    
    def stop_generating(self):
        if self.thread != None:
            self.stop = True
            self.thread.join()
    
    def still_generating(self):
        if self.thread == None: return False
        return self.thread.is_alive()
    
    async def __call__(self, cnvrs, ram='base'):
        if ram not in self.rams:
            raise ValueError(
                f'RAM {ram} IS NOT INSTALLED'
            )
        lm.set_max_ram(ram)
        self.stop = False
        self.thread = Thread(target=self._stream_ai, args=(lm.chat(cnvrs),), daemon=True)
        self.thread.start()
    
    async def interrupt(self, txt):
        if lm.classify(txt,"listen along","say something") == 'say something': return 's'
        return optionsd[classify(txt, *list(optionsd.keys()))]

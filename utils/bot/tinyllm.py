import languagemodels as lm
try:
    from utils.bot.basebots import BaseBot
except:
    try:
        from bot.basebots import BaseBot
    except:
        from basebots import BaseBot

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

class tinyllm(BaseBot):
    def __init__(self, ram='base'):
        """
        A tinyllm bot. This runs offline!
        Parameters
        ----------
        ram : str
            The amount of RAM to use. Can be 'base' or '4gb' or '15M'. Nothing really matters, as long as it works. Defaults to 'base'.
        """
        self.ram = ram
        super().__init__()
    
    async def _call_ai(self, cnvrs):
        lm.set_max_ram(self.ram)
        return lm.chat(cnvrs)
    
    async def should_interrupt(self, txt):
        if lm.classify(txt,"listen along","say something") == 'say something': return 's'

        return optionsd[classify(txt, *list(optionsd.keys()))]
    
    def __str__(self): return f'<tinyllm {str(self.ram)}GB RAM>'

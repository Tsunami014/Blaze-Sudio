import languagemodels as lm
try:
    from utils.bot.basebots import BaseBot
except:
    try:
        from bot.basebots import BaseBot
    except:
        from basebots import BaseBot

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
        out = 'hello!'#str(cnvrs)
        return out

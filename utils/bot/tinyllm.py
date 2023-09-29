import languagemodels as lm
try:
    from utils.bot.basebots import BaseBot
except:
    try:
        from bot.basebots import BaseBot
    except:
        from basebots import BaseBot

class tinyllm(BaseBot):
    
    async def _call_ai(self, cnvrs):
        out = 'hello!'#str(cnvrs)
        return out
    
    async def should_interrupt(self, conv, description=''):
        """
        Parameters
        ----------
        conv : str
            The conversation so far
        description : str, optional
            The description of the conversation, by default ''
        
        Returns
        -------
        str
            The interrupt code
        """
        conv = PARSE([(3, 0), 2], description+\
                     Summary('*\n*`You are to `(```make a statement about```|*reply to*)* this conversation*``;``*\n**Respond with one character from the following list:\n**a=agree;i=interrupt;l=leave;s=*(``say something``|*speak*)').get(0)\
                     , conv, 'Bot') #TODO: change params
        await self(conv)
        return self.out

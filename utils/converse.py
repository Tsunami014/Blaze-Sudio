
# cnvrs = CoNVeRSation/CoNVeRSe

class converse:
    def __init__(self, ic=[]):
        """
        The class for a conversation!

        Parameters
        ----------
        ic : cnvrs/[{'role': 'user'/'system'/'bot', 'content': content}, etc.] (can add more than user/system/bot, but really?)
            the initial conversation, by default nothing (new conversation)
        """
        if isinstance(ic, list):
            self.cnvrs = ic
        if isinstance(ic, converse):
            self.cnvrs = ic.cnvrs
        else:
            self.cnvrs = []
    
    def new(self):
        """
        Make the conversation blank (start a new one!)
        """
        self.cnvrs = []
    
    def append(self, role, content):
        """
        Appends a message to the conversation!

        Parameters
        ----------
        role : str
            The role ('user', 'system', or 'bot') of the person that said the message.
            can add more than user/system/bot, but really?
        content : str
            The message said by the person
        """
        self.cnvrs.append({'role': role, 'content': content})
    
    def __str__(self):
        fancify = lambda x, side: ('>   ' if side == 'user' else '   ') + x + ('   <' if side == 'bot' else '')
        out = '\n'.join([fancify(x['content'], x['role']) for x in self.cnvrs])
        return out
    def __repr__(self): return str(self)
    def __getitem__(self, key):
        return self.cnvrs[key]
    
    def tolist(self):
        return self.cnvrs

BASE_PERSONALITY = {'user': 'The human talking to the AI', 
                    'bot': 'the AI assistant, ready to help',
                    'system': 'the system, which dictates this entire conversation'}

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

class BaseBot:
    def __init__(self, ic=None):
        """
        The Base class for a bot

        Parameters
        ----------
        ic : converse, optional
            the initial conversation, by default nothing (new conversation)
        """
        self.cnvrs = ic if isinstance(ic, converse) else converse()

    def reset(self):
        """
        Reset (or start a new) conversation.
        """
        self.cnvrs.new()
    
    def _call_ai(self, cnvrs):
        out = str(cnvrs)
        return {'choices': [{'message': {'role': 'bot', 'content': out}}]}

    def __call__(self, message, ignore_prev=False):
        cnvrs = [] if ignore_prev else self.cnvrs
        cnvrs.append('user', message)
        out = self._call_ai(cnvrs)['choices'][0]['message']
        cnvrs.append(out['role'], out['content'])
        return out['content']

if __name__ == '__main__':
    bot = BaseBot()
    while True:
        print('bot : ' + bot(input('user : ')))
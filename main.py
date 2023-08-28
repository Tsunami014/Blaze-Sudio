from utils import Character
from utils.AIs import *

class GameEngine: #TODO: Better name
    def __init__(self):
        bot = ChatGPTBot()
        userbot = UserBot() # TODO: make a userbot, which inputs the user's input and detects whether they interrupt or not, etc. and whatevs
        AI = Character(bot, 'AI', 'An AI assistant for the user.')
        you = Character(userbot, 'User', '')
        you(input('You: '), AI)
        self.characters = [
            AI,
            you
        ]
        self.ongoing = []
    
    """def _interrupt(self, who, ongoing_who):
        loudness = ongoing_who.should_keep_talking(who)
        if loudness == 0: # They stop talking
            idx = self.ongoing[0].index(ongoing_who)
            del self.ongoing[0][idx]
            del self.ongoing[1][idx]
        else:
            
    
    def __call__(self, who, said):
        if self.ongoing != None:
            self._interrupt(who, self.ongoing[0])"""

    def call(self, who, said):
        self.ongoing = [(who, said)] # TODO: Make multiple people chatting at same time support

    def update(self): # TODO: Make multiple conversations at same time support
        for i in self.ongoing:
            who, said = i
            said += who.any_more()
            # defining some vars
            endpuncnum = 20
            puncnum = 30
            endnum = 40
            if len(said) > endpuncnum and '.?!' in said or len(said) > puncnum and ',./?!"\'' in said or len(said) > endnum:
                interrupts = {}
                for j in self.characters:
                    interrupts[j] = j.should_interrupt(said) # change params for multi-conversation/people support

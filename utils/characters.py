
class Character:
    def __init__(self, AI, name, personality):
        """
        A Character, with its own personality and everything and stuff

        Parameters
        ----------
        AI : AI (Any AI class in AIs.py)
            The AI this uses. Can be a multiAI, makes no difference.
        name : str
            The name of the character. For basic conversations (like the normal chatGPT), this could be 'user' or 'assistant' or something.
            For more advanced conversations, this could be 'Grapefruit' or whatnot. Yeah, you get it, right?
        personality : str # I don't know that to do about this, would it be a string? What about summarisation?
            The Personality of the character.
        """
        self.AI = AI
        self.name = name
        self.personality = personality
        self.memory = [] # of important events, may not actually be a list, can change
        self.currents = {} # Would it be a dict? Can change
        # for things like current conversations or what the character is doing, use self.currents
        # TODO: How to summarise the personality????? Maybe it uses an online AI in the background if it's avaliable and stores the result?? Who knows.
        # Maybe new personality class??
    


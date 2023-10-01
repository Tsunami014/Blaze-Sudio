import os
try:
    from utils.discussions import *
    from utils.conversation_parse import PARSE2
except ImportError:
    from discussions import *
    from conversation_parse import PARSE2

class Character:
    def __init__(self, AI, name, personality):
        self.AI = AI
        self.name = str(name) # just in case someone's an idiot (not me, but someone else)
        self.personality = personality
        path = os.getcwd()[:os.getcwd().index('AIHub')+len('AIHub')]
        self.discus = DiscussionsDB(path+'\\data\\'+self.name+'_database.db') # Would it be a dict? Can change
        self.discus.populate()
        self.current_discussion = self.discus.create_discussion()
        # for things like current conversations or what the character is doing, use self.currents
        # TODO: How to summarise the personality????? Maybe it uses an online AI in the background if it's avaliable and stores the result?? Who knows.
        # Maybe new personality class??
    
    # TODO: When game engine comes into existance, make a gradual response, and a wait until it is time to butt in, and a gradual speak
    async def __call__(self, whoelse=[]):
        msg = await self.AI(PARSE2('Reply as a helpful assistant', self.current_discussion.get_messages(), True))
        self.current_discussion.add_message(self.name, msg)
        for i in whoelse: await i.got_told(self, msg)
        return msg
    
    async def got_told(self, who, msg):
        self.current_discussion.add_message(who.name, msg)
    
    def __str__(self): return self.name
    def __repr__(self): return str(self)

    def get_messages(self):
        """Gets a list of messages information

        Returns:
            list: List of entries in the format {"id":message id, "sender":sender name, "content":message content, "type":message type, "rank": message rank}
        """
        return self.current_discussion.get_messages()
    
    def message_rank_up(self, message_id):
        """Increments the rank of the message

        Args:
            message_id (int): The id of the message to be changed
        """
        return self.current_discussion.message_rank_up(message_id)

    def message_rank_down(self, message_id):
        """Increments the rank of the message

        Args:
            message_id (int): The id of the message to be changed
        """
        return self.current_discussion.message_rank_down(message_id)
    
    def new_discussion(self):
        self.current_discussion = self.discus.create_discussion()
    
    async def interrupt(self, said, who):
        id = self.current_discussion.add_message(str(who), said)
        out = await self.AI.interrupt(PARSE2('Reply as a helpful assistant', self.current_discussion.get_messages()))
        self.current_discussion.delete_message(id)
        return out    

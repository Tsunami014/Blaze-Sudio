from utils import Character
from utils.AIs import *
from graphics.GUI import InputBox, RESIZE_H

class GameEngine: #TODO: Better name
    def __init__(self):
        self.characters = [
            Character(AI(), 'AI', 'An AI assistant for the user.'),
            Character(UserBot(), 'User', '')
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

    def call(self, who, people_listening, said=''):
        if said == '':
            said = who(people_listening)
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
                    interrupts[j] = j.should_interrupt(said, who) # change params for multi-conversation/people support

if __name__ == '__main__':
    import pygame
    pygame.init()

    WIN = pygame.display.set_mode((800, 500))
    pygame.display.set_caption('AIHub')

    GE = GameEngine()
    input_box = InputBox(100, 100, 140, 32, '', resize=RESIZE_H, maxim=1000)
    def _(cnvrs):
        input_box.rect.move_ip(0-input_box.rect.topleft[0], 0-input_box.rect.topleft[1])
        input_box.rect.move_ip(*pygame.mouse.get_pos())
        return {'choices': [{'message': {'role': 'user', 'content': input_box.interrupt(WIN)}}]}
    GE.characters[1].AI._call_ai = _

    txt = pygame.font.SysFont('Arial', 20)

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    GE.call(GE.characters[1], [])#GE.characters[0])
        
        WIN.fill((0, 0, 0))
        for who, said in GE.ongoing:
            WIN.blit(txt.render(said, True, (255, 255, 255)), (0, 0))
        pygame.display.update()
        clock.tick(60)

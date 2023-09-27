from utils import Character
from utils.bot.AIs import *
from graphics.GUI import InputBox, RESIZE_H, TextBoxFrame
from graphics.GUI.textboxify.borders import LIGHT
import pygame
import asyncio

pygame.init()

# TODO: threading

class Sparky:
    def __init__(self, WIN):
        pygame.display.set_caption('AIHub')
        
        self.WIN = WIN
        self.ongoing = []
        self.dialog_box = TextBoxFrame(
            text="",
            text_width=320,
            lines=2,
            pos=(0, 0),
            padding=(150, 100),
            font_color=(92, 53, 102),
            font_size=26,
            bg_color=(173, 127, 168),
            border=LIGHT,
        )
        self.dialog_box.rect.move_ip(WIN.get_width() / 2 - self.dialog_box.rect.w / 2,
                                     WIN.get_height() - self.dialog_box.rect.h)
        self.dialog_box.set_indicator()
        self.dialog_box.set_portrait()
        # Create sprite group for the dialog boxes.
        self.dialog_group = pygame.sprite.LayeredDirty()
        self.dialog_group.add(self.dialog_box)

        self.AIs = [ # for duplicate AIs
            AI(),
            UserBot()
        ]

        self.characters = [
            Character(self.AIs[0], 'AI', 'An AI assistant for the user.'),
            Character(self.AIs[1], 'User', '')
        ]

        self.input_box = InputBox(100, 100, 140, 32, '', resize=RESIZE_H, maxim=1000)
        def __(screen):
            # Update the changes so the user sees the text.
            self.dialog_group.update()
            rects = self.dialog_group.draw(screen)
            pygame.display.update(rects)
        async def _(cnvrs):
            self.input_box.rect.move_ip(0-self.input_box.rect.topleft[0], 0-self.input_box.rect.topleft[1])
            self.input_box.rect.move_ip(*pygame.mouse.get_pos())
            return self.input_box.interrupt(self.WIN, run_too=__)
        self.characters[1].AI._call_ai = _
        self.txt = pygame.font.SysFont('Arial', 20)
        self.clock = pygame.time.Clock()
    
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

    async def call(self, who, characters_listening):
        await who(characters_listening)
        self.ongoing = [[who, '', {}]] # TODO: Make multiple people chatting at same time support
    
    def finished(self, num):
        del self.ongoing[num]
    
    def interrupts(self, d, said):
        print(f'It was said: {said}, and in response: {str(d)}')

    async def update(self): # TODO: Make multiple conversations at same time support
        txt = []
        sep = '            '
        for who, said, figured in self.ongoing:
            place = self.ongoing.index([who, said, figured])
            said += who.any_more()
            self.ongoing[place][1] = said
            if not who.still_generating():
                for i in self.characters:
                    if i != who:
                        i.stop_generating()
                interrupts = {}
                for i in self.characters:
                    if i != who:
                        interrupts[i] = await i.should_interrupt(said, who) # change params for multi-conversation/people support
                        figured[i] = figured.get(i, 0) + len(said)
                self.interrupts(interrupts, said)
                self.finished(place)
                continue

            # defining some vars
            endpuncnum = 20
            puncnum = 30
            endnum = 40

            interrupts = {}
            for i in self.characters:
                if i != who:
                    spd = 20 if isinstance(i, G4A) else 0
                    prev = figured.get(i, 0)
                    if prev > endpuncnum-spd and '.?!' in said or prev > puncnum-spd and ',./?!"\'' in said or prev > endnum-spd:
                        if not i.still_generating():
                            interrupts[i] = await i.should_interrupt(said, who) # change params for multi-conversation/people support
                            figured[i] = prev + len(said)
            self.interrupts(interrupts, said)
            txt.append(str(who) + ': ' + said)
        self.dialog_box.very_soft_reset()
        self.dialog_box.set_text(sep.join(txt))
        self.dialog_box.update()

    async def __call__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    await self.call(self.characters[1], [])#self.characters[0])
        
        self.WIN.fill((0, 0, 0))
        await self.update()
        for _, said, __ in self.ongoing:
            self.WIN.blit(self.txt.render(said, True, (255, 255, 255)), (0, 0))
        # Update the changes so the user sees the text.
        self.dialog_group.update()
        rects = self.dialog_group.draw(self.WIN)
        pygame.display.update(rects)
        pygame.display.update()
        self.clock.tick(60)
        return True

    async def load(self): #TODO: make a loading bar
        self.WIN.fill((0, 0, 0))
        self.WIN.blit(self.txt.render('Please wait... Loading AIs...', True, (255, 255, 255)), (0, 0))
        pygame.display.update()
        for ai in self.AIs:
            if isinstance(ai, AI):
                await ai.find_current()

if __name__ == '__main__':
    WIN = pygame.display.set_mode((800, 500))
    GE = Sparky(WIN)
    asyncio.run(GE.load())
    run = True
    while run:
        run = asyncio.run(GE())

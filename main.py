from utils import Character
from utils.bot import TinyLLM, UserBot
from graphics.GUI import InputBox, RESIZE_H, TextBoxFrame
from graphics.GUI.textboxify.borders import LIGHT
import pygame, asyncio, random

pygame.init()

# TODO: threading

class randowords:
    def __init__(self, txt, sizeOScreen, font, colour=(255, 255, 255), lifespan=120):
        self.sur = font.render(txt, True, colour)
        pygame.transform.rotate(self.sur, random.randint(-40, 40))
        self.pos = (random.randint(0, sizeOScreen[0]), random.randint(0, sizeOScreen[1]))
        self.lifespan = lifespan
    
    def __call__(self, screen):
        screen.blit(self.sur, self.pos)
        self.lifespan -= 1
        return self.lifespan <= 0

class Sparky:
    def __init__(self, WIN):
        pygame.display.set_caption('AIHub')
        
        self.WIN = WIN
        self.rwords = []
        self.runningAI = False
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
            TinyLLM(),
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
        async def _():
            self.input_box.rect.move_ip(0-self.input_box.rect.topleft[0], 0-self.input_box.rect.topleft[1])
            self.input_box.rect.move_ip(*pygame.mouse.get_pos())
            return self.input_box.interrupt(self.WIN, run_too=__)
        self.characters[1].AI._call_ai = _
        self.txt = pygame.font.SysFont('Arial', 20)
        self.clock = pygame.time.Clock()

    async def call(self, who, characters_listening, out=None):
        if out == None: self.dialog_box.set_text(await who(characters_listening))
        else: self.dialog_box.set_text(out)
        self.runningAI = who
        self.dialog_box.update()
    
    async def interrupts(self, d, said):
        for i in d:
            out = await i([j for j in self.characters if j != i])
            print(f'{str(i)} : {out} ({d[i]})')
            if d[i] == 's':
                self.rwords.append(randowords(out, self.WIN.get_size(), self.txt))
            else:
                await self.call(i, [j for j in self.characters if j != i], out)
            

    async def __call__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    await self.call(self.characters[1], [])#self.characters[0])
                if event.key == pygame.K_RETURN:
                    if self.input_box._TextBoxFrame__textbox.idle:
                        self.input_box._TextBoxFrame__textbox.reset()
                        self.input_box._TextBoxFrame__textbox.update()
                        if self.dialog_box._TextBoxFrame__textbox.idle:
                            self.runningAI = False
        if self.runningAI != False and self.dialog_box._TextBoxFrame__textbox.idle:
            interrupts = {}
            print(str(self.dialog_box._TextBoxFrame__textbox.words))
            for i in self.characters:
                if i != self.runningAI:
                    interrupts[i] = await i.interrupt(str(self.dialog_box._TextBoxFrame__textbox.words), self.runningAI) # change params for multi-conversation/people support
            await self.interrupts(interrupts, str(self.dialog_box._TextBoxFrame__textbox.words))
        
        self.WIN.fill((0, 0, 0))
        # Update the changes so the user sees the text.
        self.dialog_group.update()
        rects = self.dialog_group.draw(self.WIN)
        pygame.display.update(rects)
        #self.rwords = [i for i in self.rwords if not i(self.WIN)] # text disappears after 2 secs
        for i in self.rwords: i(self.WIN) # infinite text
        pygame.display.update()
        self.clock.tick(60)
        return True

    """async def load(self):
        for ai in self.AIs:
            if isinstance(ai, AI):
                self.WIN.fill((255, 255, 255))
                pygame.display.update()
                bar = Progressbar(600, 50)
                l, tasks = await ai.list_all(False)
                res = bar(WIN, (WIN.get_width() - 600) // 2, (WIN.get_height() - 50) // 2, 5, tasks, 'Loading AI... Please wait... {2}%')
                await ai.results(l, res, False, True)"""

if __name__ == '__main__':
    WIN = pygame.display.set_mode((800, 500))
    GE = Sparky(WIN)
    #asyncio.run(GE.load())
    run = True
    while run:
        run = asyncio.run(GE())

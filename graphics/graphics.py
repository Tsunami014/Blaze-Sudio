import pygame
pygame.init()
try:
    import graphics.graphics_options as GO
except:
    import graphics_options as GO

class Graphic:
    def __init__(self):
        self.WIN = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        self.statics = []
    def set_caption(caption):
        pygame.display.set_caption(caption)
    
    def render(self, func=None):
        self.WIN.fill((255, 255, 255))
        for i in self.statics:
            self.WIN.blit(i[0], i[1])
        if func != None: func(True)
        pygame.display.flip()
    
    def graphic(self, func):
        def func2():
            prevs = [self.statics.copy()]
            run = True
            self.render(func)
            while run:
                if prevs != [self.statics]:
                    self.render(func)
                    prevs = [self.statics.copy()]
                run = func(False)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return
                self.clock.tick(60)
        return func2
    
    def add_text(self, txt, colour, font, position):
        obj = font.render(txt, 2, colour)
        self.statics.append((obj, position(self.WIN.get_size(), obj.get_size())))
    
    def clear(self):
        self.statics = []

if __name__ == '__main__':
    G = Graphic()
    @G.graphic
    def test(ui):
        if ui:
            G.add_text('HI :)', GO.CGREEN, GO.FTITLE, GO.PTOPCENTER)
            G.add_text('This is a cool thing', GO.CBLUE, GO.FFONT, GO.PCENTER)
        else:
            pass
        return True
    test()
    pygame.quit() # this here for very fast quitting

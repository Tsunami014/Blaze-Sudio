# modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

import pygame as pg

pg.init()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, end_on=None):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN and pg.K_RETURN != end_on:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                if end_on != None and event.key == end_on:
                    return False

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
    
    def interrupt(self, screen, end_on=pg.K_RETURN):
        clock = pg.time.Clock()
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if self.handle_event(event, end_on) == False:
                    done = True

            self.update()

            screen.fill((30, 30, 30))
            self.draw(screen)

            pg.display.flip()
            clock.tick(30)
        return self.text

if __name__ == '__main__':
    screen = pg.display.set_mode((640, 480))
    input_box = InputBox(100, 100, 140, 32, 'type here!')
    print('output:', input_box.interrupt(screen))

# modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 
import pygame as pg
from graphics import graphics_options as GO

class InputBox:
    def __init__(self, x, y, w, h, resize=GO.RWIDTH, placeholder='Type here!', font=GO.FSMALL, maxim=None, starting_text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.colour = GO.CINACTIVE
        self.text = starting_text
        self.active = False
        self.resize = resize
        self.maxim = maxim
        self.font = font
        self.blanktxt = placeholder
        self.render_txt()
    
    def get(self):
        return self.text
    
    def render_txt(self):
        repl = False
        if (not self.active) and self.text == '':
            self.text = self.blanktxt
            repl = True
        self.text = self.text[:self.maxim]
        self.txt_surface = self.font.render(self.text, self.colour, allowed_width=(None if self.resize == GO.RWIDTH else self.rect.w - 5))
        if self.resize == GO.RWIDTH:
            self.rect.w = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.rect.h = self.txt_surface.get_height() + 10
        if repl:
            self.text = ''

    def handle_event(self, event, end_on=None):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self.render_txt()
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if pg.K_RETURN != end_on:
                        print(self.text)
                        self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.render_txt()
                if end_on != None and event.key == end_on:
                    return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.colour, self.rect, 2)
    
    def interrupt(self, screen, end_on=pg.K_RETURN, run_too=lambda screen: None, event_callback=lambda event: None):
        clock = pg.time.Clock()
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if self.handle_event(event, end_on) == False:
                    done = True
                event_callback(event)

            screen.fill((30, 30, 30))
            self.draw(screen)
            run_too(screen)
            pg.display.flip()
            clock.tick(30)
        return self.text

class NumInputBox:
    def __init__(self, x, y, w, h, resize=GO.RWIDTH, start=0, max=float('inf'), min=float('-inf'), font=GO.FSMALL):
        self.rect = pg.Rect(x, y, w, h)
        self.colour = GO.CINACTIVE
        self.num = str(start)
        self.active = False
        self.resize = resize
        self.bounds = (max, min)
        self.font = font
        self.render_txt()
    
    def get(self):
        if self.num.startswith('-'):
            self.num = '-' + self.num.strip('-') # remove any accidental extra -'s
        self.num = str(min(max(int(self.num), self.bounds[0]), self.bounds[1]))
        return int(self.num)
    
    def render_txt(self):
        self.get()
        self.txt_surface = self.font.render(self.num, self.colour, allowed_width=self.rect.w - 5, renderdash=False)
        if self.resize == GO.RWIDTH:
            self.rect.w = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.rect.h = self.txt_surface.get_height() + 10

    def handle_event(self, event, end_on=None):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self.render_txt()
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if pg.K_RETURN != end_on:
                        print(self.num)
                        self.num = ''
                elif event.key == pg.K_BACKSPACE:
                    try: self.num = ('-' if self.num.startswith('-') else '') + \
                                    str(int(self.num[:-1]))
                    except: self.num = '0'
                elif event.key == pg.K_MINUS:
                    if self.num.startswith('-'): self.num = self.num[1:]
                    else: self.num = '-' + self.num
                else:
                    try: self.num = ('-' if self.num.startswith('-') else '') + \
                                    str(int(self.num+event.unicode))
                    except: pass
                # Re-render the text.
                self.render_txt()
                if end_on != None and event.key == end_on:
                    return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.colour, self.rect, 2)
    
    def interrupt(self, screen, end_on=pg.K_RETURN, run_too=lambda screen: None, event_callback=lambda event: None):
        clock = pg.time.Clock()
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if self.handle_event(event, end_on) == False:
                    done = True
                event_callback(event)

            screen.fill((30, 30, 30))
            self.draw(screen)
            run_too(screen)
            pg.display.flip()
            clock.tick(30)
        return self.text

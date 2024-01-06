# modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 
import pygame as pg
try:
    import graphics.graphics_options as GO
except:
    import graphics_options as GO

def renderTextCenteredAt(text, font, allowed_width): # modified from https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font 
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        if len(line_words) == 1 and font.size(line_words[0])[0] > allowed_width:
            out = []
            line = ''
            for i in line_words[0]:
                fw, fh = font.size(line+'--')
                if fw > allowed_width:
                    out.append(line+'-')
                    line = i
                else:
                    line += i
            #if line != '': out.append(line)
            lines.extend(out)
        lines.append(line)
    return lines

class InputBox:
    def __init__(self, x, y, w, h, resize=GO.RWIDTH, placeholder='Type here!', font=GO.FSMALL, maxim=None, starting_text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = GO.CINACTIVE
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
        lines = []
        if self.resize == GO.RWIDTH:
            ls = [self.text]
        else:
            ls = renderTextCenteredAt(self.text, self.font, self.rect.w - 5)
            if self.resize == GO.RNONE:
                ls = [ls[0]]

        for line in ls:
            lines.append(self.font.render(line, True, self.color))
        if lines == []: lines = [self.font.render('', True, self.color)]
        nsurface = pg.Surface((max([i.get_width() for i in lines]), sum([i.get_height() for i in lines])))
        nsurface.fill(GO.CTRANSPARENT)
        top = 0
        for i in lines:
            nsurface.blit(i, (0, top))
            top += i.get_height()
        self.txt_surface = nsurface
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
            # Change the current color of the input box.
            self.color = GO.CACTIVE if self.active else GO.CINACTIVE
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
        pg.draw.rect(screen, self.color, self.rect, 2)
    
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
        self.color = GO.CINACTIVE
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
        lines = []
        if self.resize == GO.RWIDTH:
            ls = [self.num]
        else:
            ls = renderTextCenteredAt(self.num, self.font, self.rect.w - 5)
            if self.resize == GO.RNONE:
                ls = [ls[0]]

        for line in ls:
            if line.endswith('-'): line = line[:-1]
            lines.append(self.font.render(line, True, self.color))
        if lines == []: lines = [self.font.render('', True, self.color)]
        nsurface = pg.Surface((max([i.get_width() for i in lines]), sum([i.get_height() for i in lines])))
        nsurface.fill(GO.CTRANSPARENT)
        top = 0
        for i in lines:
            nsurface.blit(i, (0, top))
            top += i.get_height()
        self.txt_surface = nsurface
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
            # Change the current color of the input box.
            self.color = GO.CACTIVE if self.active else GO.CINACTIVE
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
        pg.draw.rect(screen, self.color, self.rect, 2)
    
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

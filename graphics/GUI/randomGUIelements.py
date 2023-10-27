import pygame

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

class Button:
    def __init__(self, screen, txt, colour, txtcolour=(255, 255, 255), max_width=100, font=pygame.font.Font(None, 24), roundness=8, on_hover_enlarge=-1):
        self.roundness = roundness
        self.onHoverEnlarge = on_hover_enlarge
        self.colour = colour
        self.max_width = max_width
        self.txt = txt
        self.font = font
        self.txtcolour = txtcolour
        self.screen = pygame.Surface((0, 0))
        self.update(0, 0)
        self.screen = screen
    
    def __str__(self):
        return 'Button saying "%s"' % self.txt
    
    def __repr__(self):
        return str(self)
    
    def update(self, x, y):
        """
        draws the button to the screen, and returns whether the user has their mouse over it. So if the mousedown is also there, then they clicked it.

        Returns
        -------
        bool
            whether or not the user has their mouse ___***OVER***___ the button, NOT CLICKED.
        """
        lines = [self.font.render(line, True, self.txtcolour) for line in renderTextCenteredAt(self.txt, self.font, self.max_width)]

        self.nsurface = pygame.Surface((max([i.get_width() for i in lines]), sum([i.get_height() for i in lines])+(len(lines)-1)*10))
        self.nsurface.fill(self.colour)
        top = 0
        for i in lines:
            self.nsurface.blit(i, (0, top))
            top += i.get_height()+10

        btn = pygame.Rect(x, y, self.nsurface.get_width() + 20, self.nsurface.get_height() + 20)
        if self.onHoverEnlarge != -1 and btn.collidepoint(pygame.mouse.get_pos()):
            btn = pygame.Rect(x-self.onHoverEnlarge, y-self.onHoverEnlarge, self.nsurface.get_width() + 20 + self.onHoverEnlarge*2, self.nsurface.get_height() + 20 + self.onHoverEnlarge*2)
        pygame.draw.rect(self.screen, self.colour, btn, border_radius=self.roundness)
        self.screen.blit(self.nsurface, (x+10, y+10))
        return btn.collidepoint(pygame.mouse.get_pos())

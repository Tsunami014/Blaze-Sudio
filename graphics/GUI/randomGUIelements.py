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

def Button(txt, colour, txtcolour=(255, 255, 255), max_width=100, font=pygame.font.Font(None, 24), onHoverEnlarge=-1):
    lines = [font.render(line, True, txtcolour) for line in renderTextCenteredAt(txt, font, max_width)]

    nsurface = pygame.Surface((max([i.get_width() for i in lines]), sum([i.get_height() for i in lines])+(len(lines)-1)*10))
    nsurface.fill(colour)
    top = 0
    for i in lines:
        nsurface.blit(i, (0, top))
        top += i.get_height()+10
    
    btnsur = pygame.Rect(0, 0, nsurface.get_width() + 20, nsurface.get_height() + 20)
    return btnsur, nsurface

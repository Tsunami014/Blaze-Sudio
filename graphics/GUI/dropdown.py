import pygame

def dropdown(win, elements, spacing=5, font=None, bgcolour=(0, 0, 0), txtcolour=(255, 255, 255)):
    if font == None: font = pygame.font.SysFont(None, 20)
    elements = [font.render(i, 2, txtcolour) for i in elements]
    mx = max([i.get_width() + spacing*2 for i in elements])
    rects = []
    pos = pygame.mouse.get_pos()
    for i in elements:
        sze = i.get_size()
        sze = (mx, sze[1] + spacing*2)
        rects.append(pygame.Rect(*pos, *sze))
        pos = (pos[0], pos[1] + sze[1])
    run = True
    sur = win.copy()
    while run:
        win.fill((255, 255, 255))
        win.blit(sur, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                pass
        for i in range(len(rects)):
            pygame.draw.rect(win, bgcolour, rects[i])
            pos = rects[i].topleft
            win.blit(elements[i], (pos[0] + spacing, pos[1] + spacing))
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode()
    run = True
    while run:
        win.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                dropdown(win, ['HI', 'BYE', 'HI AGAIN'])
        pygame.display.update()
    pygame.quit()

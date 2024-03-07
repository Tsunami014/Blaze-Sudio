from logging import Handler, getLevelName

class CustomHandler(Handler):
    """
    This is a custom logging handler, which you can put a function in to run every log
    """

    def __init__(self, func=None):
        """
        Initialize the handler, with an optional function. Without a function, this is pretty useless.
        """
        Handler.__init__(self)
        if func is None:
            func = lambda: None
        self.func = func

    def emit(self, record):
        msg = self.format(record)
        self.func(msg)

    def __repr__(self):
        level = getLevelName(self.level)
        return '<CustomHandler (%s)>' % level

from threading import Thread
import pygame, os
import multiprocessing as MP
import graphics.options as GO

class TitleScreen:
    def __init__(self, width, height, amount):
        self.STATUS = [0, amount]
        self.size = (width, height)
        self.txt = ''
        self.t = None
        self.t2 = None
        self.joining = False
    
    def set_txt(self, txt):
        self.txt = txt
        self.updateQ()
    
    def update(self):
        self.STATUS[0] += 1
        self.updateQ()
    
    def whileloading(self, border, loadingtxtColour, Q, abortEvent):
        # Create the loading bar surface
        pygame.init()
        window = pygame.display.set_mode((700, 300), pygame.NOFRAME)
        window.fill((255, 255, 255))
        title = pygame.image.load('images/FoxIcon.png')
        pygame.display.set_icon(title)
        pygame.display.set_caption('Loading Blaze Sudios...')
        window.blit(title, ((window.get_width()-title.get_width())/2, (window.get_height()-title.get_height())/2))
        pygame.display.update()

        bar = pygame.Surface(self.size)
        bar.fill(GO.CBLACK)
        bar.set_colorkey(GO.CBLACK)
        font = GO.FNEW('Arial', 20)

        prev_screen = window.copy()
        running = True
        clock = pygame.time.Clock()
        dots = '.'
        dotcounter = 0
        while running:
            x, y = (window.get_width() - 600) // 2, (window.get_height() - 50) // 2
            # Handle the events
            for event in pygame.event.get():
                # If the user clicks the close button, exit the loop
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    abortEvent.set()
                    break
            try:
                gottenq = Q.get_nowait()
                self.STATUS = gottenq[0]
                self.txt = gottenq[1]
            except:
                pass # Timeout - nothing was sent
            
            dotcounter += 1
            if dotcounter > 60 / 3:
                if dots == '.': dots = '..'
                elif dots == '..': dots = '...'
                elif dots == '...': dots = '.'
                dotcounter = 0
            
            # Clear the window
            window.fill(GO.CWHITE)
            window.blit(prev_screen, (0, 0))
            # Draw the loading bar border
            pygame.draw.rect(window, GO.CBLACK, (x, y, bar.get_width(), bar.get_height()))
            # Draw the loading bar fill
            try: perc = 100/self.STATUS[1] * self.STATUS[0]
            except ZeroDivisionError: perc = 0
            perc = (perc * 100) // 100
            pygame.draw.rect(bar, GO.CGREEN, (border, border, (bar.get_width() - 2 * border) / 100 * perc, bar.get_height() - 2 * border))
            window.blit(font.render(self.txt.format(str(self.STATUS[0]), str(self.STATUS[1]), str(perc), dots), loadingtxtColour), (0, 0))
            # Blit the loading bar surface onto the window
            window.blit(bar, (x, y))
            # Update the display
            pygame.display.flip()
            clock.tick(60)
            if self.STATUS[0] >= self.STATUS[1]:
                running = False
                break
        self.txt = ''
        pygame.quit()
    
    def wait_for_aborted(self):
        while not self.joining:
            if self.EV.is_set():
                os._exit(1)
    
    def updateQ(self):
        self.Q.put((self.STATUS, self.txt))
    
    def __call__(self, border_width, loadingtxt='Loading{3} {2}% ({0} / {1})', loadingtxtColour=GO.CBLACK):
        if self.txt == '': # If something changed the text before it got time to initialise
            self.txt = loadingtxt
        self.Q = MP.Queue()
        self.EV = MP.Event()
        self.t = MP.Process(
            target=self.whileloading, args=(
            border_width, loadingtxtColour, self.Q, self.EV),
            daemon=True
        )
        self.t.start()
        self.joining = False
        self.t2 = Thread(target=self.wait_for_aborted, daemon=True)
        self.t2.start()
    
    def join(self):
        self.t.join()
        self.joining = True
        self.t2.join()
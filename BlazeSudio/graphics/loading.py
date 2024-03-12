from threading import Thread, _active
import asyncio, pygame, ctypes
import BlazeSudio.graphics.options as GO

IsLoading = [False]

class thread_with_exception(Thread):
    def __init__(self, target, *args, attempt=True):
        self.target = target
        self.args = args
        self.retargs = None
        self.attempt = attempt
        Thread.__init__(self, daemon=True)
             
    def run(self):
        if not self.attempt:
            self.retargs = self.target(*self.args)
        else:
            try:
                self.retargs = self.target(*self.args)
            finally:
                pass
          
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in _active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        if self.is_alive():
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id),
                ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
                print('Exception raise failure')

class LoadingScreen:
    def __init__(self, WIN, font):
        self.WIN = WIN
        self.font = font
        self.pic = pygame.font.Font(None, 256).render('C', 2, (0, 50, 50))
        self.clock = pygame.time.Clock()
        #for i in range(10): self.pic = pygame.transform.rotate(self.pic, random()*2)
        #self.pic = pygame.transform.scale(self.pic, (256, 256))
        self.rot = 0
    def update(self):
        self.rot -= 6
        p = pygame.transform.rotate(self.pic, self.rot)
        self.WIN.fill((255, 255, 255))
        t = self.font.render('Loading...', (0, 0, 0))
        self.WIN.blit(t, (self.WIN.get_width()//2-t.get_width()//2, 0))
        self.WIN.blit(p, (self.WIN.get_width()//2-p.get_width()//2, self.WIN.get_height()//2-p.get_height()//2))
        pygame.display.update()
        self.clock.tick(60)

def LoadingDecorator(func):
    def func2(WIN, font): # TODO: get window and use own font. Font can be override.
        IsLoading[0] = True
        class main:
            def __call__(self, *args):
                func(self, *args)
        
        ls = LoadingScreen(WIN, font)
        ls.update()
        m = main()
        t = thread_with_exception(m)
        t.start()
        run = True
        while t.is_alive() and run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            ls.update()
        end = t.is_alive()
        t.raise_exception()
        IsLoading[0] = False
        return (not end), m
    return func2

class Progressbar:
    def __init__(self, width, height):
        self.tasks = []
        self.size = (width, height)
        self.font = GO.FNEW('Arial', 20)
        self.txt = ''
    
    def set_txt(self, txt):
        self.txt = txt
    
    def whileloading(self, x, y, border, window, update_func, loadingtxtColour):
        # Create the loading bar surface
        bar = pygame.Surface(self.size)
        bar.fill(GO.CBLACK)
        bar.set_colorkey(GO.CBLACK)
        prev_screen = window.copy()
        running = True
        clock = pygame.time.Clock()
        dots = '.'
        dotcounter = 0
        while running:
            # Handle the events
            for event in pygame.event.get():
                # If the user clicks the close button, exit the loop
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break
            
            dotcounter += 1
            if dotcounter > 60 / 3:
                if dots == '.': dots = '..'
                elif dots == '..': dots = '...'
                elif dots == '...': dots = '.'
                dotcounter = 0
            
            # Clear the window
            window.fill(GO.CWHITE)
            window.blit(prev_screen, (0, 0))
            # Get the number of completed tasks from the future
            completed = sum([int(i.done()) for i in self.tasks])
            # Draw the loading bar border
            pygame.draw.rect(window, GO.CBLACK, (x, y, bar.get_width(), bar.get_height()))
            # Draw the loading bar fill
            try: perc = 100/len(self.tasks) * completed
            except ZeroDivisionError: perc = 0
            perc = (perc * 100) // 100
            pygame.draw.rect(bar, GO.CGREEN, (border, border, (bar.get_width() - 2 * border) / 100 * perc, bar.get_height() - 2 * border))
            window.blit(self.font.render(self.txt.format(str(completed), str(len(self.tasks)), str(perc), dots), loadingtxtColour), (0, 0))
            # Blit the loading bar surface onto the window
            window.blit(bar, (x, y))
            update_func()
            # Update the display
            pygame.display.flip()
            clock.tick(60)
            if perc == 100:
                running = False
                break
            # Print the number of completed tasks
            #print(f"Completed {completed} tasks out of 10")
        self.txt = ''
    
    async def main(self, tasks):
        self.tasks = [asyncio.create_task(_) for _ in tasks]
        self.results = await asyncio.gather(*self.tasks, return_exceptions=True)
    
    def __call__(self, window, x, y, border_width, tasks, loadingtxt='Loading{3} {2}% ({0} / {1})', loadingtxtColour=GO.CBLACK, update_func=lambda: None):
        if self.txt == '': # If something changed the text before it got time to initialise
            self.txt = loadingtxt
        # Create an asyncio event loop
        self.results = None
        loop = asyncio.get_event_loop()
        def run():
            task = loop.create_task(self.main(tasks))
            try:
                loop.run_until_complete(task)
            except:
                pass
        def runn():
            loop.run_in_executor(None, run)
            self.whileloading(x, y, border_width, window, update_func, loadingtxtColour)
            loop.stop()
            asyncio.get_event_loop().stop()
            return self.results
        return runn

import asyncio, pygame

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Progressbar:
    def __init__(self, width, height):
        self.tasks = []
        # Create the loading bar surface
        self.bar = pygame.Surface((width, height))
        self.bar.fill(BLACK)
        self.bar.set_colorkey(BLACK)
        self.font = pygame.font.SysFont('Arial', 20)
        self.txt = ''
    
    def set_txt(self, txt):
        self.txt = txt
    
    def whileloading(self, x, y, w, h, border, window, update_func, loadingtxtColour):
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
            window.fill(WHITE)
            window.blit(prev_screen, (0, 0))
            # Get the number of completed tasks from the future
            completed = sum([int(i.done()) for i in self.tasks])
            # Draw the loading bar border
            pygame.draw.rect(window, BLACK, (x, y, w, h))
            # Draw the loading bar fill
            try: perc = 100/len(self.tasks) * completed
            except ZeroDivisionError: perc = 0
            perc = (perc * 100) // 100
            pygame.draw.rect(self.bar, GREEN, (border, border, (w - 2 * border) / 100 * perc, h - 2 * border))
            window.blit(self.font.render(self.txt.format(str(completed), str(len(self.tasks)), str(perc), dots), True, loadingtxtColour), (0, 0))
            # Blit the loading bar surface onto the window
            window.blit(self.bar, (x, y))
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
    
    def __call__(self, window, x, y, border_width, tasks, loadingtxt='Loading{3} {2}% ({0} / {1})', loadingtxtColour=BLACK, update_func=lambda: None):
        if self.txt == '': # If something changed the text before it got time to initialise
            self.txt = loadingtxt
        # Create an asyncio event loop
        self.results = None
        loop = asyncio.get_event_loop()
        def run():
            task = loop.create_task(self.main(tasks))
            loop.run_until_complete(task)
        loop.run_in_executor(None, run)
        self.whileloading(x, y, self.bar.get_width(), self.bar.get_height(), border_width, window, update_func, loadingtxtColour)
        loop.stop()
        return self.results

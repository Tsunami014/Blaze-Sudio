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
        self.txt = pygame.font.SysFont('Arial', 20)
    
    def whileloading(self, x, y, w, h, border, window, update_func, txt, loadingtxtColour):
        prev_screen = window.copy()
        running = True
        clock = pygame.time.Clock()
        while running:
            # Handle the events
            for event in pygame.event.get():
                # If the user clicks the close button, exit the loop
                if event.type == pygame.QUIT:
                    running = False
                    break
            
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
            window.blit(self.txt.render(txt.format(str(completed), str(len(self.tasks)), str(perc)), True, loadingtxtColour), (0, 0))
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
    
    async def main(self, tasks):
        self.tasks = [asyncio.create_task(_) for _ in tasks]
        self.results = await asyncio.gather(*self.tasks, return_exceptions=True)
    
    def __call__(self, window, x, y, border_width, tasks, loadingtxt='Loading... {2}% ({0} / {1})', loadingtxtColour=BLACK, update_func=lambda: None):
        # Create an asyncio event loop
        self.results = None
        loop = asyncio.get_event_loop()
        def run():
            task = loop.create_task(self.main(tasks))
            loop.run_until_complete(task)
        loop.run_in_executor(None, run)
        self.whileloading(x, y, self.bar.get_width(), self.bar.get_height(), border_width, window, update_func, loadingtxt, loadingtxtColour)
        #loop.stop()
        return self.results

if __name__ == '__main__':
    import random
    # Define a coroutine function that waits a random amount of time
    async def wait_random():
        # Get a random number of seconds between 2 and 20
        seconds = random.randint(200, 2000) / 100
        # Print a message
        #print(f"Waiting for {seconds} seconds...")
        # Wait for that amount of time
        await asyncio.sleep(seconds)
        # Print another message
        #print(f"Done waiting for {seconds} seconds!")
        return seconds
    
    # now we initialise pygame and load the window for our demo
    pygame.init()
    WIN = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Loading Bar Example")
    WIN.fill(WHITE)
    pygame.display.update()
    # create a loading bar object
    bar = Progressbar(600, 50)
    # create a list of tasks to be completed
    tasks = [wait_random() for _ in range(500)]
    # run the loading bar
    print(bar(WIN, (WIN.get_width() - 600) // 2, (WIN.get_height() - 50) // 2, 5, tasks))
    asyncio.get_event_loop().stop()
    # exit pygame
    pygame.quit()

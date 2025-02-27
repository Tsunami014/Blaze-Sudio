import math
from threading import Thread, _active
from functools import partial
from time import time
from typing import Callable
import pygame
import ctypes
import BlazeSudio.graphics.options as GO
from BlazeSudio.graphics import mouse

__all__ = ['thread_with_exception', 'BaseLoadingScreen', 'Loading', 'Progressbar']

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

class BaseLoadingScreen:
    """
    ## USAGE EXAMPLES:

    ### As a decorator
    ```python
    import time

    @LoadingScreen.decor
    def func(slf, arg):
        time.sleep(2)
        slf['hi'] = arg
    
    success, slf = func('Hello!')
    print(success, slf.get('hi', 'NOTHING')) # `True Hello!` (or if you exited the screen, `False NOTHING`)
    ```

    ### As an instance
    ```python
    import time

    LS = LoadingScreen()

    @LS
    def func(slf, arg):
        time.sleep(2)
        slf['hi'] = arg
    
    success, slf = func('Hello!')
    print(success, slf.get('hi', 'NOTHING')) # `True Hello!` (or if you exited the screen, `False NOTHING`)
    ```
    """
    def __init__(self):
        pass

    def tick(self, WIN):
        pass

    def reset(self):
        pass

    def __runner(self, func, *fargs, **fkwargs):
        d = {}
        self.reset()
        if hasattr(self, 'func'):
            t = thread_with_exception(partial(self.func, func, d, *fargs, **fkwargs))
        else:
            t = thread_with_exception(partial(func, d, *fargs, **fkwargs))
        t.start()

        clock = pygame.time.Clock()
        WIN = pygame.display.get_surface()

        run = True
        while t.is_alive() and run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            
            mouse.Mouse.set(mouse.MouseState.NORMAL)
            mouse.Mouse.update()
            self.tick(WIN)
            pygame.display.update()
            clock.tick(60)
        
        end = t.is_alive()
        t.raise_exception()
        return (not end), d
    
    def __call__(self, func):
        return partial(self.__runner, func)
    
    @classmethod
    def decor(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]): # Called as @decorator
            instance = cls.__new__(cls)
            instance.__init__()
            return partial(instance.__runner, args[0])
        else: # called as @decorator(*args, **kwargs)
            def decor2(func):
                instance = cls.__new__(cls)
                instance.__init__(*args, **kwargs)
                return partial(instance.__runner, func)
            return decor2

class Loading(BaseLoadingScreen):
    """
    A Loading screen with a little loading pic in the middle that spins around.

    Args:
        font (pygame.Font, optional): The font of the text. Defaults to GO.FREGULAR.
    """
    def __init__(self, font=GO.FREGULAR):
        self.pic = pygame.font.Font(None, 256).render('C', 2, (0, 50, 50))
        self.font = font
    
    def reset(self):
        self.rot = 0

    def tick(self, WIN):
        self.rot -= 6
        p = pygame.transform.rotate(self.pic, self.rot)
        WIN.fill((255, 255, 255))
        s = self.font.render('Loading...', (0, 0, 0))
        WIN.blit(s, ((WIN.get_width()-s.get_width())//2, 0))
        WIN.blit(p, ((WIN.get_width()-p.get_width())//2, (WIN.get_height()-p.get_height())//2))

def DEFAULT_FORMAT_FUNC(txt, tasks, total, tme):
    secsPerCycle = 2
    cycle = math.floor((tme*secsPerCycle) / 0.25) % 4
    dots = '.'*cycle
    perc = round((tasks/total)*100, 3)
    return f'{txt}{dots} ({perc}%)'

class Progressbar(BaseLoadingScreen):
    def __init__(self, 
                 amount: int, 
                 width: int=800, 
                 height: int=100, 
                 border: int=5, 
                 yield_start: bool=True, 
                 format_func: Callable=DEFAULT_FORMAT_FUNC, 
                 loadingtxtColour: GO.C___=GO.CBLACK
                ):
        """
        A progressbar!

        The function for this needs to be a generator; where `amount` is the amount of `yield`s in the generator, and each `yield` changes the loading text.

        **The function should start with a `yield` to set the first text shown. This is expected.** To turn this off, set `yield_start` to `False`.

        Args:
            amount (int): The amount of `yield`s in the generator.
            width (int, optional): The width of the bar. Defaults to 800.
            height (int, optional): The height of the bar. Defaults to 100.
            border (int, optional): The border around the bar. Defaults to 5.
            yield_start (bool, optional): Whether the function starts with a `yield` to set the text or not. Defaults to True. If False the text will start as `Loading`.
            format_func (Callable, optional): The function called to format the loading text. Defaults to DEFAULT_FORMAT_FUNC. See below 'format_func'.
            loadingtxtColour (GO.C___, optional): The colour of the loading text. Defaults to GO.CBLACK.
        
        format_func:
            Args:

                 - str: The current text.
                 - int: The amount of tasks complete.
                 - int: The amount of total tasks.
                 - float: The current time (for loading animations).
            
            Defaults to:
        
        ```python
            def DEFAULT_FORMAT_FUNC(txt, tasks, total, tme):
                secsPerCycle = 2
                cycle = math.floor((tme*secsPerCycle) / 0.25) % 4
                dots = '.'*cycle
                perc = round((tasks/total)*100, 3)
                return f'{txt}{dots} ({perc}%)'
        ```
        
        If in the function that is loading you yield a tuple of 2 items and the second is a dictionary then it will use the first item for text and will change some settings based off of the dict.
        
        e.g. `yield 'hi', {'key': value}`

        Settings:
            amount (int): The amount of tasks that need completing.
            done (int): The amount of tasks complete (including the one you're setting it with).
            formatter (Callable): The formatter (see format_func).
        """
        self.yield_start = (-1 if yield_start else 0)
        self.amount = amount
        self.size = (width, height)
        self.border = border
        self.font = GO.FNEW('Arial', 20)
        self.formatter = format_func
        self.loadingtxtColour = loadingtxtColour
    
    def reset(self):
        self.done = self.yield_start
        self.txt = ''
    
    def func(self, func, d, *args, **kwargs):
        gen = func(d, *args, **kwargs)
        while True:
            try:
                out = next(gen)
                if isinstance(out, tuple) and len(out) == 2 and isinstance(out[1], dict):
                    self.txt = out[0]
                    self.done += 1
                    for key, it in out[1].items():
                        if key == 'amount':
                            if not isinstance(it, int):
                                raise TypeError(
                                    f"Type of item '{it}' is not int!"
                                )
                            self.amount = it
                        elif key == 'done':
                            if not isinstance(it, int):
                                raise TypeError(
                                    f"Type of item '{it}' is not int!"
                                )
                            self.done = it
                        elif key == 'formatter':
                            if not isinstance(it, Callable):
                                raise TypeError(
                                    f"Type of item '{it}' is not Callable!"
                                )
                            self.formatter = it
                        else:
                            raise ValueError(
                                f"Key '{key}' is unknown!"
                            )
                else:
                    self.txt = out
                    self.done += 1
            except StopIteration as e:
                return e.value
    
    def tick(self, WIN):
        # Clear the window
        WIN.fill(GO.CWHITE)
        # Draw the loading bar border
        w, h = self.size[0]+self.border*2, self.size[1]+self.border*2
        x, y = (WIN.get_width()-w)/2, (WIN.get_height()-h)/2
        pygame.draw.rect(WIN, GO.CBLACK, (x, y, w, h))
        # Draw the loading bar fill
        try:
            perc = (self.done/self.amount)
        except ZeroDivisionError:
            perc = 0
        perc = min(max(perc, 0), 1)
        pygame.draw.rect(WIN, GO.CGREEN, (x+self.border, y+self.border, perc*self.size[0], h - 2*self.border))

        txt = self.font.render(self.formatter(str(self.txt), min(max(self.done, 0), self.amount), self.amount, time()), self.loadingtxtColour)
        WIN.blit(txt, ((WIN.get_width()-txt.get_width())/2, 0))

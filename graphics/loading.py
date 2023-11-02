from threading import Thread, _active
from time import sleep
import ctypes, pygame
from random import random

class thread_with_exception(Thread):
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        self.retargs = None
        Thread.__init__(self, daemon=True)
             
    def run(self):
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
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

class LoadingScreen:
    def __init__(self, WIN, font):
        self.WIN = WIN
        self.font = font
    def update(self):
        try:
            self.WIN.fill((255, 255, 255))
            t = self.font.render('Loading...', 2, (0, 0, 0))
            self.WIN.blit(t, (self.WIN.get_width()//2-t.get_width()//2, 0))
            pygame.display.flip()
        except: pass

def Loading(func):
    def func2(WIN, font):
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
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        pygame.quit()
            ls.update()
        end = t.is_alive()
        t.raise_exception()
        return (not end), {i:getattr(m,i) for i in dir(m) if i not in dir(main)}
    return func2

if __name__ == '__main__':
    @Loading
    def f(self):
        for self.i in range(10):
            sleep(1)
    pygame.init()
    WIN = pygame.display.set_mode()
    font = pygame.font.Font(None, 64)
    succeeded, ret = f(WIN, font)
    print('Ran for %i seconds%s' % (ret['i'], (' Successfully! :)' if succeeded else ' And failed :(')))
    print('end')

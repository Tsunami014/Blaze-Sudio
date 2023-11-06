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
        self.pic = pygame.font.Font(None, 256).render('C', 2, (0, 50, 50))
        self.clock = pygame.time.Clock()
        #for i in range(10): self.pic = pygame.transform.rotate(self.pic, random()*2)
        #self.pic = pygame.transform.scale(self.pic, (256, 256))
        self.rot = 0
    def update(self):
        try:
            self.rot -= 6
            p = pygame.transform.rotate(self.pic, self.rot)
            self.WIN.fill((255, 255, 255))
            t = self.font.render('Loading...', 2, (0, 0, 0))
            self.WIN.blit(t, (self.WIN.get_width()//2-t.get_width()//2, 0))
            self.WIN.blit(p, (self.WIN.get_width()//2-p.get_width()//2, self.WIN.get_height()//2-p.get_height()//2))
            pygame.display.flip()
            self.clock.tick(60)
        except: pass

def Loading(func):
    def func2(WIN, font): # TODO: get window and use own font. Font can be override.
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
    pygame.quit()
    print('Ran for %i seconds%s' % (ret['i'], (' Successfully! :)' if succeeded else ' And failed :(')))
    print('end')

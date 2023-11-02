from threading import Thread, _active
from time import sleep
import ctypes

class thread_with_exception(Thread):
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        Thread.__init__(self, daemon=True)
             
    def run(self):
 
        # target function of the thread class
        try:
            self.target(*self.args)
        finally:
            pass
          
    def get_id(self):
 
        # returns id of the respective thread
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

def WithHi(func):
    # Returns: Whether the th thread quit (True) or the input function exited normally (False)
    def func2():
        with Hi() as h:
            t = thread_with_exception(func, h)
            th = h.t
            t.start()
            while t.is_alive() and h.run:
                pass
            end = t.is_alive()
        t.raise_exception()
        return end
    return func2

class Hi:
    def __enter__(self):
        self.run = True
        self.inp = ''
        self.t = Thread(target=self.whiles, daemon=True)
        self.t.start()
        return self
    
    def whiles(self):
        while self.run:
            sleep(0.1)
            print('hi')
            if self.inp == 'tuna':
                sleep(2)
                self.run = False
                return
    
    def __call__(self, inp):
        self.inp = inp
    
    def __exit__(self, *args):
        self.run = False
        try: self.t.join()
        except: pass

if __name__ == '__main__':
    @WithHi
    def f(h):
        h(input('hi'))
        sleep(4)
        print('You did not type tuna')
    f()
    print('end')

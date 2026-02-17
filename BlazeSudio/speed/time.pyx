"""
Usage:

from BlazeSudio.speed.time cimport Timer
t = Timer('test')
...
t.end()
"""
from time import perf_counter
import sys

cdef class Timer:
    def __cinit__(self, txt):
        self.start_time = perf_counter()
        self.txt = txt

    cdef double end(self) nogil:
        cdef double duration
        with gil:
            end_time = perf_counter()
            duration = end_time - self.start_time
            print(f"{self.txt}: {duration:.8f}s", file=sys.stderr)
        return duration


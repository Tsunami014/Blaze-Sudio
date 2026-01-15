from time import perf_counter
import sys

cdef class Timer:
    def __cinit__(self):
        self.start_time = perf_counter()

    cdef double end(self) nogil:
        cdef double duration
        with gil:
            end_time = perf_counter()
            duration = end_time - self.start_time
            print(f"\n{duration:.8f}s", file=sys.stderr, end="\r\033[1A")
        return duration


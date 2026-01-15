cdef class Timer:
    cdef double start_time
    cdef double end(self) nogil

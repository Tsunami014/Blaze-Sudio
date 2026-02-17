cdef class Timer:
    cdef str txt
    cdef double start_time
    cdef double end(self) nogil

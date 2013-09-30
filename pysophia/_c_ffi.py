
__all__ = ['ffi', 'lib']

from cffi import FFI

ffi = FFI()
ffi.cdef("""
void free(void *ptr);
void* malloc(size_t size);
void* realloc(void *ptr, size_t size);
""")

lib = ffi.dlopen(None)


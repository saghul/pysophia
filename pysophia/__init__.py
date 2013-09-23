
__all__ = ['Sophia', 'SophiaError']

from cffi import FFI
from pysophia._sophia_ffi import ffi, lib


# Load libc
c_ffi = FFI()
c_ffi.cdef("""
void free(void *ptr);
void * malloc(size_t size);
""")
c_lib = c_ffi.dlopen(None)


class SophiaError(Exception):
    pass


class Sophia(object):
    FL_RDWR   = lib.SPO_RDWR
    FL_RDONLY = lib.SPO_RDONLY
    FL_CREAT  = lib.SPO_CREAT

    _env = None
    _db = None
    _closed = False

    def __init__(self, path, flags):
        if self._env is not None or self._db is not None:
            raise RuntimeError('object was already initialized')
        env = lib.sp_env()
        if env == ffi.NULL:
            raise MemoryError('could not allocate environment')
        _flags = ffi.cast('int', flags)
        _path = ffi.new('char[]', path)
        r = lib.sp_ctl(env, lib.SPDIR, _flags, _path)
        if r != 0:
            error = lib.sp_error(env)
            lib.sp_destroy(env)
            raise SophiaError(ffi.string(error))
        db = lib.sp_open(env)
        if db == ffi.NULL:
            error = lib.sp_error(env)
            lib.sp_destroy(env)
            raise SophiaError(ffi.string(error))
        self._env = env
        self._db = db

    def close(self):
        if self._closed:
            return
        self._closed = True
        if self._db is not None:
            lib.sp_destroy(self._db)
        if self._env is not None:
            lib.sp_destroy(self._env)

    def set(self, key, value):
        if self._closed:
            raise RuntimeError('db is closed')
        if not isinstance(key, bytes) or not isinstance(value, bytes):
            raise TypeError('byte string objects are supported')
        _key = ffi.new('char[]', key)
        _value = ffi.new('char[]', value)
        r = lib.sp_set(self._db, _key, ffi.sizeof(_key), _value, ffi.sizeof(_value))
        if r != 0:
            error = lib.sp_error(self._db)
            raise SophiaError(ffi.string(error))

    def get(self, key):
        if self._closed:
            raise RuntimeError('db is closed')
        if not isinstance(key, bytes):
            raise TypeError('byte string objects are supported')
        _key = ffi.new('char[]', key)
        _value = ffi.new('void**')
        _value_size = ffi.new('size_t*')
        r = lib.sp_get(self._db, _key, ffi.sizeof(_key), _value, _value_size)
        if r == -1:
            error = lib.sp_error(self._db)
            raise SophiaError(ffi.string(error))
        elif r == 0:
            raise KeyError('%s not found' % key)
        value = ffi.string(ffi.cast('char*', _value[0]), _value_size[0])
        c_lib.free(_value[0])
        return value

    def delete(self, key):
        if self._closed:
            raise RuntimeError('db is closed')
        if not isinstance(key, bytes):
            raise TypeError('byte string objects are supported')
        _key = ffi.new('char[]', key)
        r = lib.sp_delete(self._db, _key, ffi.sizeof(_key))
        if r != 0:
            error = lib.sp_error(self._db)
            raise SophiaError(ffi.string(error))

    def __del__(self):
        self.close()


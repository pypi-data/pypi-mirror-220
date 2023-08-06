import os
import sys
import ctypes

from typing import Callable

if sys.platform == 'darwin':
    _lib_name = 'libminr.dylib'
elif sys.platform == 'win32':
    _lib_name = 'minr.dll'
else:
    _lib_name = 'libminr.so'

_lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'lib', _lib_name))

_report_result_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_ushort)

_find_crypto_algorithms = _lib.find_crypto_algorithms
_find_crypto_algorithms.argtypes = [ctypes.c_char_p, ctypes.c_uint64, _report_result_t]

def find_crypto_algorithms(src: bytes, report_result_callback: Callable[[str, str], None]):
    def _report_result(a, c):
        report_result_callback(a.decode("utf-8"), c)
    _find_crypto_algorithms(src, len(src), _report_result_t(_report_result))






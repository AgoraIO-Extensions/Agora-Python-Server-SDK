import time
import ctypes
from .agora_base import *

"""
AGORA_API_C_HDL agora_rtc_conn_get_agora_parameter(AGORA_HANDLE agora_rtc_conn);
AGORA_API_C_INT agora_parameter_set_parameters(AGORA_HANDLE agora_parameter, const char* json_src);
"""

agora_parameter_set_parameters = agora_lib.agora_parameter_set_parameters
agora_parameter_set_parameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
agora_parameter_set_parameters.restype = ctypes.c_int


class AgoraParameter:
    def __init__(self, handle) -> None:
        self.parameter_handle = handle
    def set_parameters(self, jsonstr):
        #convert to char_p
        params = ctypes.c_char_p(jsonstr.encode('utf-8'))
        ret = agora_parameter_set_parameters(self.parameter_handle, params)
        return ret
    def release(self):
        pass

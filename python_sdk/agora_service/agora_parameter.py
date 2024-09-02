import time
import ctypes
from .agora_base import *

"""
AGORA_API_C_HDL agora_rtc_conn_get_agora_parameter(AGORA_HANDLE agora_rtc_conn);
AGORA_API_C_INT agora_parameter_set_parameters(AGORA_HANDLE agora_parameter, const char* json_src);
AGORA_API_C_INT agora_parameter_get_string(AGORA_HANDLE agora_parameter, const char* key, char* value, uint32_t* value_size);
"""
"""
ut sample:
jsonparam = "{"key1":"value1}"
set_parameters(jsonparam)

get_string("key1", value, value_size)

if(value == "value1")
 PASS:
else
FAILED
"""

agora_parameter_set_parameters = agora_lib.agora_parameter_set_parameters
agora_parameter_set_parameters.argtypes = [AGORA_HANDLE, ctypes.c_char_p]
agora_parameter_set_parameters.restype = ctypes.c_int

agora_parameter_get_string = agora_lib.agora_parameter_get_string
agora_parameter_get_string.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
agora_parameter_get_string.restype = ctypes.c_int



class AgoraParameter:
    def __init__(self, handle) -> None:
        self.parameter_handle = handle
    def set_parameters(self, jsonstr):
        #convert to char_p
        params = ctypes.c_char_p(jsonstr.encode('utf-8'))
        ret = agora_parameter_set_parameters(self.parameter_handle, params)
        return ret
    
    #get_string: --- 可以接受的最大buffer size
    #return: (ret,strvalue, strsize)
    def get_string(self, key):
        cdata_key = ctypes.c_char_p(key.encode('utf-8'))
        value_size = ctypes.c_uint32(512)  #default to 128
        outbuffer = ctypes.create_string_buffer(value_size.value)
        ret = agora_parameter_get_string(self.parameter_handle, cdata_key, outbuffer, ctypes.byref(value_size))
        return ret,outbuffer.value.decode('utf-8')

    def release(self):
        pass

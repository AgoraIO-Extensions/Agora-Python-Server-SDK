import time
import ctypes
from .agora_base import *
from ._ctypes_handle._ctypes_data import *

agora_parameter_set_int = agora_lib.agora_parameter_set_int
agora_parameter_set_int.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
agora_parameter_set_int.restype = ctypes.c_int

agora_parameter_set_bool = agora_lib.agora_parameter_set_bool
agora_parameter_set_bool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
agora_parameter_set_bool.restype = ctypes.c_int

agora_parameter_set_uint = agora_lib.agora_parameter_set_uint
agora_parameter_set_uint.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
agora_parameter_set_uint.restype = ctypes.c_int

agora_parameter_set_number = agora_lib.agora_parameter_set_number
agora_parameter_set_number.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double]
agora_parameter_set_number.restype = ctypes.c_int

agora_parameter_set_string = agora_lib.agora_parameter_set_string
agora_parameter_set_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
agora_parameter_set_string.restype = ctypes.c_int

agora_parameter_set_array = agora_lib.agora_parameter_set_array
agora_parameter_set_array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int]
agora_parameter_set_array.restype = ctypes.c_int

agora_parameter_set_parameters = agora_lib.agora_parameter_set_parameters
agora_parameter_set_parameters.argtypes = [AGORA_HANDLE, ctypes.c_char_p]
agora_parameter_set_parameters.restype = ctypes.c_int

agora_parameter_get_int = agora_lib.agora_parameter_get_int
agora_parameter_get_int.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
agora_parameter_get_int.restype = ctypes.c_int

agora_parameter_get_bool = agora_lib.agora_parameter_get_bool
agora_parameter_get_bool.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
agora_parameter_get_bool.restype = ctypes.c_int

agora_parameter_get_uint = agora_lib.agora_parameter_get_uint
agora_parameter_get_uint.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint)]
agora_parameter_get_uint.restype = ctypes.c_int

agora_parameter_get_number = agora_lib.agora_parameter_get_number
agora_parameter_get_number.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
agora_parameter_get_number.restype = ctypes.c_int

agora_parameter_get_string = agora_lib.agora_parameter_get_string
agora_parameter_get_string.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
agora_parameter_get_string.restype = ctypes.c_int

agora_parameter_get_array = agora_lib.agora_parameter_get_array
agora_parameter_get_array.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
agora_parameter_get_array.restype = ctypes.c_int

agora_parameter_get_object = agora_lib.agora_parameter_get_object
agora_parameter_get_object.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
agora_parameter_get_object.restype = ctypes.c_int

agora_parameter_convert_path = agora_lib.agora_parameter_convert_path
agora_parameter_convert_path.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
agora_parameter_convert_path.restype = ctypes.c_int


class AgoraParameter:
    def __init__(self, handle) -> None:
        self.parameter_handle = handle

    def release(self):
        pass

    def set_int(self, key, value):
        return agora_parameter_set_int(self.parameter_handle, key.encode(), value)

    def set_bool(self, key, value):
        return agora_parameter_set_bool(self.parameter_handle, key.encode(), value)

    def set_uint(self, key, value):
        return agora_parameter_set_uint(self.parameter_handle, key.encode(), value)

    def set_number(self, key, value):
        return agora_parameter_set_number(self.parameter_handle, key.encode(), value)

    def set_string(self, key, value):
        return agora_parameter_set_string(self.parameter_handle, key.encode(), value.encode())

    def set_array(self, key, json_src):
        return agora_parameter_set_array(self.parameter_handle, key.encode(), json_src.encode())

    def set_parameters(self, json_src):
        return agora_parameter_set_parameters(self.parameter_handle, json_src.encode())

    def get_int(self, key):
        value = ctypes.c_int()
        result = agora_parameter_get_int(self.parameter_handle, key.encode(), ctypes.byref(value))
        if result == 0:
            return value.value
        else:
            return None

    def get_bool(self, key):
        value = ctypes.c_int()
        result = agora_parameter_get_bool(self.parameter_handle, key.encode(), ctypes.byref(value))
        if result == 0:
            return bool(value.value)
        else:
            return None

    def get_uint(self, key):
        value = ctypes.c_uint()
        result = agora_parameter_get_uint(self.parameter_handle, key.encode(), ctypes.byref(value))
        if result == 0:
            return value.value
        else:
            return None

    def get_number(self, key):
        value = ctypes.c_double()
        result = agora_parameter_get_number(self.parameter_handle, key.encode(), ctypes.byref(value))
        if result == 0:
            return value.value
        else:
            return None

    def get_string(self, key):
        value_size = ctypes.c_uint32(1024)
        value_buffer = ctypes.create_string_buffer(value_size.value)
        result = agora_parameter_get_string(self.parameter_handle, key.encode(), value_buffer, ctypes.byref(value_size))
        if result == 0:
            return value_buffer.value.decode()
        else:
            return None

    def get_array(self, key, json_src):
        value_size = ctypes.c_uint32(1024)
        value_buffer = ctypes.create_string_buffer(value_size.value)
        result = agora_parameter_get_array(self.parameter_handle, key.encode(), json_src.encode(), value_buffer, ctypes.byref(value_size))
        if result == 0:
            return value_buffer.value.decode()
        else:
            return None

    def get_object(self, key):
        value_size = ctypes.c_uint32(1024)
        value_buffer = ctypes.create_string_buffer(value_size.value)
        result = agora_parameter_get_object(self.parameter_handle, key.encode(), value_buffer, ctypes.byref(value_size))
        if result == 0:
            return value_buffer.value.decode()
        else:
            return None

    def convert_path(self, file_path):
        value_size = ctypes.c_uint32(1024)
        value_buffer = ctypes.create_string_buffer(value_size.value)
        result = agora_parameter_convert_path(self, file_path.encode(), value_buffer, ctypes.byref(value_size))
        if result == 0:
            return value_buffer.value.decode()
        else:
            return None

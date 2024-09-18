#!/usr/python3/bin/python3.12

# python3.6

#  PYTHONPATH=../../agora_sdk/  LD_LIBRARY_PATH=../../agora_sdk/   python3.6 demo.py
import time
import ctypes

import os
import sys

from .media_node_factory import *
from .rtc_connection import *
from .audio_pcm_data_sender import *
from .local_audio_track import *
from .rtc_conn_observer import *
from .agora_base import *

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(os.path.dirname(script_dir))



# 定义常量
AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDLR = ctypes.c_void_p

# 定义 agora_service_config 结构体
class AgoraServiceConfig(ctypes.Structure):
    _fields_ = [
        ('enable_audio_processor', ctypes.c_int),
        ('enable_audio_device', ctypes.c_int),
        ('enable_video', ctypes.c_int),
        ('context', ctypes.c_void_p),

        ('app_id', ctypes.c_char_p),
        ('area_code', ctypes.c_uint),
        ('channel_profile', ctypes.c_int),
        ('audio_scenario', ctypes.c_int),

        ('use_string_uid', ctypes.c_int),

        # ('log_path', ctypes.c_char_p),
        # ('log_size', ctypes.c_int),
    ]

    def __init__(self) -> None:
        self.log_path = ""
        self.log_size = 0    
        self.appid = ""

        # ('log_path', ctypes.c_char_p),
        # ('log_size', ctypes.c_int),




# 定义 agora_service_create 函数
agora_service_create = agora_lib.agora_service_create
agora_service_create.restype = AGORA_HANDLE

# 定义 agora_service_initialize 函数
agora_service_initialize = agora_lib.agora_service_initialize
agora_service_initialize.restype = AGORA_API_C_INT
agora_service_initialize.argtypes = [AGORA_HANDLE, ctypes.POINTER(AgoraServiceConfig)]


agora_service_create_media_node_factory = agora_lib.agora_service_create_media_node_factory
agora_service_create_media_node_factory.restype = AGORA_HANDLE
agora_service_create_media_node_factory.argtypes = [AGORA_HANDLE]

agora_service_release = agora_lib.agora_service_release
agora_service_release.restype = AGORA_API_C_INT
agora_service_release.argtypes = [AGORA_HANDLE]

agora_service_set_log_file = agora_lib.agora_service_set_log_file
agora_service_set_log_file.restype = AGORA_API_C_INT
agora_service_set_log_file.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_uint]


class AgoraService:
    def __init__(self) -> None:
        self.service_handle = agora_service_create()
        self.inited = False

    def NewConnection(self, con_config):        
        return RTCConnection(con_config,self)

    def Init(self, config: AgoraServiceConfig):        
        if self.inited == True:
            return
        config.app_id = config.appid.encode('utf-8')
        result = agora_service_initialize(self.service_handle, ctypes.byref(config))
        self.media_node_factory = agora_service_create_media_node_factory(self.service_handle)        

        if config.log_path:
            log_size = 512 * 1024
            if config.log_size > 0:
                log_size = config.log_size            
            agora_service_set_log_file(self.service_handle, ctypes.create_string_buffer(config.log_path.encode('utf-8')),log_size)

        if result == 0:
            self.inited = True
        print(f'Initialization result: {result}')
        
    def Destroy(self):                
        if self.inited == False:
            return
        agora_service_release(self.service_handle)

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
from .rtc_connection_observer import *


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

agora_media_node_factory_destroy = agora_lib.agora_media_node_factory_destroy
agora_media_node_factory_destroy.argtypes = [AGORA_HANDLE]

agora_service_release = agora_lib.agora_service_release
agora_service_release.restype = AGORA_API_C_INT
agora_service_release.argtypes = [AGORA_HANDLE]

agora_service_set_log_file = agora_lib.agora_service_set_log_file
agora_service_set_log_file.restype = AGORA_API_C_INT
agora_service_set_log_file.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_uint]

agora_service_create_custom_audio_track_pcm = agora_lib.agora_service_create_custom_audio_track_pcm
agora_service_create_custom_audio_track_pcm.argtypes = [AGORA_HANDLE, AGORA_HANDLE]
agora_service_create_custom_audio_track_pcm.restype = AGORA_HANDLE  

agora_rtc_conn_create = agora_lib.agora_rtc_conn_create
agora_rtc_conn_create.restype = AGORA_HANDLE
agora_rtc_conn_create.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnConfig)]


class AgoraService:
    def __init__(self) -> None:
        self.service_handle = agora_service_create()
        self.inited = False
        self.media_node_factory = None

    def initialize(self, config: AgoraServiceConfig):       
        if self.inited == True:
            return
        config.app_id = config.appid.encode('utf-8')
        result = agora_service_initialize(self.service_handle, ctypes.byref(config))
        if result == 0:
            self.inited = True
        print(f'Initialization result: {result}')
        
    def release(self):                
        if self.inited == False:
            return
        #release node
        if self.media_node_factory :
            agora_media_node_factory_destroy(self.media_node_factory)

        if self.service_handle:
            agora_service_release(self.service_handle)
       
        self.inited = False
        self.media_node_factory = None
        self.service_handle = None
    
    #createMediaNodeFactory	创建一个媒体节点工厂对象。
    def create_media_node_factory(self):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        self.media_node_factory = agora_service_create_media_node_factory(self.service_handle)
        if not self.media_node_factory:
            raise Exception("Failed to create media node factory")
        return MediaNodeFactory(self.media_node_factory)
    

    def create_rtc_connection(self, con_config):       
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        rtc_conn_handle = agora_rtc_conn_create(self.service_handle, ctypes.byref(con_config))
        if not rtc_conn_handle:
            raise Exception("Failed to create RTC connection")
        return RTCConnection(rtc_conn_handle)

    #感觉没有理顺Track和pcm Sender之间的创建关系？？？？
    #比如创建Track的时候，需要先创建pcm Sender
    #createCustomAudioTrackPcm	创建一个自定义音频Track。
    def create_custom_audio_track_pcm(self, audio_pcm_data_sender:AudioPcmDataSender):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        audio_track = agora_service_create_custom_audio_track_pcm(self.service_handle, audio_pcm_data_sender.sender_handle)
        if not audio_track:
            raise Exception("Failed to create custom audio track PCM")
        return LocalAudioTrack(audio_track)
    
    def set_log_file(self, log_path: str, log_size: int = 512 * 1024):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return -1
        encoded_log_path = log_path.encode('utf-8')
        result = agora_service_set_log_file(self.service_handle, ctypes.create_string_buffer(encoded_log_path), log_size)
        if result == 0:
            print(f"Log file set successfully: {log_path}")
        else:
            print(f"Failed to set log file. Error code: {result}")
        return result



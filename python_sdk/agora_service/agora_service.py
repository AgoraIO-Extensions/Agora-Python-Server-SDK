#!/usr/python3/bin/python3.12
import ctypes

from .agora_base import *
from .media_node_factory import *
from .rtc_connection import *
from .audio_pcm_data_sender import *
from .local_audio_track import *
from .rtc_connection_observer import *
from .video_frame_sender import *
from .local_video_track import *

class AgoraServiceConfig(ctypes.Structure):
    def __init__(
            self,
            log_path: str = "",
            log_size: int = 0,
            enable_audio_processor: int = 1,
            enable_audio_device: int = 0,
            enable_video: int = 0,
            context: object = None,

            appid: str = "",
            area_code: int = AreaCode.AREA_CODE_GLOB.value,
            channel_profile: ChannelProfileType = ChannelProfileType.CHANNEL_PROFILE_COMMUNICATION,
            audio_scenario: AudioScenarioType = AudioScenarioType.AUDIO_SCENARIO_DEFAULT,
            use_string_uid: int = 0,
        ) -> None:
        self.log_path = log_path
        self.log_size = log_size
        
        self.enable_audio_processor = enable_audio_processor
        self.enable_audio_device = enable_audio_device
        self.enable_video = enable_video
        self.context = context

        self.appid =  appid
        self.area_code = area_code
        self.channel_profile = channel_profile
        self.audio_scenario = audio_scenario
        self.use_string_uid = use_string_uid

    def _to_inner(self):
        inner = AgoraServiceConfigInner()
        
        inner.enable_audio_processor = self.enable_audio_processor
        inner.enable_audio_device = self.enable_audio_device
        inner.enable_video = self.enable_video
        inner.context = self.context

        inner.app_id = self.appid.encode('utf-8')
        inner.area_code = self.area_code
        inner.channel_profile = self.channel_profile.value
        inner.audio_scenario = self.audio_scenario.value

        inner.use_string_uid = self.use_string_uid
        return inner


class AgoraServiceConfigInner(ctypes.Structure):
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
    ]

    # def __init__(self) -> None:
    #     self.log_path = ""
    #     self.log_size = 0    
    #     self.appid = ""
    #     self.enable_audio_processor = 1
    #     self.enable_audio_device = 0
    #     self.enable_video = 0
    #     self.context = None
    #     self.area_code = 0
    #     # self.channel_profile = ChannelProfileType.CHANNEL_PROFILE_COMMUNICATION
    #     self.channel_profile = 0
    #     self.audio_scenario = 0
    #     self.use_string_uid = 0


agora_service_create = agora_lib.agora_service_create
agora_service_create.restype = AGORA_HANDLE

agora_service_initialize = agora_lib.agora_service_initialize
agora_service_initialize.restype = AGORA_API_C_INT
agora_service_initialize.argtypes = [AGORA_HANDLE, ctypes.POINTER(AgoraServiceConfigInner)]

agora_service_create_media_node_factory = agora_lib.agora_service_create_media_node_factory
agora_service_create_media_node_factory.restype = AGORA_HANDLE
agora_service_create_media_node_factory.argtypes = [AGORA_HANDLE]

agora_service_release = agora_lib.agora_service_release
agora_service_release.restype = AGORA_API_C_INT
agora_service_release.argtypes = [AGORA_HANDLE]

agora_service_set_log_file = agora_lib.agora_service_set_log_file
agora_service_set_log_file.restype = AGORA_API_C_INT
agora_service_set_log_file.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_uint]

agora_service_create_custom_audio_track_pcm = agora_lib.agora_service_create_custom_audio_track_pcm
agora_service_create_custom_audio_track_pcm.argtypes = [AGORA_HANDLE, AGORA_HANDLE]
agora_service_create_custom_audio_track_pcm.restype = AGORA_HANDLE  

agora_service_create_custom_audio_track_encoded = agora_lib.agora_service_create_custom_audio_track_encoded
agora_service_create_custom_audio_track_encoded.argtypes = [AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int]
agora_service_create_custom_audio_track_encoded.restype = AGORA_HANDLE

agora_rtc_conn_create = agora_lib.agora_rtc_conn_create
agora_rtc_conn_create.restype = AGORA_HANDLE
agora_rtc_conn_create.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnConfigInner)]

agora_service_create_custom_video_track_frame = agora_lib.agora_service_create_custom_video_track_frame
agora_service_create_custom_video_track_frame.restype = AGORA_HANDLE
agora_service_create_custom_video_track_frame.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

class SenderOptions(ctypes.Structure):
    _fields_ = [
        ("cc_mode", ctypes.c_int),
        ("codec_type", ctypes.c_int),
        ("target_bitrate", ctypes.c_int)
    ]

    def __init__(self, cc_mode, codec_type, target_bitrate):
        super(SenderOptions, self).__init__(cc_mode, codec_type, target_bitrate)

agora_service_create_custom_video_track_encoded = agora_lib.agora_service_create_custom_video_track_encoded
agora_service_create_custom_video_track_encoded.restype = AGORA_HANDLE
agora_service_create_custom_video_track_encoded.argtypes = [AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(SenderOptions)]



class AgoraService:
    def __init__(self) -> None:
        self.service_handle = agora_service_create()
        self.inited = False

    def initialize(self, config: AgoraServiceConfig):       
        if self.inited == True:
            return 0
        config.app_id = config.appid.encode('utf-8')
        result = agora_service_initialize(self.service_handle, ctypes.byref(config._to_inner()))
        if result == 0:
            self.inited = True
        print(f'Initialization result: {result}')

        if config.log_path:
            log_size = 512 * 1024
            if config.log_size > 0:
                log_size = config.log_size            
            agora_service_set_log_file(self.service_handle, ctypes.create_string_buffer(config.log_path.encode('utf-8')),log_size)
        
        return result
        
    def release(self):                
        if self.inited == False:
            return
        

        if self.service_handle:
            agora_service_release(self.service_handle)
       
        self.inited = False
        self.service_handle = None
    
    #createMediaNodeFactory	创建一个媒体节点工厂对象。
    def create_media_node_factory(self):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        media_node_handle = agora_service_create_media_node_factory(self.service_handle)
        if media_node_handle is None:
            return None
        return MediaNodeFactory(media_node_handle)
    

    def create_rtc_connection(self, con_config: RTCConnConfig):       
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        rtc_conn_handle = agora_rtc_conn_create(self.service_handle, ctypes.byref(con_config._to_inner()))
        if rtc_conn_handle is None:
            return None
        return RTCConnection(rtc_conn_handle)


    #createCustomAudioTrackPcm	创建一个自定义音频Track。
    def create_custom_audio_track_pcm(self, audio_pcm_data_sender:AudioPcmDataSender):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_audio_track = agora_service_create_custom_audio_track_pcm(self.service_handle, audio_pcm_data_sender.sender_handle)
        if custom_audio_track is None:
            return None
        return LocalAudioTrack(custom_audio_track)
    #mix_mode: MIX_ENABLED = 0, MIX_DISABLED = 1
    def create_custom_audio_track_encoded(self, audio_encoded_frame_sender:AudioEncodedFrameSender, mix_mode:int):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_audio_track = agora_service_create_custom_audio_track_encoded(self.service_handle, audio_encoded_frame_sender.sender_handle, mix_mode)
        if custom_audio_track is None:
            return None
        return LocalAudioTrack(custom_audio_track)
    
    def create_custom_video_track_frame(self, video_frame_sender:VideoFrameSender):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_video_track = agora_service_create_custom_video_track_frame(self.service_handle, video_frame_sender.sender_handle)
        if custom_video_track is None:
            return None
        return LocalVideoTrack(custom_video_track)
    
    def create_custom_video_track_encoded(self, video_encoded_frame_sender:VideoEncodedImageSender, options:SenderOptions):
        if not self.inited:
            print("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_video_track = agora_service_create_custom_video_track_encoded(self.service_handle, video_encoded_frame_sender.sender_handle, ctypes.byref(options))
        if custom_video_track is None:
            return None
        return LocalVideoTrack(custom_video_track)
    
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



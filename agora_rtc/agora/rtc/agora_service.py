#!/usr/python3/bin/python3.12
import ctypes

from .agora_base import *
from .media_node_factory import *

from .audio_pcm_data_sender import *
from .local_audio_track import *
from .rtc_connection_observer import *
from .video_frame_sender import *
from .local_video_track import *
import logging
logger = logging.getLogger(__name__)

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

agora_service_create_direct_custom_audio_track_pcm = agora_lib.agora_service_create_direct_custom_audio_track_pcm
agora_service_create_direct_custom_audio_track_pcm.argtypes = [AGORA_HANDLE, AGORA_HANDLE]
agora_service_create_direct_custom_audio_track_pcm.restype = AGORA_HANDLE

agora_service_create_custom_audio_track_encoded = agora_lib.agora_service_create_custom_audio_track_encoded
agora_service_create_custom_audio_track_encoded.argtypes = [AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int]
agora_service_create_custom_audio_track_encoded.restype = AGORA_HANDLE


agora_service_create_custom_video_track_frame = agora_lib.agora_service_create_custom_video_track_frame
agora_service_create_custom_video_track_frame.restype = AGORA_HANDLE
agora_service_create_custom_video_track_frame.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_service_enable_extension = agora_lib.agora_service_enable_extension
agora_service_enable_extension.restype = AGORA_API_C_INT
agora_service_enable_extension.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]

agora_service_get_agora_parameter = agora_lib.agora_service_get_agora_parameter
agora_service_get_agora_parameter.restype = AGORA_HANDLE
agora_service_get_agora_parameter.argtypes = [AGORA_HANDLE]

agora_service_create_custom_video_track_encoded = agora_lib.agora_service_create_custom_video_track_encoded
agora_service_create_custom_video_track_encoded.restype = AGORA_HANDLE
agora_service_create_custom_video_track_encoded.argtypes = [AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(SenderOptionsInner)]

#for version 2.2.2
agora_service_set_log_filter = agora_lib.agora_service_set_log_filter
agora_service_set_log_filter.restype = AGORA_API_C_INT
agora_service_set_log_filter.argtypes = [AGORA_HANDLE, ctypes.c_uint]

agora_audio_track_enable_audio_filter = agora_lib.agora_audio_track_enable_audio_filter
agora_audio_track_enable_audio_filter.restype = ctypes.c_int
agora_audio_track_enable_audio_filter.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]

agora_audio_track_set_filter_property = agora_lib.agora_audio_track_set_filter_property
agora_audio_track_set_filter_property.restype = ctypes.c_int
agora_audio_track_set_filter_property.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]


class AgoraService:
    def __init__(self) -> None:
        self.service_handle = agora_service_create()

        # set tag???
        self.inited = False
        #default to None, and never create it manually by developer from ver2.3.0
        self.media_node_factory = None
        self.enable_apm = False
        self.apm_config = None

    def initialize(self, config: AgoraServiceConfig):
        if self.inited == True:
            return 0
        
        config.app_id = config.appid.encode('utf-8')
        result = agora_service_initialize(self.service_handle, ctypes.byref(AgoraServiceConfigInner.create(config=config)))
        if result == 0:
            self.inited = True
        logger.debug(f'Initialization result: {result}')
           
        #create media node factory
        self.media_node_factory = self._create_media_node_factory()

        # to enable plugin
        provider = "agora.builtin"
        generator = "agora_audio_label_generator"
        cprovider = provider.encode('utf-8')
        cgenerator = generator.encode('utf-8')
        ctrak = ctypes.c_char_p(None)
        # agora_service_enable_extension(self.service_handle, "agora.builtin", "agora_audio_label_generator", None, 1)
        agora_service_enable_extension(self.service_handle, cprovider, cgenerator, ctrak, 1)
        agora_parameter = self.get_agora_parameter()
        agora_parameter.set_int("rtc.set_app_type", 18)

        # force audio vad v2 to be enabled
        agora_parameter.set_parameters("{\"che.audio.label.enable\": true}")
        # for apm filter: to enable apm filter
        generator = "audio_processing_remote_playback"
        cgenerator = generator.encode('utf-8')
        ctrak = ctypes.c_char_p(None)
        result = agora_service_enable_extension(self.service_handle, cprovider, cgenerator, ctrak, 1)
        if result != 0:
            logger.error(f"Failed to enable audio processing remote playback filter. Error code: {result}")
       
        #versio 2.2.0 for callback when muted
        if config.should_callbck_when_muted > 0:
            agora_parameter.set_parameters("{\"rtc.audio.enable_user_silence_packet\": true}")
        '''
        date: 2025-09-09 
	    to disable av1 resolution limitation: for any resolution, 
	    it will be encoded as av1 if config is av1 or it only work for resolution >= 360p
        '''
        agora_parameter.set_parameters("{\"che.video.min_enc_level\": 0}")

        #keep & save apm config
        self.enable_apm = config.enable_apm
        if self.enable_apm:
            if config.apm_config is None:
                self.apm_config = APMConfig()
            else:
                self.apm_config = config.apm_config
        else:
            self.apm_config = None
        

        return result

    def release(self):
        if self.inited == False:
            return

        if self.service_handle:
            agora_service_release(self.service_handle)
        if self.media_node_factory:
            self.media_node_factory.release()
            self.media_node_factory = None

        self.inited = False
        self.service_handle = None

    # createMediaNodeFactory: to create a medianode factory object
    def _create_media_node_factory(self):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        media_node_handle = agora_service_create_media_node_factory(self.service_handle)
        if media_node_handle is None:
            return None
        return MediaNodeFactory(media_node_handle)

    def get_agora_parameter(self):
        agora_parameter = agora_service_get_agora_parameter(self.service_handle)
        if not agora_parameter:
            return None
        from .agora_parameter import AgoraParameter
        return AgoraParameter(agora_parameter)

    def create_rtc_connection(self, con_config: RTCConnConfig, publish_config: RtcConnectionPublishConfig):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        from .rtc_connection import RTCConnection
        return RTCConnection(self, con_config, publish_config)

    # createCustomAudioTrackPcm: creatae a custom audio track from pcm data sender
    def _create_custom_audio_track_pcm(self, audio_pcm_data_sender: AudioPcmDataSender, scenario: AudioScenarioType) -> LocalAudioTrack:
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        if scenario == AudioScenarioType.AUDIO_SCENARIO_AI_SERVER:
            custom_audio_track = agora_service_create_direct_custom_audio_track_pcm(self.service_handle, audio_pcm_data_sender.sender_handle)
        else:
            custom_audio_track = agora_service_create_custom_audio_track_pcm(self.service_handle, audio_pcm_data_sender.sender_handle)
        if custom_audio_track is None:
            return None
        local_track =  LocalAudioTrack(custom_audio_track)
        #default for ai senario to set min delay to 10ms
        if scenario != AudioScenarioType.AUDIO_SCENARIO_AI_SERVER:
            local_track.set_send_delay_ms(10)
            local_track.set_max_buffer_audio_frame_number(100000)
        #and set enable to true
        local_track.set_enabled(True)
        return local_track
    # mix_mode: MIX_ENABLED = 0, MIX_DISABLED = 1

    def create_custom_audio_track_encoded(self, audio_encoded_frame_sender: AudioEncodedFrameSender, mix_mode: int):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_audio_track = agora_service_create_custom_audio_track_encoded(self.service_handle, audio_encoded_frame_sender.sender_handle, mix_mode)
        if custom_audio_track is None:
            return None
        return LocalAudioTrack(custom_audio_track)

    def create_custom_video_track_frame(self, video_frame_sender: VideoFrameSender):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_video_track = agora_service_create_custom_video_track_frame(self.service_handle, video_frame_sender.sender_handle)
        if custom_video_track is None:
            return None
        return LocalVideoTrack(custom_video_track)

    def create_custom_video_track_encoded(self, video_encoded_frame_sender: VideoEncodedImageSender, options: SenderOptions):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_video_track = agora_service_create_custom_video_track_encoded(self.service_handle, video_encoded_frame_sender.sender_handle, ctypes.byref(SenderOptionsInner.create(options)))
        if custom_video_track is None:
            return None
        return LocalVideoTrack(custom_video_track)

    def set_log_file(self, log_path: str, log_size: int = 512 * 1024):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return -1
        encoded_log_path = log_path.encode('utf-8')
        result = agora_service_set_log_file(self.service_handle, ctypes.create_string_buffer(encoded_log_path), log_size)
        if result == 0:
            logger.debug(f"Log file set successfully: {log_path}")
        else:
            logger.error(f"Failed to set log file. Error code: {result}")
        return result
    #apm related:
#apm related api
def _get_audio_filter_position(is_local_track: bool = False) -> int:
    if is_local_track:
        return 3
    return 2

def _enable_audio_filter_by_track(track: any, name: str, enable: bool, is_local_track: bool) -> int:
    if track is None:
        return -1000
    c_name = ctypes.c_char_p(name.encode('utf-8'))
    c_enable = ctypes.c_int(0)
    if enable:
        c_enable = ctypes.c_int(1)
    position = _get_audio_filter_position(is_local_track)
    return int(agora_audio_track_enable_audio_filter(track, c_name, c_enable, ctypes.c_int(position)))
def _set_filter_property_by_track(track: any, name: str, key: str, value: str, is_local_track: bool) -> int:
    if track is None:
        return -1000
    c_name = ctypes.c_char_p(name.encode('utf-8'))
    c_key = ctypes.c_char_p(key.encode('utf-8'))
    c_value = ctypes.c_char_p(value.encode('utf-8'))
    position = _get_audio_filter_position(is_local_track)
    return int(agora_audio_track_set_filter_property(track, c_name, c_key, c_value, ctypes.c_int(position)))

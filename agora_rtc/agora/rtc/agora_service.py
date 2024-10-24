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

agora_service_create_custom_audio_track_encoded = agora_lib.agora_service_create_custom_audio_track_encoded
agora_service_create_custom_audio_track_encoded.argtypes = [AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int]
agora_service_create_custom_audio_track_encoded.restype = AGORA_HANDLE

agora_rtc_conn_create = agora_lib.agora_rtc_conn_create
agora_rtc_conn_create.restype = AGORA_HANDLE
agora_rtc_conn_create.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnConfigInner)]

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


class AgoraService:
    def __init__(self) -> None:
        self.service_handle = agora_service_create()

        # set tag???
        self.inited = False

    def initialize(self, config: AgoraServiceConfig):
        if self.inited == True:
            return 0
        config.app_id = config.appid.encode('utf-8')
        result = agora_service_initialize(self.service_handle, ctypes.byref(AgoraServiceConfigInner.create(config=config)))
        if result == 0:
            self.inited = True
        logger.debug(f'Initialization result: {result}')

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

        if config.log_path:
            log_size = 512 * 1024
            if config.log_size > 0:
                log_size = config.log_size
            agora_service_set_log_file(self.service_handle, ctypes.create_string_buffer(config.log_path.encode('utf-8')), log_size)

        return result

    def release(self):
        if self.inited == False:
            return

        if self.service_handle:
            agora_service_release(self.service_handle)

        self.inited = False
        self.service_handle = None

    # createMediaNodeFactory: to create a medianode factory object
    def create_media_node_factory(self):
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
        return AgoraParameter(agora_parameter)

    def create_rtc_connection(self, con_config: RTCConnConfig):
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        rtc_conn_handle = agora_rtc_conn_create(self.service_handle, ctypes.byref(RTCConnConfigInner.create(con_config)))
        if rtc_conn_handle is None:
            return None
        return RTCConnection(rtc_conn_handle)

    # createCustomAudioTrackPcm: creatae a custom audio track from pcm data sender
    def create_custom_audio_track_pcm(self, audio_pcm_data_sender: AudioPcmDataSender) -> LocalAudioTrack:
        if not self.inited:
            logger.error("AgoraService is not initialized. Please call initialize() first.")
            return None
        custom_audio_track = agora_service_create_custom_audio_track_pcm(self.service_handle, audio_pcm_data_sender.sender_handle)
        if custom_audio_track is None:
            return None
        return LocalAudioTrack(custom_audio_track)
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

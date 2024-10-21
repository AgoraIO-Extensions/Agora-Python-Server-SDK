from ._ctypes_handle._ctypes_data import *
import ctypes
from .agora_base import *
import logging
logger = logging.getLogger(__name__)

# Add these function definitions at the module level
agora_local_video_track_set_enabled = agora_lib.agora_local_video_track_set_enabled
agora_local_video_track_set_enabled.restype = ctypes.c_int
agora_local_video_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_video_track_set_video_encoder_config = agora_lib.agora_local_video_track_set_video_encoder_config
agora_local_video_track_set_video_encoder_config.restype = ctypes.c_int
agora_local_video_track_set_video_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoEncoderConfigurationInner)]

agora_local_video_track_enable_simulcast_stream = agora_lib.agora_local_video_track_enable_simulcast_stream
agora_local_video_track_enable_simulcast_stream.restype = ctypes.c_int
agora_local_video_track_enable_simulcast_stream.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.POINTER(SimulcastStreamConfigInner)]

# agora_local_video_track_update_simulcast_stream = agora_lib.agora_local_video_track_update_simulcast_stream
# agora_local_video_track_update_simulcast_stream.restype = ctypes.c_int
# agora_local_video_track_update_simulcast_stream.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.POINTER(SimulcastStreamConfig)]

agora_local_video_track_get_state = agora_lib.agora_local_video_track_get_state
agora_local_video_track_get_state.restype = ctypes.c_int
agora_local_video_track_get_state.argtypes = [AGORA_HANDLE]

agora_local_video_track_get_statistics = agora_lib.agora_local_video_track_get_statistics
agora_local_video_track_get_statistics.restype = ctypes.POINTER(LocalVideoTrackStatsInner)
agora_local_video_track_get_statistics.argtypes = [AGORA_HANDLE]

agora_local_video_track_destroy_statistics = agora_lib.agora_local_video_track_destroy_statistics
agora_local_video_track_destroy_statistics.restype = None
agora_local_video_track_destroy_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(LocalVideoTrackStatsInner)]

# agora_local_video_track_get_type = agora_lib.agora_local_video_track_get_type
# agora_local_video_track_get_type.restype = ctypes.c_int
# agora_local_video_track_get_type.argtypes = [AGORA_HANDLE]

agora_local_video_track_destroy = agora_lib.agora_local_video_track_destroy
agora_local_video_track_destroy.restype = AGORA_HANDLE
agora_local_video_track_destroy.argtypes = [AGORA_HANDLE]


class LocalVideoTrack:
    def __init__(self, track_handle):
        self.track_handle = track_handle

    def set_enabled(self, enable):
        agora_local_video_track_set_enabled(self.track_handle, enable)

    def set_video_encoder_configuration(self, config: VideoEncoderConfiguration):
        ret = agora_local_video_track_set_video_encoder_config(self.track_handle, ctypes.byref(VideoEncoderConfigurationInner.create(config)))
        return ret

    def enable_simulcast_stream(self, enabled, config):
        ret = agora_local_video_track_enable_simulcast_stream(self.track_handle, enabled, ctypes.byref(config))
        return ret

    # def update_simulcast_stream(self, enabled, config):
    #     ret = agora_local_video_track_update_simulcast_stream(self.track_handle, enabled, ctypes.byref(config))
    #     return ret

    def get_state(self):
        return agora_local_video_track_get_state(self.track_handle)

    def get_statistics(self):
        stats_ptr = agora_local_video_track_get_statistics(self.track_handle)
        if not stats_ptr:
            logger.error("Failed to get local video track statistics")
            return None
        stats = stats_ptr.contents
        return stats

    def destroy_statistics(self, stats):
        if self.track_handle:
            agora_local_video_track_destroy_statistics(self.track_handle, stats)

    # def get_type(self):
    #     return agora_local_video_track_get_type(self.track_handle)

    def release(self):
        if self.track_handle:
            agora_local_video_track_destroy(self.track_handle)
            self.track_handle = None
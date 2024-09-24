import ctypes
from .agora_base import *
import logging
logger = logging.getLogger(__name__)


class RemoteAudioTrackStats(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("quality", ctypes.c_int),
        ("network_transport_delay", ctypes.c_int),
        ("jitter_buffer_delay", ctypes.c_int),
        ("audio_loss_rate", ctypes.c_int),
        ("num_channels", ctypes.c_int),
        ("received_sample_rate", ctypes.c_int),
        ("received_bitrate", ctypes.c_int),
        ("total_frozen_time", ctypes.c_int),
        ("frozen_rate", ctypes.c_int),
        ("received_bytes", ctypes.c_int64)
    ]

agora_remote_audio_track_get_statistics = agora_lib.agora_remote_audio_track_get_statistics
agora_remote_audio_track_get_statistics.restype = ctypes.POINTER(RemoteAudioTrackStats)
agora_remote_audio_track_get_statistics.argtypes = [AGORA_HANDLE]

agora_remote_audio_track_destroy_statistics = agora_lib.agora_remote_audio_track_destroy_statistics
agora_remote_audio_track_destroy_statistics.restype = None
agora_remote_audio_track_destroy_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(RemoteAudioTrackStats)]

agora_remote_audio_track_get_state = agora_lib.agora_remote_audio_track_get_state
agora_remote_audio_track_get_state.restype = ctypes.c_int
agora_remote_audio_track_get_state.argtypes = [AGORA_HANDLE]

#Note: up to now(2024.09.04),spatial audio & mediapackreceiver are not supported!
#if any request, please contact us.


class RemoteAudioTrack:
    def __init__(self, track_handle, user_id): #user_id is a string
        self.track_handle = track_handle
        self.user_id = user_id #string


    def get_statistics(self):
        stats_ptr = agora_remote_audio_track_get_statistics(self.track_handle)
        if not stats_ptr:
            logger.error("Failed to get remote audio track statistics")
            return None
        stats = stats_ptr.contents
        #NOTE: MUST call c api to release this handle! Otherwise, it will cause memory leak.
        agora_remote_audio_track_destroy_statistics(self.track_handle, stats_ptr)
    
        return stats



    def get_state(self):
        state =  agora_remote_audio_track_get_state(self.track_handle)
        return state
    
    
    #note:
    # do not release the track_handle in python/go wrapper layer, the life cycle is managed by C++ layer.
    # so just return None here and do nothing
    def release(self):
        pass
import time
import ctypes
from .agora_base import *

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
    ]

agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
agora_local_user_publish_audio.restype = AGORA_API_C_INT
agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

class LocalAudioTrack:
    def __init__(self, track) -> None:
        self.track = track
     
    def publish_audio(self, local_audio_track):
        ret = agora_local_user_publish_audio(self.connection, local_audio_track.track)
        return ret

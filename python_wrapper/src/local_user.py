import time
import ctypes
from .agora_base import *

agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
agora_local_user_publish_audio.restype = AGORA_API_C_INT
agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

class LocalUser:
    def __init__(self, local_user) -> None:
        self.local_user = local_user
     
    def publish_audio(self, local_audio_track):
        ret = agora_local_user_publish_audio(self.local_user, local_audio_track.track)
        return ret

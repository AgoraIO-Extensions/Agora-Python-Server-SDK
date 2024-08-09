import ctypes
from .agora_base import *

class PcmAudioFrame:
    def __init__(self):
        self.data = []
        self.timestamp = 0
        self.samples_per_channel = 0
        self.bytes_per_sample = 0
        self.number_of_channels = 0
        self.sample_rate = 0


agora_audio_pcm_data_sender_send = agora_lib.agora_audio_pcm_data_sender_send
agora_audio_pcm_data_sender_send.restype = AGORA_API_C_INT
agora_audio_pcm_data_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]

agora_local_audio_track_destroy = agora_lib.agora_local_audio_track_destroy
agora_local_audio_track_destroy.argtypes = [AGORA_HANDLE]

agora_audio_pcm_data_sender_destroy = agora_lib.agora_audio_pcm_data_sender_destroy
agora_audio_pcm_data_sender_destroy.argtypes = [ctypes.c_void_p]

agora_local_audio_track_set_enabled = agora_lib.agora_local_audio_track_set_enabled
agora_local_audio_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
agora_local_user_publish_audio.restype = AGORA_API_C_INT
agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unpublish_audio = agora_lib.agora_local_user_unpublish_audio
agora_local_user_unpublish_audio.restype = AGORA_API_C_INT
agora_local_user_unpublish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_audio_track_adjust_publish_volume = agora_lib.agora_local_audio_track_adjust_publish_volume
agora_local_audio_track_adjust_publish_volume.restype = AGORA_API_C_INT
agora_local_audio_track_adjust_publish_volume.argtypes = [AGORA_HANDLE, ctypes.c_int]

#todo: need check restype, by wei 0720
agora_local_audio_track_set_max_buffer_audio_frame_number = agora_lib.agora_local_audio_track_set_max_buffer_audio_frame_number
agora_local_audio_track_set_max_buffer_audio_frame_number.restype = AGORA_API_C_INT
agora_local_audio_track_set_max_buffer_audio_frame_number.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_audio_track_clear_buffer = agora_lib.agora_local_audio_track_clear_buffer
agora_local_audio_track_clear_buffer.restype = AGORA_API_C_INT
agora_local_audio_track_clear_buffer.argtypes = [AGORA_HANDLE]


class AudioPcmDataSender:
    def __init__(self, audio_pcm_data_sender, audio_track, local_user) -> None:
        self.audio_pcm_data_sender = audio_pcm_data_sender
        self.audio_track = audio_track
        self.local_user = local_user


    def Release(self):
        if self.audio_pcm_data_sender == None:
            return
        agora_local_audio_track_destroy(self.audio_pcm_data_sender)
        agora_audio_pcm_data_sender_destroy(self.audio_track)

    def Start(self):
        agora_local_audio_track_set_enabled(self.audio_track, 1)
        ret = agora_local_user_publish_audio(self.local_user, self.audio_track)
        return ret
    
    def Stop(self):
        ret = agora_local_user_unpublish_audio(self.local_user, self.audio_track)
        agora_local_audio_track_set_enabled(self.audio_track, 0)
        return ret

    def SendPcmData(self, frame):
        c_data = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
        return agora_audio_pcm_data_sender_send(self.audio_pcm_data_sender, c_data, frame.timestamp, frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)
        
    def AdjustVolume(self, volume):
        return agora_local_audio_track_adjust_publish_volume(self.audio_track, volume)
    
    def SetSendBufferSize(self, bufSize):
        ret = agora_local_audio_track_set_max_buffer_audio_frame_number(self.audio_track, bufSize)
        return ret

    def ClearSendBuffer(self):
        ret = agora_local_audio_track_clear_buffer(self.audio_track)
        return ret


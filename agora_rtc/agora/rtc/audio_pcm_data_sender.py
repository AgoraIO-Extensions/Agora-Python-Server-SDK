import ctypes
from .agora_base import *

class PcmAudioFrame:
    def __init__(self):
        self.data = None
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


class AudioPcmDataSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_audio_pcm_data(self, frame:PcmAudioFrame):
        c_data = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
        c_data_ptr = ctypes.cast(c_data, ctypes.POINTER(ctypes.c_void_p))
        return agora_audio_pcm_data_sender_send(self.sender_handle, c_data_ptr, frame.timestamp, frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)
    
    def release(self):
        agora_audio_pcm_data_sender_destroy(self.sender_handle)

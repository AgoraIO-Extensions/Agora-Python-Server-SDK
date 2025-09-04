import ctypes
from .agora_base import *
from ._ctypes_handle._ctypes_data import *


agora_audio_pcm_data_sender_send = agora_lib.agora_audio_pcm_data_sender_send
agora_audio_pcm_data_sender_send.restype = AGORA_API_C_INT
agora_audio_pcm_data_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int64,ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]

agora_audio_pcm_data_sender_destroy = agora_lib.agora_audio_pcm_data_sender_destroy
agora_audio_pcm_data_sender_destroy.restype = AGORA_API_C_VOID
agora_audio_pcm_data_sender_destroy.argtypes = [ctypes.c_void_p]


class AudioPcmDataSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_audio_pcm_data(self, frame: PcmAudioFrame):
        c_data = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
        c_data_ptr = ctypes.cast(c_data, ctypes.POINTER(ctypes.c_void_p))
        # c_data_ptr = ctypes.cast(frame.data, ctypes.c_char_p)
        pts = ctypes.c_int64(frame.present_time_ms)
        ret = agora_audio_pcm_data_sender_send(self.sender_handle, c_data_ptr, frame.timestamp, pts,frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)
        #print(f"send_audio_pcm_data: {frame.present_time_ms}, {pts}")
        frame.data = None
        frame = None
        return ret

    def release(self):
        if self.sender_handle:
            agora_audio_pcm_data_sender_destroy(self.sender_handle)
            self.sender_handle = None

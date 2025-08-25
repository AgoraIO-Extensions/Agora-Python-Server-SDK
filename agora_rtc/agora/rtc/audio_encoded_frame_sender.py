import ctypes
from .agora_base import *
from ._ctypes_handle._ctypes_data import *
import logging
logger = logging.getLogger(__name__)

agora_audio_encoded_frame_sender_send = agora_lib.agora_audio_encoded_frame_sender_send
agora_audio_encoded_frame_sender_send.restype = AGORA_API_C_INT
agora_audio_encoded_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(EncodedAudioFrameInfoInner)]

agora_audio_encoded_frame_sender_destroy = agora_lib.agora_audio_encoded_frame_sender_destroy
agora_audio_encoded_frame_sender_destroy.restype = AGORA_API_C_VOID
agora_audio_encoded_frame_sender_destroy.argtypes = [AGORA_HANDLE]


class AudioEncodedFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    # def send_encoded_audio_frame(self, frame:EncodedAudioFrame):
    #     c_date = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
    #     ownedinfo = frame.to_owned_encoded_audio_frame()
    #     ret = agora_audio_encoded_frame_sender_send(self.sender_handle, c_date, ctypes.c_uint32(len(frame.data)), ctypes.byref(ownedinfo))
    #     return ret

    def send_encoded_audio_frame(self, buffer_ptr: int, buffer_size: int, frame_info: EncodedAudioFrameInfo):
        buffer_ptr = ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_void_p))
        ret = agora_audio_encoded_frame_sender_send(self.sender_handle, buffer_ptr, ctypes.c_uint32(buffer_size), ctypes.byref(EncodedAudioFrameInfoInner.create(frame_info)))
        return ret
    def send_encoded_audio_frame_withbytes(self, data, frame_info: EncodedAudioFrameInfo):
        buffer_size = len(data)
       
            # 将 bytearray 转换为 c_char_p 而不拷贝内存
        if isinstance(data, bytearray):
            c_data = ctypes.cast(data, ctypes.POINTER(ctypes.c_void_p))
        else:
            # 如果已经是 bytes，直接转换
            c_data = ctypes.cast(data, ctypes.POINTER(ctypes.c_void_p))
        
        ret = agora_audio_encoded_frame_sender_send(self.sender_handle, c_data, ctypes.c_uint32(buffer_size), ctypes.byref(EncodedAudioFrameInfoInner.create(frame_info)))
        return ret

    def release(self):
        if self.sender_handle:
            agora_audio_encoded_frame_sender_destroy(self.sender_handle)
            self.sender_handle = None
        return 0

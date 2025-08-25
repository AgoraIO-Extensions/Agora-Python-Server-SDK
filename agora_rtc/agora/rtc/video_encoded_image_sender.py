import ctypes
from .agora_base import *
from ._ctypes_handle._ctypes_data import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)


agora_video_encoded_image_sender_send = agora_lib.agora_video_encoded_image_sender_send
agora_video_encoded_image_sender_send.restype = AGORA_API_C_INT
agora_video_encoded_image_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(EncodedVideoFrameInfoInner)]

agora_video_encoded_image_sender_destroy = agora_lib.agora_video_encoded_image_sender_destroy
agora_video_encoded_image_sender_destroy.restype = AGORA_API_C_VOID
agora_video_encoded_image_sender_destroy.argtypes = [AGORA_HANDLE]


class VideoEncodedImageSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_encoded_video_image(self, buffer_ptr: int, buffer_size: int, frame_info: EncodedVideoFrameInfo):
        buffer_pointer = ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_uint8))
        ret = agora_video_encoded_image_sender_send(self.sender_handle, buffer_pointer, buffer_size, EncodedVideoFrameInfoInner.create(frame_info))
        if ret != 1:
            logger.error(f"Failed to send video frame, error code: {ret}")
        return ret
    def send_encoded_video_image_withbytes(self, data, frame_info: EncodedVideoFrameInfo):
        buffer_size = len(data)
        if isinstance(data, bytearray):
            c_data = ctypes.cast(data, ctypes.POINTER(ctypes.c_uint8))
        else:
            c_data = ctypes.cast(data, ctypes.POINTER(ctypes.c_uint8))
        ret = agora_video_encoded_image_sender_send(self.sender_handle, c_data, buffer_size, EncodedVideoFrameInfoInner.create(frame_info)) 
        return ret

    def release(self):
        if self.sender_handle:
            agora_video_encoded_image_sender_destroy(self.sender_handle)
            self.sender_handle = None
        return

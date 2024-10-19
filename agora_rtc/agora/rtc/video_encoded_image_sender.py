import ctypes
from .agora_base import *
from ._ctypes_handle._ctypes_data import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)


agora_video_encoded_image_sender_send = agora_lib.agora_video_encoded_image_sender_send
agora_video_encoded_image_sender_send.restype = AGORA_API_C_INT
agora_video_encoded_image_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(EncodedVideoFrameInfoInner)]


class VideoEncodedImageSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_encoded_video_image(self, buffer_ptr: int, buffer_size: int, frame_info: EncodedVideoFrameInfo):
        # cdata = (ctypes.c_uint8 * size).from_buffer(data)
        # encoded_video_frame = frame_info.to_owned_encoded_video_frame_info()
        # ret = agora_video_encoded_image_sender_send(self.sender_handle, cdata, size, ctypes.byref(encoded_video_frame))
        # buffer_ptr
        buffer_pointer = ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_uint8))
        encoded_video_frame = frame_info.to_owned_encoded_video_frame_info()
        ret = agora_video_encoded_image_sender_send(self.sender_handle, buffer_pointer, buffer_size, ctypes.byref(encoded_video_frame))
        if ret != 1:
            logger.error(f"Failed to send video frame, error code: {ret}")
        return ret

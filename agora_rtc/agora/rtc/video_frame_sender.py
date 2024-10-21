from ._ctypes_handle._ctypes_data import *
import ctypes
from .agora_base import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ExternalVideoFrameInner)]

agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = None
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]


class VideoFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_video_frame(self, frame: ExternalVideoFrame):
        ret = agora_video_frame_sender_send(self.sender_handle, ctypes.byref(ExternalVideoFrameInner.create(frame)))
        frame.buffer = None
        frame = None
        return ret

    def release(self):
        if self.sender_handle:
            agora_video_frame_sender_destroy(self.sender_handle)
            self.sender_handle = None
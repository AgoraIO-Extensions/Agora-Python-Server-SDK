import ctypes
from .agora_base import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(OwnedExternalVideoFrame)]

agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = None
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]


class VideoFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_video_frame(self, frame: ExternalVideoFrame):
        owned_video_frame = frame.to_owned_external_video_frame()
        ret = agora_video_frame_sender_send(self.sender_handle, owned_video_frame)
        frame.buffer = None
        frame = None
        return ret

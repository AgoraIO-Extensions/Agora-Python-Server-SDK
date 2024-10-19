

from ._ctypes_data import *
import ctypes
from ..agora_base import *
from ..video_encoded_frame_observer import IVideoEncodedFrameObserver, EncodedVideoFrameInfo
import logging
logger = logging.getLogger(__name__)


ON_ENCODED_VIDEO_FRAME = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, uid_t, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.POINTER(EncodedVideoFrameInfoInner))


class VideoEncodedFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_encoded_video_frame", ON_ENCODED_VIDEO_FRAME)
    ]

    def __init__(self, video_encoded_frame_observer: 'IVideoEncodedFrameObserver'):
        self.video_encoded_frame_observer = video_encoded_frame_observer
        self.on_encoded_video_frame = ON_ENCODED_VIDEO_FRAME(self._on_encoded_video_frame)

    def _on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info):
        # logger.debug("VideoEncodedFrameObserverInnerCB on_encoded_video_frame")
        img_buffer = ctypes.string_at(image_buffer, length)
        vefi = video_encoded_frame_info.contents.get()
        self.video_encoded_frame_observer.on_encoded_video_frame(uid, img_buffer, length, vefi)
        return 1



import ctypes
from .agora_base import *
from ._video_frame_observer import encoded_video_frame_info
from .video_encoded_frame_observer import IVideoEncodedFrameObserver

# typedef struct _video_encoded_frame_observer {
#   int (*on_encoded_video_frame)(AGORA_HANDLE agora_video_encoded_frame_observer, uid_t uid, const uint8_t* image_buffer, size_t length,
#                                 const encoded_video_frame_info* video_encoded_frame_info);
# } video_encoded_frame_observer;

ON_ENCODED_VIDEO_FRAME = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, uid_t, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.POINTER(encoded_video_frame_info))

class VideoEncodedFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_encoded_video_frame", ON_ENCODED_VIDEO_FRAME)
    ]

    def __init__(self, video_encoded_frame_observer:'IVideoEncodedFrameObserver'):
        self.video_encoded_frame_observer = video_encoded_frame_observer
        self.on_encoded_video_frame = ON_ENCODED_VIDEO_FRAME(self._on_encoded_video_frame)
    
    def _on_encoded_video_frame(self, agora_video_encoded_frame_observer ,uid, image_buffer, length, video_encoded_frame_info):
        print("VideoEncodedFrameObserverInnerCB on_encoded_video_frame")
        self.video_encoded_frame_observer.on_encoded_video_frame(agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info)
        return 1
        # if self.on_encoded_video_frame:
        #     return self.on_encoded_video_frame(uid, image_buffer, length, video_encoded_frame_info)
        # return 0
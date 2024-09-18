

import ctypes
from .agora_base import *
from .video_encoded_frame_observer import IVideoEncodedFrameObserver, EncodedVideoFrameInfo

# typedef struct _video_encoded_frame_observer {
#   int (*on_encoded_video_frame)(AGORA_HANDLE agora_video_encoded_frame_observer, uid_t uid, const uint8_t* image_buffer, size_t length,
#                                 const encoded_video_frame_info* video_encoded_frame_info);
# } video_encoded_frame_observer;


class EncodedVideoFrameInfoInner(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("frames_per_second", ctypes.c_int),
        ("frame_type", ctypes.c_int),
        ("rotation", ctypes.c_int),
        ("track_id", ctypes.c_int),
        ("capture_time_ms", ctypes.c_int64),
        ("decode_time_ms", ctypes.c_int64),
        ("uid", ctypes.c_uint),
        ("stream_type", ctypes.c_int)
    ]

    def _to_encoded_video_frame_info(self):
        encoded_video_frame_info = EncodedVideoFrameInfo()
        encoded_video_frame_info.codec_type = self.codec_type
        encoded_video_frame_info.width = self.width
        encoded_video_frame_info.height = self.height
        encoded_video_frame_info.frames_per_second = self.frames_per_second
        encoded_video_frame_info.frame_type = self.frame_type
        encoded_video_frame_info.rotation = self.rotation
        encoded_video_frame_info.track_id = self.track_id
        encoded_video_frame_info.capture_time_ms = self.capture_time_ms
        encoded_video_frame_info.decode_time_ms = self.decode_time_ms
        encoded_video_frame_info.uid = self.uid
        encoded_video_frame_info.stream_type = self.stream_type
        return encoded_video_frame_info


ON_ENCODED_VIDEO_FRAME = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, uid_t, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.POINTER(EncodedVideoFrameInfoInner))

class VideoEncodedFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_encoded_video_frame", ON_ENCODED_VIDEO_FRAME)
    ]

    def __init__(self, video_encoded_frame_observer:'IVideoEncodedFrameObserver'):
        self.video_encoded_frame_observer = video_encoded_frame_observer
        self.on_encoded_video_frame = ON_ENCODED_VIDEO_FRAME(self._on_encoded_video_frame)
    
    def _on_encoded_video_frame(self, agora_video_encoded_frame_observer ,uid, image_buffer, length, video_encoded_frame_info):
        print("VideoEncodedFrameObserverInnerCB on_encoded_video_frame")
        img_buffer = ctypes.string_at(image_buffer, length)
        vefi = video_encoded_frame_info.contents._to_encoded_video_frame_info()
        self.video_encoded_frame_observer.on_encoded_video_frame(agora_video_encoded_frame_observer, uid, img_buffer, length, vefi)
        return 1

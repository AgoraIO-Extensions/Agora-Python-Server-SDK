import ctypes
from .agora_base import *
from .local_user import *
from .video_frame_observer import *

AGORA_HANDLE = ctypes.c_void_p

class VideoFrame(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("y_stride", ctypes.c_int),
        ("u_stride", ctypes.c_int),
        ("v_stride", ctypes.c_int),
        ("y_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("u_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("v_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("rotation", ctypes.c_int),
        ("render_time_ms", ctypes.c_int64),
        ("avsync_type", ctypes.c_int),
        ("metadata_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("metadata_size", ctypes.c_int),
        ("shared_context", ctypes.c_void_p),
        ("texture_id", ctypes.c_int),
        ("matrix", ctypes.c_float * 16),
        ("alpha_buffer", ctypes.POINTER(ctypes.c_uint8))
    ]

ON_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(VideoFrame))

class VideoFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_frame", ON_FRAME_CALLBACK)
    ]

    def __init__(self, video_frame_observer:IVideoFrameObserver, local_user:'LocalUser'):
        self.video_frame_observer = video_frame_observer
        self.local_user = local_user
        self.on_frame = ON_FRAME_CALLBACK(self._on_frame)


    def _on_frame(self, agora_handle, channel_id, user_id, video_frame):
        print("VideoFrameObserver _on_frame:", agora_handle, channel_id, user_id, video_frame)
        self.video_frame_observer.on_frame(agora_handle, channel_id, user_id, video_frame)
    



class encoded_video_frame_info(ctypes.Structure):
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

ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(encoded_video_frame_info))

class VideoEncodedImageReceiverInner(ctypes.Structure):
    _fields_ = [
        ("on_encoded_video_image_received", ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK)
    ]

    def __init__(self, video_encoded_image_receiver:'IVideoEncodedImageReceiver'):
        self.video_encoded_image_receiver = video_encoded_image_receiver
        self.on_encoded_video_image_received = ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK(self._on_encoded_video_image_received)


    def _on_encoded_video_image_received(self, agora_handle, image_buffer, length, info):
        print("VideoFrameObserver _on_frame:", agora_handle, image_buffer, length, info)
        # self.on_encoded_video_image_received(agora_handle, image_buffer, length, info)
        self.video_encoded_image_receiver.on_encoded_video_image_received(agora_handle, image_buffer, length, info)



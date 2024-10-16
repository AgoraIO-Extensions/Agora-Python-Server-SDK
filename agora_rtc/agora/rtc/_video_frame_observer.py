import ctypes
from .agora_base import *
from .local_user import *
from .video_frame_observer import *
import logging
logger = logging.getLogger(__name__)

class VideoFrameInner(ctypes.Structure):
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

    def to_video_frame(self):
        video_frame = VideoFrame()
        video_frame.type = self.type
        video_frame.width = self.width
        video_frame.height = self.height
        video_frame.y_stride = self.y_stride
        video_frame.u_stride = self.u_stride
        video_frame.v_stride = self.v_stride
        video_frame.y_buffer = ctypes.string_at(self.y_buffer, self.y_stride * self.height) if self.y_buffer else None
        video_frame.u_buffer = ctypes.string_at(self.u_buffer, self.u_stride * self.height // 2) if self.u_buffer else None
        video_frame.v_buffer = ctypes.string_at(self.v_buffer, self.v_stride * self.height // 2) if self.v_buffer else None
        video_frame.rotation = self.rotation
        video_frame.render_time_ms = self.render_time_ms
        video_frame.avsync_type = self.avsync_type
        video_frame.metadata_buffer = ctypes.string_at(self.metadata_buffer, self.metadata_size) if self.metadata_buffer else None
        video_frame.metadata_size = self.metadata_size
        video_frame.shared_context = self.shared_context.decode() if self.shared_context else None
        video_frame.texture_id = self.texture_id
        video_frame.matrix = self.matrix
        video_frame.alpha_buffer = self.alpha_buffer
        video_frame.metadata = video_frame.metadata_buffer.decode() if video_frame.metadata_buffer else None
        return video_frame

ON_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(VideoFrameInner))

agora_video_frame_observer_get_rotation_applied = agora_lib.agora_video_frame_observer_get_rotation_applied
agora_video_frame_observer_get_rotation_applied.restype = ctypes.c_int
agora_video_frame_observer_get_rotation_applied.argtypes = [AGORA_HANDLE]


class VideoFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_frame", ON_FRAME_CALLBACK)
    ]

    def __init__(self, video_frame_observer:IVideoFrameObserver, local_user:'LocalUser'):
        self.video_frame_observer = video_frame_observer
        self.local_user = local_user
        self.on_frame = ON_FRAME_CALLBACK(self._on_frame)


    def _on_frame(self, agora_handle, channel_id, remote_uid, frame:VideoFrameInner):
        vf = frame.contents
        self.video_frame_observer.on_frame(channel_id.decode() if channel_id else None, remote_uid.decode(), vf.to_video_frame())
    
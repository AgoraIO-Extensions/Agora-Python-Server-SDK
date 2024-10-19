import ctypes
from ..agora_base import *
from ..local_user import *
from ..video_frame_observer import *
import logging
logger = logging.getLogger(__name__)

ON_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(VideoFrameInner))

agora_video_frame_observer_get_rotation_applied = agora_lib.agora_video_frame_observer_get_rotation_applied
agora_video_frame_observer_get_rotation_applied.restype = ctypes.c_int
agora_video_frame_observer_get_rotation_applied.argtypes = [AGORA_HANDLE]


class VideoFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_frame", ON_FRAME_CALLBACK)
    ]

    def __init__(self, video_frame_observer: IVideoFrameObserver, local_user: 'LocalUser'):
        self.video_frame_observer = video_frame_observer
        self.local_user = local_user
        self.on_frame = ON_FRAME_CALLBACK(self._on_frame)

    def _on_frame(self, agora_handle, channel_id, remote_uid, frame: VideoFrameInner):
        vf = frame.contents
        self.video_frame_observer.on_frame(channel_id.decode() if channel_id else None, remote_uid.decode(), vf.get())

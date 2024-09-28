import ctypes
from .agora_base import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)


class OwnedExternalVideoFrame(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("format", ctypes.c_int),
        ("buffer", ctypes.c_void_p),
        ("stride", ctypes.c_int),
        ("height", ctypes.c_int),
        ("crop_left", ctypes.c_int),
        ("crop_top", ctypes.c_int),
        ("crop_right", ctypes.c_int),
        ("crop_bottom", ctypes.c_int),
        ("rotation", ctypes.c_int),
        ("timestamp", ctypes.c_longlong),
        ("egl_context", ctypes.c_void_p),
        ("egl_type", ctypes.c_int),
        ("texture_id", ctypes.c_int),
        ("matrix", ctypes.c_float * 16),
        ("metadata_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("metadata_size", ctypes.c_int),
        ("alpha_buffer", ctypes.c_void_p)
    ]

class ExternalVideoFrame:
    def __init__(self)->None:
        self.type = 1
        self.format = 0
        self.buffer = None
        self.stride = 0
        self.height = 0
        self.crop_left = 0
        self.crop_top = 0
        self.crop_right = 0
        self.crop_bottom = 0
        self.rotation = 0
        self.timestamp = 0
        self.egl_context = None
        self.egl_type = 0
        self.texture_id = 0
        self.matrix = []
        self.metadata = ""
        self.alpha_buffer = None

    def to_owned_external_video_frame(self):
        c_buffer = (ctypes.c_uint8 * len(self.buffer)).from_buffer(self.buffer)
        c_buffer_ptr = ctypes.cast(c_buffer, ctypes.c_void_p)
        cdata = bytearray(self.metadata.encode('utf-8'))
        c_metadata = (ctypes.c_uint8 * len(cdata)).from_buffer(cdata)
        c_matrix_buffer = (ctypes.c_float * 16)(*self.matrix)
        return OwnedExternalVideoFrame(
            self.type,
            self.format,
            c_buffer_ptr,
            self.stride,
            self.height,
            self.crop_left,
            self.crop_top,
            self.crop_right,
            self.crop_bottom,
            self.rotation,
            self.timestamp,
            self.egl_context,
            self.egl_type,
            self.texture_id,
            c_matrix_buffer,
            c_metadata,
            len(cdata),
            self.alpha_buffer
        )

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(OwnedExternalVideoFrame)]

agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = None
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]

class VideoFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
        
    def send_video_frame(self, frame:ExternalVideoFrame):
        owned_video_frame = frame.to_owned_external_video_frame()
        ret = agora_video_frame_sender_send(self.sender_handle, owned_video_frame)
        return ret

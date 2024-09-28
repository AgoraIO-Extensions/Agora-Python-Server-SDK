import ctypes
from .agora_base import *
from agora.rtc.video_frame_observer import *
import logging
logger = logging.getLogger(__name__)

class OwnedEncodedVideoFrameInfo(ctypes.Structure):
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

    def __init__(self, codec_type=0, width=0, height=0, frames_per_second=0, frame_type=0, rotation=0, track_id=0, capture_time_ms=0, decode_time_ms=0, uid=0, stream_type=0):
        self.codec_type = codec_type
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.frame_type = frame_type    
        self.rotation = rotation
        self.track_id = track_id
        self.capture_time_ms = capture_time_ms
        self.decode_time_ms = decode_time_ms
        self.uid = uid
        self.stream_type = stream_type
       
class EncodedVideoFrameInfo:
    def __init__(self, codec_type=0, width=0, height=0, frames_per_second=0, frame_type=0, rotation=0, track_id=0, capture_time_ms=0, decode_time_ms=0, uid=0, stream_type=0):
        self.codec_type = codec_type
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.frame_type = frame_type
        self.rotation = rotation
        self.track_id = track_id
        self.capture_time_ms = capture_time_ms
        self.decode_time_ms = decode_time_ms
        self.uid = uid
        self.stream_type = stream_type

    def __repr__(self):
        return f"EncodedVideoFrameInfo(codec_type={self.codec_type}, width={self.width}, height={self.height}, frames_per_second={self.frames_per_second}, frame_type={self.frame_type}, rotation={self.rotation}, track_id={self.track_id}, capture_time_ms={self.capture_time_ms}, decode_time_ms={self.decode_time_ms}, uid={self.uid}, stream_type={self.stream_type})"
    def to_owned_encoded_video_frame_info(self):
        return OwnedEncodedVideoFrameInfo(
            self.codec_type,
            self.width,
            self.height,
            self.frames_per_second,
            self.frame_type,
            self.rotation,
            self.track_id,
            self.capture_time_ms,
            self.decode_time_ms,
            self.uid,
            self.stream_type
        )


agora_video_encoded_image_sender_send = agora_lib.agora_video_encoded_image_sender_send
agora_video_encoded_image_sender_send.restype = AGORA_API_C_INT
agora_video_encoded_image_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(OwnedEncodedVideoFrameInfo)]

class VideoEncodedImageSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
        
    def send_encoded_video_image(self, buffer_ptr:int, buffer_size:int, frame_info:EncodedVideoFrameInfo):
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

    
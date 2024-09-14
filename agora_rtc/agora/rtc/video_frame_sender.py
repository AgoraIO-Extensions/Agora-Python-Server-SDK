import ctypes
from .agora_base import *
from agora.rtc.video_frame_observer import *


class OwnedEncodedVideoFrameInfo(ctypes.Structure):
    # _fields_ = [
    #     ('codec_type', ctypes.c_int),
    #     ('width', ctypes.c_int),
    #     ('height', ctypes.c_int),
    #     ('frames_per_second', ctypes.c_int),
    #     ('frame_type', ctypes.c_int),
    #     ('rotation', ctypes.c_int),
    #     ('track_id', ctypes.c_int),
    #     ('render_time_ms', ctypes.c_int64),
    #     ('internal_send_ts', ctypes.c_uint64),
    #     ('uid', ctypes.c_uint),
    # ]

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
        # self.metadata_buffer = bytearray()
        # self.metadata_size = 0
        self.metadata = ""
        self.alpha_buffer = None

    def to_owned_external_video_frame(self):
        c_buffer = (ctypes.c_uint8 * len(self.buffer)).from_buffer(self.buffer)
        # 将 ctypes 数组转换为 c_void_p
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

agora_video_encoded_image_sender_send = agora_lib.agora_video_encoded_image_sender_send
agora_video_encoded_image_sender_send.restype = AGORA_API_C_INT
agora_video_encoded_image_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(OwnedEncodedVideoFrameInfo)]

agora_local_video_track_set_video_encoder_config = agora_lib.agora_local_video_track_set_video_encoder_config
agora_local_video_track_set_video_encoder_config.restype = AGORA_API_C_INT
agora_local_video_track_set_video_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoEncoderConfig)]

agora_local_video_track_set_enabled = agora_lib.agora_local_video_track_set_enabled
agora_local_video_track_set_enabled.restype = AGORA_API_C_INT
agora_local_video_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

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
            print(f"Failed to send video frame, error code: {ret}")
        return ret

    
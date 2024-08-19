import ctypes
from .agora_base import *
from agora_service.video_frame_observer import *

agora_local_video_track_set_video_encoder_config = agora_lib.agora_local_video_track_set_video_encoder_config
agora_local_video_track_set_video_encoder_config.restype = AGORA_API_C_INT
agora_local_video_track_set_video_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoEncoderConfig)]

agora_local_video_track_set_enabled = agora_lib.agora_local_video_track_set_enabled
agora_local_video_track_set_enabled.restype = AGORA_API_C_INT
agora_local_video_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]


class OwnedExternalVideoFrame(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_int),
        ('format', ctypes.c_int),
        ('buffer', ctypes.c_void_p),
        ('stride', ctypes.c_int),
        ('height', ctypes.c_int),
        ('crop_left', ctypes.c_int),
        ('crop_top', ctypes.c_int),
        ('crop_right', ctypes.c_int),
        ('crop_bottom', ctypes.c_int),
        ('rotation', ctypes.c_int),
        ('timestamp', ctypes.c_longlong),
    ]
    def __init__(self, type=1, format=0, buffer=None, stride=0, height=0, crop_left=0, crop_top=0, crop_right=0, crop_bottom=0, rotation=0, timestamp=0)->None:
        self.type = type
        self.format = format
        self.buffer = buffer
        self.stride = stride
        self.height = height
        self.crop_left = crop_left
        self.crop_top = crop_top
        self.crop_right = crop_right
        self.crop_bottom = crop_bottom
        self.rotation = rotation
        self.timestamp = timestamp

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(OwnedExternalVideoFrame)]




# AGORA_API_C_VOID agora_video_frame_sender_destroy(AGORA_HANDLE agora_video_frame_sender);
agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = None
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]




class OwnedEncodedVideoFrameInfo(ctypes.Structure):
    _fields_ = [
        ('codec_type', ctypes.c_int),
        ('width', ctypes.c_int),
        ('height', ctypes.c_int),
        ('frames_per_second', ctypes.c_int),
        ('frame_type', ctypes.c_int),
        ('rotation', ctypes.c_int),
        ('track_id', ctypes.c_int),
        ('render_time_ms', ctypes.c_int64),
        ('internal_send_ts', ctypes.c_uint64),
        ('uid', ctypes.c_uint),
    ]
    def __init__(self, codec_type=0, width=0, height=0, frames_per_second=0, frame_type=0, rotation=0, track_id=0, render_time_ms=0, internal_send_ts=0, uid=0):
        self.codec_type = codec_type
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.frame_type = frame_type    
        self.rotation = rotation
        self.track_id = track_id
        self.render_time_ms = render_time_ms
        self.internal_send_ts = internal_send_ts
        self.uid = uid
       



# AGORA_API_C_INT agora_video_encoded_image_sender_send(AGORA_HANDLE agora_video_encoded_image_sender, uint8_t* image_data, uint32_t image_data_size, agora::rtc::EncodedVideoFrameInfo* info);

agora_video_encoded_image_sender_send = agora_lib.agora_video_encoded_image_sender_send
agora_video_encoded_image_sender_send.restype = AGORA_API_C_INT
agora_video_encoded_image_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(OwnedEncodedVideoFrameInfo)]

class EncodedVideoFrameInfo:
    def __init__(self, codec_type=0, width=0, height=0, frames_per_second=0, frame_type=0, rotation=0, track_id=0, render_time_ms=0, internal_send_ts=0, uid=0):
        self.codec_type = codec_type
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.frame_type = frame_type
        self.rotation = rotation
        self.track_id = track_id
        self.render_time_ms = render_time_ms
        self.internal_send_ts = internal_send_ts
        self.uid = uid

    def __repr__(self):
        return f"EncodedVideoFrameInfo(codec_type={self.codec_type}, width={self.width}, height={self.height}, frames_per_second={self.frames_per_second}, frame_type={self.frame_type}, rotation={self.rotation}, track_id={self.track_id}, render_time_ms={self.render_time_ms}, internal_send_ts={self.internal_send_ts}, uid={self.uid})"
    def to_owned_encoded_video_frame_info(self):
        return OwnedEncodedVideoFrameInfo(
            self.codec_type,
            self.width,
            self.height,
            self.frames_per_second,
            self.frame_type,
            self.rotation,
            self.track_id,
            self.render_time_ms,
            self.internal_send_ts,
            self.uid
        )


class ExternalVideoFrame:
    def __init__(self)->None:
        self.type = 1
        self.buffer = None
        self.format = 0
        self.stride = 0
        self.height = 0
        self.crop_left = 0
        self.crop_top = 0
        self.crop_right = 0
        self.crop_bottom = 0
        self.rotation = 0
        self.timestamp = 0

    def to_owned_external_video_frame(self):
        cdata = (ctypes.c_uint8 * len(self.buffer)).from_buffer(self.buffer)
        # 将 ctypes 数组转换为 c_void_p
        cdata_ptr = ctypes.cast(cdata, ctypes.c_void_p)
        return OwnedExternalVideoFrame(
            self.type,
            self.format,
            cdata_ptr,
            self.stride,
            self.height,
            self.crop_left,
            self.crop_top,
            self.crop_right,
            self.crop_bottom,
            self.rotation,
            self.timestamp
        )
       


    
class VideoFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
        
    def send(self, frame:ExternalVideoFrame):
        owned_video_frame = frame.to_owned_external_video_frame()
        ret = agora_video_frame_sender_send(self.sender_handle, ctypes.byref(owned_video_frame))
        return ret

class VideoEncodedImageSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
        
    def send_encoded_video_image(self, data,size: int, frame_info:EncodedVideoFrameInfo):
        cdata = (ctypes.c_uint8 * size).from_buffer(data)
        encoded_video_frame = frame_info.to_owned_encoded_video_frame_info()
	
        ret = agora_video_frame_sender_send(self.sender_handle, cdata, size, ctypes.byref(encoded_video_frame))
        if ret != 0:
            print(f"Failed to send video frame, error code: {ret}")
        return ret
    
    
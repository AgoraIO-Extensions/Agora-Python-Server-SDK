import ctypes
from .agora_base import *
from agora_service.video_frame_observer import *

"""
/**
* Video buffer types.
*/
enum VIDEO_BUFFER_TYPE {
/**
    * 1: Raw data.
    */
VIDEO_BUFFER_RAW_DATA = 1,
/**
    * 2: The same as VIDEO_BUFFER_RAW_DATA.
    */
VIDEO_BUFFER_ARRAY = 2,
/**
    * 3: The video buffer in the format of texture.
    */
VIDEO_BUFFER_TEXTURE = 3,
};

/**
 * Video pixel formats.
 */
enum VIDEO_PIXEL_FORMAT {
  /**
   * 0: Default format.
   */
  VIDEO_PIXEL_DEFAULT = 0,
  /**
   * 1: I420.
   */
  VIDEO_PIXEL_I420 = 1,
  /**
   * 2: BGRA.
   */
  VIDEO_PIXEL_BGRA = 2,
  /**
   * 3: NV21.
   */
  VIDEO_PIXEL_NV21 = 3,
  /**
   * 4: RGBA.
   */
  VIDEO_PIXEL_RGBA = 4,
  /**
   * 8: NV12.
   */
  VIDEO_PIXEL_NV12 = 8,
  /**
   * 10: GL_TEXTURE_2D
   */
  VIDEO_TEXTURE_2D = 10,
  /**
   * 11: GL_TEXTURE_OES
   */
  VIDEO_TEXTURE_OES = 11,
  /*
  12: pixel format for iOS CVPixelBuffer NV12
  */
  VIDEO_CVPIXEL_NV12 = 12,
  /*
  13: pixel format for iOS CVPixelBuffer I420
  */
  VIDEO_CVPIXEL_I420 = 13,
  /*
  14: pixel format for iOS CVPixelBuffer BGRA
  */
  VIDEO_CVPIXEL_BGRA = 14,
  /**
   * 16: I422.
   */
  VIDEO_PIXEL_I422 = 16,
}

refer: https://doc.shengwang.cn/api-ref/rtc/windows/API/class_externalvideoframe#ExternalVideoFrame
"""
class ExternalVideoFrame(ctypes.Structure):
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

    def __init__(self) -> None:
        self.data = None
        self.metadata = ""



class VideoDimensions(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int)
    ]

class VideoEncoderConfig(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("dimensions", VideoDimensions),
        ("frame_rate", ctypes.c_int),
        ("bitrate", ctypes.c_int),
        ("min_bitrate", ctypes.c_int),
        ("orientation_mode", ctypes.c_int),
        ("degradation_preference", ctypes.c_int),
        ("mirror_mode", ctypes.c_int)
    ]    


agora_local_video_track_set_video_encoder_config = agora_lib.agora_local_video_track_set_video_encoder_config
agora_local_video_track_set_video_encoder_config.restype = AGORA_API_C_INT
agora_local_video_track_set_video_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoEncoderConfig)]

agora_local_video_track_set_enabled = agora_lib.agora_local_video_track_set_enabled
agora_local_video_track_set_enabled.restype = AGORA_API_C_INT
agora_local_video_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_user_publish_video = agora_lib.agora_local_user_publish_video
agora_local_user_publish_video.restype = AGORA_API_C_INT
agora_local_user_publish_video.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unpublish_video = agora_lib.agora_local_user_unpublish_video
agora_local_user_unpublish_video.restype = AGORA_API_C_INT
agora_local_user_unpublish_video.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ExternalVideoFrame)]

agora_video_frame_observer2_create = agora_lib.agora_video_frame_observer2_create
agora_video_frame_observer2_create.restype = AGORA_API_C_HDL
agora_video_frame_observer2_create.argtypes = [ctypes.POINTER(VideoFrameObserver2)]

agora_local_user_register_video_frame_observer = agora_lib.agora_local_user_register_video_frame_observer
agora_local_user_register_video_frame_observer.argtypes = [AGORA_HANDLE, AGORA_HANDLE]
# agora_local_user_register_video_frame_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoFrameObserver2)]
agora_local_user_register_video_frame_observer.restype = ctypes.c_int

class VideoSender:
    def __init__(self, video_frame_sender, video_track, local_user) -> None:
        self.video_frame_sender = video_frame_sender
        self.video_track = video_track
        self.local_user = local_user

    def SetVideoEncoderConfig(self, video_encoder_config):
        return agora_local_video_track_set_video_encoder_config(self.video_track, video_encoder_config)

    def Start(self):
        agora_local_video_track_set_enabled(self.video_track, 1)
        return agora_local_user_publish_video(self.local_user, self.video_track)        

    def Stop(self):
        ret = agora_local_user_unpublish_video(self.local_user, self.video_track)     
        agora_local_video_track_set_enabled(self.video_track, 0)
        return ret
    
    def register_video_frame_observer(self, agora_video_frame_observer2):
        self.agora_video_frame_observer2 = agora_video_frame_observer2
        self.video_frame_observer_handler = agora_video_frame_observer2_create(agora_video_frame_observer2)
        result = agora_local_user_register_video_frame_observer(self.local_user, self.video_frame_observer_handler)
        if result!= 0:
            raise Exception("Failed to register video frame observer")

    def SendVideoFrame(self, external_video_frame):
        c_array = (ctypes.c_ubyte * len(external_video_frame.data)).from_buffer(external_video_frame.data)
        cdata = ctypes.cast(c_array, ctypes.c_void_p)
        external_video_frame.buffer = cdata

        cdata = bytearray(external_video_frame.metadata.encode('utf-8'))
        c_metadata = (ctypes.c_uint8 * len(cdata)).from_buffer(cdata)
        external_video_frame.metadata_buffer = c_metadata
        external_video_frame.metadata_size = len(cdata)
        print("external_video_frame:",cdata,external_video_frame.metadata_size)
        ret = agora_video_frame_sender_send(self.video_frame_sender, external_video_frame)
        return ret


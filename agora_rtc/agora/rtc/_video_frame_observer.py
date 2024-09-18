import ctypes
from .agora_base import *
from .local_user import *
from .video_frame_observer import *

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
        video_frame.y_buffer = ctypes.string_at(self.y_buffer, self.y_stride * self.height)
        video_frame.u_buffer = ctypes.string_at(self.u_buffer, self.u_stride * self.height // 2)
        video_frame.v_buffer = ctypes.string_at(self.v_buffer, self.v_stride * self.height // 2)
        video_frame.rotation = self.rotation
        video_frame.render_time_ms = self.render_time_ms
        video_frame.avsync_type = self.avsync_type
        video_frame.metadata_buffer = ctypes.string_at(self.metadata_buffer, self.metadata_size) 
        video_frame.metadata_size = self.metadata_size
        video_frame.shared_context = self.shared_context.decode() if self.shared_context else None
        video_frame.texture_id = self.texture_id
        video_frame.matrix = self.matrix
        video_frame.alpha_buffer = self.alpha_buffer
        video_frame.metadata = video_frame.metadata_buffer.decode()
        return video_frame

ON_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(VideoFrameInner))

class VideoFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_frame", ON_FRAME_CALLBACK)
    ]

    def __init__(self, video_frame_observer:IVideoFrameObserver, local_user:'LocalUser'):
        self.video_frame_observer = video_frame_observer
        self.local_user = local_user
        self.on_frame = ON_FRAME_CALLBACK(self._on_frame)


    def _on_frame(self, agora_handle, channel_id, user_id, video_frame:VideoFrameInner):
        vf = video_frame.contents
        print("VideoFrameObserver _on_frame:", agora_handle, channel_id, user_id, vf.metadata_buffer, vf.metadata_size)
        self.video_frame_observer.on_frame(agora_handle, channel_id.decode() if channel_id else None, user_id.decode(), vf.to_video_frame())
    





# ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.POINTER(encoded_video_frame_info))

# class VideoEncodedImageReceiverInner(ctypes.Structure):
#     _fields_ = [
#         ("on_encoded_video_image_received", ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK)
#     ]

#     def __init__(self, video_encoded_image_receiver:'IVideoEncodedImageReceiver'):
#         self.video_encoded_image_receiver = video_encoded_image_receiver
#         self.on_encoded_video_image_received = ON_ENCODED_VIDEO_IMAGE_RECEIVED_CALLBACK(self._on_encoded_video_image_received)


#     def _on_encoded_video_image_received(self, agora_handle, image_buffer, length, info):
#         print("VideoFrameObserver _on_frame:", agora_handle, image_buffer, length, info)
#         # self.on_encoded_video_image_received(agora_handle, image_buffer, length, info)
#         self.video_encoded_image_receiver.on_encoded_video_image_received(agora_handle, image_buffer, length, info)



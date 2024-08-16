import ctypes
from .agora_base import *
from agora_service.video_frame_observer import *

agora_local_video_track_set_video_encoder_config = agora_lib.agora_local_video_track_set_video_encoder_config
agora_local_video_track_set_video_encoder_config.restype = AGORA_API_C_INT
agora_local_video_track_set_video_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoEncoderConfig)]

agora_local_video_track_set_enabled = agora_lib.agora_local_video_track_set_enabled
agora_local_video_track_set_enabled.restype = AGORA_API_C_INT
agora_local_video_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_video_frame_sender_send = agora_lib.agora_video_frame_sender_send
agora_video_frame_sender_send.restype = AGORA_API_C_INT
agora_video_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.POINTER(ExternalVideoFrame)]


# AGORA_API_C_VOID agora_video_frame_sender_destroy(AGORA_HANDLE agora_video_frame_sender);
agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = None
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]





class VideoFrameSender:
    def __init__(self, video_frame_sender) -> None:
        self.sender_handle = video_frame_sender
        # self.video_track = video_track
        # self.local_user = local_user

    # def SetVideoEncoderConfig(self, video_encoder_config):
    #     return agora_local_video_track_set_video_encoder_config(self.video_track, video_encoder_config)

    # def Start(self):
    #     agora_local_video_track_set_enabled(self.video_track, 1)
    #     return agora_local_user_publish_video(self.local_user, self.video_track)        

    # def Stop(self):
    #     ret = agora_local_user_unpublish_video(self.local_user, self.video_track)     
    #     agora_local_video_track_set_enabled(self.video_track, 0)
    #     return ret
    
    # def register_video_frame_observer(self, agora_video_frame_observer2):
    #     # observer_ptr = ctypes.c_void_p(ctypes.addressof(agora_video_frame_observer2))
    #     observer_ptr = ctypes.byref(agora_video_frame_observer2)
    #     result = agora_local_user_register_video_frame_observer(self.local_user, observer_ptr)
    #     if result!= 0:
    #         print("Failed to register video frame observer")

    def send_video_frame(self, external_video_frame):
        c_array = (ctypes.c_ubyte * len(external_video_frame.data)).from_buffer(external_video_frame.data)
        cdata = ctypes.cast(c_array, ctypes.c_void_p)
        external_video_frame.buffer = cdata
        ret = agora_video_frame_sender_send(self.video_frame_sender, external_video_frame)
        if ret != 0:
            print(f"Failed to send video frame, error code: {ret}")
        return ret

    def destroy(self):
        if self.sender_handle:
            agora_video_frame_sender_destroy(self.sender_handle)
            self.sender_handle = None

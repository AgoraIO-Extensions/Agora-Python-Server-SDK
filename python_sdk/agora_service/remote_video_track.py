import ctypes
from .agora_base import *

agora_remote_video_track_get_statistics = agora_lib.agora_remote_video_track_get_statistics
agora_remote_video_track_get_statistics.restype = ctypes.POINTER(remote_video_track_stats)
agora_remote_video_track_get_statistics.argtypes = [AGORA_HANDLE]

agora_remote_video_track_destroy_statistics = agora_lib.agora_remote_video_track_destroy_statistics
agora_remote_video_track_destroy_statistics.restype = None
agora_remote_video_track_destroy_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(remote_video_track_stats)]

agora_remote_video_track_get_state = agora_lib.agora_remote_video_track_get_state
agora_remote_video_track_get_state.restype = ctypes.c_int
agora_remote_video_track_get_state.argtypes = [AGORA_HANDLE]

agora_remote_video_track_get_track_info = agora_lib.agora_remote_video_track_get_track_info
agora_remote_video_track_get_track_info.restype = ctypes.POINTER(video_track_info)
agora_remote_video_track_get_track_info.argtypes = [AGORA_HANDLE]

agora_remote_video_track_destroy_track_info = agora_lib.agora_remote_video_track_destroy_track_info
agora_remote_video_track_destroy_track_info.restype = None
agora_remote_video_track_destroy_track_info.argtypes = [AGORA_HANDLE, ctypes.POINTER(video_track_info)]

agora_remote_video_track_register_video_encoded_image_receiver = agora_lib.agora_remote_video_track_register_video_encoded_image_receiver
agora_remote_video_track_register_video_encoded_image_receiver.restype = ctypes.c_int
agora_remote_video_track_register_video_encoded_image_receiver.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_remote_video_track_unregister_video_encoded_image_receiver = agora_lib.agora_remote_video_track_unregister_video_encoded_image_receiver
agora_remote_video_track_unregister_video_encoded_image_receiver.restype = ctypes.c_int
agora_remote_video_track_unregister_video_encoded_image_receiver.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_remote_video_track_register_media_packet_receiver = agora_lib.agora_remote_video_track_register_media_packet_receiver
agora_remote_video_track_register_media_packet_receiver.restype = ctypes.c_int
agora_remote_video_track_register_media_packet_receiver.argtypes = [AGORA_HANDLE, ctypes.POINTER(media_packet_receiver)]

agora_remote_video_track_unregister_media_packet_receiver = agora_lib.agora_remote_video_track_unregister_media_packet_receiver
agora_remote_video_track_unregister_media_packet_receiver.restype = ctypes.c_int
agora_remote_video_track_unregister_media_packet_receiver.argtypes = [AGORA_HANDLE, ctypes.POINTER(media_packet_receiver)]

agora_remote_video_track_get_type = agora_lib.agora_remote_video_track_get_type
agora_remote_video_track_get_type.restype = ctypes.c_int
agora_remote_video_track_get_type.argtypes = [AGORA_HANDLE]

class RemoteVideoTrack:
    def __init__(self, track_handle):
        self.track_handle = track_handle

    def get_statistics(self):
        stats_ptr = agora_remote_video_track_get_statistics(self.track_handle)
        if not stats_ptr:
            print("Failed to get remote video track statistics")
            return None
        stats = stats_ptr.contents
        self.destroy_statistics(stats_ptr)
        return stats

    def destroy_statistics(self, stats):
        agora_remote_video_track_destroy_statistics(self.track_handle, stats)

    def get_state(self):
        return agora_remote_video_track_get_state(self.track_handle)

    def get_track_info(self):
        info_ptr = agora_remote_video_track_get_track_info(self.track_handle)
        if not info_ptr:
            print("Failed to get remote video track info")
            return None
        info = info_ptr.contents
        self.destroy_track_info(info_ptr)
        return info

    def destroy_track_info(self, info):
        agora_remote_video_track_destroy_track_info(self.track_handle, info)

    def register_video_encoded_image_receiver(self, receiver):
        ret = agora_remote_video_track_register_video_encoded_image_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to register video encoded image receiver, error code: {ret}")
        return ret

    def unregister_video_encoded_image_receiver(self, receiver):
        ret = agora_remote_video_track_unregister_video_encoded_image_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to unregister video encoded image receiver, error code: {ret}")
        return ret

    def register_media_packet_receiver(self, receiver):
        ret = agora_remote_video_track_register_media_packet_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to register media packet receiver, error code: {ret}")
        return ret

    def unregister_media_packet_receiver(self, receiver):
        ret = agora_remote_video_track_unregister_media_packet_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to unregister media packet receiver, error code: {ret}")
        return ret

    def get_type(self):
        return agora_remote_video_track_get_type(self.track_handle)

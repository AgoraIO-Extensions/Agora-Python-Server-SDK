import ctypes
from .agora_base import *

agora_remote_audio_track_get_statistics = agora_lib.agora_remote_audio_track_get_statistics
agora_remote_audio_track_get_statistics.restype = ctypes.POINTER(remote_audio_track_stats)
agora_remote_audio_track_get_statistics.argtypes = [AGORA_HANDLE]

agora_remote_audio_track_destroy_statistics = agora_lib.agora_remote_audio_track_destroy_statistics
agora_remote_audio_track_destroy_statistics.restype = None
agora_remote_audio_track_destroy_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(remote_audio_track_stats)]

agora_remote_audio_track_get_state = agora_lib.agora_remote_audio_track_get_state
agora_remote_audio_track_get_state.restype = ctypes.c_int
agora_remote_audio_track_get_state.argtypes = [AGORA_HANDLE]

agora_remote_audio_track_register_media_packet_receiver = agora_lib.agora_remote_audio_track_register_media_packet_receiver
agora_remote_audio_track_register_media_packet_receiver.restype = ctypes.c_int
agora_remote_audio_track_register_media_packet_receiver.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_remote_audio_track_unregister_media_packet_receiver = agora_lib.agora_remote_audio_track_unregister_media_packet_receiver
agora_remote_audio_track_unregister_media_packet_receiver.restype = ctypes.c_int
agora_remote_audio_track_unregister_media_packet_receiver.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_remote_audio_track_enable_sound_position_indication = agora_lib.agora_remote_audio_track_enable_sound_position_indication
agora_remote_audio_track_enable_sound_position_indication.restype = ctypes.c_int
agora_remote_audio_track_enable_sound_position_indication.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_remote_audio_track_set_remote_voice_position = agora_lib.agora_remote_audio_track_set_remote_voice_position
agora_remote_audio_track_set_remote_voice_position.restype = ctypes.c_int
agora_remote_audio_track_set_remote_voice_position.argtypes = [AGORA_HANDLE, ctypes.c_float, ctypes.c_float]

agora_remote_audio_track_enable_spatial_audio = agora_lib.agora_remote_audio_track_enable_spatial_audio
agora_remote_audio_track_enable_spatial_audio.restype = ctypes.c_int
agora_remote_audio_track_enable_spatial_audio.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_remote_audio_track_set_remote_user_spatial_audio_params = agora_lib.agora_remote_audio_track_set_remote_user_spatial_audio_params
agora_remote_audio_track_set_remote_user_spatial_audio_params.restype = ctypes.c_int
agora_remote_audio_track_set_remote_user_spatial_audio_params.argtypes = [AGORA_HANDLE, ctypes.POINTER(spatial_audio_params)]

class RemoteAudioTrack:
    def __init__(self, track_handle):
        self.track_handle = track_handle


    def get_statistics(self):
        stats_ptr = agora_remote_audio_track_get_statistics(self.track_handle)
        if not stats_ptr:
            print("Failed to get remote audio track statistics")
            return None
        stats = stats_ptr.contents
        self.destroy_statistics(stats_ptr)
        return stats

    def destroy_statistics(self, stats):
        agora_remote_audio_track_destroy_statistics(self.track_handle, stats)

    def get_state(self):
        return agora_remote_audio_track_get_state(self.track_handle)
    
    def register_media_packet_receiver(self, receiver):
        ret = agora_remote_audio_track_register_media_packet_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to register media packet receiver, error code: {ret}")
        return ret

    def unregister_media_packet_receiver(self, receiver):
        ret = agora_remote_audio_track_unregister_media_packet_receiver(self.track_handle, receiver)
        if ret != 0:
            print(f"Failed to unregister media packet receiver, error code: {ret}")
        return ret

    def enable_sound_position_indication(self, enabled):
        ret = agora_remote_audio_track_enable_sound_position_indication(self.track_handle, int(enabled))
        if ret != 0:
            print(f"Failed to enable sound position indication, error code: {ret}")
        return ret
    
    def set_remote_voice_position(self, pan, gain):
        ret = agora_remote_audio_track_set_remote_voice_position(self.track_handle, float(pan), float(gain))
        if ret != 0:
            print(f"Failed to set remote voice position, error code: {ret}")
        return ret

    def enable_spatial_audio(self, enabled):
        ret = agora_remote_audio_track_enable_spatial_audio(self.track_handle, int(enabled))
        if ret != 0:
            print(f"Failed to enable spatial audio, error code: {ret}")
        return ret
    
    def set_remote_user_spatial_audio_params(self, params):
        ret = agora_remote_audio_track_set_remote_user_spatial_audio_params(self.track_handle, params)
        if ret != 0:
            print(f"Failed to set remote user spatial audio params, error code: {ret}")
        return ret

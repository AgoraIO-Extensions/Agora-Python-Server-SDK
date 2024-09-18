import time
import ctypes
from threading import RLock
from .agora_base import *
from .local_video_track import *
from .local_audio_track import *
from .local_user_observer import IRTCLocalUserObserver
from ._local_user_observer import RTCLocalUserObserverInner
from ._audio_frame_observer import AudioFrameObserverInner
from .audio_frame_observer import IAudioFrameObserver
from ._video_frame_observer import VideoFrameObserverInner
from .video_frame_observer import IVideoFrameObserver
# from .video_encoded_image_receiver import IVideoEncodedImageReceiver
from .video_encoded_frame_observer import IVideoEncodedFrameObserver
from ._video_encoded_frame_observer import VideoEncodedFrameObserverInner
from .remote_audio_track import *
from .remote_video_track import *

agora_local_user_set_user_role = agora_lib.agora_local_user_set_user_role
agora_local_user_set_user_role.restype = ctypes.c_int
agora_local_user_set_user_role.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_user_get_user_role = agora_lib.agora_local_user_get_user_role
agora_local_user_get_user_role.restype = ctypes.c_int
agora_local_user_get_user_role.argtypes = [AGORA_HANDLE]

agora_local_user_set_audio_encoder_config = agora_lib.agora_local_user_set_audio_encoder_config
agora_local_user_set_audio_encoder_config.restype = AGORA_API_C_INT
agora_local_user_set_audio_encoder_config.argtypes = [AGORA_HANDLE, ctypes.POINTER(AudioEncoderConfiguration)]

agora_local_user_get_local_audio_statistics = agora_lib.agora_local_user_get_local_audio_statistics
agora_local_user_get_local_audio_statistics.restype = ctypes.POINTER(LocalAudioDetailedStatsInner)
agora_local_user_get_local_audio_statistics.argtypes = [AGORA_HANDLE]

agora_local_user_destroy_local_audio_statistics = agora_lib.agora_local_user_destroy_local_audio_statistics
agora_local_user_destroy_local_audio_statistics.restype = AGORA_API_C_VOID
agora_local_user_destroy_local_audio_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(LocalAudioDetailedStatsInner)]

agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
agora_local_user_publish_audio.restype = AGORA_API_C_INT
agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unpublish_audio = agora_lib.agora_local_user_unpublish_audio
agora_local_user_unpublish_audio.restype = AGORA_API_C_INT
agora_local_user_unpublish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_publish_video = agora_lib.agora_local_user_publish_video
agora_local_user_publish_video.restype = AGORA_API_C_INT
agora_local_user_publish_video.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unpublish_video = agora_lib.agora_local_user_unpublish_video
agora_local_user_unpublish_video.restype = AGORA_API_C_INT
agora_local_user_unpublish_video.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_subscribe_audio = agora_lib.agora_local_user_subscribe_audio
agora_local_user_subscribe_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_audio.argtypes = [AGORA_HANDLE, user_id_t]

agora_local_user_subscribe_all_audio = agora_lib.agora_local_user_subscribe_all_audio
agora_local_user_subscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_all_audio.argtypes = [AGORA_HANDLE]

agora_local_user_unsubscribe_audio = agora_lib.agora_local_user_unsubscribe_audio
agora_local_user_unsubscribe_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_audio.argtypes = [AGORA_HANDLE, ctypes.c_uint]

agora_local_user_unsubscribe_all_audio = agora_lib.agora_local_user_unsubscribe_all_audio
agora_local_user_unsubscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_all_audio.argtypes = [AGORA_HANDLE]

agora_local_user_adjust_playback_signal_volume = agora_lib.agora_local_user_adjust_playback_signal_volume
agora_local_user_adjust_playback_signal_volume.restype = AGORA_API_C_INT
agora_local_user_adjust_playback_signal_volume.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_user_get_playback_signal_volume = agora_lib.agora_local_user_get_playback_signal_volume
agora_local_user_get_playback_signal_volume.restype = AGORA_API_C_INT
agora_local_user_get_playback_signal_volume.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int)]

# agora_local_user_pull_mixed_audio_pcm_data = agora_lib.agora_local_user_pull_mixed_audio_pcm_data
# agora_local_user_pull_mixed_audio_pcm_data.restype = AGORA_API_C_INT
# agora_local_user_pull_mixed_audio_pcm_data.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.POINTER(AudioPcmDataInfo)]

agora_local_user_set_playback_audio_frame_parameters = agora_lib.agora_local_user_set_playback_audio_frame_parameters
agora_local_user_set_playback_audio_frame_parameters.restype = AGORA_API_C_INT
agora_local_user_set_playback_audio_frame_parameters.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

agora_local_user_set_recording_audio_frame_parameters = agora_lib.agora_local_user_set_recording_audio_frame_parameters
agora_local_user_set_recording_audio_frame_parameters.restype = AGORA_API_C_INT
agora_local_user_set_recording_audio_frame_parameters.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

agora_local_user_set_mixed_audio_frame_parameters = agora_lib.agora_local_user_set_mixed_audio_frame_parameters
agora_local_user_set_mixed_audio_frame_parameters.restype = AGORA_API_C_INT
agora_local_user_set_mixed_audio_frame_parameters.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int]

agora_local_user_set_playback_audio_frame_before_mixing_parameters = agora_lib.agora_local_user_set_playback_audio_frame_before_mixing_parameters
agora_local_user_set_playback_audio_frame_before_mixing_parameters.restype = AGORA_API_C_INT
agora_local_user_set_playback_audio_frame_before_mixing_parameters.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int]

agora_local_user_register_audio_frame_observer = agora_lib.agora_local_user_register_audio_frame_observer
agora_local_user_register_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_register_audio_frame_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(AudioFrameObserverInner)]

agora_local_user_unregister_audio_frame_observer = agora_lib.agora_local_user_unregister_audio_frame_observer
agora_local_user_unregister_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_audio_frame_observer.argtypes = [AGORA_HANDLE]

# agora_local_user_enable_audio_spectrum_monitor = agora_lib.agora_local_user_enable_audio_spectrum_monitor
# agora_local_user_enable_audio_spectrum_monitor.restype = AGORA_API_C_INT
# agora_local_user_enable_audio_spectrum_monitor.argtypes = [AGORA_HANDLE, ctypes.c_int]

# agora_local_user_disable_audio_spectrum_monitor = agora_lib.agora_local_user_disable_audio_spectrum_monitor
# agora_local_user_disable_audio_spectrum_monitor.restype = AGORA_API_C_INT
# agora_local_user_disable_audio_spectrum_monitor.argtypes = [AGORA_HANDLE]

# agora_local_user_register_audio_spectrum_observer = agora_lib.agora_local_user_register_audio_spectrum_observer
# agora_local_user_register_audio_spectrum_observer.restype = AGORA_API_C_INT
# agora_local_user_register_audio_spectrum_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

# agora_local_user_unregister_audio_spectrum_observer = agora_lib.agora_local_user_unregister_audio_spectrum_observer
# agora_local_user_unregister_audio_spectrum_observer.restype = AGORA_API_C_INT
# agora_local_user_unregister_audio_spectrum_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

# AGORA_API_C_HDL agora_video_encoded_image_receiver_create(video_encoded_frame_observer* receiver);


# agora_video_encoded_image_receiver_create = agora_lib.agora_video_encoded_image_receiver_create
# agora_video_encoded_image_receiver_create.restype = AGORA_API_C_HDL
# agora_video_encoded_image_receiver_create.argtypes = [ctypes.POINTER(VideoEncodedImageReceiverInner)]

# AGORA_API_C_VOID agora_video_encoded_image_receiver_destroy(AGORA_HANDLE agora_video_encoded_image_receiver);

agora_video_encoded_image_receiver_destroy = agora_lib.agora_video_encoded_image_receiver_destroy
agora_video_encoded_image_receiver_destroy.restype = AGORA_API_C_VOID
agora_video_encoded_image_receiver_destroy.argtypes = [AGORA_HANDLE]


# AGORA_API_C_HDL agora_video_encoded_frame_observer_create(video_encoded_frame_observer* observer);
agora_video_encoded_frame_observer_create = agora_lib.agora_video_encoded_frame_observer_create
agora_video_encoded_frame_observer_create.restype = AGORA_API_C_HDL
agora_video_encoded_frame_observer_create.argtypes = [ctypes.POINTER(VideoEncodedFrameObserverInner)]


# AGORA_API_C_VOID agora_video_encoded_frame_observer_destroy(AGORA_HANDLE agora_video_encoded_frame_observer);
agora_video_encoded_frame_observer_destroy = agora_lib.agora_video_encoded_frame_observer_destroy
agora_video_encoded_frame_observer_destroy.restype = AGORA_API_C_VOID
agora_video_encoded_frame_observer_destroy.argtypes = [AGORA_HANDLE]


agora_local_user_register_video_encoded_frame_observer = agora_lib.agora_local_user_register_video_encoded_frame_observer
agora_local_user_register_video_encoded_frame_observer.restype = AGORA_API_C_INT
agora_local_user_register_video_encoded_frame_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

agora_local_user_unregister_video_encoded_frame_observer = agora_lib.agora_local_user_unregister_video_encoded_frame_observer
agora_local_user_unregister_video_encoded_frame_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_video_encoded_frame_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

agora_video_frame_observer2_create = agora_lib.agora_video_frame_observer2_create
agora_video_frame_observer2_create.restype = AGORA_API_C_HDL
agora_video_frame_observer2_create.argtypes = [ctypes.POINTER(VideoFrameObserverInner)]

agora_video_frame_observer2_destroy = agora_lib.agora_video_frame_observer2_destroy
agora_video_frame_observer2_destroy.restype = AGORA_API_C_INT
agora_video_frame_observer2_destroy.argtypes = [AGORA_API_C_HDL]

agora_local_user_register_video_frame_observer = agora_lib.agora_local_user_register_video_frame_observer
agora_local_user_register_video_frame_observer.restype = AGORA_API_C_INT
agora_local_user_register_video_frame_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

agora_local_user_unregister_video_frame_observer = agora_lib.agora_local_user_unregister_video_frame_observer
agora_local_user_unregister_video_frame_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_video_frame_observer.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

# agora_local_user_set_video_subscription_options = agora_lib.agora_local_user_set_video_subscription_options
# agora_local_user_set_video_subscription_options.restype = AGORA_API_C_INT
# agora_local_user_set_video_subscription_options.argtypes = [AGORA_HANDLE, ctypes.c_uint, ctypes.POINTER(VideoSubscriptionOptions)]

agora_local_user_subscribe_video = agora_lib.agora_local_user_subscribe_video
agora_local_user_subscribe_video.restype = AGORA_API_C_INT
agora_local_user_subscribe_video.argtypes = [AGORA_HANDLE, user_id_t, ctypes.POINTER(VideoSubscriptionOptions)]

agora_local_user_subscribe_all_video = agora_lib.agora_local_user_subscribe_all_video
agora_local_user_subscribe_all_video.restype = AGORA_API_C_INT
agora_local_user_subscribe_all_video.argtypes = [AGORA_HANDLE, ctypes.POINTER(VideoSubscriptionOptions)]

agora_local_user_unsubscribe_video = agora_lib.agora_local_user_unsubscribe_video
agora_local_user_unsubscribe_video.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_video.argtypes = [AGORA_HANDLE, ctypes.c_uint]

agora_local_user_unsubscribe_all_video = agora_lib.agora_local_user_unsubscribe_all_video
agora_local_user_unsubscribe_all_video.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_all_video.argtypes = [AGORA_HANDLE]

agora_local_user_set_audio_volume_indication_parameters = agora_lib.agora_local_user_set_audio_volume_indication_parameters
agora_local_user_set_audio_volume_indication_parameters.restype = AGORA_API_C_INT
agora_local_user_set_audio_volume_indication_parameters.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_bool]

agora_local_user_register_observer = agora_lib.agora_local_user_register_observer
agora_local_user_register_observer.restype = AGORA_API_C_INT
agora_local_user_register_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCLocalUserObserverInner)]

agora_local_user_unregister_observer = agora_lib.agora_local_user_unregister_observer
agora_local_user_unregister_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_observer.argtypes = [AGORA_HANDLE]

agora_local_user_get_media_control_packet_sender = agora_lib.agora_local_user_get_media_control_packet_sender
agora_local_user_get_media_control_packet_sender.restype = ctypes.c_void_p
agora_local_user_get_media_control_packet_sender.argtypes = [AGORA_HANDLE]

agora_local_user_register_media_control_packet_receiver = agora_lib.agora_local_user_register_media_control_packet_receiver
agora_local_user_register_media_control_packet_receiver.restype = AGORA_API_C_INT
agora_local_user_register_media_control_packet_receiver.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

agora_local_user_unregister_media_control_packet_receiver = agora_lib.agora_local_user_unregister_media_control_packet_receiver
agora_local_user_unregister_media_control_packet_receiver.restype = AGORA_API_C_INT
agora_local_user_unregister_media_control_packet_receiver.argtypes = [AGORA_HANDLE, ctypes.c_void_p]

agora_local_user_send_intra_request = agora_lib.agora_local_user_send_intra_request
agora_local_user_send_intra_request.restype = AGORA_API_C_INT
agora_local_user_send_intra_request.argtypes = [AGORA_HANDLE, user_id_t]


class LocalUser:
    def __init__(self, local_user_handle, connection):
        self.user_handle = local_user_handle
        self.connection = connection
        #for AudioTrack/videoTrack in local_user, we need to keep the reference of them
        self._audio_track_lock = RLock()
        self._video_track_lock = RLock()
        #map
        self._audio_track_map = {}
        self._video_track_map = {}
        #remote audio track
        #remote video track
        self._remote_audio_track_lock = RLock()
        self._remote_video_track_lock = RLock()
        self._remote_audio_track_map = {}
        self._remote_video_track_map = {}

    def _set_audio_map(self, track_handle, track:LocalAudioTrack):
        with self._audio_track_lock:
            # no need to theck key is existed or not,just do replace
            self._audio_track_map[track_handle] = track
    def get_audio_map(self, track_handle):
        with self._audio_track_lock:
            return self._audio_track_map.get(track_handle)
    def _del_audio_map(self, track_handle):
        with self._audio_track_lock:
            if track_handle not in self._audio_track_map:
                return
            del self._audio_track_map[track_handle]

    def _set_video_map(self, track_handle, track:LocalVideoTrack):
        with self._video_track_lock:
            # no need to theck key is existed or not,just do replace
            self._video_track_map[track_handle] = track
    def get_video_map(self, track_handle):
        with self._video_track_lock:
            return self._video_track_map.get(track_handle)
    def del_video_map(self, track_handle):
        with self._video_track_lock:
            if track_handle not in self._video_track_map:
                return
            del self._video_track_map[track_handle]

    def set_remote_audio_map(self, track_handle, track:RemoteAudioTrack, user_id_str):
        with self._remote_audio_track_lock:
            # to check key is existed or not,just do replace
            #userid is unique in a channel
            self._remote_audio_track_map[track_handle] = track
    def get_remote_audio_map(self, track_handle):
        with self._remote_audio_track_lock:
            return self._remote_audio_track_map.get(track_handle)
    def del_remote_audio_map(self, user_id_str):
        with self._remote_audio_track_lock:
            if user_id_str is None:
                self._remote_audio_track_map.clear()
            else:
                for key, value in self._remote_audio_track_map.items():
                    if value.user_id == user_id_str:
                        del self._remote_audio_track_map[key]

    def set_remote_video_map(self, track_handle, track:RemoteVideoTrack):
        with self._remote_video_track_lock:
            # no need to theck key is existed or not,just do replace
            self._remote_video_track_map[track_handle] = track
    def get_remote_video_map(self, track_handle):
        with self._remote_video_track_lock:
            return self._remote_video_track_map.get(track_handle)   
    def del_remote_video_map(self, user_id_str):
        with self._remote_video_track_lock:
            if user_id_str is None:
                self._remote_video_track_map.clear()   
                return

            for key, value in self._remote_video_track_map.items():
                if value.user_id == user_id_str:
                    del self._remote_video_track_map[key]  
            return
            

    def set_user_role(self, role):
        ret = agora_local_user_set_user_role(self.user_handle, role)
        if ret < 0:
            print("Failed to set user role")
        return ret
    def get_user_role(self):
        ret = agora_local_user_get_user_role(self.user_handle)
        if ret < 0:
            print("Failed to get user role")
        return ret

    def set_audio_encoder_configuration(self, config):
        ret = agora_local_user_set_audio_encoder_config(self.user_handle, config)
        if ret < 0:
            print("Failed to set audio encoder config")
        return ret

    def get_local_audio_statistics(self):
        stats = agora_local_user_get_local_audio_statistics(self.user_handle)
        #and change it to python object：localaudiodetailedstats
        detailed_stats = stats.contents._to_local_audio_detailed_stats()
        #and then release it
        agora_local_user_destroy_local_audio_statistics(self.user_handle, stats)

        return detailed_stats

    def publish_audio(self, agora_local_audio_track:LocalAudioTrack):
        ret = agora_local_user_publish_audio(self.user_handle, agora_local_audio_track.track_handle)
        if ret < 0:
            print("Failed to publish audio")
        else:
            self._set_audio_map(agora_local_audio_track.track_handle, agora_local_audio_track)
        return ret


    def unpublish_audio(self, agora_local_audio_track:LocalAudioTrack):
        ret = agora_local_user_unpublish_audio(self.user_handle, agora_local_audio_track.track_handle)
        if ret < 0:
            print("Failed to unpublish audio")
        #wait for callback to do del, do not remove map here!
        return ret

    def publish_video(self, agora_local_video_track:LocalVideoTrack):
        ret = agora_local_user_publish_video(self.user_handle, agora_local_video_track.track_handle)
        if ret < 0:
            print("Failed to publish video")
        else:
            self._set_video_map(agora_local_video_track.track_handle, agora_local_video_track)
        return ret

    def unpublish_video(self, agora_local_video_track:LocalVideoTrack):
        ret = agora_local_user_unpublish_video(self.user_handle, agora_local_video_track.track_handle)
        if ret < 0:
            print("Failed to unpublish video")
        #note: can not del in this function, because the video track may be used in callback, 
        # move del to unpublish_video callback
        return ret

    def subscribe_audio(self, user_id):
        ret = agora_local_user_subscribe_audio(self.user_handle,ctypes.c_char_p(user_id.encode()) )
        if ret < 0:
            print("Failed to subscribe audio")
        return ret

    def subscribe_all_audio(self):
        ret = agora_local_user_subscribe_all_audio(self.user_handle)
        if ret < 0:
            print("Failed to subscribe all audio")
        return ret

    def unsubscribe_audio(self, user_id):
        ret = agora_local_user_unsubscribe_audio(self.user_handle, ctypes.c_char_p(user_id.encode()))
        if ret < 0:
            print("Failed to unsubscribe audio")
        else: 
            self.del_remote_audio_map(user_id)
        return ret

    def unsubscribe_all_audio(self):
        ret = agora_local_user_unsubscribe_all_audio(self.user_handle)
        if ret < 0:
            print("Failed to unsubscribe all audio")
        else:
            self.del_remote_audio_map(None)
        return ret

    def adjust_playback_signal_volume(self, volume):
        ret = agora_local_user_adjust_playback_signal_volume(self.user_handle, volume)
        if ret < 0:
            print("Failed to adjust playback signal volume")
        return ret

    def get_playback_signal_volume(self):
        volume = ctypes.c_int(0)
        ret = agora_local_user_get_playback_signal_volume(self.user_handle, volume)
        if ret < 0:
            print("Failed to get playback signal volume")
        return ret, volume.value

    # def pull_mixed_audio_pcm_data(self, payload_data, info):
    #     ret = agora_local_user_pull_mixed_audio_pcm_data(self.user_handle, payload_data, info)
    #     if ret < 0:
    #         print("Failed to pull mixed audio PCM data")
    #     return ret

    def set_playback_audio_frame_parameters(self, channels, sample_rate_hz, mode, samples_per_call):
        ret = agora_local_user_set_playback_audio_frame_parameters(self.user_handle, channels, sample_rate_hz, mode, samples_per_call)
        if ret < 0:
            print("Failed to set playback audio frame parameters")
        return ret

    def set_recording_audio_frame_parameters(self, channels, sample_rate_hz, mode, samples_per_call):
        ret = agora_local_user_set_recording_audio_frame_parameters(self.user_handle, channels, sample_rate_hz, mode, samples_per_call)
        if ret < 0:
            print("Failed to set recording audio frame parameters")
        return ret

    def set_mixed_audio_frame_parameters(self, channels, sample_rate_hz, samples_per_call):
        ret = agora_local_user_set_mixed_audio_frame_parameters(self.user_handle, channels, sample_rate_hz, samples_per_call)
        if ret < 0:
            print("Failed to set mixed audio frame parameters")
        return ret

    def set_playback_audio_frame_before_mixing_parameters(self, channels, sample_rate_hz):
        ret = agora_local_user_set_playback_audio_frame_before_mixing_parameters(self.user_handle, channels, sample_rate_hz)
        if ret < 0:
            print("Failed to set playback audio frame before mixing parameters")
        return ret

    def register_audio_frame_observer(self, observer:IAudioFrameObserver):
        audio_frame_observer = AudioFrameObserverInner(observer, self)
        self.audio_frame_observer = audio_frame_observer
        ret = agora_local_user_register_audio_frame_observer(self.user_handle, audio_frame_observer)
        if ret < 0:
            print("Failed to register audio frame observer")
        return ret

    def unregister_audio_frame_observer(self):
        ret = agora_local_user_unregister_audio_frame_observer(self.user_handle)
        if ret < 0:
            print("Failed to unregister audio frame observer")
       
        return ret

    # def enable_audio_spectrum_monitor(self, interval_in_ms):
    #     ret = agora_local_user_enable_audio_spectrum_monitor(self.user_handle, interval_in_ms)
    #     if ret < 0:
    #         print("Failed to enable audio spectrum monitor")
    #     return ret

    # def disable_audio_spectrum_monitor(self):
    #     ret = agora_local_user_disable_audio_spectrum_monitor(self.user_handle)
    #     if ret < 0:
    #         print("Failed to disable audio spectrum monitor")
    #     return ret

    # def register_audio_spectrum_observer(self, observer):
    #     ret = agora_local_user_register_audio_spectrum_observer(self.user_handle, observer)
    #     if ret < 0:
    #         print("Failed to register audio spectrum observer")
    #     return ret

    # def unregister_audio_spectrum_observer(self, observer):
    #     ret = agora_local_user_unregister_audio_spectrum_observer(self.user_handle, observer)
    #     if ret < 0:
    #         print("Failed to unregister audio spectrum observer")
    #     return ret

    # def register_video_encoded_frame_observer(self, agora_video_encoded_frame_observer:IVideoEncodedImageReceiver):
    def register_video_encoded_frame_observer(self, agora_video_encoded_frame_observer:IVideoEncodedFrameObserver):        
        #TO-DO: Inner
        # self.video_encoded_frame_observer = VideoEncodedImageReceiverInner(agora_video_encoded_frame_observer)
        self.video_encoded_frame_observer = VideoEncodedFrameObserverInner(agora_video_encoded_frame_observer)
        # self.video_encoded_frame_observer_handler = agora_video_encoded_image_receiver_create(self.video_encoded_frame_observer)
        self.video_encoded_frame_observer_handler = agora_video_encoded_frame_observer_create(self.video_encoded_frame_observer)
        ret = agora_local_user_register_video_encoded_frame_observer(self.user_handle, self.video_encoded_frame_observer_handler)
        if ret < 0:
            print("Failed to register video encoded frame observer")
        return ret
    
    def unregister_video_encoded_frame_observer(self, agora_video_encoded_frame_observer):
        ret = agora_local_user_unregister_video_encoded_frame_observer(self.user_handle, agora_video_encoded_frame_observer)
        if ret < 0:
            print("Failed to unregister video encoded frame observer")
        return ret

    def register_video_frame_observer(self, agora_video_frame_observer2:IVideoFrameObserver):
        self.video_frame_observer = VideoFrameObserverInner(agora_video_frame_observer2, self)        
        self.video_frame_observer_handler = agora_video_frame_observer2_create(self.video_frame_observer)
        ret = agora_local_user_register_video_frame_observer(self.user_handle, self.video_frame_observer_handler)
        if ret < 0:
            print("Failed to register video frame observer")
        return ret

    def unregister_video_frame_observer(self, agora_video_frame_observer2):
        agora_video_frame_observer2_destroy(self.video_frame_observer_handler)
        ret = agora_local_user_unregister_video_frame_observer(self.user_handle, agora_video_frame_observer2)
        if ret < 0:
            print("Failed to unregister video frame observer")
        return ret

    # def set_video_subscription_options(self, user_id, options):
    #     ret = agora_local_user_set_video_subscription_options(self.user_handle, user_id, options)
    #     if ret < 0:
    #         print("Failed to set video subscription options")
    #     return ret

    def subscribe_video(self, user_id, options:VideoSubscriptionOptions): 
        user_id_t = user_id.encode('utf-8')
        
        ret = agora_local_user_subscribe_video(self.user_handle, user_id_t, ctypes.byref(options))
        if ret < 0:
            print("Failed to subscribe video")
        return ret

    def subscribe_all_video(self, options:VideoSubscriptionOptions):
        ret = agora_local_user_subscribe_all_video(self.user_handle, ctypes.byref(options))
        if ret < 0:
            print("Failed to subscribe all video")
        return ret

    def unsubscribe_video(self, user_id):
        user_id_t = user_id.encode('utf-8')
        ret = agora_local_user_unsubscribe_video(self.user_handle, user_id_t)
        if ret < 0:
            print("Failed to unsubscribe video")
        else:
            self.del_remote_video_map(user_id)
        return ret

    def unsubscribe_all_video(self):
        ret = agora_local_user_unsubscribe_all_video(self.user_handle)
        if ret < 0:
            print("Failed to unsubscribe all video")
        else:
            self.del_remote_video_map_all(None)
        return ret

    def set_audio_volume_indication_parameters(self, interval_in_ms, smooth, report_vad):
        ret = agora_local_user_set_audio_volume_indication_parameters(self.user_handle, interval_in_ms, smooth, report_vad)
        if ret < 0:
            print("Failed to set audio volume indication parameters")
        return ret

    def register_local_user_observer(self, observer:IRTCLocalUserObserver):
        user_observer_inner = RTCLocalUserObserverInner(observer, self)
        self.user_observer_inner = user_observer_inner
        self.user_observer = observer
        ret = agora_local_user_register_observer(self.user_handle, user_observer_inner)
        if ret < 0:
            print("Failed to register observer")
        return ret

    def unregister_local_user_observer(self):
        ret = agora_local_user_unregister_observer(self.user_handle)
        if ret < 0:
            print("Failed to unregister observer")
        return ret

    def get_media_control_packet_sender(self):
        ret = agora_local_user_get_media_control_packet_sender(self.user_handle)
        if ret < 0:
            print("Failed to get media control packet sender")
        return ret

    def register_media_control_packet_receiver(self, agora_media_packet_receiver):
        ret = agora_local_user_register_media_control_packet_receiver(self.user_handle, agora_media_packet_receiver)
        if ret < 0:
            print("Failed to register media control packet receiver")
        return ret

    def unregister_media_control_packet_receiver(self, agora_media_packet_receiver):
        ret = agora_local_user_unregister_media_control_packet_receiver(self.user_handle, agora_media_packet_receiver)
        if ret < 0:
            print("Failed to unregister media control packet receiver")
        return ret

    def send_intra_request(self, uid):
        uid_t = uid.encode('utf-8')
        ret = agora_local_user_send_intra_request(self.user_handle, uid_t)
        if ret < 0:
            print("Failed to send intra request")
        return ret

    def release(self): #do nothing, just do api allign
        #clean all
        with self.remote_audio_tracks_lock:
            self._remote_audio_track_map.clear()
        with self.remote_video_tracks_lock:
            self._remote_video_track_map.clear()
        with self._audio_track_lock:
            self._audio_track_map.clear()
        with self._video_track_lock:
            self._video_track_map.clear()
        pass

    def get_rtc_connection(self):
        return self.connection
    def get_remote_audio_track(self, uid):
        #enum & get audio track
        with self.remote_audio_tracks_lock:
            for handle, remote_audio_track in self.remote_audio_tracks.items():
                if remote_audio_track.user_id == uid:
                    return remote_audio_track
        return None

import ctypes
from .agora_base import *
from .local_user import *
from .local_user_observer import *

user_id_t = ctypes.c_char_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

#========localuser observer=====



class RemoteAudioTrackStats(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("quality", ctypes.c_int),
        ("network_transport_delay", ctypes.c_int),
        ("jitter_buffer_delay", ctypes.c_int),
        ("audio_loss_rate", ctypes.c_int),
        ("num_channels", ctypes.c_int),
        ("received_sample_rate", ctypes.c_int),
        ("received_bitrate", ctypes.c_int),
        ("total_frozen_time", ctypes.c_int),
        ("frozen_rate", ctypes.c_int),
        ("received_bytes", ctypes.c_int64)
    ]

class VideoTrackInfo(ctypes.Structure):
    _fields_ = [
        ("is_local", ctypes.c_int),
        ("owner_uid", uid_t),
        ("track_id", track_id_t),
        ("channel_id", ctypes.c_char_p),
        ("stream_type", ctypes.c_int),
        ("codec_type", ctypes.c_int),
        ("encoded_frame_only", ctypes.c_int),
        ("source_type", ctypes.c_int),
        ("observation_position", ctypes.c_uint32)
    ]

class LocalVideoTrackStats(ctypes.Structure):
 _fields_ = [
        ("number_of_streams", ctypes.c_uint64),
        ("bytes_major_stream", ctypes.c_uint64),
        ("bytes_minor_stream", ctypes.c_uint64),
        ("frames_encoded", ctypes.c_uint32),
        ("ssrc_major_stream", ctypes.c_uint32),
        ("ssrc_minor_stream", ctypes.c_uint32),
        ("capture_frame_rate", ctypes.c_int),
        ("regulated_capture_frame_rate", ctypes.c_int),
        ("input_frame_rate", ctypes.c_int),
        ("encode_frame_rate", ctypes.c_int),
        ("render_frame_rate", ctypes.c_int),
        ("target_media_bitrate_bps", ctypes.c_int),
        ("media_bitrate_bps", ctypes.c_int),
        ("total_bitrate_bps", ctypes.c_int),
        ("capture_width", ctypes.c_int),
        ("capture_height", ctypes.c_int),
        ("regulated_capture_width", ctypes.c_int),
        ("regulated_capture_height", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("encoder_type", ctypes.c_uint32),
        ("uplink_cost_time_ms", ctypes.c_uint32),
        ("quality_adapt_indication", ctypes.c_int)
    ]
class RemoteVideoTrackStats(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("delay", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("received_bitrate", ctypes.c_int),
        ("decoder_output_frame_rate", ctypes.c_int),
        ("renderer_output_frame_rate", ctypes.c_int),
        ("frame_loss_rate", ctypes.c_int),
        ("packet_loss_rate", ctypes.c_int),
        ("rx_stream_type", ctypes.c_int),
        ("total_frozen_time", ctypes.c_int),
        ("frozen_rate", ctypes.c_int),
        ("total_decoded_frames", ctypes.c_uint32),
        ("av_sync_time_ms", ctypes.c_int),
        ("downlink_process_time_ms", ctypes.c_uint32),
        ("frame_render_delay_ms", ctypes.c_uint32),
        ("totalActiveTime", ctypes.c_uint64),
        ("publishDuration", ctypes.c_uint64)
    ]

class AudioVolumeInfo(ctypes.Structure):
    _fields_ = [
        ("user_id", ctypes.c_uint),
        ("volume", ctypes.c_uint),
        ("vad", ctypes.c_uint),
        ("voicePitch", ctypes.c_double)
    ]

class RemoteVideoStreamInfo(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("stream_type", ctypes.c_uint8),
        ("current_downscale_level", ctypes.c_uint8),
        ("total_downscale_level_counts", ctypes.c_uint8)
    ]

# 定义回调函数类型
ON_AUDIO_TRACK_PUBLISH_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_PUBLISH_START_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_UNPUBLISHED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_PUBLICATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int)
ON_LOCAL_AUDIO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_LOCAL_AUDIO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LocalAudioStats))
ON_REMOTE_AUDIO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(RemoteAudioTrackStats))
ON_USER_AUDIO_TRACK_SUBSCRIBED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, AGORA_HANDLE)
ON_USER_AUDIO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_AUDIO_SUBSCRIBE_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_AUDIO_PUBLISH_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_FIRST_REMOTE_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)
ON_FIRST_REMOTE_AUDIO_DECODED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)

ON_VIDEO_TRACK_PUBLISH_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_VIDEO_TRACK_PUBLISH_START_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_VIDEO_TRACK_UNPUBLISHED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_VIDEO_TRACK_PUBLICATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int)
ON_LOCAL_VIDEO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_LOCAL_VIDEO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(LocalVideoTrackStats))
ON_USER_VIDEO_TRACK_SUBSCRIBED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.POINTER(VideoTrackInfo), AGORA_HANDLE)
ON_USER_VIDEO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_REMOTE_VIDEO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(RemoteVideoTrackStats))
ON_AUDIO_VOLUME_INDICATION_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(AudioVolumeInfo), ctypes.c_uint, ctypes.c_int)
ON_ACTIVE_SPEAKER_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t)
ON_REMOTE_VIDEO_STREAM_INFO_UPDATED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RemoteVideoStreamInfo))
ON_VIDEO_SUBSCRIBE_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_VIDEO_PUBLISH_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_FIRST_REMOTE_VIDEO_FRAME_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_FIRST_REMOTE_VIDEO_DECODED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_FIRST_REMOTE_VIDEO_FRAME_RENDERED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_VIDEO_SIZE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_USER_INFO_UPDATED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int)
ON_INTRA_REQUEST_RECEIVED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE)
ON_REMOTE_SUBSCRIBE_FALLBACK_TO_AUDIO_ONLY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)
ON_STREAM_MESSAGE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t)
ON_USER_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_uint32)


"""
on_user_info_updated(user_id_t: string ;  msg: int, val: int)
msg:  
enum USER_MEDIA_INFO {
    /**
     * 0: The user has muted the audio.
     */
    USER_MEDIA_INFO_MUTE_AUDIO = 0,
    /**
     * 1: The user has muted the video.
     */
    USER_MEDIA_INFO_MUTE_VIDEO = 1,
    /**
     * 4: The user has enabled the video, which includes video capturing and encoding.
     */
    USER_MEDIA_INFO_ENABLE_VIDEO = 4,
    /**
     * 8: The user has enabled the local video capturing.
     */
    USER_MEDIA_INFO_ENABLE_LOCAL_VIDEO = 8,
  };
  val: 1: The user has muted the audio.0: unmuted the audio
参考：https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/classagora_1_1rtc_1_1_i_local_user_observer#onUserInfoUpdated()
"""
class RTCLocalUserObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_audio_track_publish_success", ON_AUDIO_TRACK_PUBLISH_SUCCESS_CALLBACK),
        ("on_audio_track_publish_start", ON_AUDIO_TRACK_PUBLISH_START_CALLBACK),
        ("on_audio_track_unpublished", ON_AUDIO_TRACK_UNPUBLISHED_CALLBACK),
        ("on_audio_track_publication_failure", ON_AUDIO_TRACK_PUBLICATION_FAILURE_CALLBACK),
        ("on_local_audio_track_state_changed", ON_LOCAL_AUDIO_TRACK_STATE_CHANGED_CALLBACK),
        ("on_local_audio_track_statistics", ON_LOCAL_AUDIO_TRACK_STATISTICS_CALLBACK),
        ("on_remote_audio_track_statistics", ON_REMOTE_AUDIO_TRACK_STATISTICS_CALLBACK),
        ("on_user_audio_track_subscribed", ON_USER_AUDIO_TRACK_SUBSCRIBED_CALLBACK),
        ("on_user_audio_track_state_changed", ON_USER_AUDIO_TRACK_STATE_CHANGED_CALLBACK),
        ("on_audio_subscribe_state_changed", ON_AUDIO_SUBSCRIBE_STATE_CHANGED_CALLBACK),
        ("on_audio_publish_state_changed", ON_AUDIO_PUBLISH_STATE_CHANGED_CALLBACK),
        ("on_first_remote_audio_frame", ON_FIRST_REMOTE_AUDIO_FRAME_CALLBACK),
        ("on_first_remote_audio_decoded", ON_FIRST_REMOTE_AUDIO_DECODED_CALLBACK),

        ("on_video_track_publish_success", ON_VIDEO_TRACK_PUBLISH_SUCCESS_CALLBACK),
        ("on_video_track_publish_start", ON_VIDEO_TRACK_PUBLISH_START_CALLBACK),
        ("on_video_track_unpublished", ON_VIDEO_TRACK_UNPUBLISHED_CALLBACK),
        ("on_video_track_publication_failure", ON_VIDEO_TRACK_PUBLICATION_FAILURE_CALLBACK),
        ("on_local_video_track_state_changed", ON_LOCAL_VIDEO_TRACK_STATE_CHANGED_CALLBACK),
        ("on_local_video_track_statistics", ON_LOCAL_VIDEO_TRACK_STATISTICS_CALLBACK),
        ("on_user_video_track_subscribed", ON_USER_VIDEO_TRACK_SUBSCRIBED_CALLBACK),
        ("on_user_video_track_state_changed", ON_USER_VIDEO_TRACK_STATE_CHANGED_CALLBACK),
        ("on_remote_video_track_statistics", ON_REMOTE_VIDEO_TRACK_STATISTICS_CALLBACK),
        ("on_audio_volume_indication", ON_AUDIO_VOLUME_INDICATION_CALLBACK),
        ("on_active_speaker", ON_ACTIVE_SPEAKER_CALLBACK),
        ("on_remote_video_stream_info_updated", ON_REMOTE_VIDEO_STREAM_INFO_UPDATED_CALLBACK),
        ("on_video_subscribe_state_changed", ON_VIDEO_SUBSCRIBE_STATE_CHANGED_CALLBACK),
        ("on_video_publish_state_changed", ON_VIDEO_PUBLISH_STATE_CHANGED_CALLBACK),
        ("on_first_remote_video_frame", ON_FIRST_REMOTE_VIDEO_FRAME_CALLBACK),
        ("on_first_remote_video_decoded", ON_FIRST_REMOTE_VIDEO_DECODED_CALLBACK),
        ("on_first_remote_video_frame_rendered", ON_FIRST_REMOTE_VIDEO_FRAME_RENDERED_CALLBACK),
        ("on_video_size_changed", ON_VIDEO_SIZE_CHANGED_CALLBACK),

        ("on_user_info_updated", ON_USER_INFO_UPDATED_CALLBACK),
        ("on_intra_request_received", ON_INTRA_REQUEST_RECEIVED_CALLBACK),
        ("on_remote_subscribe_fallback_to_audio_only", ON_REMOTE_SUBSCRIBE_FALLBACK_TO_AUDIO_ONLY_CALLBACK),
        ("on_stream_message", ON_STREAM_MESSAGE_CALLBACK),
        ("on_user_state_changed", ON_USER_STATE_CHANGED_CALLBACK)
    ]    

    def __init__(self, local_user_observer:IRTCLocalUserObserver, local_user: 'LocalUser') -> None:
        from .local_user import LocalUser
        self.local_user_observer = local_user_observer
        self.local_user = local_user
        self.on_audio_track_publish_success = ON_AUDIO_TRACK_PUBLISH_SUCCESS_CALLBACK(self._on_audio_track_publish_success)
        self.on_video_track_publish_success = ON_VIDEO_TRACK_PUBLISH_SUCCESS_CALLBACK(self._on_video_track_publish_success)
        self.on_audio_track_publish_start = ON_AUDIO_TRACK_PUBLISH_START_CALLBACK(self._on_audio_track_publish_start)
        self.on_audio_track_unpublished = ON_AUDIO_TRACK_UNPUBLISHED_CALLBACK(self._on_audio_track_unpublished)
        self.on_audio_track_publication_failure = ON_AUDIO_TRACK_PUBLICATION_FAILURE_CALLBACK(self._on_audio_track_publication_failure)
        self.on_local_audio_track_state_changed = ON_LOCAL_AUDIO_TRACK_STATE_CHANGED_CALLBACK(self._on_local_audio_track_state_changed)
        self.on_local_audio_track_statistics = ON_LOCAL_AUDIO_TRACK_STATISTICS_CALLBACK(self._on_local_audio_track_statistics)
        self.on_remote_audio_track_statistics = ON_REMOTE_AUDIO_TRACK_STATISTICS_CALLBACK(self._on_remote_audio_track_statistics)
        self.on_user_audio_track_subscribed = ON_USER_AUDIO_TRACK_SUBSCRIBED_CALLBACK(self._on_user_audio_track_subscribed)
        self.on_user_audio_track_state_changed = ON_USER_AUDIO_TRACK_STATE_CHANGED_CALLBACK(self._on_user_audio_track_state_changed)
        self.on_audio_subscribe_state_changed = ON_AUDIO_SUBSCRIBE_STATE_CHANGED_CALLBACK(self._on_audio_subscribe_state_changed)
        self.on_audio_publish_state_changed = ON_AUDIO_PUBLISH_STATE_CHANGED_CALLBACK(self._on_audio_publish_state_changed)
        self.on_first_remote_audio_frame = ON_FIRST_REMOTE_AUDIO_FRAME_CALLBACK(self._on_first_remote_audio_frame)
        self.on_first_remote_audio_decoded = ON_FIRST_REMOTE_AUDIO_DECODED_CALLBACK(self._on_first_remote_audio_decoded)
        self.on_video_track_publish_start = ON_VIDEO_TRACK_PUBLISH_START_CALLBACK(self._on_video_track_publish_start)
        self.on_video_track_unpublished = ON_VIDEO_TRACK_UNPUBLISHED_CALLBACK(self._on_video_track_unpublished)
        self.on_video_track_publication_failure = ON_VIDEO_TRACK_PUBLICATION_FAILURE_CALLBACK(self._on_video_track_publication_failure)
        self.on_local_video_track_state_changed = ON_LOCAL_VIDEO_TRACK_STATE_CHANGED_CALLBACK(self._on_local_video_track_state_changed)
        self.on_local_video_track_statistics = ON_LOCAL_VIDEO_TRACK_STATISTICS_CALLBACK(self._on_local_video_track_statistics)
        self.on_user_video_track_subscribed = ON_USER_VIDEO_TRACK_SUBSCRIBED_CALLBACK(self._on_user_video_track_subscribed)
        self.on_user_video_track_state_changed = ON_USER_VIDEO_TRACK_STATE_CHANGED_CALLBACK(self._on_user_video_track_state_changed)
        self.on_remote_video_track_statistics = ON_REMOTE_VIDEO_TRACK_STATISTICS_CALLBACK(self._on_remote_video_track_statistics)
        self.on_audio_volume_indication = ON_AUDIO_VOLUME_INDICATION_CALLBACK(self._on_audio_volume_indication)
        self.on_active_speaker = ON_ACTIVE_SPEAKER_CALLBACK(self._on_active_speaker)
        self.on_remote_video_stream_info_updated = ON_REMOTE_VIDEO_STREAM_INFO_UPDATED_CALLBACK(self._on_remote_video_stream_info_updated)
        self.on_video_subscribe_state_changed = ON_VIDEO_SUBSCRIBE_STATE_CHANGED_CALLBACK(self._on_video_subscribe_state_changed)
        self.on_video_publish_state_changed = ON_VIDEO_PUBLISH_STATE_CHANGED_CALLBACK(self._on_video_publish_state_changed)
        self.on_first_remote_video_frame = ON_FIRST_REMOTE_VIDEO_FRAME_CALLBACK(self._on_first_remote_video_frame)
        self.on_first_remote_video_decoded = ON_FIRST_REMOTE_VIDEO_DECODED_CALLBACK(self._on_first_remote_video_decoded)
        self.on_first_remote_video_frame_rendered = ON_FIRST_REMOTE_VIDEO_FRAME_RENDERED_CALLBACK(self._on_first_remote_video_frame_rendered)
        self.on_video_size_changed = ON_VIDEO_SIZE_CHANGED_CALLBACK(self._on_video_size_changed)
        self.on_user_info_updated = ON_USER_INFO_UPDATED_CALLBACK(self._on_user_info_updated)
        self.on_intra_request_received = ON_INTRA_REQUEST_RECEIVED_CALLBACK(self._on_intra_request_received)
        self.on_remote_subscribe_fallback_to_audio_only = ON_REMOTE_SUBSCRIBE_FALLBACK_TO_AUDIO_ONLY_CALLBACK(self._on_remote_subscribe_fallback_to_audio_only)
        self.on_stream_message = ON_STREAM_MESSAGE_CALLBACK(self._on_stream_message)
        self.on_user_state_changed = ON_USER_STATE_CHANGED_CALLBACK(self._on_user_state_changed)


    def _on_audio_track_publish_success(self, agora_local_user, agora_local_audio_track):
        print("LocalUserCB _on_audio_track_publish_success:", agora_local_user, agora_local_audio_track)
        self.local_user_observer.on_audio_track_publish_success(self.local_user, agora_local_audio_track)
    
    def _on_video_track_publish_success(self, agora_local_user, agora_local_video_track):
        print("LocalUserCB _on_video_track_publish_success:", agora_local_user, agora_local_video_track)
        self.local_user_observer.on_video_track_publish_success(self.local_user, agora_local_video_track)

    def _on_video_track_publish_start(self, agora_local_user, agora_local_video_track):
        print("LocalUserCB _on_video_track_publish_start:", agora_local_user, agora_local_video_track)
        self.local_user_observer.on_video_track_publish_start(self.local_user, agora_local_video_track)
        
    def _on_audio_track_publish_start(self, agora_local_user, agora_local_audio_track):
        print("LocalUserCB _on_audio_track_publish_start:", agora_local_user, agora_local_audio_track)
        self.local_user_observer.on_audio_track_publish_start(self.local_user, agora_local_audio_track)

    def _on_audio_track_unpublished(self, agora_local_user, agora_local_audio_track):
        print("LocalUserCB _on_audio_track_unpublished:", agora_local_user, agora_local_audio_track)
        self.local_user_observer.on_audio_track_unpublished(self.local_user, agora_local_audio_track)

    def _on_audio_track_publication_failure(self, agora_local_user, agora_local_audio_track, error_code):
        print("LocalUserCB _on_audio_track_publication_failure:", agora_local_user, agora_local_audio_track, error_code)
        self.local_user_observer.on_audio_track_publication_failure(self.local_user, agora_local_audio_track, error_code)
    
    def _on_local_audio_track_state_changed(self, agora_local_user, agora_local_audio_track, state, error):
        print("LocalUserCB _on_local_audio_track_state_changed:", agora_local_user, agora_local_audio_track, state, error)
        self.local_user_observer.on_local_audio_track_state_changed(self.local_user, agora_local_audio_track, state, error)

    def _on_local_audio_track_statistics(self, agora_local_user, stats):
        print("LocalUserCB _on_local_audio_track_statistics:", agora_local_user, stats)
        self.local_user_observer.on_local_audio_track_statistics(self.local_user, stats)
    
    def _on_remote_audio_track_statistics(self, agora_local_user, agora_remote_audio_track, stats):
        print("LocalUserCB _on_remote_audio_track_statistics:", agora_local_user, agora_remote_audio_track, stats)
        self.local_user_observer.on_remote_audio_track_statistics(self.local_user, agora_remote_audio_track, stats)

    def _on_user_audio_track_subscribed(self, agora_local_user, user_id, agora_remote_audio_track):
        print("LocalUserCB _on_user_audio_track_subscribed:", agora_local_user, user_id, agora_remote_audio_track)
        self.local_user_observer.on_user_audio_track_subscribed(self.local_user, user_id, agora_remote_audio_track)

    def _on_user_audio_track_state_changed(self, agora_local_user, user_id, agora_remote_audio_track, state, reason, elapsed):
        print("LocalUserCB _on_user_audio_track_state_changed:", agora_local_user, user_id, agora_remote_audio_track, state, reason, elapsed)
        self.local_user_observer.on_user_audio_track_state_changed(self.local_user, user_id, agora_remote_audio_track, state, reason, elapsed)
    
    def _on_audio_subscribe_state_changed(self, agora_local_user, channel_id, user_id, state, reason, elapsed):
        print("LocalUserCB _on_audio_subscribe_state_changed:", agora_local_user, channel_id, user_id, state, reason, elapsed)
        self.local_user_observer.on_audio_subscribe_state_changed(self.local_user, channel_id, user_id, state, reason, elapsed)

    def _on_audio_publish_state_changed(self, agora_local_user, channel_id, state, reason, elapsed):
        print("LocalUserCB _on_audio_publish_state_changed:", agora_local_user, channel_id, state, reason, elapsed)
        self.local_user_observer.on_audio_publish_state_changed(self.local_user, channel_id, state, reason, elapsed)

    def _on_first_remote_audio_frame(self, agora_local_user, user_id, elapsed):
        print("LocalUserCB _on_first_remote_audio_frame:", agora_local_user, user_id, elapsed)
        self.local_user_observer.on_first_remote_audio_frame(self.local_user, user_id, elapsed)
    
    def _on_first_remote_audio_decoded(self, agora_local_user, user_id, elapsed):
        print("LocalUserCB _on_first_remote_audio_decoded:", agora_local_user, user_id, elapsed)
        self.local_user_observer.on_first_remote_audio_decoded(self.local_user, user_id, elapsed)

    def _on_video_track_unpublished(self, agora_local_user, agora_local_video_track):
        print("LocalUserCB _on_video_track_unpublished:", agora_local_user, agora_local_video_track)
        self.local_user_observer.on_video_track_unpublished(self.local_user, agora_local_video_track)

    def _on_video_track_publication_failure(self, agora_local_user, agora_local_video_track, error_code):
        print("LocalUserCB _on_video_track_publication_failure:", agora_local_user, agora_local_video_track, error_code)
        self.local_user_observer.on_video_track_publication_failure(self.local_user, agora_local_video_track, error_code)

    def _on_local_video_track_state_changed(self, agora_local_user, agora_local_video_track, state, error):
        print("LocalUserCB _on_local_video_track_state_changed:", agora_local_user, agora_local_video_track, state, error)
        self.local_user_observer.on_local_video_track_state_changed(self.local_user, agora_local_video_track, state, error)

    def _on_local_video_track_statistics(self, agora_local_user, agora_local_video_track, stats):
        print("LocalUserCB _on_local_video_track_statistics:", agora_local_user, agora_local_video_track, stats)
        self.local_user_observer.on_local_video_track_statistics(self.local_user, agora_local_video_track, stats)

    def _on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track, video_track_info):
        print("LocalUserCB _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        self.local_user_observer.on_user_video_track_subscribed(self.local_user, user_id, video_track_info, agora_remote_video_track)

    def _on_user_video_track_state_changed(self, agora_local_user, user_id, agora_remote_video_track, state, reason, elapsed):
        print("LocalUserCB _on_user_video_track_state_changed:", agora_local_user, user_id, agora_remote_video_track, state, reason, elapsed)
        self.local_user_observer.on_user_video_track_state_changed(self.local_user, user_id, agora_remote_video_track, state, reason, elapsed)

    def _on_remote_video_track_statistics(self, agora_local_user, agora_remote_video_track, stats):
        print("LocalUserCB _on_remote_video_track_statistics:", agora_local_user, agora_remote_video_track, stats)
        self.local_user_observer.on_remote_video_track_statistics(self.local_user, agora_remote_video_track, stats)

    def _on_audio_volume_indication(self, agora_local_user, audio_volume_info, speaker_number, total_volume):
        print("LocalUserCB _on_audio_volume_indication:", agora_local_user, audio_volume_info, speaker_number, total_volume)
        self.local_user_observer.on_audio_volume_indication(self.local_user, audio_volume_info, speaker_number, total_volume)

    def _on_active_speaker(self, agora_local_user, user_id):
        print("LocalUserCB _on_active_speaker:", agora_local_user, user_id)
        self.local_user_observer.on_active_speaker(self.local_user, user_id)

    def _on_remote_video_stream_info_updated(self, agora_local_user, remote_video_stream_info):
        print("LocalUserCB _on_remote_video_stream_info_updated:", agora_local_user, remote_video_stream_info)
        self.local_user_observer.on_remote_video_stream_info_updated(self.local_user, remote_video_stream_info)

    def _on_video_subscribe_state_changed(self, agora_local_user, channel_id, user_id, state, reason, elapsed):
        print("LocalUserCB _on_video_subscribe_state_changed:", agora_local_user, channel_id, user_id, state, reason, elapsed)
        self.local_user_observer.on_video_subscribe_state_changed(self.local_user, channel_id, user_id, state, reason, elapsed)

    def _on_video_publish_state_changed(self, agora_local_user, channel_id, state, reason, elapsed):
        print("LocalUserCB _on_video_publish_state_changed:", agora_local_user, channel_id, state, reason, elapsed)
        self.local_user_observer.on_video_publish_state_changed(self.local_user, channel_id, state, reason, elapsed)

    def _on_first_remote_video_frame(self, agora_local_user, user_id, width, height, elapsed):
        print("LocalUserCB _on_first_remote_video_frame:", agora_local_user, user_id, width, height, elapsed)
        self.local_user_observer.on_first_remote_video_frame(self.local_user, user_id, width, height, elapsed)

    def _on_first_remote_video_decoded(self, agora_local_user, user_id, width, height, elapsed):
        print("LocalUserCB _on_first_remote_video_decoded:", agora_local_user, user_id, width, height, elapsed)
        self.local_user_observer.on_first_remote_video_decoded(self.local_user, user_id, width, height, elapsed)

    def _on_first_remote_video_frame_rendered(self, agora_local_user, user_id, width, height, elapsed):
        print("LocalUserCB _on_first_remote_video_frame_rendered:", agora_local_user, user_id, width, height, elapsed)
        self.local_user_observer.on_first_remote_video_frame_rendered(self.local_user, user_id, width, height, elapsed)

    def _on_video_size_changed(self, agora_local_user, user_id, width, height, elapsed):
        print("LocalUserCB _on_video_size_changed:", agora_local_user, user_id, width, height, elapsed)
        self.local_user_observer.on_video_size_changed(self.local_user, user_id, width, height, elapsed)

    def _on_user_info_updated(self, agora_local_user, user_id, msg, val):
        print("LocalUserCB _on_user_info_updated:", agora_local_user, user_id, msg, val)
        self.local_user_observer.on_user_info_updated(self.local_user, user_id, msg, val)

    def _on_intra_request_received(self, agora_local_user):
        print("LocalUserCB _on_intra_request_received:", agora_local_user)
        self.local_user_observer.on_intra_request_received(self.local_user)

    def _on_remote_subscribe_fallback_to_audio_only(self, agora_local_user, user_id, is_fallback):
        print("LocalUserCB _on_remote_subscribe_fallback_to_audio_only:", agora_local_user, user_id, is_fallback)
        self.local_user_observer.on_remote_subscribe_fallback_to_audio_only(self.local_user, user_id, is_fallback)

    def _on_stream_message(self, agora_local_user, user_id, stream_id, data, size):
        print("LocalUserCB _on_stream_message:", agora_local_user, user_id, stream_id, data, size)
        self.local_user_observer.on_stream_message(self.local_user, user_id, stream_id, data, size)

    def _on_user_state_changed(self, agora_local_user, user_id, state):
        print("LocalUserCB _on_user_state_changed:", agora_local_user, user_id, state)
        self.local_user_observer.on_user_state_changed(self.local_user, user_id, state)        

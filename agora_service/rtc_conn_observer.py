import ctypes
from .agora_base import *
from .local_user import *

class RTCConnInfo(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint64),
        ("channel_id", ctypes.c_char_p),
        ("state", ctypes.c_int),
        ("local_user_id", ctypes.c_char_p),
        ("internal_uid", ctypes.c_uint)
    ]

uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

ON_CONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_DISCONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_CONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_RECONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_RECONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)

ON_CONNECTION_LOST_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo))
ON_LASTMILE_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_LASTMILE_PROBE_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LastmileProbeResult))
ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p)
ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE)

ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_CONNECTION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_USER_JOINED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t)
ON_USER_LEFT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)
ON_TRANSPORT_STATS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCStats))

ON_CHANGE_ROLE_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_CHANGE_ROLE_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_USER_NETWORK_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int)
ON_NETWORK_TYPE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_API_CALL_EXECUTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)

ON_CONTENT_INSPECT_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_SNAPSHOT_TAKEN_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, uid_t, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p)
ON_WARNING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p)
ON_CHANNEL_MEDIA_RELAY_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)

ON_LOCAL_USER_REGISTERED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, uid_t, ctypes.c_char_p)
ON_USER_ACCOUNT_UPDATED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, uid_t, ctypes.c_char_p)
ON_STREAM_MESSAGE_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_ENCRYPTION_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_UPLOAD_LOG_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)

class RTCConnObserver(ctypes.Structure):
    _fields_ = [
        ("on_connected", ON_CONNECTED_CALLBACK),
        ("on_disconnected", ON_DISCONNECTED_CALLBACK),
        ("on_connecting", ON_CONNECTING_CALLBACK),
        ("on_reconnecting", ON_RECONNECTING_CALLBACK),
        ("on_reconnected", ON_RECONNECTED_CALLBACK),
        
        ("on_connection_lost", ON_CONNECTION_LOST_CALLBACK),
        ("on_lastmile_quality", ON_LASTMILE_QUALITY_CALLBACK),
        ("on_lastmile_probe_result", ON_LASTMILE_PROBE_RESULT_CALLBACK),
        ("on_token_privilege_will_expire", ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK),
        ("on_token_privilege_did_expire", ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK),
        
        ("on_connection_license_validation_failure", ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK),
        ("on_connection_failure", ON_CONNECTION_FAILURE_CALLBACK),
        ("on_user_joined", ON_USER_JOINED_CALLBACK),
        ("on_user_left", ON_USER_LEFT_CALLBACK),
        ("on_transport_stats", ON_TRANSPORT_STATS_CALLBACK),
        
        ("on_change_role_success", ON_CHANGE_ROLE_SUCCESS_CALLBACK),
        ("on_change_role_failure", ON_CHANGE_ROLE_FAILURE_CALLBACK),
        ("on_user_network_quality", ON_USER_NETWORK_QUALITY_CALLBACK),
        ("on_network_type_changed", ON_NETWORK_TYPE_CHANGED_CALLBACK),
        ("on_api_call_executed", ON_API_CALL_EXECUTED_CALLBACK),
        
        ("on_content_inspect_result", ON_CONTENT_INSPECT_RESULT_CALLBACK),
        ("on_snapshot_taken", ON_SNAPSHOT_TAKEN_CALLBACK),
        ("on_error", ON_ERROR_CALLBACK),
        ("on_warning", ON_WARNING_CALLBACK),
        ("on_channel_media_relay_state_changed", ON_CHANNEL_MEDIA_RELAY_STATE_CHANGED_CALLBACK),
        
        ("on_local_user_registered", ON_LOCAL_USER_REGISTERED_CALLBACK),
        ("on_user_account_updated", ON_USER_ACCOUNT_UPDATED_CALLBACK),
        ("on_stream_message_error", ON_STREAM_MESSAGE_ERROR_CALLBACK),
        ("on_encryption_error", ON_ENCRYPTION_ERROR_CALLBACK),
        ("on_upload_log_result", ON_UPLOAD_LOG_RESULT_CALLBACK)
    ]

#========localuser observer=====

class LocalAudioStats(ctypes.Structure):
    _fields_ = [
        ("num_channels", ctypes.c_int),
        ("sent_sample_rate", ctypes.c_int),
        ("sent_bitrate", ctypes.c_int),
        ("internal_codec", ctypes.c_int),
        ("voice_pitch", ctypes.c_double)
    ]

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
class RTCLocalUserObserver(ctypes.Structure):
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
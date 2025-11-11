import ctypes
from ..agora_base import *
from ..local_user import *
from ._ctypes_data import VideoTrackInfoInner
from ..remote_audio_track import RemoteAudioTrack, RemoteAudioTrackStats
from ..remote_video_track import RemoteVideoTrack, RemoteVideoTrackStats
import logging
logger = logging.getLogger(__name__)

ON_AUDIO_TRACK_PUBLISH_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_PUBLISH_START_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_UNPUBLISHED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE)
ON_AUDIO_TRACK_PUBLICATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int)
ON_LOCAL_AUDIO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_LOCAL_AUDIO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LocalAudioStatsInner))
ON_REMOTE_AUDIO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(RemoteAudioTrackStatsInner))
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
ON_LOCAL_VIDEO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(LocalVideoTrackStatsInner))
ON_USER_VIDEO_TRACK_SUBSCRIBED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.POINTER(VideoTrackInfoInner), AGORA_HANDLE)
ON_USER_VIDEO_TRACK_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, AGORA_HANDLE, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_REMOTE_VIDEO_TRACK_STATISTICS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, AGORA_HANDLE, ctypes.POINTER(RemoteVideoTrackStatsInner))
ON_AUDIO_VOLUME_INDICATION_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(AudioVolumeInfoInner), ctypes.c_uint, ctypes.c_int)
ON_ACTIVE_SPEAKER_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t)
ON_REMOTE_VIDEO_STREAM_INFO_UPDATED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RemoteVideoStreamInfoInner))
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
ON_AUDIO_META_DATA_RECEIVED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_char_p, ctypes.c_size_t)


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
        ("on_user_state_changed", ON_USER_STATE_CHANGED_CALLBACK),
        ("on_audio_meta_data_received", ON_AUDIO_META_DATA_RECEIVED_CALLBACK)
    ]

    def __init__(self, local_user_observer: IRTCLocalUserObserver, local_user: 'LocalUser') -> None:
        from ..local_user import LocalUser
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
        self.on_audio_meta_data_received = ON_AUDIO_META_DATA_RECEIVED_CALLBACK(self._on_audio_meta_data_received)

    """
    it seems that this interface does not provide much value to the user's business, 
    therefore, there is no need to convert audio_track(ctypes.handle type) into LocalAudioTrack.
    If convert is necessary, it would require recording the LocalAudioTrack during LocalUser.pub_audio, and support a get methond in LocalAudioTrack to
    get LocalAudioTrack instance from handle.
    codes may  like: LocalAudioTrack = self.local_user.get(local_audio_track_handle)
    Avoid to create a global LocalAudioTrack map table as it can significantly impact performance .
    """

    def _on_audio_track_publish_success(self, local_user_handle, local_audio_track_handle):
        logger.debug(f"LocalUserCB _on_audio_track_publish_success: {local_user_handle}, {local_audio_track_handle}")
        # note: to get
        audio_track = self.local_user.get_audio_map(local_audio_track_handle)
        self.local_user_observer.on_audio_track_publish_success(self.local_user, audio_track)

    def _on_video_track_publish_success(self, local_user_handle, local_video_track_handle):
        logger.debug(f"LocalUserCB _on_video_track_publish_success: {local_user_handle}, {local_video_track_handle}")
        video_track = self.local_user.get_video_map(local_video_track_handle)
        self.local_user_observer.on_video_track_publish_success(self.local_user, video_track)

    def _on_video_track_publish_start(self, local_user_handle, local_video_track_handle):
        logger.debug(f"LocalUserCB _on_video_track_publish_start: {local_user_handle}, {local_video_track_handle}")
        video_track = self.local_user.get_video_map(local_video_track_handle)
        self.local_user_observer.on_video_track_publish_start(self.local_user, video_track)

    def _on_audio_track_publish_start(self, local_user_handle, local_audio_track_handle):
        logger.debug(f"LocalUserCB _on_audio_track_publish_start: {local_user_handle}, {local_audio_track_handle}")
        audio_track = self.local_user.get_audio_map(local_audio_track_handle)
        self.local_user_observer.on_audio_track_publish_start(self.local_user, audio_track)

    def _on_audio_track_unpublished(self, local_user_handle, local_audio_track_handle):
        logger.debug(f"LocalUserCB _on_audio_track_unpublished: {local_user_handle}, {local_audio_track_handle}")
        audio_track = self.local_user.get_audio_map(local_audio_track_handle)
        self.local_user._del_audio_map(local_audio_track_handle)
        self.local_user_observer.on_audio_track_unpublished(self.local_user, audio_track)

    def _on_audio_track_publication_failure(self, local_user_handle, local_audio_track_handle, error_code):
        logger.debug(f"LocalUserCB _on_audio_track_publication_failure: {local_user_handle}, {local_audio_track_handle}, {error_code}")
        audio_track = self.local_user.get_audio_map(local_audio_track_handle)
        self.local_user.del_audio_map(local_audio_track_handle)
        self.local_user_observer.on_audio_track_publication_failure(self.local_user, audio_track, error_code)

    def _on_local_audio_track_state_changed(self, local_user_handle, local_audio_track_handle, state, error):
        logger.debug(f"LocalUserCB _on_local_audio_track_state_changed: {local_user_handle}, {local_audio_track_handle}, {state}, {error}")
        audio_track = self.local_user.get_audio_map(local_audio_track_handle)
        self.local_user_observer.on_local_audio_track_state_changed(self.local_user, audio_track, state, error)

    def _on_local_audio_track_statistics(self, local_user_handle, stats):
        local_audio_stats = stats.contents.get() if stats else None
        self.local_user_observer.on_local_audio_track_statistics(self.local_user, local_audio_stats)

    def _on_user_audio_track_subscribed(self, local_user_handle, user_id, remote_audio_track_handle):
        logger.debug(f"LocalUserCB _on_user_audio_track_subscribed: {local_user_handle}, {user_id}, {remote_audio_track_handle}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        #add apm filter for remote audio track
        self.local_user._set_apm_filter_properties(remote_audio_track_handle,user_id_str)
        # note: this is a pointer to agora::rtc::IRemoteAudioTrack
        remote_audio_track = RemoteAudioTrack(remote_audio_track_handle, user_id_str)
        # map to localuser to save reference
        self.local_user.set_remote_audio_map(remote_audio_track_handle, remote_audio_track, user_id_str)
        self.local_user_observer.on_user_audio_track_subscribed(self.local_user, user_id_str, remote_audio_track)

    def _on_remote_audio_track_statistics(self, local_user_handle, remote_audio_track_handle, stats):
        logger.debug(f"LocalUserCB _on_remote_audio_track_statistics: {local_user_handle}, {remote_audio_track_handle}, {stats}")
        audio_stats = stats.contents.get() if stats else None
        remote_audio_track = self.local_user.get_remote_audio_map(remote_audio_track_handle)
        self.local_user_observer.on_remote_audio_track_statistics(self.local_user, remote_audio_track, audio_stats)

    def _on_user_audio_track_state_changed(self, local_user_handle, user_id, remote_audio_track_handle, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_user_audio_track_state_changed: {local_user_handle}, {user_id}, {remote_audio_track_handle}, {state}, {reason}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        remote_audio_track = self.local_user.get_remote_audio_map(remote_audio_track_handle)
        self.local_user_observer.on_user_audio_track_state_changed(self.local_user, user_id_str, remote_audio_track, state, reason, elapsed)

    def _on_audio_subscribe_state_changed(self, local_user_handle, channel_id, user_id, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_audio_subscribe_state_changed: {local_user_handle}, {channel_id}, {user_id}, {state}, {reason}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        channel_id_str = channel_id.decode('utf-8') if channel_id else ""
        self.local_user_observer.on_audio_subscribe_state_changed(self.local_user, channel_id_str, user_id_str, state, reason, elapsed)

    def _on_audio_publish_state_changed(self, local_user_handle, channel_id, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_audio_publish_state_changed: {local_user_handle}, {channel_id}, {state}, {reason}, {elapsed}")
        channel_id_str = channel_id.decode('utf-8') if channel_id else ""
        self.local_user_observer.on_audio_publish_state_changed(self.local_user, channel_id_str, state, reason, elapsed)

    def _on_first_remote_audio_frame(self, local_user_handle, user_id, elapsed):
        logger.debug(f"LocalUserCB _on_first_remote_audio_frame: {local_user_handle}, {user_id}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_first_remote_audio_frame(self.local_user, user_id_str, elapsed)

    def _on_first_remote_audio_decoded(self, local_user_handle, user_id, elapsed):
        logger.debug(f"LocalUserCB _on_first_remote_audio_decoded: {local_user_handle}, {user_id}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_first_remote_audio_decoded(self.local_user, user_id_str, elapsed)

    def _on_video_track_unpublished(self, local_user_handle, local_video_track_handle):
        logger.debug(f"LocalUserCB _on_video_track_unpublished: {local_user_handle}, {local_video_track_handle}")
        local_video_track = self.local_user.get_video_map(local_video_track_handle)
        # and then remove it from the local user
        self.local_user.del_video_map(local_video_track_handle)
        self.local_user_observer.on_video_track_unpublished(self.local_user, local_video_track)

    def _on_video_track_publication_failure(self, local_user_handle, local_video_track_handle, error_code):
        logger.debug(f"LocalUserCB _on_video_track_publication_failure: {local_user_handle}, {local_video_track_handle}, {error_code}")
        local_video_track = self.local_user.get_video_map(local_video_track_handle)
        self.local_user_observer.on_video_track_publication_failure(self.local_user, local_video_track, error_code)

    def _on_local_video_track_state_changed(self, local_user_handle, local_video_track_handle, state, error):
        logger.debug(f"LocalUserCB _on_local_video_track_state_changed: {local_user_handle}, {local_video_track_handle}, {state}, {error}")
        local_video_track = self.local_user.get_video_map(local_video_track_handle)
        self.local_user_observer.on_local_video_track_state_changed(self.local_user, local_video_track, state, error)

    def _on_local_video_track_statistics(self, local_user_handle, local_video_track_handle, stats):
        logger.debug(f"LocalUserCB _on_local_video_track_statistics: {local_user_handle}, {local_video_track_handle}, {stats}")
        # stats: ctypes.pointer to LocalVideoTrackStats
        local_video_track = self.local_user.get_video_map(local_video_track_handle)
        video_stats = stats.contents.get() if stats else None
        self.local_user_observer.on_local_video_track_statistics(self.local_user, local_video_track, video_stats)

    def _on_user_video_track_subscribed(self, local_user_handle, user_id, video_track_info, remote_video_track_handle):
        logger.debug(f"LocalUserCB _on_user_video_track_subscribed: {local_user_handle}, {user_id}, {remote_video_track_handle}, {video_track_info}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        # track_info = video_track_info.contents.get()
        track_info = video_track_info.contents  # videoTrackInfo
        remote_video_track = RemoteVideoTrack(remote_video_track_handle, user_id_str)
        # note: for video, one user can publish multiple video tracks, so the identifier is the remote_video_track_handle,
        # its diff to audiotrack
        self.local_user.set_remote_video_map(remote_video_track_handle, remote_video_track)
        track_info = video_track_info.contents.get()
        self.local_user_observer.on_user_video_track_subscribed(self.local_user, user_id_str, track_info, remote_video_track)

    def _on_user_video_track_state_changed(self, local_user_handle, user_id, remote_video_track_handle, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_user_video_track_state_changed: {local_user_handle}, {user_id}, {remote_video_track_handle}, {state}, {reason}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        video_track = self.local_user.get_remote_video_map(remote_video_track_handle)
        self.local_user_observer.on_user_video_track_state_changed(self.local_user, user_id_str, video_track, state, reason, elapsed)

    def _on_remote_video_track_statistics(self, local_user_handle, remote_video_track_handle, stats_ptr):
        logger.debug(f"LocalUserCB _on_remote_video_track_statistics: {local_user_handle}, {remote_video_track_handle}, {stats_ptr}")
        remote_stats = stats_ptr.contents.get() if stats_ptr else None
        video_track = self.local_user.get_remote_video_map(remote_video_track_handle)
        self.local_user_observer.on_remote_video_track_statistics(self.local_user, video_track, remote_stats)

    def _on_audio_volume_indication(self, local_user_handle, audio_volume_info_ptr, speaker_number, total_volume):
        logger.debug(f"LocalUserCB _on_audio_volume_indication: {local_user_handle}, {audio_volume_info_ptr}, {speaker_number}, {total_volume}")
         
        # enum 
        audio_volume_info_list = []
        for i in range(speaker_number):
             speaker_info = audio_volume_info_ptr[i]
             audio_volume_info = audio_volume_info_ptr[i].get()
             audio_volume_info_list.append(audio_volume_info)
        self.local_user_observer.on_audio_volume_indication(self.local_user, audio_volume_info_list, speaker_number, total_volume)

    def _on_active_speaker(self, local_user_handle, user_id):
        logger.debug(f"LocalUserCB _on_active_speaker: {local_user_handle}, {user_id}")
        user_id_str = user_id.decode('utf-8')
        self.local_user_observer.on_active_speaker(self.local_user, user_id_str)

    def _on_remote_video_stream_info_updated(self, local_user_handle, remote_video_stream_info_ptr):
        logger.debug(f"LocalUserCB _on_remote_video_stream_info_updated: {local_user_handle}, {remote_video_stream_info_ptr}")
        video_stream_info = remote_video_stream_info_ptr.contents
        self.local_user_observer.on_remote_video_stream_info_updated(self.local_user, video_stream_info)

    def _on_video_subscribe_state_changed(self, local_user_handle, channel_id, user_id, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_video_subscribe_state_changed: {local_user_handle}, {channel_id}, {user_id}, {state}, {reason}, {elapsed}")
        user_id_str = user_id.decode('utf-8')
        channel_id_str = channel_id.decode('utf-8')
        self.local_user_observer.on_video_subscribe_state_changed(self.local_user, channel_id_str, user_id_str, state, reason, elapsed)

    def _on_video_publish_state_changed(self, local_user_handle, channel_id, state, reason, elapsed):
        logger.debug(f"LocalUserCB _on_video_publish_state_changed: {local_user_handle}, {channel_id}, {state}, {reason}, {elapsed}")
        channel_id_str = channel_id.decode('utf-8')
        self.local_user_observer.on_video_publish_state_changed(self.local_user, channel_id_str, state, reason, elapsed)

    def _on_first_remote_video_frame(self, local_user_handle, user_id, width, height, elapsed):
        logger.debug(f"LocalUserCB _on_first_remote_video_frame: {local_user_handle}, {user_id}, {width}, {height}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_first_remote_video_frame(self.local_user, user_id_str, width, height, elapsed)

    def _on_first_remote_video_decoded(self, local_user_handle, user_id, width, height, elapsed):
        logger.debug(f"LocalUserCB _on_first_remote_video_decoded: {local_user_handle}, {user_id}, {width}, {height}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_first_remote_video_decoded(self.local_user, user_id_str, width, height, elapsed)

    def _on_first_remote_video_frame_rendered(self, local_user_handle, user_id, width, height, elapsed):
        logger.debug(f"LocalUserCB _on_first_remote_video_frame_rendered: {local_user_handle}, {user_id}, {width}, {height}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_first_remote_video_frame_rendered(self.local_user, user_id_str, width, height, elapsed)

    def _on_video_size_changed(self, local_user_handle, user_id, width, height, elapsed):
        logger.debug(f"LocalUserCB _on_video_size_changed: {local_user_handle}, {user_id}, {width}, {height}, {elapsed}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_video_size_changed(self.local_user, user_id_str, width, height, elapsed)

    def _on_user_info_updated(self, local_user_handle, user_id, msg, val):
        logger.debug(f"LocalUserCB _on_user_info_updated: {local_user_handle}, {user_id}, {msg}, {val}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_user_info_updated(self.local_user, user_id_str, msg, val)

    def _on_intra_request_received(self, local_user_handle):
        logger.debug(f"LocalUserCB _on_intra_request_received: {local_user_handle}")
        self.local_user_observer.on_intra_request_received(self.local_user)

    def _on_remote_subscribe_fallback_to_audio_only(self, local_user_handle, user_id, is_fallback):
        logger.debug(f"LocalUserCB _on_remote_subscribe_fallback_to_audio_only: {local_user_handle}, {user_id}, {is_fallback}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_remote_subscribe_fallback_to_audio_only(self.local_user, user_id_str, is_fallback)

    def _on_stream_message(self, local_user_handle, user_id, stream_id, data, size):
        logger.debug(f"LocalUserCB _on_stream_message: {local_user_handle}, {user_id}, {stream_id}, {data}, {size}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        bytes_from_c = ctypes.string_at(data, size)
        #data_byte_array = bytearray(bytes_from_c).decode()
        # note: do not use date_byte_array.decode()  for the stream msg is binary data, not limited to only text
        self.local_user_observer.on_stream_message(self.local_user, user_id_str, stream_id, bytes_from_c, size)

    def _on_user_state_changed(self, local_user_handle, user_id, state):
        logger.debug(f"LocalUserCB _on_user_state_changed: {local_user_handle}, {user_id}, {state}")
        user_id_str = user_id.decode('utf-8') if user_id else ""
        self.local_user_observer.on_user_state_changed(self.local_user, user_id_str, state)
    def _on_audio_meta_data_received(self, local_user_handle, user_id, audio_meta_data, size):
        user_id_str = user_id.decode('utf-8') if user_id else ""
        bytes_from_c = bytearray(ctypes.string_at(audio_meta_data, size))
        
        self.local_user_observer.on_audio_meta_data_received(self.local_user, user_id_str, bytes_from_c)

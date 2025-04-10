"""
#param 
# agora_local_user: LocalUser
# agora_local_audio_track: LocalAudioTrack
# error: int
# state: int
# agora_remote_audio_track: RemoteAudioTrack
"""
from agora.rtc.agora_base import *


class IRTCLocalUserObserver():

    def on_audio_track_publish_success(self, agora_local_user, agora_local_audio_track):
        pass

    def on_audio_track_publish_start(self, agora_local_user, agora_local_audio_track):
        pass

    def on_audio_track_unpublished(self, agora_local_user, agora_local_audio_track):
        pass

    def on_audio_track_publication_failure(self, agora_local_user, agora_local_audio_track, error):
        pass

    def on_local_audio_track_state_changed(self, agora_local_user, agora_local_audio_track, state, error):
        pass

    def on_local_audio_track_statistics(self, agora_local_user, stats:LocalAudioTrackStats):
        pass

    def on_remote_audio_track_statistics(self, agora_local_user, agora_remote_audio_track, stats:RemoteAudioTrackStats):
        pass

    def on_user_audio_track_subscribed(self, agora_local_user, user_id, agora_remote_audio_track):
        pass

    def on_user_audio_track_state_changed(self, agora_local_user, user_id, agora_remote_audio_track, state, reason, elapsed):
        pass

    def on_audio_subscribe_state_changed(self, agora_local_user, channel, user_id, old_state, new_state, elapse_since_last_state):
        pass

    def on_audio_publish_state_changed(self, agora_local_user, channel, old_state, new_state, elapse_since_last_state):
        pass

    def on_first_remote_audio_frame(self, agora_local_user, user_id, elapsed):
        pass

    def on_first_remote_audio_decoded(self, agora_local_user, user_id, elapsed):
        pass

    def on_video_track_publish_success(self, agora_local_user, agora_local_video_track):
        pass

    def on_video_track_publish_start(self, agora_local_user, agora_local_video_track):
        pass

    def on_video_track_unpublished(self, agora_local_user, agora_local_video_track):
        pass

    def on_video_track_publication_failure(self, agora_local_user, agora_local_video_track, error):
        pass

    def on_local_video_track_state_changed(self, agora_local_user, agora_local_video_track, state, error):
        pass

    def on_local_video_track_statistics(self, agora_local_user, agora_local_video_track, stats:LocalVideoTrackStats):
        pass

    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        pass

    def on_user_video_track_state_changed(self, agora_local_user, user_id, agora_remote_video_track, state, reason, elapsed):
        pass

    def on_remote_video_track_statistics(self, agora_local_user, agora_remote_video_track, stats:RemoteVideoTrackStats):
        pass

    def on_audio_volume_indication(self, agora_local_user, speakers_list, speaker_number, total_volume):
        pass

    def on_active_speaker(self, agora_local_user, userId):
        pass

    def on_remote_video_stream_info_updated(self, agora_local_user, info):
        pass

    def on_video_subscribe_state_changed(self, agora_local_user, channel, user_id, old_state, new_state, elapse_since_last_state):
        pass

    def on_video_publish_state_changed(self, agora_local_user, channel, old_state, new_state, elapse_since_last_state):
        pass

    def on_first_remote_video_frame(self, agora_local_user, user_id, width, height, elapsed):
        pass

    def on_first_remote_video_decoded(self, agora_local_user, user_id, width, height, elapsed):
        pass

    def on_first_remote_video_frame_rendered(self, agora_local_user, user_id, width, height, elapsed):
        pass

    def on_video_size_changed(self, agora_local_user, user_id, width, height, rotation):
        pass

    def on_user_info_updated(self, agora_local_user, user_id, msg, val):
        pass

    def on_intra_request_received(self, agora_local_user):
        pass

    def on_remote_subscribe_fallback_to_audio_only(self, agora_local_user, user_id, is_fallback_or_recover):
        pass

    def on_stream_message(self, agora_local_user, user_id, stream_id, data, length):
        pass

    def on_user_state_changed(self, agora_local_user, user_id, state):
        pass
    # data is bytearray object, is diff to on_stream_msg which is str object
    def on_audio_meta_data_received(self, agora_local_user, user_id, data):
        pass

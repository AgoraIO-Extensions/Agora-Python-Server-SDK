#   /* return value stands for a 'bool' in C++: 1 for success, 0 for failure */
#   int (*on_record_audio_frame)(AGORA_HANDLE agora_local_user /* raw pointer */,const char* channelId, const audio_frame* frame);
#   int (*on_playback_audio_frame)(AGORA_HANDLE agora_local_user, const char* channelId, const audio_frame* frame);
#   int (*on_mixed_audio_frame)(AGORA_HANDLE agora_local_user, const char* channelId, const audio_frame* frame);
#   int (*on_ear_monitoring_audio_frame)(AGORA_HANDLE agora_local_user, const audio_frame* frame);
#   int (*on_playback_audio_frame_before_mixing)(AGORA_HANDLE agora_local_user, const char* channelId, user_id_t uid, const audio_frame* frame);
#   int (*on_get_audio_frame_position)(AGORA_HANDLE agora_local_user);
#   audio_params (*on_get_playback_audio_frame_param)(AGORA_HANDLE agora_local_user);
#   audio_params (*on_get_record_audio_frame_param)(AGORA_HANDLE agora_local_user);
#   audio_params (*on_get_mixed_audio_frame_param)(AGORA_HANDLE agora_local_user);
#   audio_params (*on_get_ear_monitoring_audio_frame_param)(AGORA_HANDLE agora_local_user);
from .agora_base import AudioFrame, AudioParams

class IAudioFrameObserver:
    #channelid: str
    #frame:AudioFrame
    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        return 1
        pass

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        return 1
        pass

    def on_mixed_audio_frame(self, agora_local_user, channelId, frame):
        return 1
        pass

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        return 1
        pass

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, frame:AudioFrame):
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        return 1
        pass

    def on_get_playback_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_record_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_mixed_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_ear_monitoring_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

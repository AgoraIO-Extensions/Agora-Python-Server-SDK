from .agora_base import AudioFrame, AudioParams


class IAudioFrameObserver:
    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        return 1

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        return 1

    def on_mixed_audio_frame(self, agora_local_user, channelId, frame):
        return 1

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        return 1

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, frame: AudioFrame, vad_result_state:int, vad_result_bytearray:bytearray):
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        return 1

    def on_get_playback_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_record_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_mixed_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

    def on_get_ear_monitoring_audio_frame_param(self, agora_local_user) -> AudioParams:
        pass

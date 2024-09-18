#!env python
import os
import datetime
from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame

source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(source_dir, 'logs', filename ,datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_folder, exist_ok=True)
class DYSAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(DYSAudioFrameObserver, self).__init__()

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     audio_params_instance = AudioParams()
    #     return audio_params_instance

    def on_record_audio_frame(self, agora_local_user ,channelId, frame):
        print("CCC on_record_audio_frame")
        return 0
    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        print("CCC on_playback_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        print("CCC on_ear_monitoring_audio_frame")
        return 0
    
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame):
        print("CCC on_playback_audio_frame_before_mixing", audio_frame.type, audio_frame.samples_per_sec, audio_frame.samples_per_channel, audio_frame.bytes_per_sample, audio_frame.channels)        
        file_path = os.path.join(log_folder, channelId + "_" + uid + '_pcm.pcm')
        with open(file_path, "ab") as f:
            f.write(audio_frame.buffer)
        return 1
    

    def on_get_audio_frame_position(self, agora_local_user):
        print("CCC on_get_audio_frame_position")
        return 0
    # def on_get_audio_frame_position(self, agora_local_user):
    #     print("CCC on_get_audio_frame_position")
    #     return 0

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_playback_audio_frame_param")
    #     return 0
    # def on_get_record_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_record_audio_frame_param")
    #     return 0
    # def on_get_mixed_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_mixed_audio_frame_param")
    #     return 0
    # def on_get_ear_monitoring_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_ear_monitoring_audio_frame_param")
    #     return 0

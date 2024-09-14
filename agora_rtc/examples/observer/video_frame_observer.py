#!env python
from agora.rtc.video_frame_observer import IVideoFrameObserver 

class DYSVideoFrameObserver(IVideoFrameObserver):
    def __init__(self):
        super(DYSVideoFrameObserver, self).__init__()

    def on_frame(self, video_frame_observer, channel_id, remote_uid, frame):
        print("DYSVideoFrameObserver on_frame:", video_frame_observer, channel_id, remote_uid, frame)
        return 0
    
    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        print("DYSVideoFrameObserver on_user_video_track_subscribed:", agora_local_user, user_id, info, agora_remote_video_track)
        return 0
    
    # def on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track:RemoteVideoTrack, video_track_info):
    #     print("DYSVideoFrameObserver _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        # agora_remote_video_track.register_video_encoded_image_receiver(video_encoded_image_receiver)


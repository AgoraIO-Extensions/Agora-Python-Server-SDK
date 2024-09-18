#!env python

import os
import datetime
from agora.rtc.video_frame_observer import IVideoFrameObserver, VideoFrame

source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(source_dir, 'logs', filename ,datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_folder, exist_ok=True)

class DYSVideoFrameObserver(IVideoFrameObserver):
    def __init__(self):
        super(DYSVideoFrameObserver, self).__init__()

    def on_frame(self, video_frame_observer, channel_id, remote_uid, frame:VideoFrame):
        print("DYSVideoFrameObserver on_frame:", video_frame_observer, channel_id, remote_uid, frame.width, frame.height, frame.y_stride, frame.u_stride, frame.v_stride, len(frame.y_buffer), len(frame.u_buffer), len(frame.v_buffer))
        file_path = os.path.join(log_folder, channel_id + "_" + remote_uid + '.yuv')
        y_size = frame.y_stride * frame.height
        uv_size = (frame.u_stride * frame.height // 2) 
        
        print("DYSVideoFrameObserver on_frame:", y_size, uv_size, len(frame.y_buffer), len(frame.u_buffer), len(frame.v_buffer))
        with open(file_path, 'ab') as f:
            f.write(frame.y_buffer[:y_size])
            f.write(frame.u_buffer[:uv_size])
            f.write(frame.v_buffer[:uv_size])            
        return 1
    
    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        print("DYSVideoFrameObserver on_user_video_track_subscribed:", agora_local_user, user_id, info, agora_remote_video_track)
        return 0
    
    # def on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track:RemoteVideoTrack, video_track_info):
    #     print("DYSVideoFrameObserver _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        # agora_remote_video_track.register_video_encoded_image_receiver(video_encoded_image_receiver)


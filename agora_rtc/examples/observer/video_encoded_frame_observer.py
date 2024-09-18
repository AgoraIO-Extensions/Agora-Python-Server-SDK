#!env python

from agora.rtc.video_encoded_frame_observer import IVideoEncodedFrameObserver


# IVideoEncodedFrameObserver
class DYSVideoEncodedFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self):
        super(DYSVideoEncodedFrameObserver, self).__init__()

    def on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info):
        print("DYSVideoEncodedFrameObserver on_encoded_video_frame:", agora_video_encoded_frame_observer, uid, length, video_encoded_frame_info.codec_type, video_encoded_frame_info.width, video_encoded_frame_info.height, video_encoded_frame_info.frames_per_second, video_encoded_frame_info.frame_type, video_encoded_frame_info.rotation, video_encoded_frame_info.track_id, video_encoded_frame_info.capture_time_ms, video_encoded_frame_info.decode_time_ms, video_encoded_frame_info.uid, video_encoded_frame_info.stream_type)
        return 1
    

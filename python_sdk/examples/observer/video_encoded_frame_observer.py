#!env python

from agora_service.video_encoded_image_receiver import IVideoEncodedImageReceiver
from agora_service.video_encoded_frame_observer import IVideoEncodedFrameObserver


# IVideoEncodedFrameObserver
class DYSVideoEncodedFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self):
        super(DYSVideoEncodedFrameObserver, self).__init__()

    def on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info):
        print("DYSVideoEncodedFrameObserver on_encoded_video_frame:", agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info)
        return 1
    
class DYSVideoEncodedImageReceiver(IVideoEncodedImageReceiver):
    def __init__(self):
        super(DYSVideoEncodedImageReceiver, self).__init__()

    def on_encoded_video_image_received(self, agora_handle, image_buffer, length, info):
        print("DYSVideoEncodedImageReceiver on_encoded_video_image_received:", agora_handle, image_buffer, length, info)
        return 0


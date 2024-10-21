#!env python

from agora.rtc.video_encoded_frame_observer import IVideoEncodedFrameObserver
import os
import datetime
import logging
logger = logging.getLogger(__name__)


source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(source_dir, 'logs', filename, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_folder, exist_ok=True)


# IVideoEncodedFrameObserver
class ExampleVideoEncodedFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self, save_to_disk=0):
        super(ExampleVideoEncodedFrameObserver, self).__init__()
        self._save_to_disk = save_to_disk

    def on_encoded_video_frame(self, uid, image_buffer, length, video_encoded_frame_info):
        logger.info(f"on_encoded_video_frame, uid={uid}, length={length}, codec_type={video_encoded_frame_info.codec_type}, width={video_encoded_frame_info.width}, height={video_encoded_frame_info.height}, frames_per_second={video_encoded_frame_info.frames_per_second}, frame_type={video_encoded_frame_info.frame_type}, rotation={video_encoded_frame_info.rotation}, track_id={video_encoded_frame_info.track_id}, capture_time_ms={video_encoded_frame_info.capture_time_ms}, decode_time_ms={video_encoded_frame_info.decode_time_ms}, uid={video_encoded_frame_info.uid}, stream_type={video_encoded_frame_info.stream_type}")
        if self._save_to_disk:
            file_path = os.path.join(log_folder, str(uid) + '.h264')
            with open(file_path, 'ab') as f:
                f.write(image_buffer[:length])
        return 1

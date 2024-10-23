#!env python

import os
import datetime
from agora.rtc.video_frame_observer import IVideoFrameObserver, VideoFrame
import logging
logger = logging.getLogger(__name__)

source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(source_dir, 'logs', filename, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_folder, exist_ok=True)


class ExampleVideoFrameObserver(IVideoFrameObserver):
    def __init__(self, save_to_disk=0):
        super(ExampleVideoFrameObserver, self).__init__()
        self._save_to_disk = save_to_disk

    def on_frame(self, channel_id, remote_uid, frame: VideoFrame):
        # logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid}, width={frame.width}, height={frame.height}, y_stride={frame.y_stride}, u_stride={frame.u_stride}, v_stride={frame.v_stride}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")

        logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid},len_alpha_buffer={len(frame.alpha_buffer) if frame.alpha_buffer else 0}")

        if self._save_to_disk:
            file_path = os.path.join(log_folder, channel_id + "_" + remote_uid + '.yuv')
            y_size = frame.y_stride * frame.height
            uv_size = (frame.u_stride * frame.height // 2)
            # logger.info(f"on_frame, file_path={file_path}, y_size={y_size}, uv_size={uv_size}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")
            with open(file_path, 'ab') as f:
                f.write(frame.y_buffer[:y_size])
                f.write(frame.u_buffer[:uv_size])
                f.write(frame.v_buffer[:uv_size])
        return 1

    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        logger.info(f"on_user_video_track_subscribed, agora_local_user={agora_local_user}, user_id={user_id}, info={info}, agora_remote_video_track={agora_remote_video_track}")
        return 0

    # def on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track:RemoteVideoTrack, video_track_info):
        # logger.info("ExampleVideoFrameObserver _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        # agora_remote_video_track.register_video_encoded_image_receiver(video_encoded_image_receiver)

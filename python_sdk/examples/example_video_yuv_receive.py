#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from observer.local_user_observer import DYSLocalUserObserver
from observer.video_frame_observer import DYSVideoFrameObserver

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig

# 通过传参将参数传进来
#python python_sdk/examples/example_video_yuv_receive.py --token=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)



config = AgoraServiceConfig()
config.enable_audio_processor = 0
config.enable_audio_device = 0
config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)

con_config = RTCConnConfig(
    auto_subscribe_audio=0,
    auto_subscribe_video=1,
    client_role_type=1,
    channel_profile=1,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

media_node_factory = agora_service.create_media_node_factory()
video_sender = media_node_factory.create_video_frame_sender()
video_track = agora_service.create_custom_video_track_frame(video_sender)
local_user = connection.get_local_user()

# video_sender = connection.GetVideoSender()
video_frame_observer = DYSVideoFrameObserver()
local_user.register_video_frame_observer(video_frame_observer)

video_track.set_enabled(1)

time.sleep(100)

video_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
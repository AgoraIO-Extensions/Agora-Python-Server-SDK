#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
from observer.video_encoded_frame_observer import ExampleVideoEncodedFrameObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, SenderOptions
from agora.rtc.agora_base import VideoSubscriptionOptions, VIDEO_STREAM_TYPE
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_video_encoded_receive.py --appId=xxx --channelId=xxx
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

config = AgoraServiceConfig()
config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)

con_config = RTCConnConfig(
    auto_subscribe_video=1,
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = ExampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

media_node_factory = agora_service.create_media_node_factory()
video_sender = media_node_factory.create_video_encoded_image_sender()
sender_options = SenderOptions(0, 2, 640)
video_track = agora_service.create_custom_video_track_encoded(video_sender, sender_options)

# video_track.register_video_encoded_image_receiver(video_sender)

local_user = connection.get_local_user()
local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
localuser_observer = ExampleLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

video_subscription_options = VideoSubscriptionOptions(
            type = VIDEO_STREAM_TYPE.VIDEO_STREAM_HIGH,
            encodedFrameOnly = 1
)
local_user.subscribe_all_video(video_subscription_options)

# video_sender = connection.GetVideoSender()
# video_frame_observer = ExampleVideoFrameObserver()
# video_encoded_image_receiver = ExampleVideoEncodedImageReceiver()
video_encoded_frame_observer = ExampleVideoEncodedFrameObserver()
local_user.register_video_encoded_frame_observer(video_encoded_frame_observer)

video_track.set_enabled(1)
local_user.publish_video(video_track)

# video_sender.Start()

# sendinterval = 1/30
# Pacer = Pacer(sendinterval)

# width = 416
# height = 240

# def send_test():
#     count = 0
#     yuv_len = int(width*height*3/2)
#     frame_buf = bytearray(yuv_len)            
#     with open(yuv_file_path, "rb") as file:
#         while True:            
#             success = file.readinto(frame_buf)
#             if not success:
#                 break
#             frame = ExternalVideoFrame()
#             frame.buffer = frame_buf
#             frame.type = 1
#             frame.format = 1
#             frame.stride = width
#             frame.height = height
#             frame.timestamp = 0
#             ret = video_sender.send_video_framee(frame)        
#             count += 1
#             Pacer.pace()

# for i in range(1):
#     send_test()

time.sleep(200)
local_user.unpublish_video(video_track)
video_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")
agora_service.release()
logger.info("end")
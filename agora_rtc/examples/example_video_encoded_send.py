#coding=utf-8
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from common.pacer import Pacer
from observer.connection_observer import DYSConnectionObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, SenderOptions
from agora.rtc.video_frame_sender import EncodedVideoFrameInfo
from agora.rtc.agora_base import *
import av

# run this example
# python agora_rtc/examples/example_video_encoded_send.py --appId=xxx --channelId=xxx --userId=xxx --videoFile=./test_data/send_video.h264
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

config = AgoraServiceConfig()
config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])

agora_service = AgoraService()
agora_service.initialize(config)

con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

media_node_factory = agora_service.create_media_node_factory()
video_sender = media_node_factory.create_video_encoded_image_sender()
sender_options = SenderOptions(0, 2, 640)
video_track = agora_service.create_custom_video_track_encoded(video_sender, sender_options)
local_user = connection.get_local_user()

video_track.set_enabled(1)
local_user.publish_video(video_track)

def read_and_send_packets(h264_file):
    sendinterval = 1/25
    pacer = Pacer(sendinterval)
    count = 0
    width = 352
    height = 288
    container = av.open(h264_file)
    for stream in container.streams:
        if stream.type == 'video':
            width = stream.width
            height = stream.height
            print(f"Video stream: width = {width}, height = {height}")
            break
    for packet in container.demux():
        if packet.stream.type == 'video':
            print(f"Read packet with size {packet.size} bytes, PTS {packet.pts}")
            is_keyframe = packet.is_keyframe
            if is_keyframe:
                print(f"Keyframe packet with size {packet.size} bytes, PTS {packet.pts}")
            else:
                print(f"Non-keyframe packet with size {packet.size} bytes, PTS {packet.pts}")

            encoded_video_frame_info = EncodedVideoFrameInfo()
            encoded_video_frame_info.codec_type = 2            
            encoded_video_frame_info.width = width
            encoded_video_frame_info.height = height
            encoded_video_frame_info.frames_per_second = 25                        
            if is_keyframe:
                encoded_video_frame_info.frame_type = 3
            else:
                encoded_video_frame_info.frame_type = 4        
            ret = video_sender.send_encoded_video_image(packet.buffer_ptr, packet.buffer_size ,encoded_video_frame_info)        
            count += 1
            print("count,ret=",count, ret)
            pacer.pace_interval(1/30)

for i in range(10):
    read_and_send_packets(sample_options.video_file)

# time.sleep(2)
local_user.unpublish_video(video_track)
video_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
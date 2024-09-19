#coding=utf-8

import time
import os
import threading
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from observer.local_user_observer import DYSLocalUserObserver
from observer.video_frame_observer import DYSVideoFrameObserver

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.agora_base import *

# run this example
# python agora_rtc/examples/example_video_yuv_receive.py --appId=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.enable_video = 1
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)


def create_conn_and_recv(channel_id, uid = 0):
        
    con_config = RTCConnConfig(
        auto_subscribe_video=1,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = DYSConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

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


threads = []
for i in range(int(sample_options.connection_number)):
    channel_id = sample_options.channel_id + str(i+1)
    print("channel_id:", channel_id)
    thread = threading.Thread(target=create_conn_and_recv, args=(channel_id, sample_options.user_id))
    thread.start()
    threads.append(thread)

    
for t in threads:
    t.join()


agora_service.release()
print("end")
#!env python

#coding=utf-8

import time
import os
import sys
import threading
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *
from observer.video_frame_observer import DYSVideoFrameObserver

# run this example
# python agora_rtc/examples/example_audio_pcm_receive.py --appId=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.enable_video = 1
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)

def create_conn_and_recv(channel_id, uid = 0):
    #---------------2. Create Connection
    con_config = RTCConnConfig(
        auto_subscribe_video=1,
        auto_subscribe_audio=1,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = DYSConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()
    audio_sender = media_node_factory.create_audio_encoded_frame_sender()
    audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 0)

    local_user = connection.get_local_user()
    local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    localuser_observer = DYSLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)
    audio_frame_observer = DYSAudioFrameObserver()
    local_user.register_audio_frame_observer(audio_frame_observer)
    # local_user.subscribe_audio("3")
    # local_user.subscribe_all_audio()


    video_frame_observer = DYSVideoFrameObserver()
    local_user.register_video_frame_observer(video_frame_observer)
    # local_user.subscribe_all_video()


    #---------------4. Send Media Stream
    # audio_track.set_enabled(1)
    # local_user.publish_audio(audio_track)

    time.sleep(100)
    # local_user.unpublish_audio(audio_track)
    # audio_track.set_enabled(0)
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
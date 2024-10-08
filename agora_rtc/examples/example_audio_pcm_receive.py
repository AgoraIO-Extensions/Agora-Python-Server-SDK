#!env python

#coding=utf-8
import asyncio
import signal
import time
import os
import threading
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import SampleConnectionObserver
from observer.audio_frame_observer import SampleAudioFrameObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *

# run this example
# python agora_rtc/examples/example_audio_pcm_receive.py --appId=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

_exit = threading.Event()

def create_conn_and_recv(agora_service:AgoraService, channel_id, uid = 0):
    #---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = SampleConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()
    audio_sender = media_node_factory.create_audio_encoded_frame_sender()
    audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 0)

    local_user = connection.get_local_user()
    local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
    local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    localuser_observer = SampleLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)
    audio_frame_observer = SampleAudioFrameObserver()
    local_user.register_audio_frame_observer(audio_frame_observer)
    # local_user.subscribe_audio("3")
    local_user.subscribe_all_audio()
    _exit.wait()
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    logger.info("connection.release")

def handle_signal(signum, frame):
    _exit.set()

def run_example():

    signal.signal(signal.SIGINT, handle_signal)  # Forward SIGINT
    signal.signal(signal.SIGTERM, handle_signal)  # Forward SIGTERM

    #---------------1. Init SDK
    config = AgoraServiceConfig()
    config.appid = sample_options.app_id
    config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])
    agora_service = AgoraService()
    agora_service.initialize(config)

    threads = []
    for i in range(int(sample_options.connection_number)):
        channel_id = sample_options.channel_id + str(i+1)
        logger.info(f"channel_id: {channel_id}")
        thread = threading.Thread(target=create_conn_and_recv, args=(agora_service, channel_id, sample_options.user_id))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    agora_service.release()
    logger.info("agora_service.release")

if __name__ == "__main__":
    run_example()
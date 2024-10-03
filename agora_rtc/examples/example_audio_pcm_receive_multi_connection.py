#!env python

#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import SampleConnectionObserver
from observer.audio_frame_observer import SampleAudioFrameObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_pcm_receive_multi_connection.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.aac
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])

agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection

con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = SampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, "dys_channel_test1", sample_options.user_id)

connection2 = agora_service.create_rtc_connection(con_config)
conn_observer2 = SampleConnectionObserver()
connection2.register_observer(conn_observer2)
connection2.connect(sample_options.token, "dys_channel_test2", sample_options.user_id)


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
local_user.subscribe_all_audio()


audio_sender2 = media_node_factory.create_audio_encoded_frame_sender()
audio_track2 = agora_service.create_custom_audio_track_encoded(audio_sender2, 0)
local_user2 = connection2.get_local_user()
local_user2.set_playback_audio_frame_before_mixing_parameters(1, 16000)
localuser_observer2 = SampleLocalUserObserver()
local_user2.register_local_user_observer(localuser_observer2)
audio_frame_observer2 = SampleAudioFrameObserver()
local_user2.register_audio_frame_observer(audio_frame_observer2)
local_user2.subscribe_all_audio()

#---------------4. Send Media Stream
# audio_track.set_enabled(1)
# local_user.publish_audio(audio_track)

time.sleep(100)
# local_user.unpublish_audio(audio_track)
# audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()

connection2.unregister_observer()
connection2.disconnect()
connection2.release()

logger.info("release")
agora_service.release()
logger.info("end")
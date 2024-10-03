#!env python

#coding=utf-8

import time
import os
import sys
import threading
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import SampleConnectionObserver
# from observer.audio_frame_observer import SampleAudioFrameObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *
from common.audio_consumer import AudioStreamConsumer
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame

# run this example
# python agora_rtc/examples/example_audio_pcm_receive.py --appId=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")




from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame
import logging
logger = logging.getLogger(__name__)

class SampleAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(SampleAudioFrameObserver, self).__init__()

    def on_record_audio_frame(self, agora_local_user ,channelId, frame):        
        logger.info(f"on_record_audio_frame")
        return 0
    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):        
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0
    
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame):
        logger.info(f"on_playback_audio_frame_before_mixing:{threading.current_thread().ident}, {len(audio_frame.buffer)}")
        audio_stream_consumer.push_pcm_data(audio_frame.buffer)



        # frame = PcmAudioFrame()
        # frame.data = audio_frame.buffer
        # frame.timestamp = 0
        # frame.samples_per_channel = 160
        # frame.bytes_per_sample = 2
        # frame.number_of_channels = 1
        # frame.sample_rate = 16000
        # logger.info(f"send_audio_pcm_data start")
        # ret = pcm_data_sender.send_audio_pcm_data(frame)
        # logger.info(f"send_audio_pcm_data start-{ret}")
        return 1
    

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")        
        return 0




#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)

# def create_conn_and_recv(channel_id, uid = 0):
    #---------------2. Create Connection
con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

media_node_factory = agora_service.create_media_node_factory()

connection = agora_service.create_rtc_connection(con_config)
conn_observer = SampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

local_user = connection.get_local_user()
local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
localuser_observer = SampleLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_frame_observer = SampleAudioFrameObserver()
local_user.register_audio_frame_observer(audio_frame_observer)
local_user.subscribe_all_audio()



send_channel = sample_options.channel_id + "_1"

connection2 = agora_service.create_rtc_connection(con_config)
conn_observer2 = SampleConnectionObserver()
connection2.register_observer(conn_observer2)
connection2.connect(sample_options.token, send_channel, sample_options.user_id)

local_user2 = connection2.get_local_user()

pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
audio_track.set_enabled(1)
local_user2.publish_audio(audio_track)
audio_stream_consumer = AudioStreamConsumer(pcm_data_sender)


time.sleep(100)
# local_user.unpublish_audio(audio_track)
# audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")



# threads = []
# for i in range(int(sample_options.connection_number)):
#     channel_id = sample_options.channel_id + str(i+1)
#     logger.info(f"channel_id: {channel_id}")
#     thread = threading.Thread(target=create_conn_and_recv, args=(channel_id, sample_options.user_id))
#     thread.start()
#     threads.append(thread)

# for t in threads:
#     t.join()

agora_service.release()
logger.info("end")
#!env python

#coding=utf-8

import time
import os
import av
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from common.pacer import Pacer
from observer.connection_observer import SampleConnectionObserver
from observer.local_user_observer import SampleLocalUserObserver

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_encoded_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.aac
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
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
audio_sender = media_node_factory.create_audio_encoded_frame_sender()
if not audio_sender:
    logger.error("create audio sender failed")
    exit(1)
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 1)
if not audio_track:
    logger.error("create audio track failed")
    exit(1)

local_user = connection.get_local_user()
localuser_observer = SampleLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
# audio_track.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track.set_enabled(1)
local_user.publish_audio(audio_track)

def test3(aac_file):
    sendinterval = 0.1
    pacer = Pacer(sendinterval)
    container = av.open(aac_file)
    sample_rate = 48000
    channels = 1
    for stream in container.streams:
        if stream.type == 'audio':
            sample_rate = stream.sample_rate
            channels = stream.channels            
            logger.info(f"Audio stream: sample rate = {sample_rate}, channels = {channels}")
            break

    for packet in container.demux():
        if packet.stream.type == 'audio':
            logger.info(f"Read audio packet with size {packet.size} bytes, PTS {packet.pts}, DTS {packet.dts}")

            frame = EncodedAudioFrame()
            frame.speech = 0
            frame.codec = AudioCodecType.AUDIO_CODEC_AACLC #https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/structagora_1_1rtc_1_1_encoded_audio_frame_info.html
            frame.sample_rate = sample_rate
            frame.samples_per_channel = 1024
            frame.number_of_channels = channels
            frame.send_even_if_empty = 1
            ret = audio_sender.send_encoded_audio_frame(packet.buffer_ptr, packet.size,frame)
            time_base = packet.stream.time_base
            duration_in_seconds = packet.duration * time_base
            pacer.pace_interval(duration_in_seconds)

for i in range(1):
    test3(sample_options.audio_file)

# time.sleep(100)
local_user.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")
agora_service.release()
logger.info("end")
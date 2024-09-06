#!env python

#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.pacer import Pacer
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.audio_pcm_data_sender import PcmAudioFrame

# 通过传参将参数传进来
#python python_sdk/examples/example_audio_pcm_send.py --token=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    auto_subscribe_audio=1,
    auto_subscribe_video=0,
    client_role_type=1,
    channel_profile=1,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_frame_observer = DYSAudioFrameObserver()
local_user.register_audio_frame_observer(audio_frame_observer)

audio_track.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track.set_enabled(1)
local_user.publish_audio(audio_track)

sendinterval = 0.1
Pacer = Pacer(sendinterval)
count = 0
packnum = int((sendinterval*1000)/10)

def send_test():
    with open(sample_options.audio_file, "rb") as file:
        global count
        global packnum
        while True:
            if count < 10:
                packnum = 100
            frame_buf = bytearray(320*packnum)            
            success = file.readinto(frame_buf)
            if not success:
                break
            frame = PcmAudioFrame()
            frame.data = frame_buf
            frame.timestamp = 0
            frame.samples_per_channel = 160*packnum
            frame.bytes_per_sample = 2
            frame.number_of_channels = 1
            frame.sample_rate = 16000

            ret = pcm_data_sender.send_audio_pcm_data(frame)
            count += 1
            print("count,ret=",count, ret)
            Pacer.pace()

for i in range(100):
    send_test()

#---------------5. Stop Media Sender And Release
time.sleep(10)
local_user.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
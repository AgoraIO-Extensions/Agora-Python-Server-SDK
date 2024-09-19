#!env python

import time
import os
import threading

from common.path_utils import get_log_path_with_filename 
from common.pacer import Pacer
from common.parse_args import parse_args_example
from common.audio_consumer import AudioStreamConsumer
from observer.connection_observer import DYSConnectionObserver
# from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame
from agora.rtc.agora_base import *

# run this example
# python agora_rtc/examples/example_audio_pcm_send.py --appId=xxx --channelId=xxx --userId=xxx --connectionNumber=1 --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])

agora_service = AgoraService()
agora_service.initialize(config)

def create_conn_and_send(channel_id, uid = 0):

    #---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = DYSConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()
    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)

    local_user = connection.get_local_user()
    localuser_observer = DYSLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)
    # audio_frame_observer = DYSAudioFrameObserver()
    # local_user.register_audio_frame_observer(audio_frame_observer)

    # audio_track.set_max_buffer_audio_frame_number(320*2000)

    #---------------4. Send Media Stream
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)
    audio_stream_consumer = AudioStreamConsumer(pcm_data_sender)

    sendinterval = 0.1
    pacer = Pacer(sendinterval)

    # def read_and_send_packets():
    #     count = 0
    #     with open(sample_options.audio_file, "rb") as file:        
    #         while True:
    #             send_size = int(sample_options.sample_rate*sample_options.num_of_channels*sendinterval*2)
    #             frame_buf = bytearray(send_size)            
    #             success = file.readinto(frame_buf)
    #             if not success:
    #                 break
    #             frame = PcmAudioFrame()
    #             frame.data = frame_buf
    #             frame.timestamp = 0
    #             frame.samples_per_channel = int(sample_options.sample_rate * sendinterval)
    #             frame.bytes_per_sample = 2
    #             frame.number_of_channels = sample_options.num_of_channels
    #             frame.sample_rate = sample_options.sample_rate
    #             ret = pcm_data_sender.send_audio_pcm_data(frame)
    #             count += 1
    #             print("count,ret=",count, ret)
    #             pacer.pace()

    def read_and_send_packets():
        with open(sample_options.audio_file, "rb") as file:        
            while True:
                send_size = int(sample_options.sample_rate*sample_options.num_of_channels*sendinterval*20)
                frame_buf = bytearray(send_size)            
                success = file.readinto(frame_buf)
                if not success:
                    break                
                audio_stream_consumer.push_pcm_data(frame_buf)
                pacer.pace()
                print("push audio data")

    for i in range(1):
        read_and_send_packets()

    #---------------5. Stop Media Sender And Release
    time.sleep(25)
    audio_stream_consumer.clear()
    audio_stream_consumer.relase()
    local_user.unpublish_audio(audio_track)
    audio_track.set_enabled(0)
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    print("connection release")


threads = []
for i in range(int(sample_options.connection_number)):
    print("channel", i)
    channel_id = sample_options.channel_id + str(i+1)

    thread = threading.Thread(target=create_conn_and_send, args=(channel_id, sample_options.user_id))
    thread.start()
    threads.append(thread)

    
for t in threads:
    t.join()


agora_service.release()
print("end")
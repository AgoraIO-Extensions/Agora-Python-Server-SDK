#!env python

#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from common.pacer import Pacer
from observer.connection_observer import DYSConnectionObserver
from observer.local_user_observer import DYSLocalUserObserver

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.audio_encoded_frame_sender import EncodedAudioFrame
from agora_service.agora_base import *

# 通过传参将参数传进来
#python python_sdk/examples/example_audio_encoded_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.aac
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

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
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
audio_sender = media_node_factory.create_audio_encoded_frame_sender()
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 1)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_track.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track.set_enabled(1)
local_user.publish_audio(audio_track)

import struct
def test2(file_path):
    SAMPLE_RATES = [
        96000, 88200, 64000, 48000, 44100, 32000,
        24000, 22050, 16000, 12000, 11025, 8000, 7350
    ]
    CHANNEL_CONFIGS = {
        0: "Defined in AOT Specifc Config",
        1: "Mono",
        2: "Stereo",
        3: "3 channels",
        4: "4 channels",
        5: "5 channels",
        6: "5.1 channels",
        7: "7.1 channels"
    }

    sendinterval = 0.1
    pacer = Pacer(sendinterval)
    with open(file_path, "rb") as f:
        while True:
            adts_header = f.read(7)
            if len(adts_header) < 7:
                break  # 文件结束

            syncword = struct.unpack('>H', adts_header[:2])[0] >> 4
            if syncword != 0xFFF:
                print("Syncword not found, skipping...")
                continue

            id_ = (adts_header[1] >> 3) & 0x01
            layer = (adts_header[1] >> 1) & 0x03
            protection_absent = adts_header[1] & 0x01
            profile = (adts_header[2] >> 6) & 0x03
            sampling_frequency_index = (adts_header[2] >> 2) & 0x0F
            private_bit = (adts_header[2] >> 1) & 0x01
            channel_configuration = ((adts_header[2] & 0x01) << 2) | ((adts_header[3] >> 6) & 0x03)
            original_copy = (adts_header[3] >> 5) & 0x01
            home = (adts_header[3] >> 4) & 0x01
            frame_length = ((adts_header[3] & 0x03) << 11) | (adts_header[4] << 3) | (adts_header[5] >> 5)
            buffer_fullness = ((adts_header[5] & 0x1F) << 6) | ((adts_header[6] >> 2) & 0x3F)
            num_raw_data_blocks = adts_header[6] & 0x03

            if sampling_frequency_index < len(SAMPLE_RATES):
                sampling_rate = SAMPLE_RATES[sampling_frequency_index]
                print(f"Sampling Frequency Index: {sampling_frequency_index} -> Sampling Rate: {sampling_rate} Hz")
            else:
                print(f"Unknown Sampling Frequency Index: {sampling_frequency_index}")

            if channel_configuration in CHANNEL_CONFIGS:
                channels = CHANNEL_CONFIGS[channel_configuration]
                print(f"Channel Configuration: {channel_configuration} -> Number of Channels: {channels}")
            else:
                print(f"Unknown Channel Configuration: {channel_configuration}")


            adts_data_length = frame_length - 7

            buffer = f.read(adts_data_length)
            if len(buffer) < adts_data_length:
                print("Warning: Incomplete frame data read.")
                break

            frame = EncodedAudioFrame()
            frame.data = bytearray(buffer)

            frame.speech = 0
            frame.codec = AUDIO_CODEC_TYPE.AUDIO_CODEC_AACLC #https://doc.shengwang.cn/api-ref/rtc/windows/API/enum_audiocodectype
            frame.sample_rate = sampling_rate
            frame.samples_per_channel = 1024
            frame.number_of_channels = channel_configuration
            frame.send_even_if_empty = 1

            ret = audio_sender.send_encoded_audio_frame(frame)
            pacer.pace_interval(22.0/1000.0)

        print(f"Read {len(buffer)} bytes of data for one ADTS frame.")
        


import av

def test3(aac_file):
    sendinterval = 0.1
    pacer = Pacer(sendinterval)
        # 打开 .aac 文件
    container = av.open(aac_file)
        # 遍历所有音频流，获取音频流的元数据
    sample_rate = 48000
    channels = 1
    for stream in container.streams:
        if stream.type == 'audio':
            sample_rate = stream.sample_rate
            channels = stream.channels            
            print(f"Audio stream: sample rate = {sample_rate}, channels = {channels}")
            break


    # 遍历每个 packet
    for packet in container.demux():
        if packet.stream.type == 'audio':
            print(f"Read audio packet with size {packet.size} bytes, PTS {packet.pts}, DTS {packet.dts}")

            frame = EncodedAudioFrame()
            # frame.data = bytearray(buffer)
            # frame.buffer_ptr = packet.buffer_ptr
            # frame.buffer_size = packet.size
            frame.speech = 0
            frame.codec = AUDIO_CODEC_TYPE.AUDIO_CODEC_AACLC #https://doc.shengwang.cn/api-ref/rtc/windows/API/enum_audiocodectype
            frame.sample_rate = sample_rate
            frame.samples_per_channel = 1024
            frame.number_of_channels = channels
            frame.send_even_if_empty = 1

            ret = audio_sender.send_encoded_audio_frame(packet.buffer_ptr, packet.size,frame)

            time_base = packet.stream.time_base
            duration_in_seconds = packet.duration * time_base
            pacer.pace_interval(duration_in_seconds)
            # pacer.pace_interval(22.0/1000.0)


            # 假设 send_packet 是你定义的发送函数，可以将 packet 数据发送出去
            # send_packet(packet)


# for i in range(10):
    # test1()
    # test2(aac_file_path)

# test2(sample_options.audio_file)

test3(sample_options.audio_file)


# time.sleep(100)
local_user.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
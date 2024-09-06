#!env python

#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.pacer import Pacer
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.audio_pcm_data_sender import EncodedAudioFrame

from common.parse_args import parse_args_example, parse_args
# 通过传参将参数传进来
#python python_sdk/examples/example_audio_encoded_send.py --token=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.aac
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 0
config.enable_audio_device = 0
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
audio_sender = media_node_factory.create_audio_encoded_frame_sender()
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 1)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_frame_observer = DYSAudioFrameObserver()
local_user.register_audio_frame_observer(audio_frame_observer)

audio_track.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track.set_enabled(1)
local_user.publish_audio(audio_track)


def test1():

    sendinterval = 0.1
    pacer = Pacer(sendinterval)
    count = 0
    # packnum = int((sendinterval*1000)/10)
    packnum = 1
    with open(sample_options.audio_file, "rb") as file:

        while True:
            frame_buf = bytearray(320*packnum)            
            success = file.readinto(frame_buf)
            if not success:
                break
            frame = EncodedAudioFrame()
            frame.data = frame_buf
            frame.size = len(frame_buf)
            frame.capture_timems = 0
            frame.codec = 8
            frame.speech = 1
            frame.send_even_if_empty = 1

            frame.samples_per_channel = 1024
            frame.number_of_channels = 1
            frame.sample_rate = 16000

            ret = audio_sender.send_encoded_audio_frame(frame)
            count += 1
            print("count,ret=",count, ret)
            pacer.pace()


# import struct

# def read_aac_file(file_path):        
#     # read aac packet and get the data , size sample_rate channel_num
#     adts_header_size = 7  
#     with open(file_path, 'rb') as f:  
#         while True:  
#             adts_header = f.read(adts_header_size)  
#             if not adts_header:  
#                 break  
              
#             # 检查是否为ADTS帧  
#             if adts_header[0] == 0xFF and (adts_header[1] & 0xF6) == 0xF0:  
#                 # # 解析ADTS帧头  
#                 # # 省略了详细的位操作解析，这里只提供基本的检查  
#                 # frame_size = (header[3] << 11) | (header[4] << 3) | (header[5] >> 5)  
#                 # sampling_frequency_index = (header[2] >> 2) & 0x0F  
#                 # channel_configuration = (header[2] >> 6) & 0x03  
  
#                 # print(f"Frame size: {frame_size}")  
#                 # print(f"Sampling Frequency Index: {sampling_frequency_index}")  
#                 # print(f"Channel Configuration: {channel_configuration}")  
  
#                 # 解析同步字（syncword）和固定部分
#                 syncword = struct.unpack('>H', adts_header[:2])[0] >> 4
#                 if syncword != 0xFFF:
#                     print("Syncword not found, skipping...")
#                     continue
                
#                 # 解析ADTS头部的各个字段
#                 id_ = (adts_header[1] >> 3) & 0x01
#                 layer = (adts_header[1] >> 1) & 0x03
#                 protection_absent = adts_header[1] & 0x01
#                 profile = (adts_header[2] >> 6) & 0x03
#                 sampling_frequency_index = (adts_header[2] >> 2) & 0x0F
#                 private_bit = (adts_header[2] >> 1) & 0x01
#                 channel_configuration = ((adts_header[2] & 0x01) << 2) | ((adts_header[3] >> 6) & 0x03)
#                 original_copy = (adts_header[3] >> 5) & 0x01
#                 home = (adts_header[3] >> 4) & 0x01
#                 frame_length = ((adts_header[3] & 0x03) << 11) | (adts_header[4] << 3) | (adts_header[5] >> 5)
#                 buffer_fullness = ((adts_header[5] & 0x1F) << 6) | ((adts_header[6] >> 2) & 0x3F)
#                 num_raw_data_blocks = adts_header[6] & 0x03
                
#                 # 打印解析出的ADTS头部信息
#                 print(f"Syncword: 0x{syncword:X}")
#                 print(f"ID: {id_}")
#                 print(f"Layer: {layer}")
#                 print(f"Protection absent: {protection_absent}")
#                 print(f"Profile: {profile}")
#                 print(f"Sampling Frequency Index: {sampling_frequency_index}")
#                 print(f"Channel Configuration: {channel_configuration}")
#                 print(f"Frame Length: {frame_length}")
#                 print(f"Buffer Fullness: {buffer_fullness}")
#                 print(f"Number of Raw Data Blocks: {num_raw_data_blocks}")

#                 # 跳过剩余帧数据，移动到下一个ADTS头
#                 f.seek(frame_length - 7, 1)  # 跳过当前帧剩余部分



#                 # 跳过当前帧，继续查找下一个  
#                 f.seek(frame_size - adts_header_size, 1)  
           


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
            frame.size = adts_data_length

            frame.speech = 0
            frame.codec = 8 #https://doc.shengwang.cn/api-ref/rtc/windows/API/enum_audiocodectype
            frame.sample_rate = sampling_rate
            frame.samples_per_channel = 1024
            frame.number_of_channels = channel_configuration
            frame.send_even_if_empty = 1

            ret = audio_sender.send_encoded_audio_frame(frame)
            pacer.pace()

        print(f"Read {len(buffer)} bytes of data for one ADTS frame.")

# 使用示例
# parse_aac_and_store_data(aac_file_path)

# for i in range(10):
    # test1()
    # test2(aac_file_path)

test2(sample_options.audio_file)

# # 打印结果，显示缓冲区的数量
# print(f"Total number of ADTS frames: {len(buffers)}")
# for i, buffer in enumerate(buffers[:5], 1):  # 仅打印前5个缓冲区的大小
#     print(f"Buffer {i} size: {len(buffer)} bytes")

# read_aac_file(aac_file_path)           
#---------------5. Stop Media Sender And Release
time.sleep(100)
local_user.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
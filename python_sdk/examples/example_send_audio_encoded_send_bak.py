#!env python

#coding=utf-8

import time
import os
import sys
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(script_dir)
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.rtc_connection_observer import IRTCConnectionObserver
from agora_service.audio_pcm_data_sender import EncodedAudioFrame
from agora_service.audio_frame_observer import IAudioFrameObserver
from agora_service.local_user_observer import IRTCLocalUserObserver

class DYSConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super(DYSConnectionObserver, self).__init__()

    def on_connected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connected:", agora_rtc_conn, conn_info.channel_id, conn_info.local_user_id, conn_info.state, conn_info.id, conn_info.internal_uid, reason)

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Disconnected:", agora_rtc_conn, conn_info, reason)

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connecting:", agora_rtc_conn, conn_info, reason)

    def on_user_joined(self, agora_rtc_conn, user_id):
        print("CCC on_user_joined:", agora_rtc_conn, user_id)

class DYSLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(DYSLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        print("CCC on_stream_message:", user_id, stream_id, data, length)
        return 0

    def on_user_info_updated(self, local_user, user_id, msg, val):
        print("CCC on_user_info_updated:", user_id, msg, val)
        return 0

class DYSAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(DYSAudioFrameObserver, self).__init__()

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     audio_params_instance = AudioParams()
    #     return audio_params_instance

    def on_record_audio_frame(self, agora_local_user ,channelId, frame):
        print("CCC on_record_audio_frame")
        return 0
    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        print("CCC on_playback_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        print("CCC on_ear_monitoring_audio_frame")
        return 0
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, frame):
        print("CCC on_playback_audio_frame_before_mixing")
        return 0
    def on_get_audio_frame_position(self, agora_local_user):
        print("CCC on_get_audio_frame_position")
        return 0


#pacer class
class Pacer:
    def __init__(self,interval):
        self.last_call_time = time.time()
        self.interval = interval

    def pace(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < self.interval:
            time.sleep(self.interval - elapsed_time)
            print("sleep time:", (self.interval - elapsed_time)*1000)
        self.last_call_time = time.time()

# 通过传参将参数传进来
# 例如： python examples/example_send_pcm.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
appid = sys.argv[1]
token = sys.argv[2]
channel_id = sys.argv[3]
aac_file_path = sys.argv[4]
# check argv len
if len(sys.argv) > 5:
    uid = sys.argv[5]
else:
    uid = "0"
print("appid:", appid, "token:", token, "channel_id:", channel_id, "aac_file_path:", aac_file_path, "uid:", uid)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 0
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = appid

sdk_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
config.log_path = os.path.join(sdk_dir, 'logs/example_send_pcm', log_folder, 'agorasdk.log')

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
connection.connect(token, channel_id, uid)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
audio_sender = media_node_factory.create_audio_encoded_frame_sender()
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 0)

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

# import subprocess

# def read_aac_file(aac_file_path):
#     command = ['ffmpeg', '-i', aac_file_path, '-f', 's16le', '-ac', '1', '-ar', '16000', '-']
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
#     while True:
#         data = process.stdout.read(320)
#         if not data:
#             break
#         yield data

# aac_file_generator = read_aac_file(aac_file_path)


# import subprocess

# def read_aac_packets(aac_file):
#     # 使用FFmpeg命令读取AAC文件的packet包
#     command = [
#         'ffmpeg',
#         '-i', aac_file,
#         '-f', 'data',
#         '-'
#     ]

#     # 启动FFmpeg进程
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # 读取输出
#     output, error = process.communicate()

#     # 检查错误
#     if process.returncode != 0:
#         print("Error:", error.decode())
#         return

#     # 处理输出数据（每个packet）
#     packets = output.split(b'\n')  # 根据需要分割数据
#     for packet in packets:
#         if packet:  # 过滤掉空行
#             print(packet)

# # 示例调用
# read_aac_packets(aac_file_path)


from pydub import AudioSegment
import struct

count = 0

def send_aac_packet(packet, frame_length):    
    frame = EncodedAudioFrame()
    frame.data = bytearray(packet)
    frame.size = frame_length
    frame.capture_timems = 0
    frame.codec = 8
    frame.number_of_channels = 1
    frame.sample_rate = 48000
    # frame.sample_rate = 16000
    frame.samples_per_channel = 1024

    frame.speech = 0
    frame.send_even_if_empty = 1

    

    ret = audio_sender.send_encoded_audio_frame(frame)
    # count += 1
    print("ret=", ret)
    Pacer.pace()


# ADTS头中定义的采样率索引与实际采样率的映射关系
SAMPLE_RATE_LOOKUP = {
    0: 96000,
    1: 88200,
    2: 64000,
    3: 48000,
    4: 44100,
    5: 32000,
    6: 24000,
    7: 22050,
    8: 16000,
    9: 12000,
    10: 11025,
    11: 8000,
    12: 7350
}

def extract_aac_packets(file_path):
    # 使用pydub加载AAC文件
    # audio = AudioSegment.from_file(file_path, format="aac")
    
    try:
        audio = AudioSegment.from_file(file_path, format="aac")
        # audio = AudioSegment.from_file(file_path, format="raw")
        print("Audio data loaded successfully.")
    except Exception as e:
        print(f"Failed to load audio data: {e}")


    # 将音频数据转换为字节流
    raw_data = audio.raw_data
    
    packets = []
    sample_rate = None

    # ADTS帧的最小长度为7字节
    offset = 0
    while offset < len(raw_data) - 7:
        # 读取ADTS帧的前7字节
        adts_header = raw_data[offset:offset + 7]
        
        # 解析ADTS头部
        syncword = struct.unpack('>H', adts_header[:2])[0] >> 4
        if syncword != 0xFFF:
            # 如果syncword不匹配，跳过这个偏移
            offset += 1
            continue
        
        # 获取AAC帧长度信息，ADTS帧的第4到5字节的前13位表示AAC帧的长度
        frame_length = struct.unpack('>H', adts_header[3:5])[0] & 0x1FFF
        
        # 提取采样率索引（在ADTS头的第2字节的5-8位）
        sample_rate_index = (adts_header[2] & 0x3C) >> 2

        # 根据采样率索引获取实际采样率
        if sample_rate is None:
            sample_rate = SAMPLE_RATE_LOOKUP.get(sample_rate_index, "Unknown")


        # 获取完整的ADTS帧
        packet = raw_data[offset:offset + frame_length]
        packets.append(packet)
        
        send_aac_packet(packet, frame_length)

        # 移动偏移量到下一个ADTS帧
        offset += frame_length
    
    return packets


def get_aac_packets(file_path):
    audio = AudioSegment.from_file(file_path)
    # 这里可能没有直接获取 packet 的方法，但可以将音频转换为字节数组来模拟数据包
    byte_data = audio.raw_data
    # 根据具体需求可以进一步分割字节数组为数据包
    # 这里只是简单返回字节数组作为示例
    return byte_data

# 使用示例
# aac_packets = extract_aac_packets(aac_file_path)

def read_adts_header(file_path):  
    adts_header_size = 7  
    with open(file_path, 'rb') as f:  
        while True:  
            header = f.read(adts_header_size)  
            if not header:  
                break  

            # 检查是否为ADTS帧  
            if header[0] == 0xFF and (header[1] & 0xF6) == 0xF0:  
                # 解析ADTS帧头  
                # 省略了详细的位操作解析，这里只提供基本的检查  
                frame_size = (header[3] << 11) | (header[4] << 3) | (header[5] >> 5)  
                sampling_frequency_index = (header[2] >> 2) & 0x0F  
                channel_configuration = (header[2] >> 6) & 0x03  
  
                print(f"Frame size: {frame_size}")  
                print(f"Sampling Frequency Index: {sampling_frequency_index}")  
                print(f"Channel Configuration: {channel_configuration}")  
  
                # 提取第4和第5个字节  
                byte4 = header[3]  
                byte5 = header[4]  
                
                # 使用位操作来提取第30到31位（从byte4中）  
                # 我们先将byte4右移22位（因为我们要的是第30和31位，而byte4是从第24位开始的）  
                # 然后与0x3（即二进制的00000011）进行位与操作，以保留这两位  
                bits_30_31 = (byte4 >> 22) & 0x3  
                
                # 提取第32到41位（从byte5中）  
                # 我们先将byte5右移相应的位数（对于第32-39位，我们不需要右移，对于第40-41位，我们稍后会处理）  
                # 但为了简化，我们可以直接处理整个byte5，因为我们需要它的全部8位  
                # 对于第32-39位，我们稍后可以通过位与操作来保留  
                bits_32_39 = byte5 & 0xFF  # 实际上，这保留了byte5的所有8位，但我们稍后会用到其中的部分  
                
                # 合并这两部分（如果只需要30-41位作为一个整体数字，则这一步是必要的）  
                # 注意：因为bits_30_31只有两位，我们需要将其左移适当的位数以与bits_32_39对齐  
                # 我们只需要bits_32_39中的第32-39位，所以实际上我们不需要对bits_32_39进行额外的位移  
                # 但为了合并，我们可以创建一个只包含第32-39位的值  
                bits_32_39_only = (bits_32_39 >> 2) & 0xFF  # 这里右移2位只是为了示例，实际上我们不需要它  
                # 然后，将bits_30_31左移6位（因为32-30=2，但我们需要的是32-31+1=3的2倍，即6位）  
                # 并与bits_32_39_only进行位或操作（但在这个例子中，我们实际上不需要bits_32_39_only，因为我们用整个byte5）  
                combined_bits = (bits_30_31 << 6) | (byte5 & 0x3FF)  # 0x3FF是二进制的00001111111111，覆盖了第0-9位  
                
                # 注意：上面的combined_bits实际上包含了比我们需要的更多的位（即第30-41位加上byte5的第0-1位）  
                # 如果我们只想要第30-41位，并且不关心它们的排列方式（即，作为一个整体数字），我们可以这样做：  
                # 我们只需要确保bits_30_31在高位，byte5的相关位在低位  
                desired_bits = (bits_30_31 << 6) | ((byte5 >> 2) & 0x3FC)  # 0x3FC是二进制的0000111111100，覆盖了第2-9位  
                
                print(f"Desired bits (30-41): {desired_bits}")

                # 跳过当前帧，继续查找下一个  
                f.seek(frame_size - adts_header_size, 1)  

# 使用示例  
# read_adts_header(aac_file_path)  # 替换为你的AAC文件路径



# print(f"Extracted {len(aac_packets)} AAC packets")

# get_aac_packets(aac_file_path)


packnum = int((sendinterval*1000)/10)
with open(aac_file_path, "rb") as file:

    while True:
        if count < 10:
            packnum = 100
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
        Pacer.pace()
           
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
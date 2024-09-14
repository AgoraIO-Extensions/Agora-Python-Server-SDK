#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from common.pacer import Pacer
from observer.connection_observer import DYSConnectionObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, SenderOptions
from agora.rtc.video_frame_sender import EncodedVideoFrameInfo
from agora.rtc.agora_base import *

# 通过传参将参数传进来
#python agora_rtc/examples/example_video_encoded_send.py --appId=xxx --channelId=xxx --userId=xxx --videoFile=./test_data/send_video.h264
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

config = AgoraServiceConfig()
config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])

agora_service = AgoraService()
agora_service.initialize(config)

con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

media_node_factory = agora_service.create_media_node_factory()
video_sender = media_node_factory.create_video_encoded_image_sender()
sender_options = SenderOptions(0, 2, 640)
video_track = agora_service.create_custom_video_track_encoded(video_sender, sender_options)
local_user = connection.get_local_user()

# video_sender = connection.GetVideoSender()
# video_frame_observer = DYSVideoFrameObserver()
# local_user.register_video_frame_observer(video_frame_observer)

video_track.set_enabled(1)
local_user.publish_video(video_track)



def test1():

    # video_sender.Start()

    sendinterval = 1/25
    pacer = Pacer(sendinterval)

    width = 100
    height = 50

    def send_test():
        count = 0
        yuv_len = int(width*height*3/2)
        frame_buf = bytearray(yuv_len)            
        with open(sample_options.audio_file, "rb") as file:
            while True:            
                success = file.readinto(frame_buf)
                if not success:
                    break

                encoded_video_frame_info = EncodedVideoFrameInfo()
                encoded_video_frame_info.codec_type = 7            
                encoded_video_frame_info.width = width
                encoded_video_frame_info.height = height
                encoded_video_frame_info.frames_per_second = 15                        
                encoded_video_frame_info.frame_type = 3
                # encoded_video_frame_info.rotation = 0
                # encoded_video_frame_info.track_id = 0
                
                ret = video_sender.send_encoded_video_image(frame_buf, len(frame_buf) ,encoded_video_frame_info)        
                count += 1
                print("count,ret=",count, ret)
                pacer.pace()



    for i in range(40):
        # 示例调用
        # read_h264_packets(encoded_file_path)
        send_test()


def test2():
    sendinterval = 1/25
    pacer = Pacer(sendinterval)

    width = 352
    height = 288

    import ffmpeg
    def is_key_frame(nal_unit):
        # 获取 NAL 单元的类型
        nal_unit_type = nal_unit[0] & 0x1F
        return nal_unit_type == 5  # 5 表示关键帧（I帧）

    def parse_slice_type(nal_unit):
        # 查找第一个字节，确定 NAL 单元类型
        nal_unit_type = nal_unit[0] & 0x1F
        
        if nal_unit_type in (1, 2):  # 非 I 帧（可能是 B 帧或 P 帧）
            # 跳过 NAL unit header (1 byte) 和 Slice header (第一个字节)
            slice_header = nal_unit[1] & 0xE0
            
            slice_type = slice_header >> 5  # 提取 Slice 类型
            if slice_type in (0, 4):  # Slice type 为 0 或 4 表示 B 帧
                return "B"
            elif slice_type in (1, 6):  # Slice type 为 1 或 6 表示 P 帧
                return "P"
        return "Other"


    def read_h264_packets(h264_file):
        process = (
            ffmpeg
            .input(h264_file)
            .output('pipe:', format='h264')
            .run(capture_stdout=True, capture_stderr=True)
        )
        count = 0

        output, error = process

        # 处理输出数据（每个packet）
        packets = output.split(b'\n')  # 根据需要分割数据
        for packet in packets:
            if packet:  # 过滤掉空行
                # print(packet)
                encoded_video_frame_info = EncodedVideoFrameInfo()
                encoded_video_frame_info.codec_type = 2            
                encoded_video_frame_info.width = width
                encoded_video_frame_info.height = height
                encoded_video_frame_info.frames_per_second = 25                        
                # encoded_video_frame_info.frame_type = 3
                if is_key_frame(packet):
                    encoded_video_frame_info.frame_type = 3
                else:
                    encoded_video_frame_info.frame_type = 4            
                # encoded_video_frame_info.rotation = 0
                # encoded_video_frame_info.track_id = 0
                packet = bytearray(packet)            
                ret = video_sender.send_encoded_video_image(packet, len(packet) ,encoded_video_frame_info)        
                count += 1
                print("count,ret=",count, ret)
                pacer.pace_interval(1/30)




    for i in range(40):
        # 示例调用
        read_h264_packets(sample_options.video_file)
        # send_test()

# test1()
# test2()


import av
def read_and_send_packets(h264_file):
    sendinterval = 1/25
    pacer = Pacer(sendinterval)
    count = 0
    width = 352
    height = 288

    # 打开 .264 文件
    container = av.open(h264_file)

    for stream in container.streams:
        if stream.type == 'video':
            width = stream.width
            height = stream.height
            print(f"Video stream: width = {width}, height = {height}")
            break

    # 遍历每个 packet
    for packet in container.demux():
        if packet.stream.type == 'video':
            # 读取到的视频 packet 可以在这里发送出去
            print(f"Read packet with size {packet.size} bytes, PTS {packet.pts}")
            is_keyframe = packet.is_keyframe
            if is_keyframe:
                print(f"Keyframe packet with size {packet.size} bytes, PTS {packet.pts}")
            else:
                print(f"Non-keyframe packet with size {packet.size} bytes, PTS {packet.pts}")

            # 假设 send_packet 是你定义的发送函数，可以将 packet 数据发送出去
            # send_packet(packet)

            encoded_video_frame_info = EncodedVideoFrameInfo()
            encoded_video_frame_info.codec_type = 2            
            encoded_video_frame_info.width = width
            encoded_video_frame_info.height = height
            encoded_video_frame_info.frames_per_second = 25                        
            # encoded_video_frame_info.frame_type = 3
            if is_keyframe:
                encoded_video_frame_info.frame_type = 3
            else:
                encoded_video_frame_info.frame_type = 4        
            # packet2 = bytearray(packet.buffer_ptr) 
            packet2 = packet.buffer_ptr         
            # continue
            ret = video_sender.send_encoded_video_image(packet.buffer_ptr, packet.buffer_size ,encoded_video_frame_info)        
            count += 1
            print("count,ret=",count, ret)
            pacer.pace_interval(1/30)

read_and_send_packets(sample_options.video_file)


# time.sleep(2)
local_user.unpublish_video(video_track)
video_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
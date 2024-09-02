#coding=utf-8

import time
import datetime
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(script_dir)
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, SenderOptions
from agora_service.rtc_connection import *
from agora_service.media_node_factory import *
from agora_service.audio_pcm_data_sender import *
from agora_service.audio_frame_observer import *
from agora_service.video_frame_sender import *
from agora_service.video_frame_observer import *
from agora_service.local_user_observer import *
from agora_service.remote_video_track import RemoteVideoTrack
from agora_service.video_encoded_image_receiver import IVideoEncodedImageReceiver
from agora_service.video_encoded_frame_observer import IVideoEncodedFrameObserver

class DYSConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super(DYSConnectionObserver, self).__init__()

    def on_connected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connected:", agora_rtc_conn, conn_info, reason)

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Disconnected:", agora_rtc_conn, conn_info, reason)

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connecting:", agora_rtc_conn, conn_info, reason)

    def on_user_joined(self, agora_rtc_conn, user_id):
        print("CCC on_user_joined:", agora_rtc_conn, user_id)

    def on_user_left(self, agora_rtc_conn, user_id, reason):
        print("CCC on_user_left:", agora_rtc_conn, user_id, reason)


class DYSLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(DYSLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        print("CCC on_stream_message:", user_id, stream_id, data, length)
        return 0

    def on_user_info_updated(self, local_user, user_id, msg, val):
        print("CCC on_user_info_updated:", user_id, msg, val)
        return 0


class DYSVideoFrameObserver(IVideoFrameObserver):
    def __init__(self):
        super(DYSVideoFrameObserver, self).__init__()

    def on_frame(self, video_frame_observer, channel_id, remote_uid, frame):
        print("DYSVideoFrameObserver on_frame:", video_frame_observer, channel_id, remote_uid, frame)
        return 0
    
    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        print("DYSVideoFrameObserver on_user_video_track_subscribed:", agora_local_user, user_id, info, agora_remote_video_track)
        return 0
    
    # def on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track:RemoteVideoTrack, video_track_info):
    #     print("DYSVideoFrameObserver _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        # agora_remote_video_track.register_video_encoded_image_receiver(video_encoded_image_receiver)


class DYSVideoEncodedImageReceiver(IVideoEncodedImageReceiver):
    def __init__(self):
        super(DYSVideoEncodedImageReceiver, self).__init__()

    def on_encoded_video_image_received(self, agora_handle, image_buffer, length, info):
        print("DYSVideoEncodedImageReceiver on_encoded_video_image_received:", agora_handle, image_buffer, length, info)
        return 0

# IVideoEncodedFrameObserver
class DYSVideoEncodedFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self):
        super(DYSVideoEncodedFrameObserver, self).__init__()

    def on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info):
        print("DYSVideoEncodedFrameObserver on_encoded_video_frame:", agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info)
        return 1

class Pacer:
    def __init__(self,interval):
        self.last_call_time = time.time()
        self.interval = interval

    def pace(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < self.interval:
            time.sleep(self.interval - elapsed_time)
            # print("sleep time:", (self.interval - elapsed_time)*1000)
        self.last_call_time = time.time()


example_dir = os.path.dirname(os.path.abspath(__file__))


# 通过传参将参数传进来
# 例如： python examples/example.py {appid} {token} {channel_id} ./test_data/103_RaceHorses_416x240p30_300.yuv {userid}
appid = sys.argv[1]
token = sys.argv[2]
channel_id = sys.argv[3]
yuv_file_path = sys.argv[4]
# check argv len
if len(sys.argv) > 5:
    uid = sys.argv[5]
else:
    uid = "0"
print("appid:", appid, "token:", token, "channel_id:", channel_id, "yuv_file_path:", yuv_file_path, "uid:", uid)


config = AgoraServiceConfig()
config.enable_audio_processor = 0
config.enable_audio_device = 0
config.enable_video = 1
config.appid = appid
sdk_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename, _ = os.path.splitext(os.path.basename(__file__))
config.log_path = os.path.join(sdk_dir, 'logs', filename ,log_folder, 'agorasdk.log')

agora_service = AgoraService()
agora_service.initialize(config)

con_config = RTCConnConfig(
    auto_subscribe_audio=0,
    auto_subscribe_video=1,
    client_role_type=1,
    channel_profile=1,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(token, channel_id, uid)

media_node_factory = agora_service.create_media_node_factory()
video_sender = media_node_factory.create_video_encoded_image_sender()
sender_options = SenderOptions(0, 2, 640)
video_track = agora_service.create_custom_video_track_encoded(video_sender, sender_options)

# video_track.register_video_encoded_image_receiver(video_sender)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

video_subscription_options = VideoSubscriptionOptions(
            type = VIDEO_STREAM_TYPE.VIDEO_STREAM_HIGH,
            encodedFrameOnly = 1
)
local_user.subscribe_all_video(video_subscription_options)

# video_sender = connection.GetVideoSender()
# video_frame_observer = DYSVideoFrameObserver()
# video_encoded_image_receiver = DYSVideoEncodedImageReceiver()
video_encoded_frame_observer = DYSVideoEncodedFrameObserver()
local_user.register_video_encoded_frame_observer(video_encoded_frame_observer)

video_track.set_enabled(1)
local_user.publish_video(video_track)

# video_sender.Start()

# sendinterval = 1/30
# Pacer = Pacer(sendinterval)

# width = 416
# height = 240

# def send_test():
#     count = 0
#     yuv_len = int(width*height*3/2)
#     frame_buf = bytearray(yuv_len)            
#     with open(yuv_file_path, "rb") as file:
#         while True:            
#             success = file.readinto(frame_buf)
#             if not success:
#                 break
#             frame = ExternalVideoFrame()
#             frame.buffer = frame_buf
#             frame.type = 1
#             frame.format = 1
#             frame.stride = width
#             frame.height = height
#             frame.timestamp = 0
#             ret = video_sender.send_video_framee(frame)        
#             count += 1
#             print("count,ret=",count, ret)
#             Pacer.pace()

# for i in range(1):
#     send_test()

time.sleep(200)
local_user.unpublish_video(video_track)
video_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
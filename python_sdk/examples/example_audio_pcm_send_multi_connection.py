#!env python

#coding=utf-8

import time
import os
import sys
import datetime
import common.path_utils 

from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.rtc_connection_observer import IRTCConnectionObserver
from agora_service.audio_pcm_data_sender import PcmAudioFrame
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
pcm_file_path = sys.argv[4]
# check argv len
if len(sys.argv) > 5:
    uid = sys.argv[5]
else:
    uid = "0"
print("appid:", appid, "token:", token, "channel_id:", channel_id, "pcm_file_path:", pcm_file_path, "uid:", uid)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.appid = appid

sdk_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename, _ = os.path.splitext(os.path.basename(__file__))
config.log_path = os.path.join(sdk_dir, 'logs', filename ,log_folder, 'agorasdk.log')

agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    client_role_type=1,
    channel_profile=1,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(token, "dys_channel_test1", uid)

connection2 = agora_service.create_rtc_connection(con_config)
conn_observer2 = DYSConnectionObserver()
connection2.register_observer(conn_observer2)
connection2.connect(token, "dys_channel_test2", uid)

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

pcm_data_sender2 = media_node_factory.create_audio_pcm_data_sender()
audio_track2 = agora_service.create_custom_audio_track_pcm(pcm_data_sender2)
local_user2 = connection2.get_local_user()
localuser_observer2 = DYSLocalUserObserver()
local_user2.register_local_user_observer(localuser_observer2)
audio_frame_observer2 = DYSAudioFrameObserver()
local_user2.register_audio_frame_observer(audio_frame_observer2)
audio_track2.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track.set_enabled(1)
local_user.publish_audio(audio_track)

audio_track2.set_enabled(1)
local_user2.publish_audio(audio_track2)

sendinterval = 0.1
Pacer = Pacer(sendinterval)
count = 0
packnum = int((sendinterval*1000)/10)

def send_test():
    with open(pcm_file_path, "rb") as file:
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
            ret2 = pcm_data_sender2.send_audio_pcm_data(frame)
            count += 1
            print("count,ret=",count, ret, ret2)
            Pacer.pace()

# for i in range(100):
#     send_test()


send_test()

#---------------5. Stop Media Sender And Release
time.sleep(10)
local_user.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()

local_user2.unpublish_audio(audio_track2)
audio_track2.set_enabled(0)
connection2.unregister_observer()
connection2.disconnect()
connection2.release()

print("release")
agora_service.release()
print("end")
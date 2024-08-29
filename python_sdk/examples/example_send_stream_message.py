#coding=utf-8
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(script_dir)
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

import time
import ctypes
import datetime
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.rtc_connection import IRTCConnectionObserver
from agora_service.local_user_observer import IRTCLocalUserObserver

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


class DYSLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(DYSLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        print("CCC on_stream_message:", user_id, stream_id, data, length)
        return 0

    def on_user_info_updated(self, local_user, user_id, msg, val):
        print("CCC on_user_info_updated:", user_id, msg, val)
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

example_dir = os.path.dirname(os.path.abspath(__file__))
pcm_file_path = os.path.join(example_dir, 'demo.pcm')

# 通过传参将参数传进来
# 例如： python examples/example_send_stream_message.py {appid} {token} {channel_id} {msg} {userid}
appid = sys.argv[1]
token = sys.argv[2]
channel_id = sys.argv[3]
msg = sys.argv[4]
# check argv len
if len(sys.argv) > 5:
    uid = sys.argv[5]
else:
    uid = "0"
print("appid:", appid, "token:", token, "channel_id:", channel_id, "uid:", uid)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = appid
sdk_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
config.log_path = os.path.join(sdk_dir, 'logs/example_send_stream_message', log_folder, 'agorasdk.log')

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

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

# connection.Connect(token, channel_id, uid)
stream_id = connection.create_data_stream(False, False)
print("stream_id:", stream_id)
for i in range(10):
    print("sendmsg:{} to:{}".format(msg, stream_id))
    connection.send_stream_message(stream_id, msg)
    time.sleep(2)

connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
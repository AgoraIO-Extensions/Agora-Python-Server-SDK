#coding=utf-8
import os
import time
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver  
from observer.local_user_observer import DYSLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.agora_base import *

# 通过传参将参数传进来
#python agora_rtc/examples/example_stream_message_send.py --appId=xxx --channelId=xxx --userId=xxx --message="hello agora"
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

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

# connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)
stream_id = connection.create_data_stream(False, False)
stream_id2 = connection.create_data_stream(False, False)
print("stream_id:", stream_id)
for i in range(100):
    msg1 = sample_options.msg + " to data_stream:" +  str(stream_id) + " idx:" +  str(i)
    msg2 = sample_options.msg + " to data_stream:" +  str(stream_id2) + " idx:" +  str(i)
    ret = connection.send_stream_message(stream_id, msg1)
    print(msg1, ret)
    ret = connection.send_stream_message(stream_id2, msg2)
    print(msg2, ret)
    time.sleep(2)

connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
#!/usr/bin/env python

import os
import time
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example
from observer.local_user_observer import DYSLocalUserObserver
from observer.connection_observer import DYSConnectionObserver
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig

# 通过传参将参数传进来
#python python_sdk/examples/example_stream_message_receive.py --token=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 0
config.enable_audio_device = 0
config.use_string_uid = 0
# config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])

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
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

time.sleep(200)

connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
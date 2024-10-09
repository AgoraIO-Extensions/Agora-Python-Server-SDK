#coding=utf-8
import os
import time
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import ExampleConnectionObserver  
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_stream_message_send.py --appId=xxx --channelId=xxx --userId=xxx --message="hello agora"
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = ExampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

local_user = connection.get_local_user()
local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
localuser_observer = ExampleLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

# connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)
stream_id = connection.create_data_stream(False, False)
stream_id2 = connection.create_data_stream(False, False)
logger.info(f"stream_id: {stream_id}")
for i in range(100):
    msg1 = sample_options.msg + " to data_stream:" +  str(stream_id) + " idx:" +  str(i)
    msg2 = sample_options.msg + " to data_stream:" +  str(stream_id2) + " idx:" +  str(i)
    ret = connection.send_stream_message(stream_id, msg1)
    logger.info(f"send_stream_message: {msg1}, ret: {ret}")
    ret = connection.send_stream_message(stream_id2, msg2)
    logger.info(f"send_stream_message: {msg2}, ret: {ret}")
    time.sleep(2)

connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")
agora_service.release()
logger.info("end")
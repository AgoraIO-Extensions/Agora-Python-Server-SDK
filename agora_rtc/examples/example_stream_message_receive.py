#!/usr/bin/env python

import os
import time
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example
from observer.local_user_observer import SampleLocalUserObserver
from observer.connection_observer import SampleConnectionObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_stream_message_receive.py --appId=xxx --channelId=xxx --userId=xxx
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
conn_observer = SampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

local_user = connection.get_local_user()
local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
localuser_observer = SampleLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

time.sleep(200)

connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")
agora_service.release()
logger.info("end")
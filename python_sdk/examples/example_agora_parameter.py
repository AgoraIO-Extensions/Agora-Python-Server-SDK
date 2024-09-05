#!env python

#coding=utf-8

import time
import os
import sys
import datetime
from common.path_utils import get_log_path_with_filename 


from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.rtc_connection_observer import IRTCConnectionObserver
from agora_service.audio_pcm_data_sender import PcmAudioFrame
from agora_service.audio_frame_observer import IAudioFrameObserver
from agora_service.local_user_observer import IRTCLocalUserObserver

from common.parse_args import parse_args_example
# 通过传参将参数传进来
#python python_sdk/examples/example_agora_parameter.py --token=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)



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



#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
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

agora_parameter = connection.get_agora_parameter()
print("audio_pcm_data_send_mode:",agora_parameter.get_string("audio_pcm_data_send_mode"))
print("ret:", agora_parameter.set_parameters("{\"audio_pcm_data_send_mode\":1}")) 
print("audio_pcm_data_send_mode:",agora_parameter.get_string("audio_pcm_data_send_mode")) 


agora_parameter = connection.get_agora_parameter()
print("che.audio.aec.enable:",agora_parameter.get_string("che.audio.aec.enable"))
print("ret:", agora_parameter.set_parameters("{\"che.audio.aec.enable\":true}")) 
print("che.audio.aec.enable:",agora_parameter.get_string("che.audio.aec.enable")) 
print("ret:", agora_parameter.set_parameters("{\"che.audio.aec.enable\":false}")) 
print("che.audio.aec.enable:",agora_parameter.get_string("che.audio.aec.enable")) 



agora_parameter = connection.get_agora_parameter()
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2")) 
print("ret:", agora_parameter.set_parameters("{\"rtc.enable_nasa2\":1}")) 
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2")) 
print("ret:", agora_parameter.set_parameters("{\"rtc.enable_nasa2\":0}")) 
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2")) 


agora_parameter = connection.get_agora_parameter()
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2"))
print("ret:", agora_parameter.set_bool("rtc.enable_nasa2",0)) 
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2")) 
print("ret:", agora_parameter.set_bool("rtc.enable_nasa2",1)) 
print("rtc.enable_nasa2:",agora_parameter.get_bool("rtc.enable_nasa2")) 


agora_parameter = connection.get_agora_parameter()
print("rtc.test111:",agora_parameter.get_bool("rtc.test111"))
print("ret:", agora_parameter.set_bool("rtc.test111",0)) 
print("rtc.test111:",agora_parameter.get_bool("rtc.test111")) 
print("ret:", agora_parameter.set_bool("rtc.test111",1)) 
print("rtc.test111:",agora_parameter.get_bool("rtc.test111")) 


connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")
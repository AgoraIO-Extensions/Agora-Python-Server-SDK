#!env python

#coding=utf-8
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig


# 通过传参将参数传进来
#python python_sdk/examples/example_agora_parameter.py --token=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)


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
#!env python

#coding=utf-8

import time
import os
import sys
import datetime
from common.path_utils import get_log_path_with_filename 


source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(source_dir, 'logs', filename ,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
log_path = os.path.join(log_folder, 'agorasdk.log')

from agora_service.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora_service.rtc_connection_observer import IRTCConnectionObserver
from agora_service.audio_pcm_data_sender import EncodedAudioFrame
from agora_service.audio_frame_observer import IAudioFrameObserver, AudioFrame
from agora_service.local_user_observer import IRTCLocalUserObserver

from common.parse_args import parse_args_example
# 通过传参将参数传进来
#python python_sdk/examples/example_audio_pcm_receive_multi_connection.py --token=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.aac
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
    def on_mixed_audio_frame(self, agora_local_user, channelId, frame):
        print("CCC on_mixed_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        print("CCC on_ear_monitoring_audio_frame")
        return 0
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame):
        print("CCC on_playback_audio_frame_before_mixing", audio_frame.type, audio_frame.samples_per_sec, audio_frame.samples_per_channel, audio_frame.bytes_per_sample, audio_frame.channels)        
        file_path = os.path.join(log_folder, channelId + 'pcm_file')
        with open(file_path, "ab") as f:
            f.write(audio_frame.buffer)
        return 1
    
    # def on_get_audio_frame_position(self, agora_local_user):
    #     print("CCC on_get_audio_frame_position")
    #     return 0

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_playback_audio_frame_param")
    #     return 0
    # def on_get_record_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_record_audio_frame_param")
    #     return 0
    # def on_get_mixed_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_mixed_audio_frame_param")
    #     return 0
    # def on_get_ear_monitoring_audio_frame_param(self, agora_local_user):
    #     print("CCC on_get_ear_monitoring_audio_frame_param")
    #     return 0


#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.appid = sample_options.app_id
config.log_path =log_path

agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
sub_opt = AudioSubscriptionOptions(
        packet_only = 0,
        pcm_data_only = 1,
        bytes_per_sample = 2,
        number_of_channels = 1,
        sample_rate_hz = 16000
)


con_config = RTCConnConfig(
    auto_subscribe_audio=1,
    auto_subscribe_video=0,
    client_role_type=1,
    channel_profile=1,
    # audio_recv_media_packet = 1,
    # audio_send_media_packet = 1,
    audio_subs_options = sub_opt,
    enable_audio_recording_or_playout = 0,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, "dys_channel_test1", sample_options.user_id)

connection2 = agora_service.create_rtc_connection(con_config)
conn_observer2 = DYSConnectionObserver()
connection2.register_observer(conn_observer2)
connection2.connect(sample_options.token, "dys_channel_test2", sample_options.user_id)


#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()

audio_sender = media_node_factory.create_audio_encoded_frame_sender()
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 0)
local_user = connection.get_local_user()
local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_frame_observer = DYSAudioFrameObserver()
local_user.register_audio_frame_observer(audio_frame_observer)
local_user.subscribe_all_audio()


audio_sender2 = media_node_factory.create_audio_encoded_frame_sender()
audio_track2 = agora_service.create_custom_audio_track_encoded(audio_sender2, 0)
local_user2 = connection2.get_local_user()
local_user2.set_playback_audio_frame_before_mixing_parameters(1, 16000)
localuser_observer2 = DYSLocalUserObserver()
local_user2.register_local_user_observer(localuser_observer2)
audio_frame_observer2 = DYSAudioFrameObserver()
local_user2.register_audio_frame_observer(audio_frame_observer2)
local_user2.subscribe_all_audio()

#---------------4. Send Media Stream
# audio_track.set_enabled(1)
# local_user.publish_audio(audio_track)

time.sleep(100)
# local_user.unpublish_audio(audio_track)
# audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()

connection2.unregister_observer()
connection2.disconnect()
connection2.release()

print("release")
agora_service.release()
print("end")
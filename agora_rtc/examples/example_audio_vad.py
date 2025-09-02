# coding=utf-8

import time
import datetime
import ctypes
from common.path_utils import get_log_path_with_filename
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.rtc_connection import *
from agora.rtc.media_node_factory import *
from agora.rtc.audio_pcm_data_sender import *
from agora.rtc.audio_frame_observer import *
import signal
from agora.rtc.local_user import *
from agora.rtc.local_user_observer import *
import threading
from collections import deque
from common.push_audio_pcm_file import push_pcm_data_from_file


# import voicesentencedetection
from agora.rtc.voice_detection import *

from agora.rtc.utils.vad_dump import VadDump
from common.push_audio_pcm_file import file_to_consumer
from agora.rtc.utils.audio_consumer import AudioConsumer

import gc
import asyncio
# memey leak test
from memory_profiler import profile


# connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    return log_path


# observer
@profile
class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        #super(MyAudioFrameObserver, self).__init__()
        self._silence_pack = bytearray(320)
        """
        # Recommended  configurations:  
            # For not-so-noisy environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -50)  
            # For noisy environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -40)  
            # For high-noise environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -30)
         """

        self._vad_instance = AudioVadV2(AudioVadConfigV2(16, 30, 50, 0.7, 0.5, 70, 70, -50))
        self._dump_path = './vad'
        self._vad_dump = VadDump(self._dump_path)
        self._vad_dump.open()
        pass

    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_record_audio_frame")
        return 0

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0


    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame, vad_result_state:int, vad_result_bytearray:bytearray):
        # logger.info(f"on_playback_audio_frame_before_mixing, channelId={channelId}, uid={uid}, type={audio_frame.type}, samples_per_sec={audio_frame.samples_per_sec}, samples_per_channel={audio_frame.samples_per_channel}, bytes_per_sample={audio_frame.bytes_per_sample}, channels={audio_frame.channels}, len={len(audio_frame.buffer)}")
        print(f"before_mixing: far = {audio_frame.far_field_flag },rms = {audio_frame.rms}, voice = {audio_frame.voice_prob}, music ={audio_frame.music_prob},pith = {audio_frame.pitch}")
        #vad v2 processing: can do in sdk callback
        state, bytes = self._vad_instance.process(audio_frame)
        print("state = ", state, len(bytes) if bytes != None else 0, vad_result_state, len(vad_result_bytearray) if vad_result_bytearray != None else 0)
        # dump to vad for debuging
        self._vad_dump.write(audio_frame, vad_result_bytearray, vad_result_state)
        if bytes != None:
            if state == 1:
                # start speaking: then start send bytes(not audio_frame) to ARS
                print("vad v2 start speaking")
            elif state == 2:
                # continue send bytes to ARS
                pass
            elif state == 3:
                # stop speaking: send bytes to ARS and then then stop  ARS
                print("vad v2 stop speaking:")
            else:
                logger.info("unknown state")
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0
# sig handleer
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True
#read pcm data from file, return the data in bytes with memoryview to avoid copy
def read_pcm_data_from_file(sample_rate, num_of_channels, buffer, audio_file):

    bytes_in_ms = int(sample_rate * num_of_channels * 2 / 1000)
    read_len = audio_file.readinto(buffer)
    read_len = int(read_len//bytes_in_ms)*bytes_in_ms
    mv = memoryview(buffer)
    slice_data = mv[:read_len]
    return slice_data



@profile
def main():

    # signal handler

    signal.signal(signal.SIGINT, signal_handler)

    # run this example
    # 例如： python examples/example.py {appid}  {channel_id}
    #check argv len
    if len (sys.argv) < 3:
        print("usage: python example_audio_vad.py appid channelname")
        return
    appid = sys.argv[1]
    channel_id = sys.argv[2]
   
    uid = "0"


    print("appid:", appid, "channel_id:", channel_id)

    config = AgoraServiceConfig()
    config.appid = appid
    # config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])

    now = time.time()*1000
    agora_service = AgoraService()
    agora_service.initialize(config)
    print("diff = ", time.time()*1000-now) # 85ms

    

    


    sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
    )

    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=0,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )
    publish_config = RtcConnectionPublishConfig(
        audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
        audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
        is_publish_audio=True,
        is_publish_video=False,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_NONE,
        video_encoded_image_sender_options=SenderOptions(target_bitrate=4160, cc_mode=TCcMode.CC_ENABLED, codec_type=VideoCodecType.VIDEO_CODEC_H264)
    )

    connection = agora_service.create_rtc_connection(con_config, publish_config)

    connection.connect(appid, channel_id, uid)

    # step2:
    

    # step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = ExampleLocalUserObserver()
    # enable volume indication
 
    connection.register_local_user_observer(local_observer)

    # note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    audio_observer = MyAudioFrameObserver()
    vad_configure  = AudioVadConfigV2(16, 30, 50, 0.7, 0.5, 70, 70, -50)
    connection.register_audio_frame_observer(audio_observer, 1, vad_configure)

    connection.publish_audio()

    # set paramter

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    # agora_parameter = connection.get_agora_parameter()
    # agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

    global g_runing

    #open file for push
    audio_file_path = "./test_data/demo.pcm"
    audio_file = open (audio_file_path, "rb")
    bytes_in_ms = int(16000 * 1 * 2 / 1000)
    buffer = bytearray(bytes_in_ms*1000*10)
    with open(audio_file_path, "rb") as audio_file:
        slice_data = read_pcm_data_from_file(16000, 1, buffer, audio_file)
        while g_runing:
            ret = connection.is_push_to_rtc_completed()
            if ret == True:
               connection.push_audio_pcm_data(slice_data, 16000, 1)
            time.sleep(0.05)


     # release resource
    connection.disconnect()
   
    connection.release()
    agora_service.release()
    
    #set to None
    audio_observer = None
    local_observer = None
    connection = None
    agora_service = None

    # for memory leak check
    print("end")


if __name__ == "__main__":
    main()


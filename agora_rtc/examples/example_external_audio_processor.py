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
from agora.rtc.external_audio_processor import *
import threading
from collections import deque
from queue import Queue



# import voicesentencedetection
from agora.rtc.voice_detection import *

from agora.rtc.utils.vad_dump import VadDump
from common.push_audio_pcm_file import file_to_consumer
from agora.rtc.utils.audio_consumer import AudioConsumer


# memey leak test
#from memory_profiler import profile

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    log_path = "./log/agorasdk.log"
    return log_path



# sig handleer
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True

class ExampleAudioSinkObserver(IAudioSinkObserver):
    def on_processed_audio_frame(self,processor: 'ExternalAudioProcessor',frame: AudioFrame,vad_result_state:int,vad_result_data:bytearray):
        print(f"ExampleAudioSinkObserver on_processed_audio_frame: voice_prob {frame.voice_prob}, rms {frame.rms}, pitch {frame.pitch}, far_field_flag {frame.far_field_flag}, vad_result_state {vad_result_state}, vad_result_data length {len(vad_result_data)}")

#@profile
def main():

    # signal handler

    signal.signal(signal.SIGINT, signal_handler)

    # run this example
    # 例如： python examples/example.py {appid}  {channel_id}
    #check argv len
    if len (sys.argv) < 7:
        print("usage: python example_audio_vad.py appid channelname pcm_file_path sample_rate channels mode")
        return
    appid = sys.argv[1]
    channel_id = sys.argv[2]
    pcm_file_path = sys.argv[3]
    sample_rate = int(sys.argv[4])
    channels = int(sys.argv[5])
    mode = int(sys.argv[6])
    uid = "0"
    


    logger.info("appid:", appid, "channel_id:", channel_id)
   
    config = AgoraServiceConfig()
    config.appid = appid
    config.enable_video = 1
    config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_AI_SERVER
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])
    config.log_path = "./agora_rtc_log/agorasdk.log"
    config.log_file_size_kb = 1024
    config.data_dir = "./agora_rtc_log"
    config.config_dir = "./agora_rtc_log"
    #apm related config: if want to use apm, please ontact with us.
    #in common, no need to enable it.
    # note: enable_apm is a switch that controls whether intermediate processed audio data will be dumped to local disk. 
    # Only use it in debug mode.
    config.enable_apm = True
   

    #test callback when muted
    config.should_callbck_when_muted = 0
    config.domain_limit = 0

    now = time.time()*1000
    agora_service = AgoraService()
    agora_service.initialize(config)
    print("diff = ", time.time()*1000-now) # 85ms

    amp_config = APMConfig(
        ai_aec_config=AiAecConfig(enabled=False),
        ai_ns_config=AiNsConfig(),
        bghvs_c_config=BghvsCConfig(),
        agc_config=AgcConfig(enabled=False),
        enable_dump=True,
    )
    my_observer = ExampleAudioSinkObserver()
    external_audio_processor = ExternalAudioProcessor(agora_service)
    external_audio_processor.initialize(amp_config, 48000, 2, AudioVadConfigV2(), my_observer)
    global g_runing

   

    #open a file and read pcm data
    file = open(pcm_file_path, "rb")
    bytearray_data = bytearray(480)
   

    while g_runing:
        read_len = file.readinto(bytearray_data)
        if read_len <= 0:
            break
        external_audio_processor.push_audio_pcm_data(bytearray_data[:read_len], sample_rate, channels)
        time.sleep(0.05)
    file.close()
     # release resource
    logger.info("release resource now")

   
    

    
    logger.info("release agora service now")
    agora_service.release()
    logger.info("release agora service done")
    
    #set to None
   
    agora_service = None

    # for memory leak check
    logger.info("end")
    print("end")


if __name__ == "__main__":
    main()
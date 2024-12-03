"""
# an example of audio consumer with pcm data
"""
# coding=utf-8

import time
import datetime
import ctypes
from common.path_utils import get_log_path_with_filename
from agora.rtc.utils.audio_consumer import AudioConsumer
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
from agora.rtc.audio_vad import *
from agora.rtc.local_user import *
from agora.rtc.local_user_observer import *
import threading
from collections import deque

# import voicesentencedetection
from agora.rtc.voice_detection import *
from agora.rtc.audio_vad import *

import gc
import asyncio


# connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    return log_path


# observer
class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(MyAudioFrameObserver, self).__init__()
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

    def _dump_to_file(self, fd, audio_frame: AudioFrame):
        fd.write(audio_frame.buffer)

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame):
        # logger.info(f"on_playback_audio_frame_before_mixing, channelId={channelId}, uid={uid}, type={audio_frame.type}, samples_per_sec={audio_frame.samples_per_sec}, samples_per_channel={audio_frame.samples_per_channel}, bytes_per_sample={audio_frame.bytes_per_sample}, channels={audio_frame.channels}, len={len(audio_frame.buffer)}")
       
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0
    


# sig handleer


def shut_down(loop, exit_event):
    exit_event.set()
    print("prsss ctrl+c: ", 1)







#模拟产生的数据，足够多，可以一直播放
def push_file_to_consumer(file, consumer, packnum):
        frame_buf = bytearray(320)
        pushed = 0
        while pushed < packnum:
            ret = file.readinto(frame_buf)
            if ret < 320: # reach end of file
                file.seek(0)
                break
            else:
                consumer.push_pcm_data(frame_buf)
                pushed += 1
                print("pushed:", pushed)
        frame_buf = None   
        pass
async def read_file_to_consumer(pcm_file_path, consumer,interval_in_ms, exit_event):
    pack_nums = interval_in_ms//10
    frame_buf = bytearray(320*pack_nums)
    frame_view = None
    start_time = 0
    with open(pcm_file_path, "rb") as file:
        
        total_len = file.tell()
        print("total_len:",total_len)
        # for the first time , read all data into consumer
        push_file_to_consumer(file,consumer, 0x7fffffff)
        file.seek(0)
        start_time = time.time()*1000
        total_file_duration = (total_len//(320))*10  #in ms
        act_total_pushed = 0
        while True:
            if exit_event.is_set():
                break
            #下面的操作：只是模拟生产的数据。
            # - 在sample中，为了确保生产产生的数据能够一直播放，需要生产足够多的数据，所以用这样的方式来模拟
            # - 在实际使用中，数据是实时产生的，所以不需要这样的操作。只需要在TTS生产数据的时候，调用AudioConsumer.push_pcm_data()
            len = consumer.len()
            if len < interval_in_ms*320*1.5:
                push_file_to_consumer(file,consumer, 0x7fffffff)
           
            await asyncio.sleep(interval_in_ms/1000)
    pass
async def do_consume(consumer, interval_in_ms, exit_event):
    while True:
        print("consume:",time.time()*1000)
        if exit_event.is_set():
            break
        consumer.consume()
        await asyncio.sleep(interval_in_ms/1000)
        
    pass
async def main(exit_event):

    # signal handler

    

    # run this example
    # 例如： python examples/example.py {appid}  {channel_id} ./test_data/demo.pcm 
    #check argv len
    if len(sys.argv) < 4:
        print("usage: python example_audio_consumer.py appid  channelname pcm_file_path")
        return
    appid = sys.argv[1]
    channel_id = sys.argv[2]
    pcm_file_path = sys.argv[3]
   
    uid = "0"

    print("appid:", appid,  "channel_id:", channel_id, "pcm_file_path:", pcm_file_path)

    config = AgoraServiceConfig()
    config.appid = appid
    # config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])

    agora_service = AgoraService()
    agora_service.initialize(config)

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
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER ,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)

    connection.connect(appid, channel_id, uid)

    # step2:
    media_node_factory = agora_service.create_media_node_factory()
    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)

    # step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = ExampleLocalUserObserver()
    # enable volume indication
    localuser.set_audio_volume_indication_parameters(100, 3, 1)
    localuser.register_local_user_observer(local_observer)

    # note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    audio_observer = MyAudioFrameObserver()
    localuser.register_audio_frame_observer(audio_observer)

    # ret = localuser.get_user_role()
    # localuser.set_user_role(con_config.client_role_type)

    # step4: pub
    audio_track.set_enabled(1)
    localuser.publish_audio(audio_track)
    localuser.subscribe_all_audio()

   
    # stream msg
    stream_id = connection.create_data_stream(0, 0)
    print(f"streamid: {stream_id}")

    # for debug audio problems: can dump audio data to file; 
    # ONLY FOR DEBUG mode, NOT FOR PRODUCTION
    # its not recommended to use this function in production

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    # agora_parameter = connection.get_agora_parameter()
    # agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")



    """
    # 我们启动2个task
    # 一个task，用来模拟从TTS接收到语音，然后将语音push到audio_consumer
    # 另一个task，用来模拟播放语音：从audio_consumer中取出语音播放
    # 在实际应用中，可以是TTS返回的时候，直接将语音push到audio_consumer
    # 然后在另外一个“timer”的触发函数中，调用audio_consumer.consume()。
    # 推荐：
    # “Timer”可以是asycio的模式；也可以是threading.Timer的模式；也可以和业务已有的timer结合在一起使用，都可以。只需要在timer 触发的函数中，调用audio_consumer.consume()即可
    # “Timer”的触发间隔，可以和业务已有的timer间隔一致，也可以根据业务需求调整，推荐在40～80ms之间  
    """
    audio_consumer = AudioConsumer(pcm_data_sender,16000, 1)
    produce_task = asyncio.create_task(read_file_to_consumer(pcm_file_path,audio_consumer, 100, exit_event))
    consumer_task = asyncio.create_task(do_consume(audio_consumer, 40,exit_event))
    await asyncio.gather(produce_task, consumer_task)

    # release resource
    # release AudioConsumer firstly
    audio_consumer.release()
    
    localuser.unpublish_audio(audio_track)
    audio_track.set_enabled(0)

    localuser.unregister_audio_frame_observer()
    localuser.unregister_local_user_observer()

    connection.disconnect()
    connection.unregister_observer()

    localuser.release()
    connection.release()

    
    audio_track.release()
    pcm_data_sender.release()
    audio_consumer.release()

    media_node_factory.release()
    agora_service.release()
    
    #set to None
    audio_track = None
    audio_observer = None
    local_observer = None
    localuser = None
    connection = None
    agora_service = None

    print("end")


if __name__ == "__main__":
    # event: 用来做退出的信号
    exit_event = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shut_down, loop, exit_event)
    loop.run_until_complete(main(exit_event))
    loop.close()
    exit_event = None




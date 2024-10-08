#!env python

import time
import os
import asyncio
import threading
import signal
from multiprocessing import Process
from common.path_utils import get_log_path_with_filename 
# from common.pacer import Pacer
from common.parse_args import parse_args_example, SampleOptions
from observer.connection_observer import SampleConnectionObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
from agora.rtc.agora_base import *
from agora.rtc.video_frame_sender import ExternalVideoFrame, VideoFrameSender
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_send_pcm_yuv.py --appId=xxx --channelId=xxx --userId=xxx --connectionNumber=1 --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1

_exit = False

class Pacer:
    def __init__(self,interval):
        self.last_call_time = time.time()
        self.interval = interval
    async def pace_interval(self, time_interval_s):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < time_interval_s:
            # time.sleep(time_interval_s - elapsed_time)
            await asyncio.sleep(time_interval_s - elapsed_time)
            # print("sleep time(ms):", (time_interval_s - elapsed_time)*1000)
        self.last_call_time = time.time()        

async def push_pcm_data_from_file(sample_rate, num_of_channels , pcm_data_sender:AudioPcmDataSender, audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        global _exit
        pcm_sendinterval = 0.1
        pacer_pcm = Pacer(pcm_sendinterval)
        pcm_count = 0
        while not _exit:
            send_size = int(sample_rate*num_of_channels*pcm_sendinterval*2)
            frame_buf = bytearray(send_size)            
            success = audio_file.readinto(frame_buf)
            if not success:
                audio_file.seek(0)
                continue
            frame = PcmAudioFrame()
            frame.data = frame_buf
            frame.timestamp = 0
            frame.samples_per_channel = int(sample_rate * pcm_sendinterval)
            frame.bytes_per_sample = 2
            frame.number_of_channels = num_of_channels
            frame.sample_rate = sample_rate
            ret = pcm_data_sender.send_audio_pcm_data(frame)
            pcm_count += 1
            logger.debug(f"send pcm: count,ret={pcm_count}, {ret}, {send_size}, {pcm_sendinterval}")
            await pacer_pcm.pace_interval(0.1)

async def push_yuv_data_from_file(width, height, fps, video_sender:VideoFrameSender, video_file_path):
    with open(video_file_path, "rb") as video_file:
        global _exit
        yuv_sendinterval = 1.0/fps
        pacer_yuv = Pacer(yuv_sendinterval)
        yuv_count = 0
        yuv_len = int(width*height*3/2)
        frame_buf = bytearray(yuv_len)
        while not _exit:
            success = video_file.readinto(frame_buf)
            if not success:
                video_file.seek(0)
                continue
            frame = ExternalVideoFrame()
            frame.buffer = frame_buf
            frame.type = 1
            frame.format = 1
            frame.stride = width
            frame.height = height
            frame.timestamp = 0
            frame.metadata = "hello metadata"
            ret = video_sender.send_video_frame(frame)        
            yuv_count += 1
            logger.debug("send yuv: count,ret=%d, %s", yuv_count, ret)
            await pacer_yuv.pace_interval(yuv_sendinterval)

async def send(sample_options:SampleOptions, pcm_data_sender, video_sender):
    pcm_task = asyncio.create_task(push_pcm_data_from_file(sample_options.sample_rate, sample_options.num_of_channels, pcm_data_sender, sample_options.audio_file))
    yuv_task = asyncio.create_task(push_yuv_data_from_file(sample_options.width, sample_options.height, sample_options.fps, video_sender, sample_options.video_file))
    await pcm_task
    await yuv_task

async def create_conn_and_send(agora_service:AgoraService, channel_id, sample_options:SampleOptions):
    #---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = SampleConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, sample_options.user_id)

    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()

    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
    # audio_track.set_max_buffer_audio_frame_number(320*2000)
    
    video_sender = media_node_factory.create_video_frame_sender()
    video_track = agora_service.create_custom_video_track_frame(video_sender)

    local_user = connection.get_local_user()
    local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
    localuser_observer = SampleLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)

    #---------------4. Send Media Stream
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)

    video_track.set_enabled(1)
    local_user.publish_video(video_track)

    await send(sample_options, pcm_data_sender,video_sender)
    
    local_user.unpublish_audio(audio_track)
    local_user.unpublish_video(video_track)
    audio_track.set_enabled(0)
    video_track.set_enabled(0)
    connection.unregister_observer()
    connection.disconnect()
    connection.release()

def handle_signal():
    global _exit
    _exit = True
async def run_example():
    sample_options = parse_args_example()
    logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)

    #---------------1. Init SDK
    config = AgoraServiceConfig()
    config.appid = sample_options.app_id
    config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])
    agora_service = AgoraService()
    agora_service.initialize(config)

    async with asyncio.TaskGroup() as tg:
        for i in range(int(sample_options.connection_number)):
            logger.info(f"channel {i}")
            channel_id = sample_options.channel_id + str(i+1)
            tg.create_task(create_conn_and_send(agora_service, channel_id, sample_options))

    agora_service.release()
    logger.info("agora_service.release-coro")


if __name__ == '__main__':
    asyncio.run(run_example())
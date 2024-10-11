#!env python

import os
import asyncio
import random
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from agora_rtc.examples.common.push_audio_pcm_file import push_pcm_data_from_file
from agora_rtc.examples.common.push_video_yuv_file import push_yuv_data_from_file
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from observer.video_frame_observer import ExampleVideoFrameObserver
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_send_pcm_yuv.py --appId=xxx --channelId=xxx --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
        self.conn_exit = asyncio.Event()
    def handle_signal(self):
        self._exit.set()
        self.timer.cancel()
        self.conn_exit.set()    
    async def my_conn_life_timer(self, delay):
        logger.info(f"conn_life_timer: {delay}")
        await asyncio.sleep(delay)  
        logger.info(f"conn_life_timer: {delay} finish")
        self.conn_exit.set()
    async def create_connections(self, sample_options:ExampleOptions, agora_service):
        while not self._exit.is_set():
            self.conn_exit.clear()
            tasks = []
            for i in range(int(sample_options.connection_number)):
                if i == 0:
                    channel_id = sample_options.channel_id
                else:
                    channel_id = sample_options.channel_id + str(i)
                logger.info(f"------channel_id: {channel_id}, uid: {sample_options.user_id}")
                tasks.append(asyncio.create_task(self.connect_and_release(agora_service, channel_id, sample_options)))
            self.timer =asyncio.create_task(self.my_conn_life_timer(5+random.uniform(0, 5)))
            tasks.append(self.timer)            
            await asyncio.gather(*tasks, return_exceptions=True)
            

    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        media_node_factory = agora_service.create_media_node_factory()
        local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
        audio_frame_observer = ExampleAudioFrameObserver()
        ret = local_user.register_audio_frame_observer(audio_frame_observer)
        if ret < 0:
            logger.error(f"register_audio_frame_observer failed")
            return
        video_frame_observer = ExampleVideoFrameObserver()
        local_user.register_video_frame_observer(video_frame_observer)

        pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
        audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
        yuv_data_sender = media_node_factory.create_video_frame_sender()
        video_track = agora_service.create_custom_video_track_frame(yuv_data_sender)

        audio_track.set_enabled(1)
        local_user.publish_audio(audio_track)
        video_track.set_enabled(1)
        local_user.publish_video(video_track)

        await self.send(sample_options, pcm_data_sender,yuv_data_sender)

        local_user.unpublish_audio(audio_track)
        local_user.unpublish_video(video_track)
        audio_track.set_enabled(0)
        video_track.set_enabled(0)
        local_user.unregister_audio_frame_observer()
        local_user.unregister_video_frame_observer()
        
    async def send(self,sample_options:ExampleOptions, pcm_data_sender, yuv_data_sender):
        pcm_task = asyncio.create_task(push_pcm_data_from_file(sample_options.sample_rate, sample_options.num_of_channels, pcm_data_sender, sample_options.audio_file, self.conn_exit))
        yuv_task = asyncio.create_task(push_yuv_data_from_file(sample_options.width, sample_options.height, sample_options.fps, yuv_data_sender, sample_options.video_file, self.conn_exit))
        await pcm_task
        await yuv_task
        logger.info("send finish")
    def set_conn_config(self):
        self._conn_config.auto_subscribe_video = 1
        self._conn_config.auto_subscribe_audio = 1

if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
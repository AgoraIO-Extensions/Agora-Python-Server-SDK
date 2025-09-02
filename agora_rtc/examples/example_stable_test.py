#!env python

import gc
import os
import asyncio
import random
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_audio_pcm_file import push_pcm_data_from_file
from common.push_video_yuv_file import push_yuv_data_from_file
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from observer.video_frame_observer import ExampleVideoFrameObserver
from agora.rtc.agora_service import AgoraService
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.local_user import LocalUser
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_send_pcm_yuv.py --appId=xxx --channelId=xxx --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self, con_config: RTCConnConfig, publish_config: RtcConnectionPublishConfig):
        super().__init__(con_config, publish_config)
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

    async def create_connections(self, sample_options: ExampleOptions, agora_service):
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
            self.timer = asyncio.create_task(self.my_conn_life_timer(5+random.uniform(0, 5)))
            tasks.append(self.timer)
            await asyncio.gather(*tasks, return_exceptions=True)
            gc.collect()
            print(gc.isenabled())

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        
        local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
        audio_frame_observer = ExampleAudioFrameObserver(save_to_disk=sample_options.save_to_disk)
        ret = connection.register_audio_frame_observer(audio_frame_observer,0,None)
       
        video_frame_observer = ExampleVideoFrameObserver(save_to_disk=sample_options.save_to_disk)
        connection.register_video_frame_observer(video_frame_observer)

        connection.publish_audio()
        connection.publish_video()

        connection.send_stream_message(b"hello")

        await self.send(sample_options, connection)
    def set_serv_config(self):
        self._serv_config.enable_video = 1
        pass

    async def send(self, sample_options: ExampleOptions, connection: RTCConnection):
        pcm_task = asyncio.create_task(push_pcm_data_from_file(sample_options.sample_rate, sample_options.num_of_channels, connection, sample_options.audio_file, self.conn_exit))
        yuv_task = asyncio.create_task(push_yuv_data_from_file(sample_options.width, sample_options.height, sample_options.fps, connection, sample_options.video_file, self.conn_exit))
        await pcm_task
        await yuv_task
        logger.info("send finish")

    # def set_conn_config(self):
    #     self._conn_config.auto_subscribe_video = 1
    #     self._conn_config.auto_subscribe_audio = 1


async def run():
    sample_options = parse_args_example()
    sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
    )
    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=1,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )
    publish_config = RtcConnectionPublishConfig(
        audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
        audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_YUV,
        is_publish_audio=True,
        is_publish_video=True,
        video_encoded_image_sender_options=SenderOptions(
            codec_type=VideoCodecType.VIDEO_CODEC_H264,
        ),
    )
    rtc = RTCProcessIMPL(con_config, publish_config)
   
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


if __name__ == '__main__':
    logger.warning(f"Main process ID: {os.getpid()}")
    asyncio.run(run())

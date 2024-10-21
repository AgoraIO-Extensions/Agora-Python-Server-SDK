#!env python

# coding=utf-8
from common.path_utils import get_log_path_with_filename
from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
from agora.rtc.agora_base import *
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from observer.local_user_observer import ExampleLocalUserObserver
from observer.connection_observer import ExampleConnectionObserver
from common.parse_args import parse_args_example
import asyncio
import signal
import os
import time
import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# run this example： mode 0 or 1. 0: no delay, 1: with delay. default delay value =180ms
# python agora_rtc/examples/example_audio_pcm_loopback.py --appId=xxx --channelId=xxx --mode=1
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")


class ExampleAudioFrameObserver(IAudioFrameObserver):
    def __init__(self, pcm_data_sender: AudioPcmDataSender, loop, enable_delay_mode=True) -> None:
        self._loop = loop
        self._pcm_data_sender = pcm_data_sender
        # for delay test to verify sdk's inner delay
        self._last_push_time = time.time()*1000  # in ms
        self._data = bytearray()
        self._is_delay_pushed = False
        self._enable_delay_mode = enable_delay_mode  # default to true

    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_record_audio_frame")
        return 0

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame):
        logger.info(f"on_playback_audio_frame_before_mixing: {type(audio_frame.buffer)}")
        frame = PcmAudioFrame(
            data=audio_frame.buffer,
            timestamp=0,
            samples_per_channel=160,
            bytes_per_sample=2,
            number_of_channels=1,
            sample_rate=16000
        )

        # self._loop.call_soon_threadsafe(
        #     self._pcm_data_sender.send_audio_pcm_data,frame
        # )
        self._pcm_data_sender.send_audio_pcm_data(frame)
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0


async def push_init_pcm(pcm_sender: AudioPcmDataSender):
    packs = 18
    data = bytearray(320*packs)
    frame = PcmAudioFrame()
    frame.data = data
    frame.timestamp = 0
    frame.samples_per_channel = 160*packs
    frame.bytes_per_sample = 2
    frame.number_of_channels = 1
    frame.sample_rate = 16000
    pcm_sender.send_audio_pcm_data(frame)
    await asyncio.sleep(1)


async def run_example():
    loop = asyncio.get_event_loop()
    _exit = loop.create_future()

    def handle_signal():
        _exit.set_result(None)
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)

    # ---------------1. Init SDK
    config = AgoraServiceConfig()
    config.appid = sample_options.app_id
    config.log_path = get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0])
    agora_service = AgoraService()
    agora_service.initialize(config)

    # ---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)

    media_node_factory = agora_service.create_media_node_factory()
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

    local_user = connection.get_local_user()
    local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
    local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    local_user.subscribe_all_audio()
    localuser_observer = ExampleLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)

    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
    audio_track.set_send_delay_ms(10)
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)
    # logger.info(f"push_init_pcm: before time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}")
    # await push_init_pcm(pcm_data_sender)
    # logger.info(f"rpush_init_pcm: after time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}")
    audio_frame_observer = ExampleAudioFrameObserver(pcm_data_sender, loop, True if sample_options.mode == 1 else False)
    local_user.register_audio_frame_observer(audio_frame_observer)

    await _exit
    local_user.unpublish_audio(audio_track)
    audio_track.set_enabled(0)
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    logger.info("connection release")

    agora_service.release()
    logger.info("agora_service release")


if __name__ == "__main__":
    asyncio.run(run_example())

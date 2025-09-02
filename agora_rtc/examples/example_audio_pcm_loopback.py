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
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# run this example： mode 0 or 1. 0: no delay, 1: with delay. default delay value =180ms
# python agora_rtc/examples/example_audio_pcm_loopback.py --appId=xxx --channelId=xxx --mode=1
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")


class ExampleAudioFrameObserver(IAudioFrameObserver):
    def __init__(self, connection, loop, enable_delay_mode=True) -> None:
        self._loop = loop
        self._connection = connection
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

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame, vad_result_state: int, vad_result_bytearray: bytearray):
        # logger.info(f"on_playback_audio_frame_before_mixing: {audio_frame}")
       
        self._loop.call_soon_threadsafe(
            self._connection.push_audio_pcm_data,audio_frame.buffer, 16000, 1
         )
        #self._connection.push_audio_pcm_data(audio_frame.buffer, 16000, 1)
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


async def run_example(sample_options):
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
        is_publish_audio=True,
        is_publish_video=False,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_NONE,
        video_encoded_image_sender_options=SenderOptions(target_bitrate=4160, cc_mode=TCcMode.CC_ENABLED, codec_type=VideoCodecType.VIDEO_CODEC_H264)
    )
    connection = agora_service.create_rtc_connection(con_config, publish_config)

   
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.app_id, sample_options.channel_id, sample_options.user_id)
    print(f"connect success: {sample_options.app_id}, {sample_options.channel_id}, {sample_options.user_id}")

    local_user = connection.get_local_user()
    local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    localuser_observer = ExampleLocalUserObserver()
    connection.register_local_user_observer(localuser_observer)

    connection.publish_audio()
    # logger.info(f"push_init_pcm: before time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}")
    # await push_init_pcm(pcm_data_sender)
    # logger.info(f"rpush_init_pcm: after time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}")
    audio_frame_observer = ExampleAudioFrameObserver(connection, loop, True if sample_options.mode == 1 else False)
    #in this example, we only test loopback,so disable vad
    connection.register_audio_frame_observer(audio_frame_observer, 0 ,None)

    await _exit
    
    connection.disconnect()
    connection.release()
    logger.info("connection release")

    agora_service.release()

    logger.info("agora_service release")


if __name__ == "__main__":
    sample_options = parse_args_example()
    asyncio.run(run_example(sample_options))

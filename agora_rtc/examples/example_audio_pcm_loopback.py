#!env python

#coding=utf-8
import asyncio
import signal
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import ExampleConnectionObserver
# from observer.audio_frame_observer import ExampleAudioFrameObserver
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.audio_encoded_frame_sender import EncodedAudioFrame
from agora.rtc.agora_base import *
from common.audio_consumer import AudioStreamConsumer
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame

# run this example
# python agora_rtc/examples/example_audio_pcm_loopback.py --appId=xxx --channelId=xxx
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")
from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame

class ExampleAudioFrameObserver(IAudioFrameObserver):
    def __init__(self, pcm_data_sender, loop) -> None:
        self._loop = loop
        self._pcm_data_sender = pcm_data_sender

    def on_record_audio_frame(self, agora_local_user ,channelId, frame):        
        logger.info(f"on_record_audio_frame")
        return 0
    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):        
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame):
        # logger.info(f"on_playback_audio_frame_before_mixing:{threading.current_thread().ident}, {len(audio_frame.buffer)}")
        frame = PcmAudioFrame()
        frame.data = audio_frame.buffer
        frame.timestamp = 0
        frame.samples_per_channel = 160
        frame.bytes_per_sample = 2
        frame.number_of_channels = 1
        frame.sample_rate = 16000        
        self._loop.call_soon_threadsafe(
            self._pcm_data_sender.send_audio_pcm_data,frame
        )
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")        
        return 0

async def run_example():
    loop = asyncio.get_event_loop()
    _exit = loop.create_future()
    def handle_signal():
        _exit.set_result(None)
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)

    #---------------1. Init SDK
    config = AgoraServiceConfig()
    config.appid = sample_options.app_id
    config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])
    agora_service = AgoraService()
    agora_service.initialize(config)

    #---------------2. Create Connection
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
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)

    audio_frame_observer = ExampleAudioFrameObserver(pcm_data_sender, loop)
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
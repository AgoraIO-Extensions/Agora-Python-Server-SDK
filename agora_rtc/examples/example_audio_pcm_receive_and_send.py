#!env python

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_audio_pcm_file import push_pcm_data_from_file
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_pcm_receive.py --appId=xxx --channelId=xxx


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        media_node_factory = agora_service.create_media_node_factory()
        local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
        audio_frame_observer = ExampleAudioFrameObserver(save_to_disk=sample_options.save_to_disk)
        ret = local_user.register_audio_frame_observer(audio_frame_observer)
        if ret < 0:
            logger.error(f"register_audio_frame_observer failed")
            return
        pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
        audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
        audio_track.set_enabled(1)
        local_user.publish_audio(audio_track)

        await self.send(sample_options, pcm_data_sender)

        local_user.unpublish_audio(audio_track)
        audio_track.set_enabled(0)
        local_user.unregister_audio_frame_observer()

        pcm_data_sender.release()
        audio_track.release()
        media_node_factory.release()

        pcm_data_sender = None
        audio_track = None
        media_node_factory = None
        audio_frame_observer = None

    async def send(self, sample_options: ExampleOptions, pcm_data_sender):
        pcm_task = asyncio.create_task(push_pcm_data_from_file(sample_options.sample_rate, sample_options.num_of_channels, pcm_data_sender, sample_options.audio_file, self._exit))
        await pcm_task
        logger.info("send finish")

    def set_conn_config(self):
        self._conn_config.auto_subscribe_audio = 1


async def run():
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


if __name__ == '__main__':
    asyncio.run(run())

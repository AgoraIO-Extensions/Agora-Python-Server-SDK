#!env python

# coding=utf-8

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_audio_encoded_file import push_encoded_audio_from_file
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService
from agora.rtc.agora_base import *
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.local_user import LocalUser
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_encoded_send.py --appId=xxx --channelId=xxx --audioFile=./test_data/demo.aac


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self, conn_config: RTCConnConfig = None, publish_config: RtcConnectionPublishConfig = None):
        super().__init__(conn_config, publish_config)

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        connection.publish_audio()
        await self.send(sample_options, connection)
        
    async def send(self, sample_options: ExampleOptions, connection: RTCConnection):
        audio_task = asyncio.create_task(push_encoded_audio_from_file(connection, sample_options.audio_file, self._exit))
        await audio_task
        logger.info("send finish")


async def run():
    sample_options = parse_args_example()
    publish_config = RtcConnectionPublishConfig(
         audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
         audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
         is_publish_audio=True,
        is_publish_video=False,
            audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_ENCODED_PCM,
            video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_YUV,
            video_encoded_image_sender_options=SenderOptions(
                target_bitrate=4160,
                cc_mode=TCcMode.CC_ENABLED,
                codec_type=VideoCodecType.VIDEO_CODEC_H264,
            )
    )
    rtc = RTCProcessIMPL(conn_config=None, publish_config=publish_config)
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))

if __name__ == '__main__':
    asyncio.run(run())

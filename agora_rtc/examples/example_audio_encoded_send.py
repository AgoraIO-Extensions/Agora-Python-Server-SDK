#!env python

#coding=utf-8

import os
import asyncio
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from common.push_audio_encoded_file import push_encoded_audio_from_file
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_encoded_send.py --appId=xxx --channelId=xxx --audioFile=./test_data/demo.aac

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        media_node_factory = agora_service.create_media_node_factory()
        audio_sender = media_node_factory.create_audio_encoded_frame_sender()
        if not audio_sender:
            logger.error("create audio sender failed")
            exit(1)
        audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 1)
        if not audio_track:
            logger.error("create audio track failed")
            exit(1)
        audio_track.set_enabled(1)
        local_user.publish_audio(audio_track)
        await self.send(sample_options, audio_sender)        
        local_user.unpublish_audio(audio_track)
        audio_track.set_enabled(0)

    async def send(self,sample_options:ExampleOptions, audio_sender):
        audio_task = asyncio.create_task(push_encoded_audio_from_file(audio_sender, sample_options.audio_file, self._exit))
        await audio_task
        logger.info("send finish")

if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
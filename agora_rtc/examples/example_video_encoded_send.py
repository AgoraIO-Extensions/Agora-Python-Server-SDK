#!env python

# coding=utf-8

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_video_encoded_file import push_encoded_video_from_file
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection, SenderOptions
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_video_encoded_send.py --appId=xxx --channelId=xxx --videoFile=./test_data/send_video.h264


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        media_node_factory = agora_service.create_media_node_factory()
        video_sender = media_node_factory.create_video_encoded_image_sender()
        if not video_sender:
            logger.error("create video sender failed")
            exit(1)
        sender_options = SenderOptions(
            cc_mode=TCcMode.CC_ENABLED,
            codec_type=VideoCodecType.VIDEO_CODEC_H264,
            target_bitrate=640)
        video_track = agora_service.create_custom_video_track_encoded(video_sender, sender_options)
        if not video_track:
            logger.error("create video track failed")
            exit(1)
        video_track.set_enabled(1)
        local_user.publish_video(video_track)
        await self.send(sample_options, video_sender)
        local_user.unpublish_video(video_track)
        video_track.set_enabled(0)

        video_sender.release()
        video_track.release()
        media_node_factory.release()

        video_sender = None
        video_track = None
        media_node_factory = None

    async def send(self, sample_options: ExampleOptions, video_sender):
        video_task = asyncio.create_task(push_encoded_video_from_file(video_sender, sample_options.video_file, self._exit))
        await video_task
        logger.info("send finish")

    def set_serv_config(self):
        self._serv_config.enable_video = 1


async def run():
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


if __name__ == '__main__':
    asyncio.run(run())

# coding=utf-8

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_video_yuv_file import push_yuv_data_from_file,push_jpeg_from_file
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
import logging
import signal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example

# python examples/example_jpeg_send.py --appId=you_app_id --channelId=you_channelid --dir=/Users/weihognqin/Downloads/zhipusource --width=720 --height=1280 --fps=30 --connectionNumber=1

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        media_node_factory = agora_service.create_media_node_factory()
        yuv_data_sender = media_node_factory.create_video_frame_sender()
        video_track = agora_service.create_custom_video_track_frame(yuv_data_sender)
        video_config = VideoEncoderConfiguration(
            frame_rate=sample_options.fps,
            dimensions=VideoDimensions(
                width=sample_options.width,
                height=sample_options.height
            ),
            #disable or enable alpha encoding 
            #case1: enable alpha encoding:
                # 1. encode_alpha = 1 
                # 2. set ExternalVideoFrame::alpha_buffer to a buffer
            #case2: disable alpha encoding:
                #1. encode_alpha = 0
                #2. set ExternalVideoFrame::alpha_buffer = None
            encode_alpha=0,
            #bitrate=8500
        )
        video_track.set_video_encoder_configuration(video_config)

        video_track.set_enabled(1)
        local_user.publish_video(video_track)

        await self.send(sample_options, yuv_data_sender)

        local_user.unpublish_video(video_track)
        video_track.set_enabled(0)

        yuv_data_sender.release()
        video_track.release()
        media_node_factory.release()

        yuv_data_sender = None
        video_track = None
        media_node_factory = None

    async def send(self, sample_options: ExampleOptions, yuv_data_sender):
        #dir_path = '/Users/weihognqin/Downloads/zhipusource'  #format like this:
        dir_path = sample_options.dir_path
        yuv_task = asyncio.create_task(push_jpeg_from_file(dir_path, yuv_data_sender,  sample_options.fps, self._exit))
        await yuv_task
        logger.info("send finish")

    def set_serv_config(self):
        self._serv_config.enable_video = 1

def handle_signal():
    global _exit
    _exit.set_result(None)
async def run():
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


 
if __name__ == '__main__':
    asyncio.run(run())
 

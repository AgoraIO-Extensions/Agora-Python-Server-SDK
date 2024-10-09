#!env python

import os
import asyncio
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
from observer.video_encoded_frame_observer import ExampleVideoEncodedFrameObserver
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_video_encoded_receive.py --appId=xxx --channelId=xxx

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        video_subscription_options = VideoSubscriptionOptions(
                    type = VIDEO_STREAM_TYPE.VIDEO_STREAM_HIGH,
                    encodedFrameOnly = 1
        )
        local_user.subscribe_all_video(video_subscription_options)
        video_encoded_frame_observer = ExampleVideoEncodedFrameObserver()
        ret = local_user.register_video_encoded_frame_observer(video_encoded_frame_observer)
        if ret < 0:
            logger.error(f"register_video_encoded_frame_observer failed")
            return
        await self._exit.wait()        
        local_user.unregister_video_encoded_frame_observer()

    def set_serv_config(self):
        self._serv_config.enable_video = 1

if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
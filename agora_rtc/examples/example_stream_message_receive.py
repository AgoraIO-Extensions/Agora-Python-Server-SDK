#!/usr/bin/env python

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_stream_message_receive.py --appId=xxx --channelId=xxx


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        await self._exit.wait()


if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0])))

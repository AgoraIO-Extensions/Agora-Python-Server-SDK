import os
import asyncio
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_agora_parameter.py --appId=xxx --channelId=xxx

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):

        stream_id = connection.create_data_stream(False, False)
        stream_id2 = connection.create_data_stream(False, False)
        logger.info(f"stream_id: {stream_id}")
        idx = 0
        while not self._exit.is_set():
            msg1 = sample_options.msg + " to data_stream:" +  str(stream_id) + " idx:" +  str(idx)
            msg2 = sample_options.msg + " to data_stream:" +  str(stream_id2) + " idx:" +  str(idx)
            ret = connection.send_stream_message(stream_id, msg1)
            logger.info(f"send_stream_message: {msg1}, ret: {ret}")
            ret = connection.send_stream_message(stream_id2, msg2)
            logger.info(f"send_stream_message: {msg2}, ret: {ret}")
            await asyncio.sleep(1)
            idx += 1
        
if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
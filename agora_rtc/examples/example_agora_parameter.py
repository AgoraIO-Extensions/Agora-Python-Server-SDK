import os
import asyncio
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from observer.video_frame_observer import ExampleVideoFrameObserver
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_agora_parameter.py --appId=xxx --channelId=xxx

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        agora_parameter = connection.get_agora_parameter()
        logger.info(f"audio_pcm_data_send_mode: {agora_parameter.get_string('audio_pcm_data_send_mode')}")
        logger.info(f"ret: {agora_parameter.set_parameters('{\"audio_pcm_data_send_mode\":1}')}")
        logger.info(f"audio_pcm_data_send_mode: {agora_parameter.get_string('audio_pcm_data_send_mode')}")

        agora_parameter = connection.get_agora_parameter()
        logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")
        logger.info(f"ret: {agora_parameter.set_parameters('{\"che.audio.aec.enable\":true}')}")
        logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")
        logger.info(f"ret: {agora_parameter.set_parameters('{\"che.audio.aec.enable\":false}')}")
        logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")

        agora_parameter = connection.get_agora_parameter()
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
        logger.info(f"ret: {agora_parameter.set_parameters('{\"rtc.enable_nasa2\":1}')}")
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
        logger.info(f"ret: {agora_parameter.set_parameters('{\"rtc.enable_nasa2\":0}')}")
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")

        agora_parameter = connection.get_agora_parameter()
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
        logger.info(f"ret: {agora_parameter.set_bool('rtc.enable_nasa2', 0)}")
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
        logger.info(f"ret: {agora_parameter.set_bool('rtc.enable_nasa2', 1)}")
        logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")

        agora_parameter = connection.get_agora_parameter()
        logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")
        logger.info(f"ret: {agora_parameter.set_bool('rtc.test111', 0)}")
        logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")
        logger.info(f"ret: {agora_parameter.set_bool('rtc.test111', 1)}")
        logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")
    def set_serv_config(self):
        self._serv_config.area_code = AreaCode.AREA_CODE_CN.value | AreaCode.AREA_CODE_JP.value
        logger.info(f"config.area_code: {self._serv_config.area_code}")



if __name__ == '__main__':
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
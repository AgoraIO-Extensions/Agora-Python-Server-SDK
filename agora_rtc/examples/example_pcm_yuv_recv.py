import os
import asyncio
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example, ExampleOptions
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from observer.video_frame_observer import ExampleVideoFrameObserver
from agora.rtc.agora_service import AgoraService, LocalUser, RTCConnection
from agora.rtc.agora_base import *
# from observer.local_user_observer import ExampleLocalUserObserver

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_audio_pcm_receive.py --appId=xxx --channelId=xxx

class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self):
        super().__init__()
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        logger.info(f"setup_receiver --- app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

        local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
        audio_frame_observer = ExampleAudioFrameObserver()
        ret = local_user.register_audio_frame_observer(audio_frame_observer)
        logger.info(f"register_audio_frame_observer ret:{ret}")

        video_frame_observer = ExampleVideoFrameObserver()
        local_user.register_video_frame_observer(video_frame_observer)

        await self._exit.wait()
        
        local_user.unregister_audio_frame_observer()
        local_user.unregister_video_frame_observer()

    def set_conn_config(self):
        self._conn_config.auto_subscribe_video = 1
        self._conn_config.auto_subscribe_audio = 1
        logger.info(f"auto_subscribe_video: {self._conn_config.auto_subscribe_video}, auto_subscribe_audio: {self._conn_config.auto_subscribe_audio}")
        
    def set_serv_config(self):
        self._serv_config.enable_video = 1

if __name__ == '__main__':
    
    sample_options = parse_args_example()
    rtc = RTCProcessIMPL()
    asyncio.run(rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id,os.path.splitext(__file__)[0])))
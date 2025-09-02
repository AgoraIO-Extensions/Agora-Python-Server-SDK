#!env python

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_audio_pcm_file import push_pcm_data_from_file
from common.example_base import RTCBaseProcess
from observer.audio_frame_observer import ExampleAudioFrameObserver
from agora.rtc.agora_service import AgoraService
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.local_user import LocalUser
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python3 agora_rtc/examples/example_audio_pcm_receive_and_send.py --appId={} --channelId= {} --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self, conn_config: RTCConnConfig = None, publish_config: RtcConnectionPublishConfig = None):
        super().__init__(conn_config, publish_config)

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        local_user = connection.get_local_user()
        local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)
        audio_frame_observer = ExampleAudioFrameObserver(save_to_disk=sample_options.save_to_disk)
        #note: disable vad in this sample, but you can set to 1 with an vadconfigureV2 to enable it
        ret = connection.register_audio_frame_observer(audio_frame_observer, 0, None)
        connection.publish_audio()

        await self.send(sample_options, connection)

        

    async def send(self, sample_options: ExampleOptions, connection: RTCConnection):
        pcm_task = asyncio.create_task(push_pcm_data_from_file(sample_options.sample_rate, sample_options.num_of_channels, connection, sample_options.audio_file, self._exit))
        await pcm_task
        logger.info("send finish")

    def set_conn_config(self):
        pass
        
async def run():
    sample_options = parse_args_example()
    publish_config = RtcConnectionPublishConfig(
        audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
        audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
        is_publish_audio=True,
        is_publish_video=False,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_NONE,
        video_encoded_image_sender_options=SenderOptions(target_bitrate=4160, cc_mode=TCcMode.CC_ENABLED, codec_type=VideoCodecType.VIDEO_CODEC_H264)
    )
    conn_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=1,
        audio_recv_media_packet=0,
        audio_subs_options=AudioSubscriptionOptions(
            packet_only=0,
            pcm_data_only=1,
            bytes_per_sample=2,
            number_of_channels=1,
            sample_rate_hz=16000
        )
    )
    rtc = RTCProcessIMPL(conn_config, publish_config)
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


if __name__ == '__main__':
    asyncio.run(run())

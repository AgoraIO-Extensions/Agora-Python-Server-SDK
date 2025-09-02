# coding=utf-8

import os
import asyncio
from common.path_utils import get_log_path_with_filename
from common.parse_args import parse_args_example, ExampleOptions
from common.push_video_yuv_file import push_yuv_data_from_file
from common.example_base import RTCBaseProcess
from agora.rtc.agora_service import AgoraService
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.local_user import LocalUser
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_video_yuv_send.py --appId=xxx --channelId=xxx --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --connectionNumber=1


class RTCProcessIMPL(RTCBaseProcess):
    def __init__(self, con_config: RTCConnConfig, publish_config: RtcConnectionPublishConfig):
        super().__init__(con_config, publish_config)

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        video_config = VideoEncoderConfiguration(
            frame_rate=sample_options.fps,
            codec_type=VideoCodecType.VIDEO_CODEC_H264,
            dimensions=VideoDimensions(
                width=sample_options.width,
                height=sample_options.height
            ),
            bitrate=sample_options.bitrate,
            min_bitrate=int(sample_options.bitrate/3),
            #disable or enable alpha encoding 
            #case1: enable alpha encoding:
                # 1. encode_alpha = 1 
                # 2. set ExternalVideoFrame::alpha_buffer to a buffer
            #case2: disable alpha encoding:
                #1. encode_alpha = 0
                #2. set ExternalVideoFrame::alpha_buffer = None
            encode_alpha=0
        )
        connection.set_video_encoder_configuration(video_config)

        connection.publish_video()
        connection.publish_audio()

        await self.send(sample_options, connection)

    async def send(self, sample_options: ExampleOptions, connection: RTCConnection):
        yuv_task = asyncio.create_task(push_yuv_data_from_file(sample_options.width, sample_options.height, sample_options.fps, connection, sample_options.video_file, self._exit))
        await yuv_task
        logger.info("send finish")

    def set_serv_config(self):
        self._serv_config.enable_video = 1


async def run():
    sample_options = parse_args_example()
    sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
    )
    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=1,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )
    publish_config = RtcConnectionPublishConfig(
        audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
        audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_YUV,
        is_publish_audio=True,
        is_publish_video=True,
        video_encoded_image_sender_options=SenderOptions(
            codec_type=VideoCodecType.VIDEO_CODEC_H264,
            target_bitrate=3600,
            cc_mode=TCcMode.CC_ENABLED,

        ),
    )
    rtc = RTCProcessIMPL(con_config, publish_config)
    await rtc.run(sample_options, get_log_path_with_filename(sample_options.channel_id, os.path.splitext(__file__)[0]))


if __name__ == '__main__':
    asyncio.run(run())

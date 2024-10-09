#coding=utf-8

import time
import os
import threading
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from common.pacer import Pacer
from observer.connection_observer import ExampleConnectionObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.video_frame_sender import ExternalVideoFrame
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_video_yuv_send.py --appId=xxx --channelId=xxx --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --connectionNumber=1
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}, video_file: {sample_options.video_file}")
            
config = AgoraServiceConfig()
config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)


def create_conn_and_send(channel_id, uid = 0):

    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

    media_node_factory = agora_service.create_media_node_factory()
    video_sender = media_node_factory.create_video_frame_sender()
    video_track = agora_service.create_custom_video_track_frame(video_sender)
    video_config = VideoEncoderConfig(
        frame_rate=sample_options.fps,
        dimensions = VideoDimensions(
            width = sample_options.width,
            height = sample_options.height
        ),
    )

    video_track.set_video_encoder_configuration(video_config)
    local_user = connection.get_local_user()
    local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)

    video_track.set_enabled(1)
    local_user.publish_video(video_track)

    sendinterval = 1/30
    pacer = Pacer(sendinterval)

    width = sample_options.width
    height = sample_options.height

    def send_test():
        count = 0
        yuv_len = int(width*height*3/2)
        frame_buf = bytearray(yuv_len)            
        with open(sample_options.video_file, "rb") as file:
            while True:            
                success = file.readinto(frame_buf)
                if not success:
                    break
                frame = ExternalVideoFrame()
                frame.buffer = frame_buf
                frame.type = 1
                frame.format = 1
                frame.stride = width
                frame.height = height
                frame.timestamp = 0
                frame.metadata = "hello metadata"
                logger.info(f"send video frame: frame.width: {frame.stride}, frame.height: {frame.height}, frame.timestamp: {frame.timestamp}, frame.metadata: {frame.metadata}")
                ret = video_sender.send_video_frame(frame)        
                count += 1
                pacer.pace()

    for i in range(1):
        send_test()

    time.sleep(2)
    local_user.unpublish_video(video_track)
    video_track.set_enabled(0)
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    logger.info("release")

threads = []
for i in range(int(sample_options.connection_number)):
    channel_id = sample_options.channel_id + str(i+1)
    logger.info(f"start: ---------------------- {channel_id}")
    thread = threading.Thread(target=create_conn_and_send, args=(channel_id, sample_options.user_id))
    thread.start()
    threads.append(thread)

    
for t in threads:
    t.join()


agora_service.release()
logger.info("end")
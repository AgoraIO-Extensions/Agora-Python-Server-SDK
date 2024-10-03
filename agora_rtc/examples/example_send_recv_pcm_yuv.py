#!env python

import time
import os
import threading
from common.path_utils import get_log_path_with_filename 
from common.pacer import Pacer
from common.parse_args import parse_args_example
from observer.connection_observer import SampleConnectionObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame
from agora.rtc.agora_base import *
from agora.rtc.video_frame_sender import ExternalVideoFrame
from observer.audio_frame_observer import SampleAudioFrameObserver
from observer.video_frame_observer import SampleVideoFrameObserver
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# run this example
# python agora_rtc/examples/example_send_pcm_yuv.py --appId=xxx --channelId=xxx --userId=xxx --connectionNumber=1 --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv --width=416 --height=240 --fps=30 --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

exit_loop = False
if sample_options.hours == 0:
    exit_loop = True
#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)
def create_conn_and_send(channel_id, uid = 0):

    #---------------2. Create Connection
    con_config = RTCConnConfig(
        auto_subscribe_video=1,
        auto_subscribe_audio=1,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)
    if not connection:
        logger.error("create connection failed")
        return
    conn_observer = SampleConnectionObserver()
    connection.register_observer(conn_observer)
    ret = connection.connect(sample_options.token, channel_id, uid)
    if ret < 0:
        logger.error(f"connect failed: {ret}")
        return
    
    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()
    if not media_node_factory:
        logger.error("create media node factory failed")
        return

    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    if not pcm_data_sender:
        logger.error("create pcm data sender failed")
        return
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
    if not audio_track:
        logger.error("create audio track failed")
        return
    # audio_track.set_max_buffer_audio_frame_number(320*2000)
    
    video_sender = media_node_factory.create_video_frame_sender()
    if not video_sender:
        logger.error("create video frame sender failed")
        return
    video_track = agora_service.create_custom_video_track_frame(video_sender)
    if not video_track:
        logger.error("create video track failed")
        return

    local_user = connection.get_local_user()
    local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
    localuser_observer = SampleLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)

    audio_frame_observer = SampleAudioFrameObserver()
    local_user.register_audio_frame_observer(audio_frame_observer)

    video_frame_observer = SampleVideoFrameObserver()
    local_user.register_video_frame_observer(video_frame_observer)

    #---------------4. Send Media Stream
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)

    video_track.set_enabled(1)
    local_user.publish_video(video_track)

    pcm_sendinterval = 0.1
    yuv_sendinterval = 1.0/sample_options.fps
    pacer_yuv = Pacer(yuv_sendinterval)
    pacer_pcm = Pacer(pcm_sendinterval)
    pcm_count = 0
    yuv_count = 0
    running = True
    last_pcm_time = 0

    def push_pcm_data_from_file(audio_file):
        nonlocal last_pcm_time, pcm_count, running
        if last_pcm_time == 0:
            last_pcm_time = time.time()
            return
    
        sendinterval = time.time() - last_pcm_time
        if sendinterval < pcm_sendinterval:
            return
        send_size = int(sample_options.sample_rate*sample_options.num_of_channels*pcm_sendinterval*2)
        frame_buf = bytearray(send_size)            
        success = audio_file.readinto(frame_buf)
        if not success:
            running = False
            return
        frame = PcmAudioFrame()
        frame.data = frame_buf
        frame.timestamp = 0
        frame.samples_per_channel = int(sample_options.sample_rate * pcm_sendinterval)
        frame.bytes_per_sample = 2
        frame.number_of_channels = sample_options.num_of_channels
        frame.sample_rate = sample_options.sample_rate
        ret = pcm_data_sender.send_audio_pcm_data(frame)
        pcm_count += 1
        logger.info(f"send pcm: count,ret={pcm_count}, {ret}, {send_size}, {pcm_sendinterval}")
        last_pcm_time = time.time()        
        pacer_pcm.pace_interval(0.1)

    width = sample_options.width
    height = sample_options.height
    yuv_len = int(width*height*3/2)
    frame_buf = bytearray(yuv_len)
    def push_video_data_from_file(video_file):
        nonlocal running, yuv_count        
        success = video_file.readinto(frame_buf)
        if not success:
            running = False
            return
        frame = ExternalVideoFrame()
        frame.buffer = frame_buf
        frame.type = 1
        frame.format = 1
        frame.stride = width
        frame.height = height
        frame.timestamp = 0
        frame.metadata = "hello metadata"
        ret = video_sender.send_video_frame(frame)        
        yuv_count += 1
        logger.info(f"send yuv: count,ret={yuv_count}, {ret}")
        pacer_yuv.pace_interval(yuv_sendinterval)

    def send_test():
        nonlocal running
        with open(sample_options.audio_file, "rb") as audio_file, open(sample_options.video_file, "rb") as video_file:
            while running:
                push_pcm_data_from_file(audio_file)
                push_video_data_from_file(video_file)

    while True:
        send_test() 
        if exit_loop:
            break
        

    local_user.unpublish_audio(audio_track)
    local_user.unpublish_video(video_track)
    audio_track.set_enabled(0)
    video_track.set_enabled(0)
    connection.unregister_observer()
    ret = connection.disconnect()
    if ret < 0:
        logger.error(f"disconnect failed: {ret}")
        return
    connection.release()
    logger.info("release")
    

threads = []
for i in range(int(sample_options.connection_number)):
    logger.info(f"channel {i}")
    channel_id = sample_options.channel_id + str(i+1)
    thread = threading.Thread(target=create_conn_and_send, args=(channel_id, sample_options.user_id))
    thread.start()
    threads.append(thread)


def time_down():
    global exit_loop
    exit_loop = True

t = int(sample_options.hours*3600)
timer = threading.Timer(t, time_down)
timer.start()


for t in threads:
    t.join()

agora_service.release()
logger.info("end")
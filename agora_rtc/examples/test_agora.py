import os
import time
import logging


import datetime
import ctypes
#from common.path_utils import get_log_path_with_filename
#from observer.connection_observer import ExampleConnectionObserver
#from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.rtc_connection import *
from agora.rtc.media_node_factory import *
from agora.rtc.audio_pcm_data_sender import *
from agora.rtc.audio_frame_observer import *
import signal
from agora.rtc.local_user import *
from agora.rtc.local_user_observer import *
import threading
from collections import deque

"""
from agora.rtc.agora_base import AudioScenarioType, ClientRoleType, ChannelProfileType
from agora.rtc.agora_service import AgoraService, AgoraServiceConfig, RTCConnConfig, AudioSubscriptionOptions
from agora.rtc.rtc_connection_observer import IRTCConnectionObserver
from agora.rtc.video_frame_observer import IVideoFrameObserver, VideoFrame
from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame
from agora.rtc.video_encoded_frame_observer import IVideoEncodedFrameObserver
"""

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup log folder
log_folder = "received_streams"
os.makedirs(log_folder, exist_ok=True)

# Receive encoded video through the on_encoded_video_frame callback and output it as a file
class SampleVideoEncodedFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self):
        super().__init__()
        self.frame_counter = {}  # Track frames by user ID
        
    def on_encoded_video_frame(self, uid, image_buffer, length, video_encoded_frame_info):
        file_path = os.path.join(log_folder, str(uid) + '.h264')
        with open(file_path, 'ab') as f:
            f.write(image_buffer[:length])
            
        # Count frames and log only every 200 frames
        if uid not in self.frame_counter:
            self.frame_counter[uid] = 0
            logger.info(f"First encoded video frame received for user {uid}")
        
        self.frame_counter[uid] += 1
        if self.frame_counter[uid] % 200 == 0:
            logger.info(f"Received encoded video frames for user {uid}, frame count: {self.frame_counter[uid]}, last frame length: {length}")
        
        return 1

# Receive YUV format video through the on_frame callback and output it as a file
class SampleVideoFrameObserver(IVideoFrameObserver):
    def __init__(self):
        super().__init__()
        self.frame_counter = {}  # Track frames by channel and user
        
    def on_frame(self, channel_id, remote_uid, frame:VideoFrame):
        print(f"Received video frame for user {remote_uid} in channel {channel_id}, size: {frame.width}x{frame.height}")
        file_path = os.path.join(log_folder, channel_id + "_" + remote_uid + '.yuv')
        y_size = frame.y_stride * frame.height
        uv_size = (frame.u_stride * frame.height) // 2
        with open(file_path, 'ab') as f:
            f.write(frame.y_buffer[:y_size])
            f.write(frame.u_buffer[:uv_size])
            f.write(frame.v_buffer[:uv_size])
            
        # Count frames and log only every 200 frames
        key = f"{channel_id}_{remote_uid}"
        if key not in self.frame_counter:
            self.frame_counter[key] = 0
            logger.info(f"First YUV video frame received for user {remote_uid} in channel {channel_id}, size: {frame.width}x{frame.height}")
        
        self.frame_counter[key] += 1
        if self.frame_counter[key] % 200 == 0:
            logger.info(f"Received YUV video frames for user {remote_uid}, frame count: {self.frame_counter[key]}, size: {frame.width}x{frame.height}")
        
        return 1

# Receive PCM format audio through the on_playback_audio_frame_before_mixing callback and output it as a file
class SampleAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super().__init__()
        self.frame_counter = {}  # Track frames by channel and user
        
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame, vad_result_state:int, vad_result_bytearray:bytearray):
        file_path = os.path.join(log_folder, channelId + "_" + uid + '.pcm')
        with open(file_path, "ab") as f:
            f.write(audio_frame.buffer)

        print(f"Received audio frame for user {uid} in channel {channelId}, length: {len(audio_frame.buffer)}")
            
        # Count frames and log only every 200 frames
        key = f"{channelId}_{uid}"
        if key not in self.frame_counter:
            self.frame_counter[key] = 0
            logger.info(f"First audio frame received for user {uid} in channel {channelId}, length: {len(audio_frame.buffer)}")
        
        self.frame_counter[key] += 1
        if self.frame_counter[key] % 200 == 0:
            logger.info(f"Received audio frames for user {uid}, frame count: {self.frame_counter[key]}, last frame length: {len(audio_frame.buffer)}")
        
        return 1


class ConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super().__init__()
        
    def on_connection_state_changed(self, channel_id, state, reason):
        logger.info(f"Connection state changed - Channel: {channel_id}, State: {state}, Reason: {reason}")
        
    def on_user_joined(self, channel_id, user_id):
        logger.info(f"User joined - Channel: {channel_id}, User ID: {user_id}")
        
    def on_user_left(self, channel_id, user_id, reason):
        logger.info(f"User left - Channel: {channel_id}, User ID: {user_id}, Reason: {reason}")
        
    def on_token_privilege_will_expire(self, channel_id, token):
        logger.warning(f"Token will expire soon - Channel: {channel_id}")
        
    def on_token_privilege_did_expire(self, channel_id):
        logger.warning(f"Token has expired - Channel: {channel_id}")

class StreamReceiveTest:
    def __init__(self, app_id, channel_id, token, uid):
        self.app_id = app_id
        self.channel_id = channel_id
        self.token = token
        self.uid = uid
        self.agora_service = None
        self.connection = None
        self.connection_observer = None
        self.video_observer = None
        self.audio_observer = None
        self.encoded_video_observer = None
        self.local_user = None
        
    def initialize(self):
        # Create service instance
        self.agora_service = AgoraService()

        # Configure service
        config = AgoraServiceConfig()
        config.appid = self.app_id
        config.enable_video = 1 #added by wei, if not set, the video will not be received
        config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
        result = self.agora_service.initialize(config)
        if result < 0:
            logger.error(f"Failed to initialize Agora service: {result}")
            return False
            
        logger.info("Agora service initialized successfully")

	# Set log path
        ret = self.agora_service.set_log_file("/tmp/agora_moderation.log")
        if ret == 0:
           logger.info(f"Set log file to /tmp/agora_moderation.log")
        else:
           logger.error(f"Failed to set log file")
        
        # Configure connection parameters
        # add by wei, if not set, the video will not be received
        sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
        )
        con_config = RTCConnConfig(
            client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,  # Receive stream as audience role
            channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,  # Live broadcasting mode
	    auto_subscribe_audio=1,
            auto_subscribe_video=1,
            audio_recv_media_packet=0,
            video_recv_media_packet=0,
            enable_audio_recording_or_playout=0,
            audio_subs_options=sub_opt
        )
        
        # Create connection instance
        self.connection = self.agora_service.create_rtc_connection(con_config)
        if not self.connection:
            logger.error("Failed to create RTC connection")
            return False
            
        # Register connection observer
        self.connection_observer = ConnectionObserver()
        self.connection.register_observer(self.connection_observer)
        
        logger.info("Connection observer registered successfully")
        return True
    
    def join_channel(self):
        # Connect to channel
        logger.info(f"Connecting to channel: {self.channel_id}, User ID: 0")
        ret = self.connection.connect(self.token, self.channel_id, str(0))
        if ret < 0:
            logger.error(f"Failed to connect to channel: {ret}")
            return False
            
        # Get local user object
        self.local_user = self.connection.get_local_user()
        if not self.local_user:
            logger.error("Failed to get local user object")
            return False
        
        # Register video frame observer
        self.video_observer = SampleVideoFrameObserver()
        result = self.local_user.register_video_frame_observer(self.video_observer)
        if result < 0:
            logger.error(f"Failed to register video frame observer: {result}")
        else:
            logger.info("Video frame observer registered successfully")
        #self.local_user.subscribe_video(str(self.uid), None)
        #logger.info(f"local_user subscribe video for user {self.uid} !!!!!")
        
        
        # Register encoded video frame observer
        #self.encoded_video_observer = SampleVideoEncodedFrameObserver()
        #result = self.local_user.register_video_encoded_frame_observer(self.encoded_video_observer)
        #if result < 0:
        #    logger.error(f"Failed to register encoded video frame observer: {result}")
        #else:
        #    logger.info("Encoded video frame observer registered successfully")
        
        # Register audio frame observer
       	self.audio_observer = SampleAudioFrameObserver()
        self.local_user.set_playback_audio_frame_before_mixing_parameters(1, 16000)  # 单声道，16kHz采样率
        result = self.local_user.register_audio_frame_observer(self.audio_observer, 0, None)
        if result < 0:
            logger.error(f"Failed to register audio frame observer: {result}")
        else:
            logger.info("Audio frame observer registered successfully")
        #self.local_user.subscribe_audio(str(self.uid))
        #logger.info(f"local_user subscribe audio for user {self.uid} !!!!!")
        
        logger.info(f"Successfully connected to channel {self.channel_id}")
        return True
    
    def leave_channel(self):
        self.local_user.unregister_audio_frame_observer()
        self.local_user.unregister_local_user_observer()
        self.local_user.unregister_video_frame_observer()
        

        self.connection.disconnect()
        self.connection.unregister_observer()

        self.local_user.release()
        self.connection.release()
    

    
        
        
        self.agora_service.release()
    
        #set to None
       
        self.audio_observer = None
        self.video_observer = None
        
        self.local_user = None
        self.connection = None
        self.agora_service = None
        # Unregister observers
        if self.local_user:
            if self.video_observer:
                self.local_user.unregister_video_frame_observer()
            if self.encoded_video_observer:
                self.local_user.unregister_video_encoded_frame_observer()
            if self.audio_observer:
                self.local_user.unregister_audio_frame_observer()
            logger.info("Unregistered all observers")
        
        if self.connection:
            if self.connection_observer:
                self.connection.unregister_observer()
            self.connection.disconnect()
            logger.info("Disconnected from channel")
        
        if self.agora_service:
            self.agora_service.release()
            logger.info("Released Agora service resources")

def main():
    # Use provided parameters
    S3_BUCKET_NAME = "agora-moderation"
    os.environ['MODERATION_BUCKET_NAME'] = S3_BUCKET_NAME
    logger.info(f"S3 bucket set: {S3_BUCKET_NAME}")

   
    # penny 
    #app_id = "fa50196782894da68faa6b495719315a"
    #channel_id = "ContentModeration"
    #user_id = 12321
    #token = "007eJxTYHgaenpVTtrd4sOFlnwLczYeXfN7o+3rEvuUtWZex79e5wlTYDCxSLZITTRLSU40TjExMEhNMk80trBMNjFJSzY2MkgxaA1nyGgIZGRY5PWehZEBAkF8Xoasyvjc/JTUosSSzPw8BgYAQsslKw==" 

    # jyzhan
    app_id = "48c8ea6dca3d400eb7a389c44fc320d0"
    channel_id = "jy_moderation"
    user_id = 0 #65456
    token = "007eJxTYJA8rcDc8sf6iXHsyYZ91yYHznD4cNki8reYm+6OLZvLTrgqMJhYJFukJpqlJCcap5gYGKQmmScaW1gmm5ikJRsbGaQYvD2rl9EQyMhw7+IZBkYoBPF5GbIq43PzU1KLEksy8/MYGAD8xiWU"
  
    # Create and initialize test instance
    test = StreamReceiveTest(app_id, channel_id, token, user_id)
    
    try:
        # Initialize Agora service
        if not test.initialize():
            logger.error("Initialization failed, exiting test")
            return
        
        # Join channel and register observers
        if not test.join_channel():
            logger.error("Failed to join channel, exiting test")
            return
        
        # Wait for stream data
        logger.info("Waiting to receive stream data, press Ctrl+C to exit...")
        test_duration = 6000000  # seconds, set to 5 minutes
        logger.info(f"Will continue receiving for {test_duration} seconds...")
        
        start_time = time.time()
        while time.time() - start_time < test_duration:
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            if elapsed % 10 == 0:  # Print progress every 10 seconds
                logger.info(f"Running for: {elapsed} seconds, remaining: {test_duration - elapsed} seconds")
            
    except KeyboardInterrupt:
        logger.info("User interrupted, exiting...")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        # Leave channel and release resources
        test.leave_channel()
        
        # Check if any stream files were received
        files = os.listdir(log_folder)
        if files:
            logger.info(f"Successfully received stream files, total: {len(files)}:")
            for file in files:
                file_path = os.path.join(log_folder, file)
                file_size = os.path.getsize(file_path)
                logger.info(f"- {file}: {file_size} bytes")
        else:
            logger.warning("No stream files received, please check if the channel ID and APP_ID are correct, and if there are active streams in the channel.")

if __name__ == "__main__":
    main()

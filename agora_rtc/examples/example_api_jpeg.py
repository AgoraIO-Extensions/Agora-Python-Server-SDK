# coding=utf-8

import time
import datetime
import ctypes
from common.path_utils import get_log_path_with_filename
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
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
from queue import Queue



# import voicesentencedetection
from agora.rtc.voice_detection import *

from agora.rtc.utils.vad_dump import VadDump
from common.push_audio_pcm_file import file_to_consumer
from agora.rtc.utils.audio_consumer import AudioConsumer

import gc
import asyncio
from math import sqrt,log10
# memey leak test
#from memory_profiler import profile


# connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    log_path = "./log/agorasdk.log"
    return log_path

'''
event manager
'''
#global variable
g_send_intra_request_time = 0



# observer
#@profile

class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self, conn: RTCConnection, is_loop: int, aduio_queue: Queue):
        #super(MyAudioFrameObserver, self).__init__()
        self._silence_pack = bytearray(320)
        self._conn = conn
        self._is_loop = is_loop
        self._audio_queue = aduio_queue
        """
        # Recommended  configurations:  
            # For not-so-noisy environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -50)  
            # For noisy environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -40)  
            # For high-noise environments, use this configuration: (16, 30, 50, 0.7, 0.5, 70, 70, -30)
         """

        self._vad_instance = AudioVadV2(AudioVadConfigV2(16, 30, 50, 0.7, 0.5, 70, 70, -50))
        self._dump_path = './vad'
        self._vad_dump = VadDump(self._dump_path)
        self._vad_dump.open()
        self._processor = None
        #self._processor = AsyncAudioFrameProcessor()
        #self._processor.start()
        pass

    def initialize(self):
         if self._processor:
            self._processor.start()

    def cleanup(self):
        if self._processor:
            self._processor.stop()

    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_record_audio_frame")
        return 0

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        #print(f"on_playback_audio_frame: {len(frame.buffer)}")
        return 0

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0


    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame, vad_result_state:int, vad_result_bytearray:bytearray):
        # Create a task to enqueue the frame
        #asyncio.create_task(self._processor.enqueue_frame(audio_frame, vad_result_bytearray, vad_result_state))
        
        self._vad_dump.write(audio_frame, vad_result_bytearray, vad_result_state)
        if vad_result_bytearray is not None:
            if vad_result_state == 1:
                # start speaking: then start send bytes(not audio_frame) to ARS
                print(f"vad v2 start speaking{uid}")
            elif vad_result_state == 2:
                # continue send bytes to ARS
                pass
            elif vad_result_state == 3:
                # stop speaking: send bytes to ARS and then then stop  ARS
                print(f"vad v2 stop speaking:{uid}")
            else:
                logger.info(f"unknown state:{uid}")
        if (self._is_loop == 1):
            self._audio_queue.put(audio_frame)
            #ret = self._conn.push_audio_pcm_data(audio_frame.buffer, audio_frame.samples_per_sec, audio_frame.channels)
            #print(f"push_audio_pcm_data ret: {ret}")
       
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0

    def __del__(self):
        if self._processor:
            self._processor.stop()

'''
local user observer
'''

#@profile
class MyLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self, local_user, event_queue: Queue):
        super().__init__()
        self._local_user = local_user
        self._event_queue = event_queue
    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        logger.info(f"on_stream_message, user_id={user_id}, stream_id={stream_id}, data={data}, length={length}")
        self._event_queue.put(bytearray(data))
        pass

    def on_user_info_updated(self, local_user, user_id, msg, val):
        logger.info(f"on_user_info_updated, user_id={user_id}, msg={msg}, val={val}")
        pass
    
    def on_audio_volume_indication(self, agora_local_user, speakers_list, speaker_number, total_volume):
        #print(f"xxxxxx xxxx on_audio_volume_indication: number = {speaker_number },totoal volume = {total_volume}")
        for i in range(speaker_number):
            speaker = speakers_list[i]
            #print("on vulume indication: ", speaker)
        pass
    """
    # how to define remote user's Mute /UnMute state:
    for (reason ==5 and state ==0) : remote user is Muted
    for (reason ==6 and state ==1 ) : remote user is UnMuted

    #on_user_audio_track_state_changed
    # if reason==5, indicate the remote user is muted by self
    # if reason==6, indicate the remote user is unmuted by self
    # an sample for state change activity:
    # 1. when remote user call MuteAudio: the state is :(will trigger only once)
    on_user_audio_track_state_changed: user_id=182883922,state=0, reason=5, elapsed=275780
    # 2. when remote user call UnmuteAudio: the state is : (will trigger twice)
    on_user_audio_track_state_changed: user_id=182883922,state=1, reason=6, elapsed=275780
    on_user_audio_track_state_changed: user_id=182883922,state=2, reason=6, elapsed=290281
    """
    def on_user_audio_track_state_changed(self, agora_local_user, user_id, agora_remote_audio_track, state, reason, elapsed):
        print(f"on_user_audio_track_state_changed: user_id={user_id},state={state}, reason={reason}, elapsed={elapsed}")
        pass
    def on_audio_meta_data_received(self, agora_local_user, user_id, data):
        now = time.time()*1000
        print(f"on_audio_meta_data_received: user_id={user_id}, data={data},now={now}")
        for b in data:
            print(b, end=" ")
        print()
        #self._local_user.send_audio_meta_data( data)
        pass
    def on_local_audio_track_statistics(self, agora_local_user, stats:LocalAudioTrackStats):
        #print(f"on_local_audio_track_statistics: stats={stats.sent_bitrate}")
        pass
    def on_remote_audio_track_statistics(self, agora_local_user, remote_audio_track, stats:RemoteAudioTrackStats):
        #print(f"on_remote_audio_track_statistics: track={remote_audio_track}, stats={stats.jitter_buffer_delay}, uid = {stats.uid}")
        pass
    def on_local_video_track_statistics(self, agora_local_user, local_video_track, stats:LocalVideoTrackStats):
        #print(f"on_local_video_track_statistics: stats={stats.input_frame_rate}, {stats.capture_frame_rate}, {stats.encode_frame_rate}, {stats.render_frame_rate}")
        pass
    def on_remote_video_track_statistics(self, agora_local_user, remote_video_track, stats:RemoteVideoTrackStats):
        #print(f"on_remote_video_track_statistics: {stats.uid},{stats.renderer_output_frame_rate}, {stats.frame_render_delay_ms}")
        pass
    
class MyVideoFrameObserver(IVideoFrameObserver):
    def __init__(self, conn: RTCConnection, save_to_disk=0):
        super().__init__()
        self._save_to_disk = save_to_disk
        self._conn = conn
        #for calculation
        self._last_time = 0
        self._frame_count = 0

    def on_frame(self, channel_id, remote_uid, frame: VideoFrame):
        # logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid}, width={frame.width}, height={frame.height}, y_stride={frame.y_stride}, u_stride={frame.u_stride}, v_stride={frame.v_stride}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")
        now = time.time()*1000
        #self._last_time = time.time()*1000
        self._frame_count += 1
        #for every 10 seconds
        if now - self._last_time  > 1000*10:
            print(f"on_frame,  remote_uid={remote_uid}, frame_count={self._frame_count}, fps={self._frame_count/(now-self._last_time)*1000}")
            self._last_time = now
            self._frame_count = 0
        #logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid},len_alpha_buffer={len(frame.alpha_buffer) if frame.alpha_buffer else 0}")
        print(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid}, width={frame.width}x{frame.height}x{len(frame.y_buffer)}")

        out = ExternalVideoFrame()
        out_buffer = bytearray()
        out_buffer.extend(frame.y_buffer)
        out_buffer.extend(frame.u_buffer)
        out_buffer.extend(frame.v_buffer)
        out.buffer = out_buffer
        out.type = 1
        out.format = 1
        out.stride = frame.width
        out.height = frame.height
        out.timestamp = 0
        out.metadata = None
        
        
        
        self._conn.push_video_frame(out)


        if self._save_to_disk:
            file_path = os.path.join('./log/', channel_id + "_" + remote_uid + '.yuv')
            y_size = frame.y_stride * frame.height
            uv_size = (frame.u_stride * frame.height // 2)
            # logger.info(f"on_frame, file_path={file_path}, y_size={y_size}, uv_size={uv_size}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")
            with open(file_path, 'ab') as f:
                f.write(frame.y_buffer[:y_size])
                f.write(frame.u_buffer[:uv_size])
                f.write(frame.v_buffer[:uv_size])
        return 1

    def on_user_video_track_subscribed(self, agora_local_user, user_id, info, agora_remote_video_track):
        logger.info(f"on_user_video_track_subscribed, agora_local_user={agora_local_user}, user_id={user_id}, info={info}, agora_remote_video_track={agora_remote_video_track}")
        return 0
#connection observer
class MyConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super().__init__()
        self.remote_user_id = None
    def on_connected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")
        
    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_disconnected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connecting, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_user_joined(self, agora_rtc_conn, user_id):
        logger.info(f"on_user_joined, agora_rtc_conn={agora_rtc_conn}, user_id={user_id}")
        self.remote_user_id = user_id

    def on_encryption_error(self, agora_rtc_conn, error_type):
        print(f"********on_encryption_error, agora_rtc_conn={agora_rtc_conn}, error_type={error_type}")
    def on_aiqos_capability_missing(self, agora_rtc_conn, recommend_audio_scenario):
        print(f"********on_aiqos_capability_missing, agora_rtc_conn={agora_rtc_conn}, recommend_audio_scenario={recommend_audio_scenario}")
        specified_scenario = AudioScenarioType.AUDIO_SCENARIO_GAME_STREAMING
        return specified_scenario

class MyEncodedVideoFrameObserver(IVideoEncodedFrameObserver):
    def __init__(self, conn: RTCConnection):
        super().__init__()
        self._conn = conn
    def on_encoded_video_frame(self, uid, image_buffer, length, video_encoded_frame_info:EncodedVideoFrameInfo):
        print(f"on_encoded_video_frame, uid={uid}, length={length}, codec_type={video_encoded_frame_info.codec_type}, width={video_encoded_frame_info.width}, height={video_encoded_frame_info.height}, frames_per_second={video_encoded_frame_info.frames_per_second}, frame_type={video_encoded_frame_info.frame_type}, rotation={video_encoded_frame_info.rotation}, track_id={video_encoded_frame_info.track_id}, capture_time_ms={video_encoded_frame_info.capture_time_ms}, decode_time_ms={video_encoded_frame_info.decode_time_ms}, uid={video_encoded_frame_info.uid}, stream_type={video_encoded_frame_info.stream_type}")
        if video_encoded_frame_info.frame_type == 3:
            current_time = time.time()*1000
            global g_send_intra_request_time
            diff = current_time - g_send_intra_request_time
            print(f"on_encoded_video_frame, diff={diff}, size={length}, len = {len(image_buffer)}")
            save_file = os.path.join('./log/', f"encoded_video_frame_{uid}_{time.time()*1000}.jpeg")
            with open(save_file, 'wb') as f:
                f.write(image_buffer[:length])
            print(f"save file to {save_file}")
        return 1
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True

#@profile
def main():

    # signal handler

    signal.signal(signal.SIGINT, signal_handler)

    # run this example
    # 例如： python examples/example.py {appid}  {channel_id}
    #check argv len
    if len (sys.argv) < 3:
        print("usage: python example_audio_vad.py appid channelname")
        return
    appid = sys.argv[1]
    channel_id = sys.argv[2]
   
    uid = "0"
    is_encrypt = 0
    #input source pcm file and format
    
   
    jpeg_file_path = ""
    is_send_jpeg = 0

    if len(sys.argv) > 3:
        jpeg_file_path = sys.argv[3]
        is_send_jpeg = 1

    print("appid:", appid, "channel_id:", channel_id, "jpeg_file_path:", jpeg_file_path)
   
    config = AgoraServiceConfig()
    config.appid = appid
    config.enable_video = 1
    config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_DEFAULT
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])
    config.log_path = "./agora_rtc_log/agorasdk.log"
    config.log_file_size_kb = 1024
    config.data_dir = "./agora_rtc_log"
    config.config_dir = "./agora_rtc_log"
    
    
    print("log_path:", config.log_path)

    #test callback when muted
    config.should_callbck_when_muted = 0
    config.domain_limit = 0

    now = time.time()*1000
    agora_service = AgoraService()
    agora_service.initialize(config)
    print("diff = ", time.time()*1000-now) # 85ms

    # when remote user do MuteLocalAudio, the audio frame will still receive the audio frame or not
    # default to false; if set to true, still can receive audio frame in inactivity frame
    agora_parameter = agora_service.get_agora_parameter()
    
    

    #agora_parameter.set_parameters("{\"rtc.audio.enable_user_silence_packet\": true}")
    


    sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
    )
    
    video_sub_opt = VideoSubscriptionOptions(
        type=VideoStreamType.VIDEO_STREAM_HIGH,
        encodedFrameOnly=True
    )

    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=0,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )
    publish_config = RtcConnectionPublishConfig(
        audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
        audio_scenario=AudioScenarioType.AUDIO_SCENARIO_DEFAULT,
        is_publish_audio=True,
        is_publish_video=True,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_ENCODED_IMAGE,
        video_encoded_image_sender_options=SenderOptions(
            target_bitrate=6500, #6500 is the max bitrate for 1080p
            cc_mode=TCcMode.CC_ENABLED,
            codec_type=VideoCodecType.VIDEO_CODEC_GENERIC_JPEG
        )
    )

   
    connection = agora_service.create_rtc_connection(con_config, publish_config)
    agora_parameter = connection.get_agora_parameter()
    conn_observer = MyConnectionObserver()
    connection.register_observer(conn_observer)



    #agora_parameter.set_parameters("{\"rtc.enable_voqa_jitter\":false}") #会额外的增加延迟，因此去掉
    
    #end
    now = time.time()*1000
    connection.connect(appid, channel_id, uid)
    print(f"connect time = {time.time()*1000-now}")
    # step2:
    
  
    # video frame observer
    video_observer = MyVideoFrameObserver(connection, 0)
    video_encoded_observer = MyEncodedVideoFrameObserver(connection)
    
    


    # step3: localuser:must regiseter before connect

    localuser = connection.get_local_user()
    local_observer = MyLocalUserObserver(localuser, None)
    # enable volume indication
    #localuser.set_audio_volume_indication_parameters(100, 1, 3)
   
    connection.register_local_user_observer(local_observer)

   
    connection.register_video_encoded_frame_observer(video_encoded_observer)
    localuser.subscribe_all_video(video_sub_opt)
  
    connection.publish_video()

   

    connection.publish_audio()
    

   




    # stream msg


    # set paramter

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    
    #agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

    global g_runing
    if is_send_jpeg == 1:
        jpeg_file = open(jpeg_file_path, 'rb')
        data = jpeg_file.read()
    else:
        data = None

    while g_runing:

        if is_send_jpeg == 1:
            video_encoded_frame_info = EncodedVideoFrameInfo(
                codec_type=VideoCodecType.VIDEO_CODEC_GENERIC_JPEG,
                width=1920,
                height=1080,
                frames_per_second=1,
                frame_type=3,
            )
            connection.push_video_encoded_data(data,  video_encoded_frame_info)
            print(f"send jpeg frame, size={len(data)}")
        time.sleep(1)


     # release resource
    print("release resource now")

    connection.disconnect()
   
    print("release connection now")
    connection.release()
    

    
    print("release agora service now")
    agora_service.release()
    print("release agora service done")
    
    #set to None
    audio_observer = None
    local_observer = None
    localuser = None
    connection = None
    agora_service = None

    # for memory leak check
    print("end")


if __name__ == "__main__":
    main()

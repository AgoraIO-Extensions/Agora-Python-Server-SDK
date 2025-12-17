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


# observer
#@profile
class AsyncAudioFrameProcessor:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._running = False
        self._task = None
        
    async def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._process_frames())
    
    async def stop(self):
        if self._running:
            self._running = False
            await self._queue.put(None)  # Signal to stop
            if self._task:
                await self._task
                self._task = None
    
    async def _process_frames(self):
        while self._running:
            try:
                frame_data = await self._queue.get()
                if frame_data is None:  # Stop signal
                    break
                    
                audio_frame, bytes_data, state = frame_data
                # Process the frame asynchronously here
                await self._process_single_frame(audio_frame, bytes_data, state)
                
            except Exception as e:
                print(f"Error processing frame: {e}")
    
    async def _process_single_frame(self, audio_frame, bytes_data, state):
        # Add your async processing logic here
        # For example, you could:
        # - Process the audio data
        # - Send it to another service
        # - Save it to a file
        # - etc.
        pass
    
    async def enqueue_frame(self, audio_frame, bytes_data, state):
        if self._running:
            await self._queue.put((audio_frame, bytes_data, state))

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
        print(f"on_playback_audio_frame: {len(frame.buffer)}")
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
    def __init__(self, local_user):
        super().__init__()
        self._local_user = local_user

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        logger.info(f"on_stream_message, user_id={user_id}, stream_id={stream_id}, data={data}, length={length}")
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
        print(f"on_remote_audio_track_statistics: track={remote_audio_track}, stats={stats.jitter_buffer_delay}, uid = {stats.uid}")
    def on_local_video_track_statistics(self, agora_local_user, local_video_track, stats:LocalVideoTrackStats):
        print(f"on_local_video_track_statistics: stats={stats.input_frame_rate}, {stats.capture_frame_rate}, {stats.encode_frame_rate}, {stats.render_frame_rate}")
    def on_remote_video_track_statistics(self, agora_local_user, remote_video_track, stats:RemoteVideoTrackStats):
        print(f"on_remote_video_track_statistics: {stats.uid},{stats.renderer_output_frame_rate}, {stats.frame_render_delay_ms}")
    
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
    def on_connected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_disconnected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connecting, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_user_joined(self, agora_rtc_conn, user_id):
        logger.info(f"on_user_joined, agora_rtc_conn={agora_rtc_conn}, user_id={user_id}")

    def on_encryption_error(self, agora_rtc_conn, error_type):
        print(f"********on_encryption_error, agora_rtc_conn={agora_rtc_conn}, error_type={error_type}")
    def on_aiqos_capability_missing(self, agora_rtc_conn, recommend_audio_scenario):
        print(f"********on_aiqos_capability_missing, agora_rtc_conn={agora_rtc_conn}, recommend_audio_scenario={recommend_audio_scenario}")
        specified_scenario = AudioScenarioType.AUDIO_SCENARIO_GAME_STREAMING
        return specified_scenario

# sig handleer
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True

def test_encryption_config():
    # 正常情况
    config = EncryptionConfig(
        encryption_mode=1,
        encryption_key="my_key",
        encryption_kdf_salt=bytes([1, 2, 3, 4])
    )
    inner = EncryptionConfigInner.create(config)
    print(f"Salt values: {list(inner.encryption_kdf_salt)}")
    
    # 空盐值
    config = EncryptionConfig(
        encryption_mode=1,
        encryption_key="my_key",
        encryption_kdf_salt=None
    )
    inner = EncryptionConfigInner.create(config)
    print(f"Empty salt: {inner.encryption_kdf_salt}")
    
    # 超长盐值
    config = EncryptionConfig(
        encryption_mode=1,
        encryption_key="my_key",
        encryption_kdf_salt=bytes([1] * 40)
    )
    inner = EncryptionConfigInner.create(config)
    print(f"Truncated salt: {list(inner.encryption_kdf_salt)}")
    # 用户case
    encryption_key = "123456789"
    encryption_kdf_salt = None
    salt = "3t6pvC+qHvVW300B3f+g5J49U3Y×QR40tWKEP/Zz+4="

    config = EncryptionConfig(
        encryption_mode=1, 
        encryption_key=encryption_key,
        encryption_kdf_salt=None
    )
    inner = EncryptionConfigInner.create(config)
    print(f"Truncated salt: {list(inner.encryption_kdf_salt)}")
    config = EncryptionConfig(
        encryption_mode=7, 
        encryption_key="oLB41X/IGpxgUMzsYpE+IOpNLOyIbpr8C7qe+mb7QRHkmrELtVsWw6Xr6rQ0XAK03fsBXJJVCkXeL2X7J492qXjR89Q=",
        encryption_kdf_salt=bytearray(salt.encode('utf-8'))
    )
    inner = EncryptionConfigInner.create(config)
    print(f"User case salt: {list(inner.encryption_kdf_salt)}")
    print(f"User case key: {list(bytearray(salt.encode('utf-8')))}")




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
   
    uid = "99999"
    is_encrypt = 1


    print("appid:", appid, "channel_id:", channel_id)
   
    config = AgoraServiceConfig()
    config.appid = appid
    config.enable_video = 1
    config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_AI_SERVER
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])
    config.log_path = "./agora_rtc_log/agorasdk.log"
    config.log_file_size_kb = 1024
    config.data_dir = "./agora_rtc_log"
    config.config_dir = "./agora_rtc_log"
    #apm related config: if want to use apm, please ontact with us.
    #in common, no need to enable it.
    # note: enable_apm is a switch that controls whether intermediate processed audio data will be dumped to local disk. 
    # Only use it in debug mode.
    config.enable_apm = True
    config.apm_config = APMConfig(
            ai_aec_config=AiAecConfig(enabled=False),
            ai_ns_config=AiNsConfig(),
            bghvs_c_config=BghvsCConfig(),
            agc_config=AgcConfig(enabled=False),
            enable_dump=True,
    )
    json = config.apm_config._to_json_string()
    print(f"**********APM: json = {json}")
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
        is_publish_audio=True,
        is_publish_video=True,
        audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_PCM,
        video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_YUV,
        video_encoded_image_sender_options=SenderOptions(
            target_bitrate=6500, #6500 is the max bitrate for 1080p
            cc_mode=TCcMode.CC_ENABLED,
            codec_type=VideoCodecType.VIDEO_CODEC_H264
        )
    )
    connection = agora_service.create_rtc_connection(con_config, publish_config)
    agora_parameter = connection.get_agora_parameter()
    conn_observer = MyConnectionObserver()
    connection.register_observer(conn_observer)

    #set encryption key
    encryption_key = "123456789"
    encryption_kdf_salt = None
    salt = "3t6pvC+qHvVW300B3f+g5J49U3Y×QR40tWKEP/Zz+4="

    encryption_config = EncryptionConfig(
        encryption_mode=1, 
        encryption_key=encryption_key,
        encryption_kdf_salt=None
    )
    encryption_config = EncryptionConfig(
        encryption_mode=7, 
        encryption_key="oLB41X/IGpxgUMzsYpE+IOpNLOyIbpr8C7qe+mb7QRHkmrELtVsWw6Xr6rQ0XAK03fsBXJJVCkXeL2X7J492qXjR89Q=",
        encryption_kdf_salt=bytearray(salt.encode('utf-8'))
    )
   
    ret = connection.enable_encryption(0, encryption_config)
    print(f"enable_encryption ret = {ret}")
    '''
    connection.enable_encryption(1, EncryptionConfig(
        encryption_mode=is_encrypt, 
        encryption_key=encryption_key, 
        encryption_kdf_salt=encryption_kdf_salt))
    '''

    
    # set video low delay mode:only for test, do not use in production
    
    agora_parameter.set_parameters("{\"che.video.vpr.enable\":false}")
    agora_parameter.set_parameters("{\"rtc.video.avsync\":false}")
    agora_parameter.set_parameters("{\"rtc.video.enable_pvc\":false}")
    agora_parameter.set_parameters("{\"rtc.video.enable_sr\":{\"enabled\":false,\"mode\":2}}")
    

    #agora_parameter.set_parameters("{\"rtc.enable_voqa_jitter\":false}") #会额外的增加延迟，因此去掉
    
    #end
    now = time.time()*1000
    connection.connect(appid, channel_id, uid)
    print(f"connect time = {time.time()*1000-now}")
    # step2:
    
  
    # video frame observer
    video_observer = MyVideoFrameObserver(connection, 0)
    
    

    audio_consumer  = AudioConsumer(pcm_sender= None, sample_rate=16000, channels=1)

    # step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = MyLocalUserObserver(localuser)
    # enable volume indication
    #localuser.set_audio_volume_indication_parameters(100, 1, 3)
   
    connection.register_local_user_observer(local_observer)

    #localuser.register_video_frame_observer(video_observer)

    # note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    #localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    localuser.set_playback_audio_frame_parameters(1, 16000, 1, 320)
    audio_queue = Queue()
    video_queue = Queue()
    audio_observer = MyAudioFrameObserver(connection, 1, audio_queue)
    #vad_configure  = AudioVadConfigV2(16, 30, 50, 0.7, 0.5, 70, 70, -50)
    vad_configure = AudioVadConfigV2()
    connection.register_audio_frame_observer(audio_observer, 1, vad_configure)

    #videoframe observer
    connection.register_video_frame_observer(video_observer)
  
    connection.publish_video()

    #sub 
    """
    remote_uid = "123"
    localuser.subscribe_audio(remote_uid)
    localuser.unsubscribe_audio(remote_uid)
    localuser.subscribe_video(remote_uid, None)
    localuser.unsubscribe_video(remote_uid)
    """


    connection.publish_audio()
    localuser.subscribe_all_audio()

   




    # stream msg


    # set paramter

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    
    #agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

    global g_runing

    #open for consumer
    frame_buffer = bytearray(320)
    audio_file = open ("../test_data/demo.pcm", "rb")
    file_to_consumer(audio_file, frame_buffer, audio_consumer)

    audio_frame = PcmAudioFrame()
    #init sample rate and channels
    audio_frame.sample_rate = 16000
    audio_frame.number_of_channels = 1

    #audio parame
    audio_frame.bytes_per_sample = 2
    
    #init pcmaudioframe
    audio_frame.timestamp = 0
    has_send_complted = 0
    audio_file.seek(320*100)

    #connection.update_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
    # recv mode
    while g_runing:
        """
        audio_consumer.consume()
        remain_len = audio_consumer.len()
        is_publish_complted = audio_consumer.is_push_to_rtc_completed()
        if is_publish_complted > 0 and has_send_complted == 0:
            has_send_complted = 1
            print("publish completed")
            connection.send_stream_message(stream_id, "publish completed")
            localuser.send_audio_meta_data("audio publish completed")
            has_send_complted = 1
            """
            
            
        '''
        if remain_len < 320*50*150: #interval*1000/10 *1.5. where 1.5 is the redundancy coeficient
            file_to_consumer(audio_file, frame_buffer, audio_consumer)
        '''
        
        #ret = audio_consumer.consume()
        #audio_frame.data = frame_buffer
        #pcm_data_sender.send_audio_pcm_data(audio_frame)
        str = "test"
        #byte_str = str.encode('utf-8')
        #localuser.send_audio_meta_data(str)
        while not audio_queue.empty():
            audio_frame = audio_queue.get()
            ret = connection.push_audio_pcm_data(audio_frame.buffer, audio_frame.samples_per_sec, audio_frame.channels)
            #print(f"push_audio_pcm_data ret = {ret}")
        time.sleep(0.05)
        #connection.send_stream_message("stream test")
        #connection.send_audio_meta_data("audio meta data test")

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
    test_encryption_config()
    main()
    #asyncio.run(main())
# for audiostream processing
class AudioStreamProcessor:
    def __init__(self, sample_rate, num_channels, interval=0.1):
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.interval = interval
        self.buffer_size = 65536 #64k
        self.send_size = int(sample_rate * num_channels * interval * 2)
        self.buffer = bytearray()
        self.pack_size = int(sample_rate * num_channels * 2 / 100)
        
    async def process_stream(self, response, audio_consumer, interrupt_event):
        if response.status != 200:
            return
            
        try:
            async for chunk in response.content.iter_chunked(self.buffer_size):
                if not chunk or interrupt_event.is_set():
                    break
                    
                self.buffer.extend(chunk)
                buffer_len = len(self.buffer)
                #需要拆分为10ms的整数倍
            
                pack_num = buffer_len // self.pack_size
                if pack_num > 0 and audio_consumer:
                    #push to audio consumer
                    data = self.buffer[:pack_num * self.pack_size]
                    self.buffer = self.buffer[pack_num * self.pack_size:]
                    audio_consumer.push_pcm_data(data)
                   
                
                    
        except Exception as e:
            logger.error(f"Error processing audio stream: {e}")
        finally:
            # 处理剩余数据
            if self.buffer and audio_consumer:
                # check if buffer is 10ms
                pack_num = len(self.buffer) // self.pack_size
                if pack_num > 0:
                    data = self.buffer[:pack_num * self.pack_size]
                    self.buffer = self.buffer[pack_num * self.pack_size:]
                    audio_consumer.push_pcm_data(data)




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


# import voicesentencedetection
from agora.rtc.voice_detection import *

from agora.rtc.utils.vad_dump import VadDump
from common.push_audio_pcm_file import file_to_consumer
from agora.rtc.utils.audio_consumer import AudioConsumer

import gc
import asyncio
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
class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self, pcm_data_sender: AudioPcmDataSender, is_loop: int):
        #super(MyAudioFrameObserver, self).__init__()
        self._silence_pack = bytearray(320)
        self._pcm_data_sender = pcm_data_sender
        self._is_loop = is_loop
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
        pass

    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_record_audio_frame")
        return 0

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0


    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame, vad_result_state:int, vad_result_bytearray:bytearray):
        # logger.info(f"on_playback_audio_frame_before_mixing, channelId={channelId}, uid={uid}, type={audio_frame.type}, samples_per_sec={audio_frame.samples_per_sec}, samples_per_channel={audio_frame.samples_per_channel}, bytes_per_sample={audio_frame.bytes_per_sample}, channels={audio_frame.channels}, len={len(audio_frame.buffer)}")
        #print(f"before_mixing: far = {audio_frame.far_field_flag },rms = {audio_frame.rms}, voice = {audio_frame.voice_prob}, music ={audio_frame.music_prob},pith = {audio_frame.pitch}")
        #vad v2 processing: can do in sdk callback
        #state, bytes = self._vad_instance.process(audio_frame)
        state = vad_result_state
        #print("state = ", state, len(bytes) if bytes != None else 0, vad_result_state, len(vad_result_bytearray) if vad_result_bytearray != None else 0)
        # dump to vad for debuging
        if (self._is_loop == 1):
            frame = PcmAudioFrame(
            data=audio_frame.buffer,
            timestamp=0,
            samples_per_channel=160,
            bytes_per_sample=2,
            number_of_channels=1,
            sample_rate=16000)
            self._pcm_data_sender.send_audio_pcm_data(frame)
        else:
            self._vad_dump.write(audio_frame, bytes, state)
            if bytes != None:
                if state == 1:
                    # start speaking: then start send bytes(not audio_frame) to ARS
                    print("vad v2 start speaking")
                elif state == 2:
                    # continue send bytes to ARS
                    pass
                elif state == 3:
                    # stop speaking: send bytes to ARS and then then stop  ARS
                    print("vad v2 stop speaking:")
                else:
                    logger.info("unknown state")
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0
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
        self._local_user.send_audio_meta_data( data)
        pass
    

class MyVideoFrameObserver(IVideoFrameObserver):
    def __init__(self, yuv_sender, save_to_disk=0):
        super().__init__()
        self._save_to_disk = save_to_disk
        self._yuv_sender = yuv_sender

    def on_frame(self, channel_id, remote_uid, frame: VideoFrame):
        # logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid}, width={frame.width}, height={frame.height}, y_stride={frame.y_stride}, u_stride={frame.u_stride}, v_stride={frame.v_stride}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")

        logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid},len_alpha_buffer={len(frame.alpha_buffer) if frame.alpha_buffer else 0}")
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
        
        
        
        self._yuv_sender.send_video_frame(out)


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
# sig handleer
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


    print("appid:", appid, "channel_id:", channel_id)

    config = AgoraServiceConfig()
    config.appid = appid
    config.enable_video = 1
    # config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])
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
    agora_parameter.set_parameters("{\"che.audio.label.enable\": true}")
    

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

    connection = agora_service.create_rtc_connection(con_config)
    agora_parameter = connection.get_agora_parameter()
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)

    media_node_factory = agora_service.create_media_node_factory()

    yuv_data_sender = media_node_factory.create_video_frame_sender()
    video_track = agora_service.create_custom_video_track_frame(yuv_data_sender)

    # video frame observer
    video_observer = MyVideoFrameObserver(yuv_data_sender, False)
    
    # set video low delay mode
    '''
    agora_parameter.set_parameters("{\"che.video.vpr.enable\":false}")
    agora_parameter.set_parameters("{\"rtc.video.avsync\":false}")
    agora_parameter.set_parameters("{\"rtc.video.enable_pvc\":false}")
    agora_parameter.set_parameters("{\"rtc.video.enable_sr\":{\"enabled\":false,\"mode\":2}}")

    #agora_parameter.set_parameters("{\"rtc.enable_voqa_jitter\":false}") #会额外的增加延迟，因此去掉
    '''
    #end

    connection.connect(appid, channel_id, uid)

    # step2:
    
    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)

    # test firt audio frame
    
    

    audio_consumer  = AudioConsumer(pcm_sender= pcm_data_sender, sample_rate=16000, channels=1)

    # step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = MyLocalUserObserver(localuser)
    # enable volume indication
  
    localuser.register_local_user_observer(local_observer)

    localuser.register_video_frame_observer(video_observer)

    # note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    audio_observer = MyAudioFrameObserver(pcm_data_sender, 1)
    vad_configure  = AudioVadConfigV2(16, 30, 50, 0.7, 0.5, 70, 70, -50)
    localuser.register_audio_frame_observer(audio_observer, 0, vad_configure)

    #sub 
    remote_uid = "123"
    localuser.subscribe_audio(remote_uid)
    localuser.unsubscribe_audio(remote_uid)
    localuser.subscribe_video(remote_uid, None)
    localuser.unsubscribe_video(remote_uid)

    # ret = localuser.get_user_role()
    # localuser.set_user_role(con_config.client_role_type)

    # step4: pub
    audio_track.set_enabled(1)
    localuser.publish_audio(audio_track)
    localuser.subscribe_all_audio()

    video_track.set_enabled(1)
    localuser.publish_video(video_track)





    # stream msg
    stream_id = connection.create_data_stream(0, 0)
    print(f"streamid: {stream_id}")

    # set paramter

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    
    agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

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
    # recv mode
    while g_runing:
        remain_len = audio_consumer.len()
        if remain_len < 320*50*150: #interval*1000/10 *1.5. where 1.5 is the redundancy coeficient
            file_to_consumer(audio_file, frame_buffer, audio_consumer)
        #ret = audio_consumer.consume()
        #audio_frame.data = frame_buffer
        #pcm_data_sender.send_audio_pcm_data(audio_frame)
        str = "test"
        #byte_str = str.encode('utf-8')
        #localuser.send_audio_meta_data(str)
        time.sleep(0.05)

     # release resource
    audio_consumer.release()
    localuser.unpublish_audio(audio_track)
    audio_track.set_enabled(0)

    localuser.unregister_audio_frame_observer()
    localuser.unregister_local_user_observer()

    connection.disconnect()
    connection.unregister_observer()

    localuser.release()
    connection.release()
    

    
    audio_track.release()
    pcm_data_sender.release()
    

    media_node_factory.release()
    agora_service.release()
    
    #set to None
    audio_track = None
    audio_observer = None
    local_observer = None
    localuser = None
    connection = None
    agora_service = None

    # for memory leak check
    print("end")

async def producer(queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(0.05)
    
async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            print("consumer exit")
            break
        print(item)
        queue.task_done()
        await asyncio.sleep(0.05)
async def aio_main():
    queue = asyncio.Queue()
    
    #task4 = asyncio.create_task(producer(queue))
    producer_task = [asyncio.create_task(producer(queue)) for i in range(3)]
    consumer_list = [asyncio.create_task(consumer(queue)) for i in range(3)]
    await asyncio.gather(*producer_task)
    for _ in consumer_list:
        await queue.put(None)
        print("producer None:", time.time()*1000)
    await asyncio.gather(*consumer_list)
    print("end:%d", time.time()*1000)


if __name__ == "__main__":
    asyncio.run(aio_main())




#coding=utf-8

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
from agora.rtc.audio_vad import *
from agora.rtc.local_user import *
from agora.rtc.local_user_observer import *
import threading
from collections import deque

#import voicesentencedetection
from agora.rtc.voice_detection import *
from agora.rtc.audio_vad import *

import gc
import asyncio








#connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    return log_path



#observer
class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(MyAudioFrameObserver, self).__init__()
        self._source_file = open("./vad_source.pcm", "wb")
        self._case1_file = open("./vad_case1.pcm", "wb")
        self._case2_file = open("./vad_case2.pcm", "wb")
        self._case3_file = open("./vad_case3.pcm", "wb")
        self._silence_pack = bytearray(320)
        self._vad_file = None #open("./vad_file.pcm", "wb")
        self._log_file = None #open("./vad_log.txt", "w")
        """
        # Recommended  configurations:  
            # For not-so-noisy environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -50)  
            # For noisy environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -40)  
            # For high-noise environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -30)

         """
        
       
        self._vad_instance = AudioVadV2(AudioVadConfigV2(16, 30, 20, 0.7, 0.5, 70, 70, -50))
        self._vad_counts = 0
        #vad v1 related
        self.v1_configure = VadConfig()
        #modify v1 vad configure
        self.v1_configure.voiceProbThr = 0.5
        self.v1_configure.rmsThr = -40
        self.v1_configure.aggressive = 2.0
        self.v1_configure.preStartRecognizeCount = 18
        self.v1_configure.startRecognizeCount = 16
        self.v1_configure.stopRecognizeCount = 20
        self.v1_configure.activePercent = 0.6
        self.v1_configure.inactivePercent = 0.2

        self._vad_v1_instance = AudioVad()
        self._vad_v1_instance.Create(self.v1_configure)
        self._vad_v1_counts = 0
        self._vad_v1_file = None #open("./vad_file_v1.pcm", "wb")

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     audio_params_instance = AudioParams()
    #     return audio_params_instance

    def on_record_audio_frame(self, agora_local_user ,channelId, frame):        
        logger.info(f"on_record_audio_frame")
        return 0
    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0
    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):        
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0
    
    def _dump_to_file(self, fd, audio_frame:AudioFrame):
        fd.write(audio_frame.buffer)
    
    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame:AudioFrame):
        #logger.info(f"on_playback_audio_frame_before_mixing, channelId={channelId}, uid={uid}, type={audio_frame.type}, samples_per_sec={audio_frame.samples_per_sec}, samples_per_channel={audio_frame.samples_per_channel}, bytes_per_sample={audio_frame.bytes_per_sample}, channels={audio_frame.channels}, len={len(audio_frame.buffer)}")
        print(f"before_mixing: far = {audio_frame.far_field_flag },rms = {audio_frame.rms}, voice = {audio_frame.voice_prob}, music ={audio_frame.music_prob},pith = {audio_frame.pitch}")
        #strategies 
        #anyway, dump source file
        #if audio_frame.buffer:
        self._source_file.write(audio_frame.buffer)
        v1_datas = audio_frame.buffer
 
        
        #vad v2
        state, bytes = self._vad_instance.process(audio_frame)
        print("state = ", state, len(bytes) if bytes != None else 0)
        #save and append to file
        if bytes != None:
            if state ==1:
                #open and write to file
                print("vad v2 start speaking:",self._vad_counts)
                cur_time = int(time.time()*1000)
                name = f"./vad_{self._vad_counts}.pcm"
                self._vad_file = open(name, "wb")
                self._vad_file.write(bytes)
            elif state == 2:
                self._vad_file.write(bytes)
            elif state == 3:
                self._vad_file.write(bytes)
                self._vad_file.close()
                self._vad_counts += 1
                print("vad v2 stop speaking:", self._vad_counts-1)
            else:
                logger.info("unknown state")
        #vad v1
        ret, frameout, flag = self._vad_v1_instance.Proc(v1_datas)
        print(f"vad v1 ret = {ret}, flag = {flag}")
        if ret == 0 and flag == 1:
            #start speaking
            print("vad v1 start speaking:", self._vad_v1_counts)
            cur_time = int(time.time()*1000)
            name = f"./vad1_{self._vad_v1_counts}.pcm"
            self._vad_v1_file = open(name, "wb")
            self._vad_v1_file.write(frameout)
        elif ret == 0 and flag == 2:
            #speaking:
            self._vad_v1_file.write(frameout)
        elif ret == 0 and flag == 3:
            #stop speaking
            self._vad_v1_file.write(frameout)
            self._vad_v1_file.close()
            self._vad_v1_counts += 1
            print("vad v1 stop speaking:", self._vad_v1_counts-1)
        
       
        
        """
        
        """

        #case 1
        if audio_frame.far_field_flag == 1:
            self._case1_file.write(audio_frame.buffer)
        else:
            self._case1_file.write(self._silence_pack)
        
        #case2
        if audio_frame.far_field_flag == 1 and audio_frame.voice_prob > 75:
            self._case2_file.write(audio_frame.buffer)
        else:
            self._case2_file.write(self._silence_pack)

        #case3
        if audio_frame.far_field_flag == 1 and audio_frame.voice_prob > 75 and audio_frame.rms > -35:
            self._case3_file.write(audio_frame.buffer)
        else:
            self._case3_file.write(self._silence_pack)
            
        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")        
        return 0
    # def on_get_audio_frame_position(self, agora_local_user):
    #     logger.info("CCC on_get_audio_frame_position")
    #     return 0

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_playback_audio_frame_param")
    #     return 0
    # def on_get_record_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_record_audio_frame_param")
    #     return 0
    # def on_get_mixed_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_mixed_audio_frame_param")
    #     return 0
    # def on_get_ear_monitoring_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_ear_monitoring_audio_frame_param")
    #     return 0


class AsyncAudioStreamConsumer:
    def __init__(self, pcm_sender) -> None:
        self._lock = threading.Lock()
        self._data = bytearray()
        self._interval = 0.05 #50ms 
        
        self._start_time = 0
        self._consumed_packages = 0
        self._run = True
        self._event = threading.Event()
        self._pcm_sender = pcm_sender

        self._task = asyncio.create_task(self._start_task())
        
        pass
        
    def push_pcm_data(self, data):
        #add to buffer, lock
        with self._lock:
            self._data += data
        pass
    async def _start_task(self):
        while self._run:
            await asyncio.sleep(self._interval)
            await self._consume()
    
    async def _consume(self):
        with self._lock:
            # cal current duration
            cur_time = time.time()*1000
            elapsed_time = cur_time - self._start_time
            wanted_packages = int(elapsed_time/10) - self._consumed_packages

            if wanted_packages > 18:  # 180ms, a new session
                wanted_packages = 18
                self._start_time = cur_time
                self._consumed_packages = -18
            #check datasize to get min(packages*320, len(data))
            data_len = len(self._data)
            wanted_packages = min(wanted_packages, data_len//320)
            print("wanted_packages:", wanted_packages, "data_len:", data_len, "consumed_packages:", self._consumed_packages, "elapsed_time:", elapsed_time)
            if self._data and wanted_packages > 0:
                #pop data
                frame_size = 320*wanted_packages
                frame_buf = bytearray(frame_size)
                frame_buf[:] = self._data[:frame_size]
                self._data = self._data[frame_size:]
                #print("pop data:", len(frame_buf))
                #send data
                frame = PcmAudioFrame()
                frame.data = frame_buf
                frame.timestamp = 0
                frame.samples_per_channel = 160*wanted_packages
                frame.bytes_per_sample = 2
                frame.number_of_channels = 1
                frame.sample_rate = 16000
                ret = self._pcm_sender.send_audio_pcm_data(frame)
                #print("second,ret=",wanted_packages, ret)
                self._consumed_packages += wanted_packages
        pass
    def relase(self):
        self._run = False
        
        self._task.cancel()
       
        self._data = None
        
        pass
    def clear(self):
        with self._lock:
            self._data = bytearray()

class AsycncAudioStreamProducer:
    def __init__(self, file_path, consumer) -> None:
        self._file = open (file_path, "rb")
        self._consumer = consumer
        self._task = asyncio.create_task(self._produce())
        pass
    def simulate_process_data(self):
        pass
    async def _produce(self):
        while True:
            frame_buf = bytearray(320*200)
            success = self._file.readinto(frame_buf)
            if success <= 0:
                print("read file error,ret=",success)
                self._file.seek(0,0)
                self._file.readinto(frame_buf)
            self._consumer.push_pcm_data(frame_buf)
            await asyncio.sleep(0.05)


class AudioStreamConsumer:
    def __init__(self, pcm_sender) -> None:
        self._lock = threading.Lock()
        self._data = bytearray()
        self._interval = 0.05 #50ms 
        self._timer = threading.Timer(self._interval, self._consume).start()
        self._start_time = 0
        self._consumed_packages = 0
        self._run = True
        self._event = threading.Event()
        self._pcm_sender = pcm_sender
        
        pass
        
    def push_pcm_data(self, data):
        #add to buffer, lock
        with self._lock:
            self._data += data
        pass
    
    def _consume(self):
        with self._lock:
            # cal current duration
            cur_time = time.time()*1000
            elapsed_time = cur_time - self._start_time
            wanted_packages = int(elapsed_time/10) - self._consumed_packages
            data_len = len(self._data)
            
            #for the first time(wanted_packages>18), at least 6 packages shoud be sent to make sure the sdk has enough data buffer to 
            # o as to eliminate the jitter of the producer and the timer.
            if wanted_packages > 18 and data_len // 320 < 6:
                print("data_len:", data_len, "wanted_packages:", wanted_packages)
                return

            if wanted_packages > 18:  # 180ms, a new session
                wanted_packages = 18
                self._start_time = cur_time
                self._consumed_packages = -18
            #check datasize to get min(packages*320, len(data))
            data_len = len(self._data)
            wanted_packages = min(wanted_packages, data_len//320)
            print("wanted_packages:", wanted_packages, "data_len:", data_len, "consumed_packages:", self._consumed_packages, "elapsed_time:", elapsed_time)
            if self._data and wanted_packages > 0:
                #pop data
                frame_size = 320*wanted_packages
                frame_buf = bytearray(frame_size)
                frame_buf[:] = self._data[:frame_size]
                self._data = self._data[frame_size:]
                #print("pop data:", len(frame_buf))
                #send data
                frame = PcmAudioFrame()
                frame.data = frame_buf
                frame.timestamp = 0
                frame.samples_per_channel = 160*wanted_packages
                frame.bytes_per_sample = 2
                frame.number_of_channels = 1
                frame.sample_rate = 16000
                ret = self._pcm_sender.send_audio_pcm_data(frame)
                #print("second,ret=",wanted_packages, ret)
                self._consumed_packages += wanted_packages
                

            #restart timer
            if self._run:
                self._timer = threading.Timer(self._interval, self._consume).start()
            else:
                self._event.set()
        pass
    def relase(self):
        self._run = False
        
        self._event.wait()
        self._timer = None
        self._data = None
        self._event = None
        pass
    def clear(self):
        with self._lock:
            self._data = bytearray()
            



def pushPcmDatafromFile(file, packnum, pcmsender):
    frame_buf = bytearray(320*packnum)
    success = file.readinto(frame_buf)
    if not success:
        #print("read pcm file failed")
        return -1
    frame = PcmAudioFrame()
    frame.data = frame_buf
    frame.timestamp = 0
    frame.samples_per_channel = 160*packnum
    frame.bytes_per_sample = 2
    frame.number_of_channels = 1
    frame.sample_rate = 16000

    #do voulume adjust
   

    ret = pcmsender.send_audio_pcm_data(frame)
    #print("first,ret=",packnum, ret)
    return ret

#sig handleer
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)

def CalEnergy(frame):
    energy = 0
    buffer = (ctypes.c_ubyte * len(frame)).from_buffer(frame)
    ptr = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_int16))
    for i in range(len(frame)//2): # 16bit
        energy += ptr[i] * ptr[i]
    energy = energy / (len(frame)//2)
    #round to int16
    energy = energy/(2**15)
    
    return energy

def vadcallback(frameout, size):
    print("vadcallback:", len(frameout), "size:", size)

def DoVadTest(filepath):
    print("DoVadTest")
    # vad testing
    vadcg = VadConfig()
    vad = AudioVad()
    vad.Create(vadcg)
    inVadData = VadAudioData()
    outVadData = VadAudioData()
    vadflag = VAD_STATE()
    #read pcm file& output status

    with open(pcm_file_path, "rb") as file:
    
        #seek wav file header :44 byte
        file.seek(44)
        frame_buf = bytearray(320)
        
        outfile = open("/Users/weihognqin/Documents/work/python_rtc_sdk/vadcopy.pcm", "wb")
        index = 0
        total = 0
        energy = 0
        while True:
            ret = file.readinto(frame_buf)
            if ret < 320:
                break
            energy = 0
        
            ret,frame_out, flag = vad.Proc(frame_buf)
            if ret == 0 and len(frame_out) > 0 :
                energy = CalEnergy(frame_out)
                outfile.write(frame_out)

                out = frame_out
                vadcallback(out, len(out))
            index += 1
            total += len(frame_out)
            #print("index:", index, "ret:", ret, "vadflag:", flag, "size:", len(output), "total:", total, "energy:", energy)

            #print("index:", index, "ret:", ret, "vadflag:", flag, "size:", len(frame_out), "total:", total, "energy:", energy)
    
            #print("index:", index, "ret:", ret, "vadflag:", vadflag.value, "size:", outVadData.size, "data",outVadData.audioData)
    #release
    vad.Destroy()
    file.close()
    outfile.close()
    
    return 0

g_runing = True
def main():

#signal handler
    

    signal.signal(signal.SIGINT, signal_handler)

    # run this example
    # 例如： python examples/example.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
    appid = sys.argv[1]
    token = sys.argv[2]
    channel_id = sys.argv[3]
    pcm_file_path = sys.argv[4]
    # check argv len
    if len(sys.argv) > 5:
        uid = sys.argv[5]
    else:
        uid = "0"

    #send stream or not
    if len(sys.argv) > 7:
        send_stream = int(sys.argv[7])
    else:
        send_stream = 0
    if len(sys.argv) > 8:
        role_type = int(sys.argv[8])
    else:
        role_type = 2

    """
    #check vad sample file
    if len(sys.argv) > 6:
        DoVadTest(sys.argv[6])
    """
    print("appid:", appid, "token:", token, "channel_id:", channel_id, "pcm_file_path:", pcm_file_path, "uid:", uid, "send_stream:", send_stream)



    config = AgoraServiceConfig()
    config.appid = appid
    #config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = local_get_log_path_with_filename() #get_log_path_with_filename(os.path.splitext(__file__)[0])


    agora_service = AgoraService()
    agora_service.initialize(config)
  
    sub_opt = AudioSubscriptionOptions(
            packet_only = 0,
            pcm_data_only = 1,
            bytes_per_sample = 2,
            number_of_channels = 1,
            sample_rate_hz = 16000
    )


    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=0,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER if role_type == 1 else ClientRoleType.CLIENT_ROLE_AUDIENCE,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet = 0,
        audio_subs_options = sub_opt,
        enable_audio_recording_or_playout = 0,
    )

    #enable audio label: do not commit htis
    parameters = agora_service.get_agora_parameter()
    parameters.set_bool("che.audio.label.enable", 1)
    


    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)





    connection.connect(token, channel_id, uid)

    #step2: 
    media_node_factory = agora_service.create_media_node_factory()
    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)


    #step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = ExampleLocalUserObserver()
    localuser.register_local_user_observer(local_observer)

    #note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    audio_observer = MyAudioFrameObserver()
    localuser.register_audio_frame_observer(audio_observer)



    #ret = localuser.get_user_role()
    #localuser.set_user_role(con_config.client_role_type)


    #step4: pub
    audio_track.set_enabled(1)
    localuser.publish_audio(audio_track)
    localuser.subscribe_all_audio()

    #test
#todo:  ??? ERROR!!
    
    #detailed_stat = localuser.get_local_audio_statistics()
    #print("detailed_stat:", detailed_stat.local_ssrc, detailed_stat.codec_name)

    #stream msg 
    stream_id = connection.create_data_stream(0, 0)
    print(f"streamid: {stream_id}")



   

    #set paramter
 
    #nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    #connection.SetParameter(nearindump)
    #agora_parameter = connection.get_agora_parameter()
    #agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

    sendinterval = 0.05 #50ms   

    packnum = int((sendinterval*1000)/10)
    





    global g_runing
    #recv mode
    while g_runing:
        time.sleep(0.05)
  

    #audio_stream.relase()
    localuser.unpublish_audio(audio_track)
    audio_track.set_enabled(0)
    localuser.release()
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    print("release")
    time.sleep(0.01)
    agora_service.release()
    print("end")

if __name__ == "__main__":
    main()

"""
#asyn mode, cpu wast 35
  audio_strem = AsyncAudioStreamConsumer(pcm_data_sender)
    audio_producer = AsycncAudioStreamProducer(pcm_file_path, audio_strem)
    try:
        await asyncio.Future()
    except Exception as e:
        print("exception:", e)
if __name__ == "__main__":
    asyncio.run(main())

# sync mode, cpu wast ~~5.5
 
    # sync mode
    if role_type == 1:
        audio_stream = AudioStreamConsumer(pcm_data_sender)
        with open(pcm_file_path, "rb") as file:
            while  g_runing :
                frame_buf = bytearray(320*200)
                success = file.readinto(frame_buf)
                if success <= 0:
                    print("read file error,ret=",success)
                    file.seek(0,0)
                    file.readinto(frame_buf)
                audio_stream.push_pcm_data(frame_buf)
                #print("push pcm data")
                time.sleep(0.2)
    else:
        #just runing
        while g_runing:
            time.sleep(0.05)
    
    with open(pcm_file_path, "rb") as file:
        #第一次读区 180ms的数据
        packnum = 18
        ret = pushPcmDatafromFile(file, packnum, pcm_data_sender)
        #print("first,ret=",packnum, ret)

        #fortesting

        packnum = int((sendinterval*1000)/10)
        sessionstarttick = int(time.time()*1000) #round to ms
        cursendtotalpack = 0
        frame_buf = bytearray(packnum*320)

        

        while  g_runing :
            # check
            curtime = int(time.time()*1000)

            #every 1500ms do check
            checkinterval = curtime - sessionstarttick
            
            needcompensationpack = int( checkinterval/10) - cursendtotalpack
            #print("needcompensationpack:", needcompensationpack)
            if needcompensationpack > 0:
                ret = pushPcmDatafromFile(file, needcompensationpack, pcm_data_sender)
                if ret < 0:
                    print("read file error,ret=",ret)
                    #re-seek to file header
                    file.seek(0, 0)
                else:
                    cursendtotalpack += needcompensationpack

            #send steam msg
            if send_stream == 1:
                time_str = f"send stream msg,total packs: {cursendtotalpack}, curtime:{curtime}"
                ret = connection.send_stream_message(stream_id, time_str)
                print(f"send stream msg ret={ret}, msg={time_str}")
        

            time.sleep(sendinterval)
            #print("goruning = ", g_runing)
                
    """

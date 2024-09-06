#coding=utf-8

import time
import datetime
import ctypes
from common.path_utils import get_log_path_with_filename 
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver

from agora_service.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora_service.rtc_connection import *
from agora_service.media_node_factory import *
from agora_service.audio_pcm_data_sender import *
from agora_service.audio_frame_observer import *
import signal
from agora_service.audio_vad import *
from agora_service.local_user import *
from agora_service.local_user_observer import *

import gc



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


#signal handler
g_runing = True

signal.signal(signal.SIGINT, signal_handler)

# 通过传参将参数传进来
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
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)
"""
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
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    # audio_recv_media_packet = 1,
    # audio_send_media_packet = 1,
    audio_subs_options = sub_opt,
    enable_audio_recording_or_playout = 1,
)

note：  必须audiodevice=1 && record&playback=1
这个不符合server的预期
预期应该都是0
"""
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
    client_role_type=role_type, #1: broadcaster, 2: audience
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    audio_recv_media_packet = 0,
    audio_subs_options = sub_opt,
    enable_audio_recording_or_playout = 0,
)




connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)





connection.connect(token, channel_id, uid)

#step2: 
media_node_factory = agora_service.create_media_node_factory()
pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)


#step3: localuser:must regiseter before connect
localuser = connection.get_local_user()
local_observer = DYSLocalUserObserver()
localuser.register_local_user_observer(local_observer)

#note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
audio_observer = DYSAudioFrameObserver()
localuser.register_audio_frame_observer(audio_observer)


#ret = localuser.get_user_role()
#localuser.set_user_role(con_config.client_role_type)


#step4: pub
audio_track.set_enabled(1)
localuser.publish_audio(audio_track)
localuser.subscribe_all_audio()

#test

detailed_stat = localuser.get_local_audio_statistics()
print("detailed_stat:", detailed_stat.local_ssrc, detailed_stat.codec_name)

#stream msg 
stream_id = connection.create_data_stream(0, 0)
print(f"streamid: {stream_id}")



"""
1、创建rtc connection
create conneciton
regiser connection observer
conn。connect
2、创建medianode & audiotrack
media node
pcm sender
locaktrack 
locol user

"""

#set paramter
"""
用途：是当音频有问题的时候，用来做定位的
用法：
1、测试阶段：
测试阶段关闭，有问题的时候，打开
2、线上
如果能做到可配置打开是最好的；不好做，就关闭

总体看，这个会dump数据到磁盘，通常关闭
"""
#nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
#connection.SetParameter(nearindump)

sendinterval = 0.05 #50ms   

packnum = int((sendinterval*1000)/10)
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
              

localuser.unpublish_audio(audio_track)
audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
time.sleep(0.01)
agora_service.release()
print("end")
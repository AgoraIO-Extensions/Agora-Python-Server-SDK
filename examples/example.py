#coding=utf-8

import time
import ctypes
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(script_dir)
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)
from agora_service.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora_service.rtc_connection import *
from agora_service.media_node_factory import *
from agora_service.audio_pcm_data_sender import *
from agora_service.audio_frame_observer import *
import signal
from agora_service.audio_vad import *

import gc

# conn_observer callback
def on_connected(agora_rtc_conn, conn_info, reason):
    print("Connected:", agora_rtc_conn, conn_info, reason)

def on_disconnected(agora_rtc_conn, conn_info, reason):
    print("Disconnected:", agora_rtc_conn, conn_info, reason)

def on_connecting(agora_rtc_conn, conn_info, reason):
    print("Connecting:", agora_rtc_conn, conn_info, reason)

def on_user_joined(agora_rtc_conn, user_id):
    print("on_user_joined:", agora_rtc_conn, user_id)
def on_user_left(agora_rtc_conn, user_id, reason):
    print("on_user_left:", agora_rtc_conn, user_id, reason)

# def on_get_playback_audio_frame_param(agora_local_user):
#     audio_params_instance = AudioParams()
#     return audio_params_instance

def on_playback_audio_frame_before_mixing(agora_local_user, channelId, uid, frame):
    print("on_playback_audio_frame_before_mixing")#, channelId, uid)
    return 0

def on_record_audio_frame(agora_local_user ,channelId, frame):
    print("on_record_audio_frame")
    return 0

def on_playback_audio_frame(agora_local_user, channelId, frame):
    print("on_playback_audio_frame")
    return 0

def on_mixed_audio_frame(agora_local_user, channelId, frame):
    print("on_mixed_audio_frame")
    return 0

def on_ear_monitoring_audio_frame(agora_local_user, frame):
    print("on_ear_monitoring_audio_frame")
    return 0

def on_playback_audio_frame_before_mixing(agora_local_user, channelId, uid, frame):
    print("on_playback_audio_frame_before_mixing")
    return 0

def on_get_audio_frame_position(agora_local_user):
    print("on_get_audio_frame_position")
    return 0

#c api def
# AGORA_HANDLE agora_local_user, user_id_t user_id, int stream_id, const char* data, size_t length
#user_id: string type; steream_id: int, data: byte, lenght: int
def on_stream_message(local_user, user_id, stream_id, data, length):
    print("on_stream_message:", user_id, stream_id, data, length)
    #print("on_stream_message: userid is {user_id}, streamid is {stream_id}, data is {data}, length is {length }")
    return 0

#void (*on_user_info_updated)(AGORA_HANDLE agora_local_user, user_id_t user_id, int msg, int val);
#user_id: string type; msg: int, val: int
def on_user_info_updated(local_user, user_id, msg, val):
    print("on_user_info_updated:", user_id, msg, val)
    return 0

#adjust volume


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
   

    ret = audio_pcm_data_sender.SendPcmData(frame)
    print("first,ret=",packnum, ret)
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


example_dir = os.path.dirname(os.path.abspath(__file__))
pcm_file_path = os.path.join(example_dir, 'demo.pcm')

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
"""
#check vad sample file
if len(sys.argv) > 6:
    DoVadTest(sys.argv[6])
"""
print("appid:", appid, "token:", token, "channel_id:", channel_id, "pcm_file_path:", pcm_file_path, "uid:", uid)


config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = appid
config.log_path = os.path.join(example_dir, 'agorasdk.log')

agora_service = AgoraService()
agora_service.Init(config)

con_config = RTCConnConfig(
    auto_subscribe_audio=1,
    auto_subscribe_video=0,
    client_role_type=1,
    channel_profile=1,
)

pcm_observer = AudioFrameObserver(
    on_record_audio_frame=ON_RECORD_AUDIO_FRAME_CALLBACK(on_record_audio_frame),
    on_playback_audio_frame=ON_PLAYBACK_AUDIO_FRAME_CALLBACK(on_playback_audio_frame),
    on_ear_monitoring_audio_frame=ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK(on_ear_monitoring_audio_frame),
    on_playback_audio_frame_before_mixing=ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK(on_playback_audio_frame_before_mixing),
    on_get_audio_frame_position=ON_GET_AUDIO_FRAME_POSITION_CALLBACK(on_get_audio_frame_position),
)

con_config.pcm_observer = pcm_observer

connection = agora_service.NewConnection(con_config)

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

conn_observer = RTCConnObserver(
    on_connected=ON_CONNECTED_CALLBACK(on_connected),
    on_disconnected=ON_CONNECTED_CALLBACK(on_disconnected),
    on_user_joined=ON_USER_JOINED_CALLBACK(on_user_joined),
    on_user_left=ON_USER_LEFT_CALLBACK(on_user_left)
)
#local userobserver
localuser_observer = RTCLocalUserObserver( 
    on_stream_message=ON_STREAM_MESSAGE_CALLBACK(on_stream_message),
    on_user_info_updated=ON_USER_INFO_UPDATED_CALLBACK(on_user_info_updated)
)

connection.RegisterObserver(conn_observer,localuser_observer)

connection.Connect(token, channel_id, uid)

#vad test



# connection.SubscribeAudio(9981)

audio_pcm_data_sender = connection.NewPcmSender()
#audio_pcm_data_sender.SetSendBufferSize(320*2000)# set to 1s
sendinterval = 0.05 #unit: s

audio_pcm_data_sender.Start()

packnum = int((sendinterval*1000)/10)
with open(pcm_file_path, "rb") as file:
    #第一次读区 180ms的数据
    packnum = 18
    ret = pushPcmDatafromFile(file, packnum, audio_pcm_data_sender)
    print("first,ret=",packnum, ret)

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
            ret = pushPcmDatafromFile(file, needcompensationpack, audio_pcm_data_sender)
            if ret < 0:
                print("read file error,ret=",ret)
                #re-seek to file header
                file.seek(0, 0)
            else:
                cursendtotalpack += needcompensationpack

        time.sleep(sendinterval)
        #print("goruning = ", g_runing)
              
connection.Disconnect()
connection.Release()
print("release")
time.sleep(0.01)
agora_service.Destroy()
print("end")
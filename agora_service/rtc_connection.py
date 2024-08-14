import time
import ctypes
from .agora_base import *
from .local_user import *
from .rtc_conn_observer import *
from .audio_pcm_data_sender import AudioPcmDataSender
from .video_sender import VideoSender
from .audio_frame_observer import AudioFrameObserver


# 定义 audio_subscription_options 结构体
class AudioSubscriptionOptions(ctypes.Structure):
    _fields_ = [
        ('packet_only', ctypes.c_int),
        ('pcm_data_only', ctypes.c_int),
        ('bytes_per_sample', ctypes.c_uint32),
        ('number_of_channels', ctypes.c_uint32),
        ('sample_rate_hz', ctypes.c_uint32),
    ]



# 定义 _rtc_conn_config 结构体
class RTCConnConfig(ctypes.Structure):
    _fields_ = [
        ('auto_subscribe_audio', ctypes.c_int),
        ('auto_subscribe_video', ctypes.c_int),
        ('enable_audio_recording_or_playout', ctypes.c_int),
        ('max_send_bitrate', ctypes.c_int),
        ('min_port', ctypes.c_int),
        ('max_port', ctypes.c_int),
        ('audio_subs_options', AudioSubscriptionOptions),
        ('client_role_type', ctypes.c_int),
        ('channel_profile', ctypes.c_int),
        ('audio_recv_media_packet', ctypes.c_int),
        ('video_recv_media_packet', ctypes.c_int),

        # ('pcm_observer', ctypes.POINTER(AudioFrameObserver)),
    ]    

agora_rtc_conn_get_local_user = agora_lib.agora_rtc_conn_get_local_user
agora_rtc_conn_get_local_user.restype = AGORA_HANDLE
agora_rtc_conn_get_local_user.argtypes = [AGORA_HANDLE]

agora_rtc_conn_connect = agora_lib.agora_rtc_conn_connect
agora_rtc_conn_connect.restype = AGORA_API_C_INT
agora_rtc_conn_connect.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]


agora_rtc_conn_disconnect = agora_lib.agora_rtc_conn_disconnect
agora_rtc_conn_disconnect.restype = AGORA_API_C_INT
agora_rtc_conn_disconnect.argtypes = [AGORA_HANDLE]

agora_rtc_conn_register_observer = agora_lib.agora_rtc_conn_register_observer
agora_rtc_conn_register_observer.restype = AGORA_API_C_INT
agora_rtc_conn_register_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnObserver)]
#unregister
agora_rtc_conn_unregister_observer = agora_lib.agora_rtc_conn_unregister_observer
agora_rtc_conn_unregister_observer.restype = AGORA_API_C_INT
agora_rtc_conn_unregister_observer.argtypes = [AGORA_HANDLE]

#release
agora_rtc_conn_release = agora_lib.agora_rtc_conn_destroy
#note: for c void return type, we use default
agora_rtc_conn_release.argtypes = [AGORA_HANDLE]

agora_media_node_factory_create_audio_pcm_data_sender = agora_lib.agora_media_node_factory_create_audio_pcm_data_sender
agora_media_node_factory_create_audio_pcm_data_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_pcm_data_sender.argtypes = [AGORA_HANDLE]

agora_local_user_subscribe_audio = agora_lib.agora_local_user_subscribe_audio
agora_local_user_subscribe_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_audio.argtypes = [AGORA_HANDLE, user_id_t]

agora_local_user_unsubscribe_audio = agora_lib.agora_local_user_unsubscribe_audio
agora_local_user_unsubscribe_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_audio.argtypes = [AGORA_HANDLE, user_id_t]

#sub&unsub all audio
agora_local_user_subscribe_all_audio = agora_lib.agora_local_user_subscribe_all_audio
agora_local_user_subscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_all_audio.argtypes = [AGORA_HANDLE]

agora_local_user_unsubscribe_all_audio = agora_lib.agora_local_user_unsubscribe_all_audio
agora_local_user_unsubscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_all_audio.argtypes = [AGORA_HANDLE]

#pub&unpub audio
"""
AGORA_API_C_INT agora_local_user_publish_audio(AGORA_HANDLE agora_local_user, AGORA_HANDLE agora_local_audio_track);
AGORA_API_C_INT agora_local_user_unpublish_audio(AGORA_HANDLE agora_local_user, AGORA_HANDLE agora_local_audio_track);

"""
# agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
# agora_local_user_publish_audio.restype = AGORA_API_C_INT
# agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]
# agora_local_user_unpublish_audio = agora_lib.agora_local_user_unpublish_audio
# agora_local_user_unpublish_audio.restype = AGORA_API_C_INT
# agora_local_user_unpublish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

#mdia node: internal methods
agora_media_node_factory_create_video_frame_sender = agora_lib.agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_frame_sender.argtypes = [AGORA_HANDLE]

agora_service_create_custom_video_track_frame = agora_lib.agora_service_create_custom_video_track_frame
agora_service_create_custom_video_track_frame.restype = AGORA_HANDLE
agora_service_create_custom_video_track_frame.argtypes = [AGORA_HANDLE,AGORA_HANDLE]

agora_local_video_track_destroy = agora_lib.agora_local_video_track_destroy
agora_local_video_track_destroy.restype = AGORA_HANDLE
agora_local_video_track_destroy.argtypes = [AGORA_HANDLE]

agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = AGORA_HANDLE
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]


agora_local_user_register_audio_frame_observer = agora_lib.agora_local_user_register_audio_frame_observer
agora_local_user_register_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_register_audio_frame_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(AudioFrameObserver)]

agora_local_user_unregister_audio_frame_observer = agora_lib.agora_local_user_unregister_audio_frame_observer
agora_local_user_unregister_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_audio_frame_observer.argtypes = [AGORA_HANDLE]

agora_rtc_conn_create = agora_lib.agora_rtc_conn_create
agora_rtc_conn_create.restype = AGORA_HANDLE
agora_rtc_conn_create.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnConfig)]


agora_local_user_set_playback_audio_frame_before_mixing_parameters = agora_lib.agora_local_user_set_playback_audio_frame_before_mixing_parameters
agora_local_user_set_playback_audio_frame_before_mixing_parameters.restype = AGORA_API_C_INT
agora_local_user_set_playback_audio_frame_before_mixing_parameters.argtypes = [AGORA_HANDLE, ctypes.c_uint32, ctypes.c_uint32]

#定义datastream 有关的函数
agora_rtc_conn_create_data_stream = agora_lib.agora_rtc_conn_create_data_stream
agora_rtc_conn_create_data_stream.restype = AGORA_API_C_INT
agora_rtc_conn_create_data_stream.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]

agora_rtc_conn_send_stream_message = agora_lib.agora_rtc_conn_send_stream_message
agora_rtc_conn_send_stream_message.restype = AGORA_API_C_INT
agora_rtc_conn_send_stream_message.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]


agora_local_user_register_observer = agora_lib.agora_local_user_register_observer
agora_local_user_register_observer.restype = AGORA_API_C_INT
agora_local_user_register_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCLocalUserObserver)]

agora_local_user_unregister_observer = agora_lib.agora_local_user_unregister_observer
agora_local_user_unregister_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_observer.argtypes = [AGORA_HANDLE]

#set paramter 
#AGORA_API_C_HDL agora_rtc_conn_get_agora_parameter(AGORA_HANDLE agora_rtc_conn);
agora_rtc_conn_get_agora_parameter = agora_lib.agora_rtc_conn_get_agora_parameter
agora_rtc_conn_get_agora_parameter.restype = ctypes.c_void_p
agora_rtc_conn_get_agora_parameter.argtypes = [AGORA_HANDLE]

#AGORA_API_C_INT agora_parameter_set_parameters(AGORA_HANDLE agora_parameter, const char* json_src);
agora_parameter_set_parameters = agora_lib.agora_parameter_set_parameters
agora_parameter_set_parameters.restype = AGORA_API_C_INT
agora_parameter_set_parameters.argtypes = [AGORA_HANDLE, ctypes.c_char_p]

#renew token
#AGORA_API_C_INT agora_rtc_conn_renew_token(AGORA_HANDLE agora_rtc_conn, const char* token);
agora_rtc_conn_renew_token = agora_lib.agora_rtc_conn_renew_token
agora_rtc_conn_renew_token.restype = AGORA_API_C_INT
agora_rtc_conn_renew_token.argtypes = [AGORA_HANDLE, ctypes.c_char_p]

#unpublish video track
agora_local_user_unpublish_video = agora_lib.agora_local_user_unpublish_video
agora_local_user_unpublish_video.restype = AGORA_API_C_INT
agora_local_user_unpublish_video.argtypes = [AGORA_HANDLE, AGORA_HANDLE]



class RTCConnection:
    def __init__(self, con_config, service) -> None:
        self.service = service
        self.con_config = con_config
        conn_handle = agora_rtc_conn_create(service.service_handle, ctypes.byref(con_config))                
        self.connection = conn_handle
        #by wei to save pcm oberser 
        self.pcmobserver = con_config.pcm_observer
        #custom audio local track for push pcm data
        self.pcm_sender_track = None 
        self.con_observer = None
        self.localuser_observer = None
        self.video_track = None

        if con_config.pcm_observer != None:            
            self.local_user = agora_rtc_conn_get_local_user(conn_handle)
            # if con_config.audio_subs_options == None:
            con_config.audio_subs_options.number_of_channels = 1
            con_config.audio_subs_options.sample_rate_hz = 16000
            ret = agora_local_user_set_playback_audio_frame_before_mixing_parameters(self.local_user, con_config.audio_subs_options.number_of_channels, con_config.audio_subs_options.sample_rate_hz)
            print(f"agora_local_user_set_playback_audio_frame_before_mixing_parameters:{ret}")
            ret = agora_local_user_register_audio_frame_observer(self.local_user, con_config.pcm_observer)
            print(f"agora_local_user_register_audio_frame_observer:{ret}")
    
    def __get_local_user(self):
        if not self.local_user:            
            self.local_user = agora_rtc_conn_get_local_user(self.connection)
        return self.local_user

    def RegisterObserver(self, conn_observer, localuser_observer):

        self.con_observer = conn_observer
        self.localuser_observer = localuser_observer
        
        agora_rtc_conn_register_observer(self.connection, conn_observer)
        #register stream msessage observer
        #if not self.local_user:            
        self.local_user = agora_rtc_conn_get_local_user(self.connection)
        #register to local user
        agora_local_user_register_observer(self.local_user, localuser_observer)

    def NewPcmSender(self):
        pcm_data_sender = agora_media_node_factory_create_audio_pcm_data_sender(self.service.media_node_factory)
        self.pcm_sender_track = agora_service_create_custom_audio_track_pcm(self.service.service_handle, pcm_data_sender)
        self.local_user = agora_rtc_conn_get_local_user(self.connection)
        # agora_local_user_publish_audio(self.local_user, self.pcm_sender_track)
        return AudioPcmDataSender(pcm_data_sender, self.pcm_sender_track, self.__get_local_user())

    def GetVideoSender(self):
        video_frame_sender = agora_media_node_factory_create_video_frame_sender(self.service.media_node_factory)
        self.video_track = agora_service_create_custom_video_track_frame(self.service.service_handle, video_frame_sender)
        self.video_sender = VideoSender(video_frame_sender, self.video_track, self.__get_local_user())
        return self.video_sender

    def ReleaseVideoSender(self):
        if not self.video_sender:
            return
        agora_local_video_track_destroy(self.video_sender.video_track)
        agora_video_frame_sender_destroy(self.video_sender.video_frame_sender)
        self.video_sender = None

    def Connect(self, token, chan_id, user_id):
        return agora_rtc_conn_connect(self.connection, ctypes.create_string_buffer(token.encode('utf-8')),ctypes.create_string_buffer(chan_id.encode('utf-8')), ctypes.create_string_buffer(user_id.encode('utf-8')))
    
    def Disconnect(self):
        if not self.connection:
            return -1
        
        if self.con_config.pcm_observer != None:     
            ret = agora_local_user_unregister_audio_frame_observer(self.local_user)
            if ret != 0:
                print("agora_local_user_unregister_audio_frame_observer error:{}".format(ret))    
        ret = agora_local_user_unregister_observer(self.local_user)
        if ret != 0:
            print("agora_local_user_unregister_observer error:{}".format(ret))    

        ret = agora_rtc_conn_unregister_observer(self.connection)
        if ret != 0:
            print("agora_rtc_conn_unregister_observer error:{}".format(ret))    
     
        ret = agora_rtc_conn_disconnect(self.connection)
        if ret != 0:
            print("agora_rtc_conn_disconnect error:{}".format(ret))            
        return ret
    
    def SubscribeAudio(self, user_id):
        # return agora_local_user_subscribe_audio(self.connection, self.local_user)
        print(f"agora_local_user_subscribe_audio1")
        ret = agora_local_user_subscribe_audio(self.__get_local_user(), user_id)
        print(f"agora_local_user_subscribe_audio:{ret}")
        return ret
        # return agora_local_user_subscribe_audio(self.__get_local_user(), user_id)

    
    def UnsubscribeAudio(self, user_id):
        return agora_local_user_unsubscribe_audio(self.local_user, user_id)
    
    #sub&unsub all audio
    def SubscribeAllAudio(self):
        return agora_local_user_subscribe_all_audio(self.connection, self.local_user)
    def UnsubscribeAllAudio(self):
        return agora_local_user_unsubscribe_all_audio(self.connection, self.local_user)
    
    #return value: (stream_id, ret), ret: 0 success, -1 failed
    def CreateDataStream(self, reliable, order):
        stream_id = ctypes.c_int(0)
        ret = agora_rtc_conn_create_data_stream(self.connection, ctypes.pointer(stream_id), reliable, order)
        return stream_id.value, ret

    def SendStreamMessage(self, stream_id, msg):
        c_sream_id = ctypes.c_int(stream_id)
        message = msg.encode('utf-8')
        msglen = len(message)
        return agora_rtc_conn_send_stream_message(self.connection, c_sream_id, message, msglen)
    def Release(self):
        #unrigster all observer
        if not self.connection:
            return
            
        #then do release
        agora_rtc_conn_release(self.connection)

        #set to none
        self.con_observer = None
        self.localuser_observer = None
        self.local_user = None
        self.connection = None
        

    def SetParameter(self, jsonstr):
        #get handle first
        #then do set
        if not self.connection:
            return -1
        hdl = agora_rtc_conn_get_agora_parameter(self.connection)
        if not hdl:
            return -2
        return agora_parameter_set_parameters(hdl, jsonstr.encode('utf-8'))
    def RenewToken(self, token):
        if not self.connection:
            return
        return agora_rtc_conn_renew_token(self.connection, token.encode('utf-8'))
    


import time
import ctypes

from .agora_base import *
from .agora_service import AgoraService
from .local_user import LocalUser
from .rtc_connection_observer import IRTCConnectionObserver
from ._ctypes_handle._audio_frame_observer import AudioFrameObserverInner
from .agora_parameter import AgoraParameter
from ._utils.globals import AgoraHandleInstanceMap
from ._ctypes_handle._rtc_connection_observer import RTCConnectionObserverInner
from ._ctypes_handle._ctypes_data import *
import logging
logger = logging.getLogger(__name__)

agora_rtc_conn_create = agora_lib.agora_rtc_conn_create
agora_rtc_conn_create.restype = AGORA_HANDLE
agora_rtc_conn_create.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnConfigInner)]


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
agora_rtc_conn_register_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnectionObserverInner)]

agora_rtc_conn_unregister_observer = agora_lib.agora_rtc_conn_unregister_observer
agora_rtc_conn_unregister_observer.restype = AGORA_API_C_INT
agora_rtc_conn_unregister_observer.argtypes = [AGORA_HANDLE]

agora_rtc_conn_release = agora_lib.agora_rtc_conn_destroy
agora_rtc_conn_release.restype = AGORA_API_C_VOID
agora_rtc_conn_release.argtypes = [AGORA_HANDLE]

agora_rtc_conn_create_data_stream = agora_lib.agora_rtc_conn_create_data_stream
agora_rtc_conn_create_data_stream.restype = AGORA_API_C_INT
agora_rtc_conn_create_data_stream.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]

agora_rtc_conn_send_stream_message = agora_lib.agora_rtc_conn_send_stream_message
agora_rtc_conn_send_stream_message.restype = AGORA_API_C_INT
agora_rtc_conn_send_stream_message.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]

agora_rtc_conn_get_agora_parameter = agora_lib.agora_rtc_conn_get_agora_parameter
agora_rtc_conn_get_agora_parameter.restype = ctypes.c_void_p
agora_rtc_conn_get_agora_parameter.argtypes = [AGORA_HANDLE]

agora_rtc_conn_renew_token = agora_lib.agora_rtc_conn_renew_token
agora_rtc_conn_renew_token.restype = AGORA_API_C_INT
agora_rtc_conn_renew_token.argtypes = [AGORA_HANDLE, ctypes.c_char_p]

#AGORA_API_C_INT agora_rtc_conn_enable_encryption(AGORA_HANDLE agora_rtc_conn, int enabled, const encryption_config* config);

agora_rtc_conn_enable_encryption = agora_lib.agora_rtc_conn_enable_encryption
agora_rtc_conn_enable_encryption.restype = AGORA_API_C_INT
agora_rtc_conn_enable_encryption.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.POINTER(EncryptionConfigInner)]


class RTCConnection:
    def __init__(self, service: AgoraService, conn_config: RTCConnConfig, publish_config: RtcConnectionPublishConfig) -> None:
        self.conn_handle = None
        self.con_observer = None
        self.local_user = None
        self.rtc_engine = service
        #1 create conn_handle
        self.conn_handle = agora_rtc_conn_create(self.rtc_engine.service_handle, ctypes.byref(RTCConnConfigInner.create(conn_config)))
        if self.conn_handle is None:
            return None
        #2 create local_user
        self.local_user_handle = agora_rtc_conn_get_local_user(self.conn_handle)
        if self.local_user_handle:
            self.local_user = LocalUser(self.local_user_handle, self)
        #keep publish_config
        self.publish_config = publish_config
        #and prepare track and sender for publish
        self._audio_track = None
        self._video_track = None
        self._audio_sender = None
        self._audio_encoded_sender = None
        self._video_sender = None
        self._video_encoded_sender = None
        self._prepare_publish_track_and_sender()
        #3 set profile and scenario
        self.local_user.set_audio_scenario(self.publish_config.audio_scenario)
        audio_encoder_config = AudioEncoderConfiguration(audioProfile=self.publish_config.audio_profile)
        self.local_user.set_audio_encoder_configuration(audio_encoder_config)    
        #4 inner register qios capability observer 
        #5 prepare senders and tracks for publish, and set track properties like enable, maxbuffersize,mindelay etc
        #6. create data stream for default 
        self._data_stream_id = -1
        self._data_stream_id = self._create_data_stream(False, False)
        #7. init audio frame observer, video frame observer, video encoded frame observer

    def _prepare_publish_track_and_sender(self)->int:
        if self.publish_config.is_publish_audio:
           if self.publish_config.audio_publish_type == AudioPublishType.AUDIO_PUBLISH_TYPE_PCM:
               self._audio_sender = self.rtc_engine.media_node_factory.create_audio_pcm_data_sender()
               self._audio_track = self.rtc_engine._create_custom_audio_track_pcm(self._audio_sender, self.publish_config.audio_scenario)
           elif self.publish_config.audio_publish_type == AudioPublishType.AUDIO_PUBLISH_TYPE_ENCODED_PCM:
               self._audio_encoded_sender = self.rtc_engine.media_node_factory.create_audio_encoded_data_sender()
               self._audio_track = self.rtc_engine.create_custom_audio_track_encoded(self.audio_encoded_sender)
        if self.publish_config.is_publish_video:
            if self.publish_config.video_publish_type == VideoPublishType.VIDEO_PUBLISH_TYPE_YUV:
                self._video_sender = self.rtc_engine.media_node_factory.create_video_frame_sender()
                self._video_track = self.rtc_engine.create_custom_video_track_frame(self._video_sender)
            elif self.publish_config.video_publish_type == VideoPublishType.VIDEO_PUBLISH_TYPE_ENCODED_IMAGE:
                self._video_encoded_sender = self.rtc_engine.media_node_factory.create_video_encoded_data_sender()
                self._video_track = self.rtc_engine.create_custom_video_track_encoded(self._video_encoded_sender)
        if self._audio_track:
            self._audio_track.set_enabled(True)
        if self._video_track:
            self._video_track.set_enabled(True)
        return 0
      

    #
    def connect(self, token: str, chan_id: str, user_id: str) -> int:
        ret = agora_rtc_conn_connect(self.conn_handle, ctypes.create_string_buffer(token.encode('utf-8')), ctypes.create_string_buffer(chan_id.encode('utf-8')), ctypes.create_string_buffer(user_id.encode('utf-8')))
        return ret

    #
    def disconnect(self) -> int:
        #1. unpublish all tracks
        self.unpublish_audio()
        self.unpublish_video()

        #2. unregister all observers, but except rtc connection observer
        self._unregister_audio_frame_observer()
        self._unregister_video_frame_observer()
        self._unregister_video_encoded_frame_observer()
        self._unregister_audio_encoded_frame_observer()

        self._unregister_local_user_observer()

        

        ret = agora_rtc_conn_disconnect(self.conn_handle)
        return ret

    # update token when token expired
    def renew_token(self, token) -> int:
        ret = agora_rtc_conn_renew_token(self.conn_handle, token.encode('utf-8'))
        return ret

    #
    def register_observer(self, conn_observer: IRTCConnectionObserver) -> int:
        ret = -1000
        if self.con_observer:
            self._unregister_observer()
        self.con_observer = RTCConnectionObserverInner(conn_observer, self)
        ret = agora_rtc_conn_register_observer(self.conn_handle, self.con_observer)
        return ret
    #
    def _unregister_observer(self) -> int:
        ret = 0
        if self.con_observer:
            ret = agora_rtc_conn_unregister_observer(self.conn_handle)
        self.con_observer = None
        return ret
    
    # send data stream message to connection
    def send_stream_message(self, data) -> int:
        encoded_data = data.encode('utf-8')
        length = len(encoded_data)
        ret = agora_rtc_conn_send_stream_message(
            self.conn_handle,
            self._data_stream_id,
            encoded_data,
            length
        )
        return ret

    #
    def get_agora_parameter(self):
        agora_parameter = agora_rtc_conn_get_agora_parameter(self.conn_handle)
        if not agora_parameter:
            return None
        return AgoraParameter(agora_parameter)

    #

    def get_local_user(self):
        return self.local_user
   
    def enable_encryption(self, enabled: int, config: EncryptionConfig) -> int:
        """
        Enables or disables encryption for the connection.

        Args:
            enabled (int): 1 to enable encryption, 0 to disable.
            config (EncryptionConfig): The encryption configuration.

        Returns:
            int: The result of the operation. 0 if successful, otherwise an error code.
        Note:
            This method must be called before self.connect()
        """
        if enabled == 0:
            return 0
        
        inner_config = EncryptionConfigInner.create(config)
        return agora_rtc_conn_enable_encryption(self.conn_handle, enabled, ctypes.byref(inner_config))

    def release(self):
        # release con observer
        self._unregister_observer()
        # release local user
        self.local_user._release()
        # release local user map
        if self.conn_handle:
            #AgoraHandleInstanceMap().del_local_user_map(self.conn_handle)
            agora_rtc_conn_release(self.conn_handle)
        self.conn_handle = None
        self.local_user = None

        #relese tracks 
        if self._audio_track:
            self._audio_track.release()
            self._audio_track = None
        if self._video_track:
            self._video_track.release()
            self._video_track = None
        if self._audio_sender:
            self._audio_sender.release()
            self._audio_sender = None
        if self._audio_encoded_sender:
            self._audio_encoded_sender.release()
            self._audio_encoded_sender = None
        if self._video_sender:
            self._video_sender.release()
            self._video_sender = None
        if self._video_encoded_sender:
            self._video_encoded_sender.release()
            self._video_encoded_sender = None
            #release data stream
        
        self._data_stream_id = -1
      


    #from verison 2.3.0 new added & modified
        # create a data stream
    def _create_data_stream(self, reliable, ordered) -> int:
        stream_id = ctypes.c_int(0)
        ret = agora_rtc_conn_create_data_stream(self.conn_handle, ctypes.byref(stream_id), int(reliable), int(ordered))
        if ret < 0:
            return None
        return stream_id.value
    
    def register_audio_frame_observer(self, observer,  enable_vad: int, vad_configure) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._register_audio_frame_observer(observer, enable_vad, vad_configure)
        return ret  
    def register_local_user_observer(self, observer) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._register_local_user_observer(observer)
        return ret
    def register_video_frame_observer(self, observer) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._register_video_frame_observer(observer)
        return ret
    def register_video_encoded_frame_observer(self, observer) -> int:   
        ret = -1000
        if self.local_user:
            ret = self.local_user._register_video_encoded_frame_observer(observer)
        return ret
    def register_audio_encoded_frame_observer(self, observer) -> int:
        ret = -1000
        #todo: need to implement， but not used now
        return ret
    def _unregister_audio_frame_observer(self) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._unregister_audio_frame_observer()
        return ret
    def _unregister_local_user_observer(self) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._unregister_local_user_observer()
        return ret
    def _unregister_video_frame_observer(self) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._unregister_video_frame_observer()
        return ret
    def _unregister_video_encoded_frame_observer(self) -> int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._unregister_video_encoded_frame_observer()
        return ret
    def _unregister_audio_encoded_frame_observer(self) -> int:
        ret = -1000
        #todo: need to implement， but not used now
        return ret
    def publish_audio(self)->int:
        ret = -1000
        if self.local_user and self._audio_track:
            ret = self.local_user._publish_audio(self._audio_track)
        return ret
    def unpublish_audio(self)->int:
        ret = -1000
        if self.local_user and self._audio_track:
            ret = self.local_user._unpublish_audio(self._audio_track)
        return ret
    def publish_video(self)->int:
        ret = -1000
        if self.local_user and self._video_track:
            ret = self.local_user._publish_video(self._video_track)
        return ret
    def unpublish_video(self)->int:
        ret = -1000
        if self.local_user and self._video_track:
            ret = self.local_user._unpublish_video(self._video_track)
        return ret
    def interrupt_audio(self)->int:
        ret = -1000
        if self.local_user is None:
            ret = -1001
        elif self.publish_config.audio_scenario == AudioScenarioType.AUDIO_SCENARIO_AI_SERVER:
            self.unpublish_audio()
            self.publish_audio()
        elif self._audio_track:
            self._audio_track.clear_sender_buffer()
        return ret
    def send_audio_meta_data(self, data)->int:
        ret = -1000
        if self.local_user:
            ret = self.local_user._send_audio_meta_data(data)
        return ret

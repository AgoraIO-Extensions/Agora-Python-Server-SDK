import time
import ctypes

from .agora_base import *
from .agora_service import AgoraService, _set_filter_property_by_track
from .local_user import LocalUser
from .rtc_connection_observer import IRTCConnectionObserver
from ._ctypes_handle._audio_frame_observer import AudioFrameObserverInner
from .agora_parameter import AgoraParameter
from ._utils.globals import AgoraHandleInstanceMap
from ._ctypes_handle._rtc_connection_observer import RTCConnectionObserverInner, CapabilitiesObserverInner
from ._ctypes_handle._ctypes_data import *
from .utils.audio_consumer import PcmConsumeStats
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

#aiqoscapability observer
agora_local_user_capabilities_observer_create = agora_lib.agora_local_user_capabilities_observer_create
agora_local_user_capabilities_observer_create.restype = AGORA_API_C_HDL
agora_local_user_capabilities_observer_create.argtypes = [ctypes.POINTER(CapabilitiesObserverInner)]

agora_local_user_capabilities_observer_destory = agora_lib.agora_local_user_capabilities_observer_destory
agora_local_user_capabilities_observer_destory.restype = AGORA_API_C_VOID
agora_local_user_capabilities_observer_destory.argtypes = [AGORA_HANDLE]


agora_local_user_register_capabilities_observer = agora_lib.agora_local_user_register_capabilities_observer
agora_local_user_register_capabilities_observer.restype = AGORA_API_C_INT
agora_local_user_register_capabilities_observer.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unregister_capabilities_observer = agora_lib.agora_local_user_unregister_capabilities_observer
agora_local_user_unregister_capabilities_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_capabilities_observer.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

class RTCConnection:
    def __init__(self, service: AgoraService, conn_config: RTCConnConfig, publish_config: RtcConnectionPublishConfig) -> None:
        self.conn_handle = None
        self.con_observer_handle = None
        self.local_user = None
        self.rtc_engine = service
        self._con_observer = None
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
        self._pcm_consume_stats = PcmConsumeStats()
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
        #7. register capabilities observer
        self._capabilities_observer_handle = None
        self._capabilities_observer_obj = None
        if self.publish_config.audio_scenario == AudioScenarioType.AUDIO_SCENARIO_AI_SERVER:
            self._register_capabilities_observer()

    def _prepare_publish_track_and_sender(self)->int:
        if self.publish_config.is_publish_audio:
           if self.publish_config.audio_publish_type == AudioPublishType.AUDIO_PUBLISH_TYPE_PCM:
               self._audio_sender = self.rtc_engine.media_node_factory.create_audio_pcm_data_sender()
               self._audio_track = self.rtc_engine._create_custom_audio_track_pcm(self._audio_sender, self.publish_config.audio_scenario)
           elif self.publish_config.audio_publish_type == AudioPublishType.AUDIO_PUBLISH_TYPE_ENCODED_PCM:
               self._audio_encoded_sender = self.rtc_engine.media_node_factory.create_audio_encoded_frame_sender()
               self._audio_track = self.rtc_engine.create_custom_audio_track_encoded(self._audio_encoded_sender, 1)#mix_mode: MIX_ENABLED = 0, MIX_DISABLED = 1
        if self.publish_config.is_publish_video:
            if self.publish_config.video_publish_type == VideoPublishType.VIDEO_PUBLISH_TYPE_YUV:
                self._video_sender = self.rtc_engine.media_node_factory.create_video_frame_sender()
                self._video_track = self.rtc_engine.create_custom_video_track_frame(self._video_sender)
            elif self.publish_config.video_publish_type == VideoPublishType.VIDEO_PUBLISH_TYPE_ENCODED_IMAGE:
                self._video_encoded_sender = self.rtc_engine.media_node_factory.create_video_encoded_image_sender()
                self._video_track = self.rtc_engine.create_custom_video_track_encoded(self._video_encoded_sender, self.publish_config.video_encoded_image_sender_options)
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
        if self.con_observer_handle:
            self._unregister_observer()
        self.con_observer_handle = RTCConnectionObserverInner(conn_observer, self)
        self._con_observer = conn_observer
        ret = agora_rtc_conn_register_observer(self.conn_handle, self.con_observer_handle)
        return ret
    #
    def _unregister_observer(self) -> int:
        ret = 0
        if self.con_observer_handle:
            ret = agora_rtc_conn_unregister_observer(self.conn_handle)
        self.con_observer_handle = None
        return ret
    
    # send data stream message to connection
    def send_stream_message(self, data) -> int:
        length = len(data)
        c_data = ctypes.c_char_p(data)
        ret = agora_rtc_conn_send_stream_message(
            self.conn_handle,
            self._data_stream_id,
            c_data,
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
        self._unregister_and_release_capabilities_observer()
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
    """
    Args:
        data: bytes, the audio data to send
        sample_rate: int, the sample rate of the audio data
        channels: int, the number of channels of the audio data
    Returns:
        int, the result of the operation. 0 if successful, otherwise an error code.
    Note:
        This method is used to send audio data to the server.
        The data is a bytes object, and the sample rate and channels are the sample rate and channels of the audio data.
        The data length MUST be a multiple of the number of channels * 2 * sample_rate / 1000, i.e the bytes in 1ms.
        for example, if the sample rate is 16000 and the channels is 1, the data length MUST be multiple of 16000 * 2 * 1 / 1000 = 32.
        
    """
    def push_audio_pcm_data(self, data, sample_rate, channels, start_pts:int=0)->int:
        ret = -1000
        if self._audio_sender is None:
            return -1001
        readLen = len(data)
        bytes_per_frame_in_ms = (sample_rate / 1000) * 2 * channels
        remainder = readLen % bytes_per_frame_in_ms
        if remainder != 0:
            return -1002
        pack_num_in_ms = readLen // bytes_per_frame_in_ms
        
        frame = PcmAudioFrame()
        frame.data = data
        frame.sample_rate = sample_rate
        frame.number_of_channels = channels
        frame.bytes_per_sample = 2
        frame.timestamp = 0
        frame.samples_per_channel = readLen // (channels * 2)
        frame.present_time_ms = start_pts

        ret = self._audio_sender.send_audio_pcm_data(frame)
        self._pcm_consume_stats.add_pcm_data(readLen, sample_rate, channels)
        return ret
    def push_audio_encoded_data(self, data, info: EncodedAudioFrameInfo)->int:
        ret = -1000
        if self._audio_encoded_sender:
            ret = self._audio_encoded_sender.send_encoded_audio_frame_withbytes(data, info)
        return ret
    
    def push_video_frame(self, frame: ExternalVideoFrame)->int:
        ret = -1000
        if self._video_sender:
            ret = self._video_sender.send_video_frame(frame)
        return ret
    def push_video_encoded_data(self, data,  info: EncodedVideoFrameInfo)->int:
        ret = -1000
        if self._video_encoded_sender:
            ret = self._video_encoded_sender.send_encoded_video_image_withbytes(data, info)
        return ret
    def update_audio_scenario(self, scenario: AudioScenarioType)->int:
        ret = -1000
        #1. validity check
        if self is None or self.conn_handle is None:
            return -1001
        if self.publish_config.audio_scenario == scenario:
            return 0
        #2. unpublish audio
        self.unpublish_audio()
        #3. change scenario
        self.local_user.set_audio_scenario(scenario)
        #4. update audio track
        
        updated_track = None
        delayed_del_track = None
        if self._audio_sender:
            updated_track = self.rtc_engine._create_custom_audio_track_pcm(self._audio_sender, scenario)
        elif self._audio_encoded_sender:
            updated_track = self.rtc_engine.create_custom_audio_track_encoded(self._audio_encoded_sender, scenario)
            
        if updated_track:
            delayed_del_track = self._audio_track
            self._audio_track = updated_track
            self._audio_track.set_enabled(True)
      
        if delayed_del_track:
            delayed_del_track.release()
       
        #5. update scenario
        self.local_user.set_audio_scenario(scenario)
        self.publish_config.audio_scenario = scenario
        ret = self.publish_audio()
        return ret
    def set_video_encoder_configuration(self, config: VideoEncoderConfiguration)->int:
        ret = -1000
        #ensure video track is yuv type
        if self._video_track and self._video_sender:
            ret = self._video_track.set_video_encoder_configuration(config)
        return ret
    def is_push_to_rtc_completed(self) -> bool:
        return self._pcm_consume_stats.is_push_to_rtc_completed()
    def _on_capabilities_changed(self, capabilities)->int:
        ret = -1000
        if self.conn_handle is None:
            return -1001
        fallback_scenario = True
        #capabilities is a list of Capabilities
        index = 0
        item_index = 0
        for cap in capabilities:
            item_index = 0
            print(f"Capability[{index}] - Type: {cap.capability_type}")
            index += 1
            for item in cap.item_map.item:
                print(f"Item[{item_index}] - ID: {item.id}, Name: {item.name}")
                item_index += 1
                if cap.capability_type == 19 and item.name and item.name.upper() == "SUPPORT":
                    fallback_scenario = False
                    break
        #a magic number to indicate different logic processing path
        custome_specified = -987654321
        if fallback_scenario and self._con_observer and self._con_observer.on_aiqos_capability_missing:
            self.publish_config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_AI_SERVER
            
            custome_specified = self._con_observer.on_aiqos_capability_missing(self, AudioScenarioType.AUDIO_SCENARIO_GAME_STREAMING)
            if custome_specified >= 0:
                self.update_audio_scenario(AudioScenarioType(custome_specified))
           
        print(f"update audio scenario to {fallback_scenario},custom_specified: {custome_specified}")
        return ret
    
    def _register_capabilities_observer(self)->int:
        if self.conn_handle is None:
            return -1001
        self._capabilities_observer_obj = CapabilitiesObserverInner(self)
        #create a handle for capabilities observer
        self._capabilities_observer_handle = agora_local_user_capabilities_observer_create(self._capabilities_observer_obj)
        if self._capabilities_observer_handle is None:
            return -1002
        #register capabilities handle
        ret = agora_local_user_register_capabilities_observer(self.local_user_handle, self._capabilities_observer_handle)
        if ret < 0:
            return -1003
        return 0
    def _unregister_and_release_capabilities_observer(self)->int:
        if self.conn_handle is None:
            return -1001
        if self._capabilities_observer_handle is None:
            return 0
        ret = agora_local_user_unregister_capabilities_observer(self.local_user_handle, self._capabilities_observer_handle)
        #anyway, release capabilities observer
        #release capabilities observer
        if self._capabilities_observer_handle:
            agora_local_user_capabilities_observer_destory(self._capabilities_observer_handle)
            self._capabilities_observer_handle = None
        if self._capabilities_observer_obj:
            self._capabilities_observer_obj = None
        return 0

    def _set_apm_filter_properties(self, remote_audio_track_handle, user_id_str)->int:
        ret = -1000
        is_enabled = self.rtc_engine.enable_apm
        if not is_enabled:
            return -1001
        apm_config = self.rtc_engine.apm_config
        if apm_config is None:
            return -1002
        apm_config_json = apm_config._to_json_string()
        if apm_config_json is None:
            return -1003
        #Load AINS resource
        ret = _set_filter_property_by_track(remote_audio_track_handle, "audio_processing_remote_playback", "apm_load_resource", "ains", False)
        
        print(f"**********APM: to set apm_load_resource, error: {ret}")
        

	    #Set APM configuration
        ret = _set_filter_property_by_track(remote_audio_track_handle, "audio_processing_remote_playback", "apm_config", apm_config_json, False)
        print(f"**********APM: to set apm_config, error: {ret}, apm_config_json: {apm_config_json}")
        #Enable dump
        if apm_config.enable_dump:
            ret = _set_filter_property_by_track(remote_audio_track_handle, "audio_processing_remote_playback", "apm_dump", "true", False)
            print(f"**********APM: to enable apm_dump, error: {ret}")
        return ret
    
    
    
import time
import ctypes

from .agora_base import *
from .agora_service import AgoraService, _set_filter_property_by_track, _enable_audio_filter_by_track
from .local_user import LocalUser
from .rtc_connection_observer import IRTCConnectionObserver
from ._ctypes_handle._audio_frame_observer import AudioFrameObserverInner
from .agora_parameter import AgoraParameter
from ._utils.globals import AgoraHandleInstanceMap
from ._ctypes_handle._rtc_connection_observer import RTCConnectionObserverInner, CapabilitiesObserverInner
from ._ctypes_handle._ctypes_data import *
from .utils.audio_consumer import PcmConsumeStats
from .voice_detection import AudioVadConfigV2, AudioVadV2
import logging
logger = logging.getLogger(__name__)




class IAudioSinkObserver:
    def on_processed_audio_frame(self,processor: 'ExternalAudioProcessor',frame: AudioFrame,vad_result_state:int,vad_result_data:bytearray):
        pass

agora_audio_sink_create = agora_lib.agora_audio_sink_create
agora_audio_sink_create.restype = ctypes.c_void_p
agora_audio_sink_create.argtypes = [ctypes.c_void_p]

agora_audio_track_add_audio_sink = agora_lib.agora_audio_track_add_audio_sink
agora_audio_track_add_audio_sink.restype = ctypes.c_int
agora_audio_track_add_audio_sink.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(AudioSinkWantesInner)]

agora_audio_sink_destroy = agora_lib.agora_audio_sink_destroy
agora_audio_sink_destroy.restype = None
agora_audio_sink_destroy.argtypes = [ctypes.c_void_p]

#call back dec
ON_AUDIO_SINK_DATA_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(AudioPcmFrameInner))


class AudioSinkObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_audio_sink_data", ON_AUDIO_SINK_DATA_CALLBACK),
        ("user_data", ctypes.c_void_p),
    ]
    def __init__(self, processor: 'ExternalAudioProcessor'):
        self.on_audio_sink_data = ON_AUDIO_SINK_DATA_CALLBACK(self._on_audio_sink_data)
        self._processor = processor
        pass
    def _on_audio_sink_data(self, handle: ctypes.c_void_p, audio_pcm_frame_inner_ptr: ctypes.POINTER(AudioPcmFrameInner)):

        #validity check
        if audio_pcm_frame_inner_ptr is None:
            return -1000
    
        #convert to aduioframe, and get user data
        pcm_frame = audio_pcm_frame_inner_ptr.contents
       
        #conver to audioframe
        audio_frame = pcm_frame.get()
        
        if self._processor:
            self._processor._do_result_frame(audio_frame)

        return 0

class AudioSink:
    def __init__(self, audio_processor: 'ExternalAudioProcessor'):
        self._audio_sink_observer_inner = None
        self._c_sink = None
        self._audio_processor = audio_processor
        pass
    def release(self):
        if self._c_sink:
            agora_audio_sink_destroy(ctypes.c_void_p(self._c_sink))
            self._c_sink = None
        self._audio_sink_observer_inner = None
        self._audio_processor = None
        pass

class ExternalAudioProcessor:
    
    def __init__(self, engine: AgoraService):
        self._pcm_sender = None
        self._local_audio_track = None
        self._engine = engine
        self._is_initialized = False
        #do create sender and track
        self._pcm_sender = self._engine.media_node_factory.create_audio_pcm_data_sender()
        self._local_audio_track = self._engine._create_custom_audio_track_pcm(self._pcm_sender, AudioScenarioType.AUDIO_SCENARIO_DEFAULT)
        self._audio_sink = self._create_audio_sink()
        self._vad_instance = None
        self._observer = None
        pass
    def initialize(self, apm_config: APMConfig, out_sample_rate: int, out_channels: int, vad_config: AudioVadConfigV2, observer: IAudioSinkObserver)->int:
        if self._is_initialized:
            return 0
        if apm_config is None and vad_config is None:
            logger.error("[ExternalAudioProcessor] apm_config and vad_config are both None")
            return -1000
        if out_sample_rate <= 0 or out_channels <= 0:
            logger.error("[ExternalAudioProcessor] out_sample_rate or out_channels is invalid")
            return -1001
        if observer is None:
            logger.error("[ExternalAudioProcessor] observer is None")
            return -1002

               #set filer properties
        ret = self._set_filter_properties(apm_config)
        if ret < 0:
            logger.info(f"[ExternalAudioProcessor] Failed to set filter properties, error: {ret}")
            return ret

        #add sink
        ret = self._add_audio_sink(out_sample_rate, out_channels)
        if ret < 0:
            logger.info(f"[ExternalAudioProcessor] Failed to add audio sink, error: {ret}")
            return ret
 
        #set track properties
        self._local_audio_track.set_send_delay_ms(10)
        self._local_audio_track.set_max_buffer_audio_frame_number(100000)
        self._local_audio_track.set_enabled(True)

        self._observer = observer

        # create vad instance
        if vad_config is not None:
            self._vad_instance = AudioVadV2(vad_config)
        return ret
        pass
        
    def push_audio_pcm_data(self, data, sample_rate, channels, start_pts:int=0)->int:
        ret = -1000
        if self._pcm_sender is None:
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

        ret = self._pcm_sender.send_audio_pcm_data(frame)
        return ret
    def _create_audio_sink(self)->AudioSink:
        audio_sink = AudioSink(self)
        audio_sink_observer_inner = AudioSinkObserverInner(self)
        audio_sink._audio_sink_observer_inner = audio_sink_observer_inner
        audio_sink._c_sink = agora_audio_sink_create(ctypes.byref(audio_sink_observer_inner))
        if audio_sink._c_sink is None:
            return None
        
        return audio_sink
    def _add_audio_sink(self, out_sample_rate: int, out_channels: int)->int:
        if self._audio_sink is None or self._audio_sink._c_sink is None:
            return -1000

        # call to c api
        wants = AudioSinkWantesInner(samples_per_sec=out_sample_rate, channels=out_channels)
        ret = agora_audio_track_add_audio_sink(self._local_audio_track.track_handle, self._audio_sink._c_sink, ctypes.byref(wants))
        return ret
        pass
    def _set_filter_properties(self, apm_config: APMConfig)->int:
        if self._audio_sink is None or self._audio_sink._c_sink is None:
            return -2000
        if apm_config is None:
            return 0
        #call to c api
        track_handle = self._local_audio_track.track_handle
        ret = _enable_audio_filter_by_track(track_handle, "audio_processing_pcm_source", True, True)
        if ret != 0:
            logger.info(f"[ExternalAudioProcessor] Failed to enable audio filter by track, error: {ret}")
            return -2003

        ret = _set_filter_property_by_track(track_handle, "audio_processing_pcm_source", "apm_load_resource", "ains", True)
        if ret != 0:
            logger.info(f"[ExternalAudioProcessor] Failed to set filter property by track, error: {ret}")
            return -2004

        apm_config_json = apm_config._to_json_string()
        if apm_config_json is None:
            logger.info(f"[ExternalAudioProcessor] Failed to get apm config json")
            return -2005


        ret = _set_filter_property_by_track(track_handle, "audio_processing_pcm_source", "apm_config", apm_config_json, True)
        if ret != 0:
            logger.info(f"[ExternalAudioProcessor]Failed to set filter property by track, error: {ret}")
            return -2006
        logger.info(f"[ExternalAudioProcessor] apm configure json: {apm_config_json}")

        if apm_config.enable_dump:
            ret = _set_filter_property_by_track(track_handle, "audio_processing_pcm_source", "apm_dump", "true", True)
            if ret != 0:
                logger.info(f"[ExternalAudioProcessor] Failed to set filter property by track, error: {ret}")
                return -2007
        
        return ret
    def _do_result_frame(self, audio_frame: AudioFrame):
        print(f"ExternalAudioProcessor _do_result_frame: audio_frame voice_prob {audio_frame.voice_prob}, rms {audio_frame.rms}, pitch {audio_frame.pitch}, far_field_flag {audio_frame.far_field_flag}")
        ret  = 0
        data = None
        if self._vad_instance is not None:
            ret, data = self._vad_instance.process(audio_frame)
            print(f"ExternalAudioProcessor _do_result_frame: vad result ret {ret}, data length {len(data)}")
        #do callback now
        if self._observer is not None:
            self._observer.on_processed_audio_frame(self, audio_frame, ret, data)
        pass




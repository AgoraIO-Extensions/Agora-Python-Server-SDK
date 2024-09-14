import ctypes
from .agora_base import *
from .local_user import *
import ctypes
from .audio_frame_observer import *


class AudioFrameInner(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("samples_per_channel", ctypes.c_int),
        ("bytes_per_sample", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("samples_per_sec", ctypes.c_int),
        ("buffer", ctypes.c_void_p),
        ("render_time_ms", ctypes.c_int64),
        ("avsync_type", ctypes.c_int)
    ]
    def _to_audio_frame(self):
        audio_frame = AudioFrame()
        audio_frame.type = self.type
        audio_frame.samples_per_channel = self.samples_per_channel
        audio_frame.bytes_per_sample = self.bytes_per_sample
        audio_frame.channels = self.channels
        audio_frame.samples_per_sec = self.samples_per_sec
        cdata = ctypes.string_at(self.buffer, self.samples_per_channel * self.bytes_per_sample * self.channels)
        audio_frame.buffer = bytearray(cdata)
        audio_frame.render_time_ms = self.render_time_ms
        audio_frame.avsync_type = self.avsync_type
        return audio_frame
    

ON_RECORD_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrameInner))
ON_PLAYBACK_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrameInner))
ON_MIXED_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrameInner))
ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.POINTER(AudioFrameInner))
ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(AudioFrameInner))
ON_GET_AUDIO_FRAME_POSITION_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE)
ON_GET_PLAYBACK_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_RECORD_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_MIXED_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_EAR_MONITORING_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)

class AudioFrameObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_record_audio_frame", ON_RECORD_AUDIO_FRAME_CALLBACK),
        ("on_playback_audio_frame", ON_PLAYBACK_AUDIO_FRAME_CALLBACK),
        ("on_mixed_audio_frame", ON_MIXED_AUDIO_FRAME_CALLBACK),
        ("on_ear_monitoring_audio_frame", ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK),

        ("on_playback_audio_frame_before_mixing", ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK),
        ("on_get_audio_frame_position", ON_GET_AUDIO_FRAME_POSITION_CALLBACK),
        ("on_get_playback_audio_frame_param", ON_GET_PLAYBACK_AUDIO_FRAME_PARAM_CALLBACK),
        ("on_get_record_audio_frame_param", ON_GET_RECORD_AUDIO_FRAME_PARAM_CALLBACK),
        
        ("on_get_mixed_audio_frame_param", ON_GET_MIXED_AUDIO_FRAME_PARAM_CALLBACK),
        ("on_get_ear_monitoring_audio_frame_param", ON_GET_EAR_MONITORING_AUDIO_FRAME_PARAM_CALLBACK)
    ]

    def __init__(self, observer:IAudioFrameObserver, local_user: 'LocalUser'):
        self.observer = observer
        self.local_user = local_user
        self.on_record_audio_frame = ON_RECORD_AUDIO_FRAME_CALLBACK(self._on_record_audio_frame)
        self.on_playback_audio_frame = ON_PLAYBACK_AUDIO_FRAME_CALLBACK(self._on_playback_audio_frame)
        self.on_mixed_audio_frame = ON_MIXED_AUDIO_FRAME_CALLBACK(self._on_mixed_audio_frame)
        self.on_ear_monitoring_audio_frame = ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK(self._on_ear_monitoring_audio_frame)
        self.on_playback_audio_frame_before_mixing = ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK(self._on_playback_audio_frame_before_mixing)
        self.on_get_audio_frame_position = ON_GET_AUDIO_FRAME_POSITION_CALLBACK(self._on_get_audio_frame_position)

        # self.on_get_playback_audio_frame_param = ON_GET_PLAYBACK_AUDIO_FRAME_PARAM_CALLBACK(self._on_get_playback_audio_frame_param)
        # self.on_get_record_audio_frame_param = ON_GET_RECORD_AUDIO_FRAME_PARAM_CALLBACK(self._on_get_record_audio_frame_param)
        # self.on_get_mixed_audio_frame_param = ON_GET_MIXED_AUDIO_FRAME_PARAM_CALLBACK(self._on_get_mixed_audio_frame_param)
        # self.on_get_ear_monitoring_audio_frame_param = ON_GET_EAR_MONITORING_AUDIO_FRAME_PARAM_CALLBACK(self._on_get_ear_monitoring_audio_frame_param)

    def _on_record_audio_frame(self, local_user_handle, channel_id, audio_frame_inner):
        print("AudioFrameObserverInner _on_record_audio_frame", local_user_handle, channel_id, audio_frame_inner)
        channel_id_str = channel_id.decode('utf-8')
        frame = audio_frame_inner.contents._to_audio_frame()
        ret = self.observer.on_record_audio_frame(self.local_user, channel_id_str, frame)
        return ret

    def _on_playback_audio_frame(self, local_user_handle, channel_id, audio_frame_inner):
        print("AudioFrameObserverInner _on_playback_audio_frame", local_user_handle, channel_id, audio_frame_inner)
        channel_id_str = channel_id.decode('utf-8')
        frame = audio_frame_inner.contents._to_audio_frame()
        ret = self.observer.on_playback_audio_frame(self.local_user, channel_id_str, frame)
        return ret

    def _on_mixed_audio_frame(self, local_user_handle, channel_id, audio_frame_inner):
        print("AudioFrameObserverInner _on_mixed_audio_frame", local_user_handle, channel_id, audio_frame_inner)
        ret = self.observer.on_mixed_audio_frame(self.local_user, audio_frame_inner)
        return ret

    def _on_ear_monitoring_audio_frame(self, local_user_handle, audio_frame_inner):
        print("AudioFrameObserverInner _on_ear_monitoring_audio_frame", local_user_handle, audio_frame_inner)
        ret = self.observer.on_ear_monitoring_audio_frame(self.local_user, audio_frame_inner)
        return ret

    def _on_playback_audio_frame_before_mixing(self, local_user_handle, channel_id, user_id, audio_frame_inner):
        print("AudioFrameObserverInner _on_playback_audio_frame_before_mixing", local_user_handle, channel_id, user_id, audio_frame_inner)
        if channel_id is None:
            channel_id_str = ""
        else:
            channel_id_str = channel_id.decode('utf-8')

        user_id_str = user_id.decode('utf-8')
        frame = audio_frame_inner.contents._to_audio_frame()
        ret = self.observer.on_playback_audio_frame_before_mixing(self.local_user, channel_id_str, user_id_str, frame)
        return ret
    
    def _on_get_audio_frame_position(self, local_user_handle):
        print("AudioFrameObserverInner _on_get_audio_frame_position", local_user_handle)
        return 0
        return self.observer.on_get_audio_frame_position(self.local_user)

    def _on_get_playback_audio_frame_param(self, local_user_handle):
        print("AudioFrameObserverInner _on_get_playback_audio_frame_param", local_user_handle)
        params = AudioParams()
        params.sample_rate = 16000  # 示例值
        params.channels = 1          # 示例值
        params.mode = 0              # 示例值
        params.samples_per_call = 1024  # 示例值
        return params
        return self.observer.on_get_playback_audio_frame_param(self.local_user)

    def _on_get_record_audio_frame_param(self, local_user_handle):
        print("AudioFrameObserverInner _on_get_record_audio_frame_param", local_user_handle)
        params = AudioParams()
        params.sample_rate = 16000  # 示例值
        params.channels = 1          # 示例值
        params.mode = 0              # 示例值
        params.samples_per_call = 1024  # 示例值
        return params
        return self.observer.on_get_record_audio_frame_param(self.local_user)

    def _on_get_mixed_audio_frame_param(self, local_user_handle):
        print("AudioFrameObserverInner _on_get_mixed_audio_frame_param", local_user_handle)
        params = AudioParams()
        params.sample_rate = 16000  # 示例值
        params.channels = 1          # 示例值
        params.mode = 0              # 示例值
        params.samples_per_call = 1024  # 示例值
        return params
        return self.observer.on_get_mixed_audio_frame_param(self.local_user)

    def _on_get_ear_monitoring_audio_frame_param(self, local_user_handle):
        print("AudioFrameObserverInner _on_get_ear_monitoring_audio_frame_param", local_user_handle)
        params = AudioParams()
        params.sample_rate = 16000  # 示例值
        params.channels = 1          # 示例值
        params.mode = 0              # 示例值
        params.samples_per_call = 1024  # 示例值
        return params
        return self.observer.on_get_ear_monitoring_audio_frame_param(self.local_user)


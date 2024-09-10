import ctypes
from .agora_base import *
from .local_user import *
import ctypes


class RAW_AUDIO_FRAME_OP_MODE_TYPE(ctypes.c_int):
    RAW_AUDIO_FRAME_OP_MODE_READ_ONLY = 0
    RAW_AUDIO_FRAME_OP_MODE_READ_WRITE = 2

class AUDIO_FRAME_POSITION(ctypes.c_int):
    AUDIO_FRAME_POSITION_PLAYBACK = 0x0001
    AUDIO_FRAME_POSITION_RECORD = 0x0002
    AUDIO_FRAME_POSITION_MIXED = 0x0004
    AUDIO_FRAME_POSITION_BEFORE_MIXING = 0x0008

class AudioFrame(ctypes.Structure):
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
    pass


class AudioParams(ctypes.Structure):
    _fields_ = [
        ("sample_rate", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("mode", ctypes.c_int),
        ("samples_per_call", ctypes.c_int)
    ]
    pass

ON_RECORD_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrame))
ON_PLAYBACK_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrame))
ON_MIXED_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(AudioFrame))
ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.POINTER(AudioFrame))
ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE, ctypes.c_char_p, user_id_t, ctypes.POINTER(AudioFrame))
ON_GET_AUDIO_FRAME_POSITION_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, AGORA_HANDLE)
ON_GET_PLAYBACK_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_RECORD_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_MIXED_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)
ON_GET_EAR_MONITORING_AUDIO_FRAME_PARAM_CALLBACK = ctypes.CFUNCTYPE(AudioParams, AGORA_HANDLE)

class AudioFrameObserver(ctypes.Structure):
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
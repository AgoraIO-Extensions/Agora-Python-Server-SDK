import ctypes
from .agora_base import *

class PcmAudioFrame:
    def __init__(self):
        self.data = []
        self.timestamp = 0
        self.samples_per_channel = 0
        self.bytes_per_sample = 0
        self.number_of_channels = 0
        self.sample_rate = 0

#ref to: https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/structagora_1_1rtc_1_1_encoded_audio_frame_advanced_settings.html
class EncodedAudioFrameAdvancedSettings:
    def __init__(self)->None:
        self.sendEvenIfEmpty = 1 #bool value, 是否发送空音频帧,default TRUE
        self.speech = 1 #bool, 是否是语音,default TRUE
class EncodedAudioFrameInfo:
    def __init__(self)->None:
        self.advancedSettings = EncodedAudioFrameAdvancedSettings()
        self.captureTimeMs = 0 #int64, 音频帧的 Unix 时间戳（毫秒）
        #int, 音频帧的编码格式; ref: https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/namespaceagora_1_1rtc#ac211c1a503d38d504c92b5f006240053
        self.codec = 1
        self.numberOfChannels = 2
        self.sampleRateHz = 16000
        #int, 对于 aac 编码格式，默认为 1024；对于 Opus 编码格式，默认为 960
        self.samplesPerChannel = 960
        

class EncodedAudioFrame:
    def __init__(self)->None:
        self.data = []
        self.size = 0
        self.audioFrameInfo = EncodedAudioFrameInfo()


agora_audio_pcm_data_sender_send = agora_lib.agora_audio_pcm_data_sender_send
agora_audio_pcm_data_sender_send.restype = AGORA_API_C_INT
agora_audio_pcm_data_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]

agora_local_audio_track_destroy = agora_lib.agora_local_audio_track_destroy
agora_local_audio_track_destroy.argtypes = [AGORA_HANDLE]

agora_audio_pcm_data_sender_destroy = agora_lib.agora_audio_pcm_data_sender_destroy
agora_audio_pcm_data_sender_destroy.argtypes = [ctypes.c_void_p]

agora_local_audio_track_set_enabled = agora_lib.agora_local_audio_track_set_enabled
agora_local_audio_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_user_publish_audio = agora_lib.agora_local_user_publish_audio
agora_local_user_publish_audio.restype = AGORA_API_C_INT
agora_local_user_publish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_user_unpublish_audio = agora_lib.agora_local_user_unpublish_audio
agora_local_user_unpublish_audio.restype = AGORA_API_C_INT
agora_local_user_unpublish_audio.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_audio_track_adjust_publish_volume = agora_lib.agora_local_audio_track_adjust_publish_volume
agora_local_audio_track_adjust_publish_volume.restype = AGORA_API_C_INT
agora_local_audio_track_adjust_publish_volume.argtypes = [AGORA_HANDLE, ctypes.c_int]

#todo: need check restype, by wei 0720
agora_local_audio_track_set_max_buffer_audio_frame_number = agora_lib.agora_local_audio_track_set_max_buffer_audio_frame_number
agora_local_audio_track_set_max_buffer_audio_frame_number.restype = AGORA_API_C_INT
agora_local_audio_track_set_max_buffer_audio_frame_number.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_audio_track_clear_buffer = agora_lib.agora_local_audio_track_clear_buffer
agora_local_audio_track_clear_buffer.restype = AGORA_API_C_INT
agora_local_audio_track_clear_buffer.argtypes = [AGORA_HANDLE]


class AudioPcmDataSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
       

    # def SendAudioPcmData(self, frame:PcmAudioFrame):
    #     c_data = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
    #     return agora_audio_pcm_data_sender_send(self.sender_handle, c_data, frame.timestamp, frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)

    def send(self, data, timestamp, samples_per_channel, bytes_per_sample, number_of_channels, sample_rate):
        c_data = (ctypes.c_char * len(data)).from_buffer(data)
        return agora_audio_pcm_data_sender_send(
            self.sender_handle,
            c_data,
            ctypes.c_uint32(timestamp),
            ctypes.c_uint32(samples_per_channel),
            ctypes.c_uint32(bytes_per_sample),
            ctypes.c_uint32(number_of_channels),
            ctypes.c_uint32(sample_rate)
        )


    
class AudioEncodedFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
    def sendEncodedAudioFrame(self, frame:EncodedAudioFrame):
        return agora_audio_encoded_frame_sender_send(self.sender_handle, frame.data, frame.length, frame.type, frame.timestamp, frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)

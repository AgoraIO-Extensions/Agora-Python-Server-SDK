import ctypes
from .agora_base import *

class PcmAudioFrame:
    def __init__(self):
        self.data = None
        self.timestamp = 0
        self.samples_per_channel = 0
        self.bytes_per_sample = 0
        self.number_of_channels = 0
        self.sample_rate = 0

#ref to: https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/structagora_1_1rtc_1_1_encoded_audio_frame_advanced_settings.html

class EncodedAudioFrame:
    def __init__(self)->None:
        self.data = []
        self.size = 0
        
        self.capture_timems = 0 #int64, 音频帧的 Unix 时间戳（毫秒）
        #int, 音频帧的编码格式; ref: https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/namespaceagora_1_1rtc#ac211c1a503d38d504c92b5f006240053
        self.codec = 1
        self.number_of_channels = 2
        self.sample_rate = 16000
        #int, 对于 aac 编码格式，默认为 1024；对于 Opus 编码格式，默认为 960
        self.samples_per_channel = 960
        self.send_even_if_empty = 1 #bool value, 是否发送空音频帧,default TRUE
        self.speech = 1 #bool, 是否是语音,default TRUE

    def to_owned_encoded_audio_frame(self):
        info = OwnedEncodedAudioFrameInfo()
        info.speech = self.speech
        info.codec = self.codec
        info.sample_rate_hz = self.sample_rate
        info.samples_per_channel = self.samples_per_channel
        info.send_even_if_empty = self.send_even_if_empty
        info.number_of_channels = self.number_of_channels
        return info


agora_audio_pcm_data_sender_send = agora_lib.agora_audio_pcm_data_sender_send
agora_audio_pcm_data_sender_send.restype = AGORA_API_C_INT
agora_audio_pcm_data_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]

"""
int32_t
AGORA_API_C_INT agora_audio_encoded_frame_sender_send(AGORA_HANDLE agora_audio_encoded_frame_sender,
                                                             const uint8_t* payload_data,
                                                             uint32_t payload_size,
                                                             const encoded_audio_frame_info* info);

 typedef struct _encoded_audio_frame_info {
  /**
   * Determines whether the audio frame source is a speech.
   * - 1: (Default) The audio frame source is a speech.
   * - 0: The audio frame source is not a speech.
   */
  int speech;
  /**
   * The audio codec: AUDIO_CODEC_TYPE.
   */
  int codec;
  /**
   * The sample rate (Hz) of the audio frame.
   */
  int sample_rate_hz;
  /**
   * The number of samples per audio channel.
   *
   * If this value is not set, it is 1024 for AAC, 960 for OPUS default.
   */
  int samples_per_channel;
  /**
   * Determines whether to sent the audio frame even when it is empty.
   * - 1: (Default) Send the audio frame even when it is empty.
   * - 0: Do not send the audio frame when it is empty.
   */
  int send_even_if_empty;
 
  int number_of_channels;

} encoded_audio_frame_info;                                                            
"""



class OwnedEncodedAudioFrameInfo(ctypes.Structure):
    _fields_ = [
        ('speech', ctypes.c_int),
        ('codec', ctypes.c_int),
        ('sample_rate_hz', ctypes.c_int),
        ('samples_per_channel', ctypes.c_int),
        ('send_even_if_empty', ctypes.c_int),
        ('number_of_channels', ctypes.c_int)
    ]

    # def __init__(self):
    #     self.speech = 1
    #     self.codec = 1
    #     self.sample_rate_hz = 16000
    #     self.samples_per_channel = 960
    #     self.send_even_if_empty = 1
    #     self.number_of_channels = 2

agora_audio_encoded_frame_sender_send = agora_lib.agora_audio_encoded_frame_sender_send
agora_audio_encoded_frame_sender_send.restype = AGORA_API_C_INT
agora_audio_encoded_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(OwnedEncodedAudioFrameInfo)]

agora_local_audio_track_destroy = agora_lib.agora_local_audio_track_destroy
agora_local_audio_track_destroy.argtypes = [AGORA_HANDLE]

agora_audio_pcm_data_sender_destroy = agora_lib.agora_audio_pcm_data_sender_destroy
agora_audio_pcm_data_sender_destroy.argtypes = [ctypes.c_void_p]


class AudioPcmDataSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle

    def send_audio_pcm_data(self, frame:PcmAudioFrame):
        c_data = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
        c_data_ptr = ctypes.cast(c_data, ctypes.POINTER(ctypes.c_void_p))
        return agora_audio_pcm_data_sender_send(self.sender_handle, c_data_ptr, frame.timestamp, frame.samples_per_channel, frame.bytes_per_sample, frame.number_of_channels, frame.sample_rate)
    
    def release(self):
        agora_audio_pcm_data_sender_destroy(self.sender_handle)


class AudioEncodedFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
    
    def send_encoded_audio_frame(self, frame:EncodedAudioFrame):
        c_date = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
        size = frame.size
        ownedinfo = frame.to_owned_encoded_audio_frame()
        return agora_audio_encoded_frame_sender_send(self.sender_handle, c_date, ctypes.c_uint32(size), ctypes.byref(ownedinfo))
    
    def release(self):
        # agora_local_audio_track_destroy(self.sender_handle)
        pass
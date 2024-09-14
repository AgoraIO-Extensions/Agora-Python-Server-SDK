import ctypes
from .agora_base import *

class EncodedAudioFrame:
    def __init__(
            self, 
            # data: bytearray = None,
            # buffer_ptr: int = 0,
            # buffer_size: int = 0,
            capture_timems: int = 0,
            codec: AudioCodecType = AudioCodecType.AUDIO_CODEC_AACLC, 
            number_of_channels: int = 1,
            sample_rate: int = 16000,
            samples_per_channel: int = 1024,
            send_even_if_empty: int = 1,
            speech: int = 1
            )->None:
        # self.data = data        
        # self.buffer_ptr = buffer_ptr
        # self.buffer_size = buffer_size
        self.capture_timems = capture_timems #int64, 音频帧的 Unix 时间戳（毫秒）
        #int, 音频帧的编码格式; ref: https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/namespaceagora_1_1rtc#ac211c1a503d38d504c92b5f006240053
        self.codec = codec
        self.number_of_channels = number_of_channels
        self.sample_rate = sample_rate
        #int, 对于 aac 编码格式，默认为 1024；对于 Opus 编码格式，默认为 960
        self.samples_per_channel = samples_per_channel
        self.send_even_if_empty = send_even_if_empty #bool value, 是否发送空音频帧,default TRUE
        self.speech = speech #bool, 是否是语音,default TRUE

    def to_owned_encoded_audio_frame(self):
        info = OwnedEncodedAudioFrameInfo()
        info.speech = self.speech
        info.codec = self.codec.value
        info.sample_rate_hz = self.sample_rate
        info.samples_per_channel = self.samples_per_channel
        info.send_even_if_empty = self.send_even_if_empty
        info.number_of_channels = self.number_of_channels
        return info


class OwnedEncodedAudioFrameInfo(ctypes.Structure):
    _fields_ = [
        ('speech', ctypes.c_int),
        ('codec', ctypes.c_int),
        ('sample_rate_hz', ctypes.c_int),
        ('samples_per_channel', ctypes.c_int),
        ('send_even_if_empty', ctypes.c_int),
        ('number_of_channels', ctypes.c_int)
    ]

    def __init__(self):
        self.speech = 0
        self.codec = 1
        self.sample_rate_hz = 16000
        self.samples_per_channel = 960
        self.send_even_if_empty = 1
        self.number_of_channels = 1

agora_audio_encoded_frame_sender_send = agora_lib.agora_audio_encoded_frame_sender_send
agora_audio_encoded_frame_sender_send.restype = AGORA_API_C_INT
agora_audio_encoded_frame_sender_send.argtypes = [AGORA_HANDLE, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(OwnedEncodedAudioFrameInfo)]

agora_local_audio_track_destroy = agora_lib.agora_local_audio_track_destroy
agora_local_audio_track_destroy.argtypes = [AGORA_HANDLE]


class AudioEncodedFrameSender:
    def __init__(self, handle) -> None:
        self.sender_handle = handle
    
    # def send_encoded_audio_frame(self, frame:EncodedAudioFrame):
    #     c_date = (ctypes.c_char * len(frame.data)).from_buffer(frame.data)
    #     ownedinfo = frame.to_owned_encoded_audio_frame()
    #     ret = agora_audio_encoded_frame_sender_send(self.sender_handle, c_date, ctypes.c_uint32(len(frame.data)), ctypes.byref(ownedinfo))
    #     if ret < 0:
    #         print("Failed to send encoded audio frame with error code: ", ret)
    #     return ret
    
    def send_encoded_audio_frame(self, buffer_ptr:int, buffer_size:int, frame:EncodedAudioFrame):
        buffer_ptr = ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_void_p))
        ownedinfo = frame.to_owned_encoded_audio_frame()
        ret = agora_audio_encoded_frame_sender_send(self.sender_handle, buffer_ptr, ctypes.c_uint32(buffer_size), ctypes.byref(ownedinfo))
        if ret < 0:
            print("Failed to send encoded audio frame with error code: ", ret)
        return ret

    
    def release(self):
        # agora_local_audio_track_destroy(self.sender_handle)
        pass
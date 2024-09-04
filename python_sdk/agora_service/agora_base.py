import time
import ctypes
from enum import Enum
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(os.path.dirname(script_dir))
lib_path = os.path.join(sdk_dir, 'agora_sdk')
if sys.platform == 'darwin':
    lib_agora_rtc_path =os.path.join(lib_path, 'libAgoraRtcKit.dylib')
elif sys.platform == 'linux':
    lib_agora_rtc_path =os.path.join(lib_path, 'libagora_rtc_sdk.so')    
try:
    agora_lib = ctypes.CDLL(lib_agora_rtc_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    print(f"Attempted to load from: {lib_agora_rtc_path}")
    sys.exit(1)


AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDLL = ctypes.c_void_p
AGORA_API_C_VOID = None
AGORA_HANDLE = ctypes.c_void_p
user_id_t = ctypes.c_char_p
AGORA_API_C_HDL = ctypes.c_void_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

class LastmileProbeOneWayResult(ctypes.Structure):
    _fields_ = [
        ("packet_loss_rate", ctypes.c_uint),
        ("jitter", ctypes.c_uint),
        ("available_bandwidth", ctypes.c_uint)
    ]

class LastmileProbeResult(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_int),
        ("uplink_report", LastmileProbeOneWayResult),
        ("downlink_report", LastmileProbeOneWayResult),
        ("rtt", ctypes.c_uint)
    ]


class RTCStats(ctypes.Structure):
    _fields_ = [
        ("connection_id", ctypes.c_uint),
        ("duration", ctypes.c_uint),
        ("tx_bytes", ctypes.c_uint),
        ("rx_bytes", ctypes.c_uint),
        ("tx_audio_bytes", ctypes.c_uint),
        ("tx_video_bytes", ctypes.c_uint),
        ("rx_audio_bytes", ctypes.c_uint),
        ("rx_video_bytes", ctypes.c_uint),
        ("tx_k_bit_rate", ctypes.c_ushort),
        ("rx_k_bit_rate", ctypes.c_ushort),
        ("rx_audio_k_bit_rate", ctypes.c_ushort),
        ("tx_audio_k_bit_rate", ctypes.c_ushort),
        ("rx_video_k_bit_rate", ctypes.c_ushort),
        ("tx_video_k_bit_rate", ctypes.c_ushort),
        ("lastmile_delay", ctypes.c_ushort),
        ("user_count", ctypes.c_uint),
        ("cpu_app_usage", ctypes.c_double),
        ("cpu_total_usage", ctypes.c_double),
        ("gateway_rtt", ctypes.c_int),
        ("memory_app_usage_ratio", ctypes.c_double),
        ("memory_total_usage_ratio", ctypes.c_double),
        ("memory_app_usage_in_kbytes", ctypes.c_int),
        ("connect_time_ms", ctypes.c_int),
        ("first_audio_packet_duration", ctypes.c_int),
        ("first_video_packet_duration", ctypes.c_int),
        ("first_video_key_frame_packet_duration", ctypes.c_int),
        ("packets_before_first_key_frame_packet", ctypes.c_int),
        ("first_audio_packet_duration_after_unmute", ctypes.c_int),
        ("first_video_packet_duration_after_unmute", ctypes.c_int),
        ("first_video_key_frame_packet_duration_after_unmute", ctypes.c_int),
        ("first_video_key_frame_decoded_duration_after_unmute", ctypes.c_int),
        ("first_video_key_frame_rendered_duration_after_unmute", ctypes.c_int),
        ("tx_packet_loss_rate", ctypes.c_int),
        ("rx_packet_loss_rate", ctypes.c_int)
    ]    



class VIDEO_STREAM_TYPE(ctypes.c_int):
    VIDEO_STREAM_HIGH = 0
    VIDEO_STREAM_LOW = 1

class VideoSubscriptionOptions(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("encodedFrameOnly", ctypes.c_bool)
    ]
    def __init__(self, type = VIDEO_STREAM_TYPE.VIDEO_STREAM_HIGH, encodedFrameOnly = False) -> None:
        self.type = type
        self.encodedFrameOnly = encodedFrameOnly
        

class AudioPcmDataInfo(ctypes.Structure):
    _fields_ = [
        ("samplesPerChannel", ctypes.c_size_t),
        ("channelNum", ctypes.c_int16),
        ("samplesOut", ctypes.c_size_t),
        ("elapsedTimeMs", ctypes.c_int64),
        ("ntpTimeMs", ctypes.c_int64)
    ]

    def __init__(self):
        self.samplesPerChannel = 0
        self.channelNum = 0
        self.samplesOut = 0
        self.elapsedTimeMs = 0
        self.ntpTimeMs = 0


class LocalAudioStats(ctypes.Structure):
    _fields_ = [
        ("num_channels", ctypes.c_int),
        ("sent_sample_rate", ctypes.c_int),
        ("sent_bitrate", ctypes.c_int),
        ("internal_codec", ctypes.c_int),
        ("voice_pitch", ctypes.c_double)
    ]


class AUDIO_PROFILE_TYPE(ctypes.c_int):
    AUDIO_PROFILE_DEFAULT = 0
    AUDIO_PROFILE_SPEECH_STANDARD = 1
    AUDIO_PROFILE_MUSIC_STANDARD = 2
    AUDIO_PROFILE_MUSIC_STANDARD_STEREO = 3
    AUDIO_PROFILE_MUSIC_HIGH_QUALITY = 4
    AUDIO_PROFILE_MUSIC_HIGH_QUALITY_STEREO = 5
    AUDIO_PROFILE_IOT = 6
    AUDIO_PROFILE_NUM = 7

class AudioEncoderConfiguration(ctypes.Structure):
    _fields_ = [
        ("audioProfile", AUDIO_PROFILE_TYPE)
    ]

    def __init__(self):
        self.audioProfile = AUDIO_PROFILE_TYPE.AUDIO_PROFILE_DEFAULT

"""
/**
* Video buffer types.
*/
enum VIDEO_BUFFER_TYPE {
/**
    * 1: Raw data.
    */
VIDEO_BUFFER_RAW_DATA = 1,
/**
    * 2: The same as VIDEO_BUFFER_RAW_DATA.
    */
VIDEO_BUFFER_ARRAY = 2,
/**
    * 3: The video buffer in the format of texture.
    */
VIDEO_BUFFER_TEXTURE = 3,
};

/**
 * Video pixel formats.
 */
enum VIDEO_PIXEL_FORMAT {
  /**
   * 0: Default format.
   */
  VIDEO_PIXEL_DEFAULT = 0,
  /**
   * 1: I420.
   */
  VIDEO_PIXEL_I420 = 1,
  /**
   * 2: BGRA.
   */
  VIDEO_PIXEL_BGRA = 2,
  /**
   * 3: NV21.
   */
  VIDEO_PIXEL_NV21 = 3,
  /**
   * 4: RGBA.
   */
  VIDEO_PIXEL_RGBA = 4,
  /**
   * 8: NV12.
   */
  VIDEO_PIXEL_NV12 = 8,
  /**
   * 10: GL_TEXTURE_2D
   */
  VIDEO_TEXTURE_2D = 10,
  /**
   * 11: GL_TEXTURE_OES
   */
  VIDEO_TEXTURE_OES = 11,
  /*
  12: pixel format for iOS CVPixelBuffer NV12
  */
  VIDEO_CVPIXEL_NV12 = 12,
  /*
  13: pixel format for iOS CVPixelBuffer I420
  */
  VIDEO_CVPIXEL_I420 = 13,
  /*
  14: pixel format for iOS CVPixelBuffer BGRA
  */
  VIDEO_CVPIXEL_BGRA = 14,
  /**
   * 16: I422.
   */
  VIDEO_PIXEL_I422 = 16,
}

refer: https://doc.shengwang.cn/api-ref/rtc/windows/API/class_externalvideoframe#ExternalVideoFrame
"""
# class ExternalVideoFrame(ctypes.Structure):
#     _fields_ = [
#         ("type", ctypes.c_int),
#         ("format", ctypes.c_int),
#         ("buffer", ctypes.c_void_p),
#         ("stride", ctypes.c_int),
#         ("height", ctypes.c_int),
#         ("crop_left", ctypes.c_int),
#         ("crop_top", ctypes.c_int),
#         ("crop_right", ctypes.c_int),
#         ("crop_bottom", ctypes.c_int),
#         ("rotation", ctypes.c_int),
#         ("timestamp", ctypes.c_longlong),
#         ("egl_context", ctypes.c_void_p),
#         ("egl_type", ctypes.c_int),
#         ("texture_id", ctypes.c_int),
#         ("matrix", ctypes.c_float * 16),
#         ("metadata_buffer", ctypes.POINTER(ctypes.c_uint8)),
#         ("metadata_size", ctypes.c_int),
#         ("alpha_buffer", ctypes.c_void_p)
#     ]

#     def __init__(self) -> None:
#         self.data = None



class VideoDimensions(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int)
    ]

class VideoEncoderConfig(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("dimensions", VideoDimensions),
        ("frame_rate", ctypes.c_int),
        ("bitrate", ctypes.c_int),
        ("min_bitrate", ctypes.c_int),
        ("orientation_mode", ctypes.c_int),
        ("degradation_preference", ctypes.c_int),
        ("mirror_mode", ctypes.c_int)
    ]    


class LocalVideoTrackStats(ctypes.Structure):
    _fields_ = [
        ("number_of_streams", ctypes.c_uint64),
        ("bytes_major_stream", ctypes.c_uint64),
        ("bytes_minor_stream", ctypes.c_uint64),
        ("frames_encoded", ctypes.c_uint32),
        ("ssrc_major_stream", ctypes.c_uint32),
        ("ssrc_minor_stream", ctypes.c_uint32),
        ("capture_frame_rate", ctypes.c_int),
        ("regulated_capture_frame_rate", ctypes.c_int),
        ("input_frame_rate", ctypes.c_int),
        ("encode_frame_rate", ctypes.c_int),
        ("render_frame_rate", ctypes.c_int),
        ("target_media_bitrate_bps", ctypes.c_int),
        ("media_bitrate_bps", ctypes.c_int),
        ("total_bitrate_bps", ctypes.c_int),
        ("capture_width", ctypes.c_int),
        ("capture_height", ctypes.c_int),
        ("regulated_capture_width", ctypes.c_int),
        ("regulated_capture_height", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("encoder_type", ctypes.c_uint32),
        ("uplink_cost_time_ms", ctypes.c_uint32),
        ("quality_adapt_indication", ctypes.c_int)
    ]
import ctypes

class VideoDimensions(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int)
    ]

class SimulcastStreamConfig(ctypes.Structure):
    _fields_ = [
        ("dimensions", VideoDimensions),
        ("bitrate", ctypes.c_int),
        ("framerate", ctypes.c_int)
    ]



k_max_codec_name_len = 100
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

class AnaStats(ctypes.Structure):
    _fields_ = [
        ("bitrate_action_counter", ctypes.c_uint32),
        ("channel_action_counter", ctypes.c_uint32),
        ("dtx_action_counter", ctypes.c_uint32),
        ("fec_action_counter", ctypes.c_uint32),
        ("frame_length_increase_counter", ctypes.c_uint32),
        ("frame_length_decrease_counter", ctypes.c_uint32),
        ("uplink_packet_loss_fraction", ctypes.c_float)
    ]

class AudioProcessingStats(ctypes.Structure):
    _fields_ = [
        ("echo_return_loss", ctypes.c_double),
        ("echo_return_loss_enhancement", ctypes.c_double),
        ("divergent_filter_fraction", ctypes.c_double),
        ("delay_median_ms", ctypes.c_int32),
        ("delay_standard_deviation_ms", ctypes.c_int32),
        ("residual_echo_likelihood", ctypes.c_double),
        ("residual_echo_likelihood_recent_max", ctypes.c_double),
        ("delay_ms", ctypes.c_int32)
    ]

class LocalAudioDetailedStats(ctypes.Structure):
    _fields_ = [
        ("local_ssrc", ctypes.c_uint32),
        ("bytes_sent", ctypes.c_int64),
        ("packets_sent", ctypes.c_int32),
        ("packets_lost", ctypes.c_int32),
        ("fraction_lost", ctypes.c_float),
        ("codec_name", ctypes.c_char * k_max_codec_name_len),
        ("codec_payload_type", ctypes.c_int),
        ("ext_seqnum", ctypes.c_int32),
        ("jitter_ms", ctypes.c_int32),
        ("rtt_ms", ctypes.c_int64),
        ("audio_level", ctypes.c_int32),
        ("total_input_energy", ctypes.c_double),
        ("total_input_duration", ctypes.c_double),
        ("typing_noise_detected", ctypes.c_int),
        ("ana_statistics", AnaStats),
        ("apm_statistics", AudioProcessingStats)
    ]    

class VideoTrackInfo(ctypes.Structure):
    def __init__(self) -> None:
        self.is_local = 1
        self.owner_uid = 0
        self.track_id = 0
        self.channel_id = None
        self.stream_type = 0
        self.codec_type = 0
        self.encoded_frame_only = 0
        self.source_type = 0
        self.observation_position = 0

class RAW_AUDIO_FRAME_OP_MODE_TYPE(ctypes.c_int):
    RAW_AUDIO_FRAME_OP_MODE_READ_ONLY = 0
    RAW_AUDIO_FRAME_OP_MODE_READ_WRITE = 2

class AUDIO_FRAME_POSITION(ctypes.c_int):
    AUDIO_FRAME_POSITION_PLAYBACK = 0x0001
    AUDIO_FRAME_POSITION_RECORD = 0x0002
    AUDIO_FRAME_POSITION_MIXED = 0x0004
    AUDIO_FRAME_POSITION_BEFORE_MIXING = 0x0008

class AudioFrame:
    def __init__(self) -> None:
        self.type = 0
        self.samples_per_channel = 0
        self.bytes_per_sample = 0
        self.channels = 0
        self.samples_per_sec = 0
        self.buffer = None
        self.render_time_ms = 0
        self.avsync_type = 0
    


class AudioParams(ctypes.Structure):
    _fields_ = [
        ("sample_rate", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("mode", ctypes.c_int),
        ("samples_per_call", ctypes.c_int)
    ]


class ChannelProfileType(Enum):
    CHANNEL_PROFILE_COMMUNICATION = 0
    CHANNEL_PROFILE_LIVE_BROADCASTING = 1
    CHANNEL_PROFILE_GAME = 2
    CHANNEL_PROFILE_CLOUD_GAMING = 3
    CHANNEL_PROFILE_COMMUNICATION_1v1 = 4



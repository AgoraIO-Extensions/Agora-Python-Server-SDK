import time
import ctypes

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
user_id_t = ctypes.c_uint


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
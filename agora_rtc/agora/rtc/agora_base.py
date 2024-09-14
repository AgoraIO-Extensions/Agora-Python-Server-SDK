import ctypes
from enum import Enum
from . import agora_lib

AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDL = ctypes.c_void_p
AGORA_API_C_VOID = None
user_id_t = ctypes.c_char_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint
k_max_codec_name_len = 100

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


class AudioProfileType(ctypes.c_int):
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
        ("audioProfile", AudioProfileType)
    ]

    def __init__(self):
        self.audioProfile = AudioProfileType.AUDIO_PROFILE_DEFAULT



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

class LocalAudioDetailedStatsInner(ctypes.Structure):
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
    def _to_local_audio_detailed_stats(self): 
        stats = LocalAudioDetailedStats()
        stats.local_ssrc = self.local_ssrc
        stats.bytes_sent = self.bytes_sent
        stats.packets_sent = self.packets_sent
        stats.packets_lost = self.packets_lost
        stats.fraction_lost = self.fraction_lost
        stats.codec_name = self.codec_name.decode('utf-8') if self.codec_name else None
        stats.codec_payload_type = self.codec_payload_type
        stats.ext_seqnum = self.ext_seqnum
        stats.jitter_ms = self.jitter_ms
        stats.rtt_ms = self.rtt_ms
        stats.audio_level = self.audio_level
        stats.total_input_energy = self.total_input_energy
        stats.total_input_duration = self.total_input_duration
        stats.typing_noise_detected = self.typing_noise_detected
        stats.ana_statistics = self.ana_statistics
        stats.apm_statistics = self.apm_statistics
        return stats

class LocalAudioDetailedStats():
    def __init__(self) -> None:
        self.local_ssrc = 0
        self.bytes_sent = 0
        self.packets_sent = 0
        self.packets_lost = 0
        self.fraction_lost = 0.0
        self.codec_name = None
        self.codec_payload_type = 0
        self.ext_seqnum = 0
        self.jitter_ms = 0
        self.rtt_ms = 0
        self.audio_level = 0
        self.total_input_energy = 0.0
        self.total_input_duration = 0.0
        self.typing_noise_detected = 0
        self.ana_statistics = AnaStats()
        self.apm_statistics = AudioProcessingStats()
        pass

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

class RawAudioFrameOpModeType(ctypes.c_int):
    RAW_AUDIO_FRAME_OP_MODE_READ_ONLY = 0
    RAW_AUDIO_FRAME_OP_MODE_READ_WRITE = 2

class AudioFramePosition(ctypes.c_int):
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

class ClientRoleType(Enum):
    CLIENT_ROLE_BROADCASTER = 1
    CLIENT_ROLE_AUDIENCE = 2


class AudioCodecType(Enum):
    AUDIO_CODEC_OPUS = 1
    # AUDIO_CODEC_PCMA = 3
    AUDIO_CODEC_PCMA = 3
    AUDIO_CODEC_PCMU = 4
    AUDIO_CODEC_G722 = 5
    # AUDIO_CODEC_AACLC = 8
    AUDIO_CODEC_AACLC = 8
    AUDIO_CODEC_HEAAC = 9
    AUDIO_CODEC_JC1 = 10
    AUDIO_CODEC_HEAAC2 = 11
    AUDIO_CODEC_LPCNET = 12
    AUDIO_CODEC_OPUSMC = 13

class AreaCode(Enum):
    AREA_CODE_CN = 0x00000001
    AREA_CODE_NA = 0x00000002
    AREA_CODE_EU = 0x00000004
    AREA_CODE_AS = 0x00000008
    AREA_CODE_JP = 0x00000010
    AREA_CODE_IN = 0x00000020
    AREA_CODE_GLOB = 0xFFFFFFFF

class AudioScenarioType(Enum):
    AUDIO_SCENARIO_DEFAULT = 0
    AUDIO_SCENARIO_GAME_STREAMING = 3
    AUDIO_SCENARIO_CHATROOM = 5
    AUDIO_SCENARIO_CHORUS = 7
    AUDIO_SCENARIO_MEETING = 8
    AUDIO_SCENARIO_NUM = 9

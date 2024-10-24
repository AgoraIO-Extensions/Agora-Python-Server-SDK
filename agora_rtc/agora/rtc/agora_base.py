from enum import IntEnum
from dataclasses import dataclass, field


class ChannelProfileType(IntEnum):
    CHANNEL_PROFILE_COMMUNICATION = 0
    CHANNEL_PROFILE_LIVE_BROADCASTING = 1


class ClientRoleType(IntEnum):
    CLIENT_ROLE_BROADCASTER = 1
    CLIENT_ROLE_AUDIENCE = 2


class VideoStreamType(IntEnum):
    VIDEO_STREAM_HIGH = 0
    VIDEO_STREAM_LOW = 1


class AudioCodecType(IntEnum):
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


class VideoCodecType(IntEnum):
    VIDEO_CODEC_NONE = 0
    VIDEO_CODEC_VP8 = 1
    VIDEO_CODEC_H264 = 2
    VIDEO_CODEC_H265 = 3
    VIDEO_CODEC_VP9 = 5
    VIDEO_CODEC_GENERIC = 6
    VIDEO_CODEC_GENERIC_H264 = 7
    VIDEO_CODEC_AV1 = 12
    VIDEO_CODEC_GENERIC_JPEG = 20


class AreaCode(IntEnum):
    AREA_CODE_CN = 0x00000001
    AREA_CODE_NA = 0x00000002
    AREA_CODE_EU = 0x00000004
    AREA_CODE_AS = 0x00000008
    AREA_CODE_JP = 0x00000010
    AREA_CODE_IN = 0x00000020
    AREA_CODE_GLOB = 0xFFFFFFFF


class AudioScenarioType(IntEnum):
    AUDIO_SCENARIO_DEFAULT = 0
    AUDIO_SCENARIO_GAME_STREAMING = 3
    AUDIO_SCENARIO_CHATROOM = 5
    AUDIO_SCENARIO_CHORUS = 7
    AUDIO_SCENARIO_MEETING = 8
    AUDIO_SCENARIO_NUM = 9


class RawAudioFrameOpModeType(IntEnum):
    RAW_AUDIO_FRAME_OP_MODE_READ_ONLY = 0
    RAW_AUDIO_FRAME_OP_MODE_READ_WRITE = 2


class AudioFramePosition(IntEnum):
    AUDIO_FRAME_POSITION_PLAYBACK = 0x0001
    AUDIO_FRAME_POSITION_RECORD = 0x0002
    AUDIO_FRAME_POSITION_MIXED = 0x0004
    AUDIO_FRAME_POSITION_BEFORE_MIXING = 0x0008


class AudioProfileType(IntEnum):
    AUDIO_PROFILE_DEFAULT = 0
    AUDIO_PROFILE_SPEECH_STANDARD = 1
    AUDIO_PROFILE_MUSIC_STANDARD = 2
    AUDIO_PROFILE_MUSIC_STANDARD_STEREO = 3
    AUDIO_PROFILE_MUSIC_HIGH_QUALITY = 4
    AUDIO_PROFILE_MUSIC_HIGH_QUALITY_STEREO = 5
    AUDIO_PROFILE_IOT = 6
    AUDIO_PROFILE_NUM = 7


class TCcMode(IntEnum):
    CC_ENABLED = 0
    CC_DISABLED = 1


@dataclass(frozen=True, kw_only=True)
class LastmileProbeOneWayResult:
    packet_loss_rate: int
    jitter: int
    available_bandwidth: int


@dataclass(frozen=True, kw_only=True)
class LastmileProbeResult:
    state: int
    uplink_report: LastmileProbeOneWayResult
    downlink_report: LastmileProbeOneWayResult
    rtt: int


@dataclass(frozen=True, kw_only=True)
class RTCStats:
    connection_id: int
    duration: int
    tx_bytes: int
    rx_bytes: int
    tx_audio_bytes: int
    tx_video_bytes: int
    rx_audio_bytes: int
    rx_video_bytes: int
    tx_k_bit_rate: int
    rx_k_bit_rate: int
    rx_audio_k_bit_rate: int
    tx_audio_k_bit_rate: int
    rx_video_k_bit_rate: int
    tx_video_k_bit_rate: int
    lastmile_delay: int
    user_count: int
    cpu_app_usage: float
    cpu_total_usage: float
    gateway_rtt: int
    memory_app_usage_ratio: float
    memory_total_usage_ratio: float
    memory_app_usage_in_kbytes: int
    connect_time_ms: int
    first_audio_packet_duration: int
    first_video_packet_duration: int
    first_video_key_frame_packet_duration: int
    packets_before_first_key_frame_packet: int
    first_audio_packet_duration_after_unmute: int
    first_video_packet_duration_after_unmute: int
    first_video_key_frame_packet_duration_after_unmute: int
    first_video_key_frame_decoded_duration_after_unmute: int
    first_video_key_frame_rendered_duration_after_unmute: int
    tx_packet_loss_rate: int
    rx_packet_loss_rate: int


@dataclass(frozen=True, kw_only=True)
class LocalAudioStats:
    num_channels: int
    sent_sample_rate: int
    sent_bitrate: int
    internal_codec: int
    voice_pitch: float


@dataclass(frozen=True, kw_only=True)
class VideoTrackInfo:
    is_local: int
    owner_uid: int
    track_id: int
    channel_id: str
    stream_type: int
    codec_type: int
    encoded_frame_only: int
    source_type: int
    observation_position: int


@dataclass(frozen=True, kw_only=True)
class RemoteVideoTrackStats:
    uid: int
    delay: int
    width: int
    height: int
    received_bitrate: int
    decoder_output_frame_rate: int
    renderer_output_frame_rate: int
    frame_loss_rate: int
    packet_loss_rate: int
    rx_stream_type: int
    total_frozen_time: int
    frozen_rate: int
    total_decoded_frames: int
    av_sync_time_ms: int
    downlink_process_time_ms: int
    frame_render_delay_ms: int
    total_active_time: int
    publish_duration: int


@dataclass(frozen=True, kw_only=True)
class RemoteAudioTrackStats:
    uid: int
    quality: int
    network_transport_delay: int
    jitter_buffer_delay: int
    audio_loss_rate: int
    num_channels: int
    received_sample_rate: int
    received_bitrate: int
    total_frozen_time: int
    frozen_rate: int
    received_bytes: int


@dataclass(frozen=True, kw_only=True)
class AudioFrame:
    type: int
    samples_per_channel: int
    bytes_per_sample: int
    channels: int
    samples_per_sec: int
    buffer: bytearray
    render_time_ms: int
    avsync_type: int
    far_field_flag: int
    rms: int
    voice_prob: int
    music_prob: int
    pitch: int


@dataclass(frozen=True, kw_only=True)
class AudioVolumeInfo:
    user_id: int
    volume: int
    vad: int
    voice_pitch: float


@dataclass(frozen=True, kw_only=True)
class LocalVideoTrackStats:
    number_of_streams: int
    bytes_major_stream: int
    bytes_minor_stream: int
    frames_encoded: int
    ssrc_major_stream: int
    ssrc_minor_stream: int
    capture_frame_rate: int
    regulated_capture_frame_rate: int
    input_frame_rate: int
    encode_frame_rate: int
    render_frame_rate: int
    target_media_bitrate_bps: int
    media_bitrate_bps: int
    total_bitrate_bps: int
    capture_width: int
    capture_height: int
    regulated_capture_width: int
    regulated_capture_height: int
    width: int
    height: int
    encoder_type: int
    uplink_cost_time_ms: int
    quality_adapt_indication: int


@dataclass(frozen=True, kw_only=True)
class RemoteVideoStreamInfo:
    uid: int
    stream_type: int
    current_downscale_level: int
    total_downscale_level_counts: int


@dataclass(frozen=True, kw_only=True)
class RTCConnInfo():
    id: int
    channel_id: str
    state: int
    local_user_id: str
    internal_uid: int


@dataclass(kw_only=True)
class VideoFrame():
    type: int = 0
    width: int = 0
    height: int = 0
    y_stride: int = 0
    u_stride: int = 0
    v_stride: int = 0
    y_buffer: bytearray = None
    u_buffer: bytearray = None
    v_buffer: bytearray = None
    rotation: int = 0
    render_time_ms: int = 0
    avsync_type: int = 0
    metadata: str = None
    shared_context: str = None
    texture_id: int = 0
    matrix: list = None
    alpha_buffer: bytearray = None
    alpha_mode: int = 0


@dataclass(kw_only=True)
class AgoraServiceConfig:
    log_path: str = ""
    log_size: int = 0
    enable_audio_processor: int = 1
    enable_audio_device: int = 0
    enable_video: int = 0
    context: object = None
    appid: str = ""
    area_code: int = AreaCode.AREA_CODE_GLOB.value
    channel_profile: ChannelProfileType = ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING
    audio_scenario: AudioScenarioType = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    use_string_uid: int = 0


@dataclass(kw_only=True)
class AudioSubscriptionOptions:
    packet_only: int = 0
    pcm_data_only: int = 0
    bytes_per_sample: int = 0
    number_of_channels: int = 0
    sample_rate_hz: int = 0


@dataclass(kw_only=True)
class RTCConnConfig:
    auto_subscribe_audio: int = 0
    auto_subscribe_video: int = 0
    enable_audio_recording_or_playout: int = 0
    max_send_bitrate: int = 0
    min_port: int = 0
    max_port: int = 0
    audio_subs_options: 'AudioSubscriptionOptions' = field(default_factory=AudioSubscriptionOptions)
    client_role_type: ClientRoleType = ClientRoleType.CLIENT_ROLE_BROADCASTER
    channel_profile: ChannelProfileType = ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING
    audio_recv_media_packet: int = 0
    audio_recv_encoded_frame: int = 0
    video_recv_media_packet: int = 0


@dataclass(kw_only=True)
class VideoSubscriptionOptions:
    type: VideoStreamType = VideoStreamType.VIDEO_STREAM_HIGH
    encodedFrameOnly: bool = False


@dataclass(kw_only=True)
class AudioPcmDataInfo:
    samplesPerChannel: int
    channelNum: int
    samplesOut: int
    elapsedTimeMs: int
    ntpTimeMs: int


@dataclass(kw_only=True)
class PcmAudioFrame:
    data: bytearray = None
    samples_per_channel: int = 0
    bytes_per_sample: int = 0
    number_of_channels: int = 0
    sample_rate: int = 0
    timestamp: int = 0


@dataclass(kw_only=True)
class AudioEncoderConfiguration:
    audioProfile: AudioProfileType = AudioProfileType.AUDIO_PROFILE_DEFAULT


@dataclass(kw_only=True)
class EncodedAudioFrameInfo:
    capture_timems: int = 0
    codec: AudioCodecType = AudioCodecType.AUDIO_CODEC_AACLC
    number_of_channels: int = 1
    sample_rate: int = 16000
    samples_per_channel: int = 1024
    send_even_if_empty: int = 1
    speech: int = 1


@dataclass(kw_only=True)
class AudioParams:
    sample_rate: int
    channels: int
    mode: int
    samples_per_call: int


@dataclass(kw_only=True)
class VideoDimensions:
    width: int
    height: int


@dataclass(kw_only=True)
class SenderOptions:
    target_bitrate: int
    cc_mode: TCcMode = TCcMode.CC_ENABLED
    codec_type: VideoCodecType = VideoCodecType.VIDEO_CODEC_NONE


@dataclass(kw_only=True)
class EncodedVideoFrameInfo:
    codec_type: VideoCodecType = VideoCodecType.VIDEO_CODEC_NONE
    width: int = 0
    height: int = 0
    frames_per_second: int = 0
    frame_type: int = 0
    rotation: int = 0
    track_id: int = 0
    capture_time_ms: int = 0
    decode_time_ms: int = 0
    uid: int = 0
    stream_type: int = 0


@dataclass(kw_only=True)
class VideoEncoderConfiguration:
    dimensions: VideoDimensions
    codec_type: VideoCodecType = VideoCodecType.VIDEO_CODEC_NONE
    frame_rate: int = 15
    bitrate: int = 0
    min_bitrate: int = 0
    orientation_mode: int = 0
    degradation_preference: int = 0
    mirror_mode: int = 0
    encode_alpha: int = 0


@dataclass(kw_only=True)
class ExternalVideoFrame:
    type: int = 1
    format: int = 0
    buffer: bytearray = None
    stride: int = 0
    height: int = 0
    crop_left: int = 0
    crop_top: int = 0
    crop_right: int = 0
    crop_bottom: int = 0
    rotation: int = 0
    timestamp: int = 0
    egl_context: bytearray = None
    egl_type: int = 0
    texture_id: int = 0
    matrix: list = field(default_factory=list)
    metadata: str = ""
    alpha_buffer: bytearray = field(default_factory=bytearray)
    fill_alpha_buffer: int = 0
    alpha_mode: int = 0


@dataclass(kw_only=True)
class SimulcastStreamConfig:
    dimensions: VideoDimensions
    bitrate: int
    framerate: int


@dataclass(kw_only=True)
class AnaStats:
    bitrate_action_counter: int
    channel_action_counter: int
    dtx_action_counter: int
    fec_action_counter: int
    frame_length_increase_counter: int
    frame_length_decrease_counter: int
    uplink_packet_loss_fraction: float


@dataclass(kw_only=True)
class AudioProcessingStats:
    echo_return_loss: float
    echo_return_loss_enhancement: float
    divergent_filter_fraction: float
    delay_median_ms: int
    delay_standard_deviation_ms: int
    residual_echo_likelihood: float
    residual_echo_likelihood_recent_max: float
    delay_ms: int


@dataclass(kw_only=True)
class LocalAudioDetailedStats:
    local_ssrc: int
    bytes_sent: int
    packets_sent: int
    packets_lost: int
    fraction_lost: float
    codec_name: str
    codec_payload_type: int
    ext_seqnum: int
    jitter_ms: int
    rtt_ms: int
    audio_level: int
    total_input_energy: float
    total_input_duration: float
    typing_noise_detected: int
    ana_statistics: AnaStats
    apm_statistics: AudioProcessingStats

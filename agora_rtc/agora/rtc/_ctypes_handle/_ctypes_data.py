import ctypes
from ..agora_base import *
from .. import agora_lib
AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDL = ctypes.c_void_p
AGORA_API_C_VOID = None
user_id_t = ctypes.c_char_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint
k_max_codec_name_len = 100


class AudioEncoderConfigurationInner(ctypes.Structure):
    _fields_ = [
        ("audioProfile", ctypes.c_int)
    ]

    @staticmethod
    def create(config: AudioEncoderConfiguration) -> 'AudioEncoderConfigurationInner':

        return AudioEncoderConfigurationInner(config.audioProfile.value)


class RTCStatsInner(ctypes.Structure):
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

    def get(self):
        return RTCStats(
            connection_id=self.connection_id,
            duration=self.duration,
            tx_bytes=self.tx_bytes,
            rx_bytes=self.rx_bytes,
            tx_audio_bytes=self.tx_audio_bytes,
            tx_video_bytes=self.tx_video_bytes,
            rx_audio_bytes=self.rx_audio_bytes,
            rx_video_bytes=self.rx_video_bytes,
            tx_k_bit_rate=self.tx_k_bit_rate,
            rx_k_bit_rate=self.rx_k_bit_rate,
            rx_audio_k_bit_rate=self.rx_audio_k_bit_rate,
            tx_audio_k_bit_rate=self.tx_audio_k_bit_rate,
            rx_video_k_bit_rate=self.rx_video_k_bit_rate,
            tx_video_k_bit_rate=self.tx_video_k_bit_rate,
            lastmile_delay=self.lastmile_delay,
            user_count=self.user_count,
            cpu_app_usage=self.cpu_app_usage,
            cpu_total_usage=self.cpu_total_usage,
            gateway_rtt=self.gateway_rtt,
            memory_app_usage_ratio=self.memory_app_usage_ratio,
            memory_total_usage_ratio=self.memory_total_usage_ratio,
            memory_app_usage_in_kbytes=self.memory_app_usage_in_kbytes,
            connect_time_ms=self.connect_time_ms,
            first_audio_packet_duration=self.first_audio_packet_duration,
            first_video_packet_duration=self.first_video_packet_duration,
            first_video_key_frame_packet_duration=self.first_video_key_frame_packet_duration,
            packets_before_first_key_frame_packet=self.packets_before_first_key_frame_packet,
            first_audio_packet_duration_after_unmute=self.first_audio_packet_duration_after_unmute,
            first_video_packet_duration_after_unmute=self.first_video_packet_duration_after_unmute,
            first_video_key_frame_packet_duration_after_unmute=self.first_video_key_frame_packet_duration_after_unmute,
            first_video_key_frame_decoded_duration_after_unmute=self.first_video_key_frame_decoded_duration_after_unmute,
            first_video_key_frame_rendered_duration_after_unmute=self.first_video_key_frame_rendered_duration_after_unmute,
            tx_packet_loss_rate=self.tx_packet_loss_rate,
            rx_packet_loss_rate=self.rx_packet_loss_rate
        )


class LastmileProbeOneWayResultInner(ctypes.Structure):
    _fields_ = [
        ("packet_loss_rate", ctypes.c_uint),
        ("jitter", ctypes.c_uint),
        ("available_bandwidth", ctypes.c_uint)
    ]

    def get(self):
        return LastmileProbeOneWayResult(
            packet_loss_rate=self.packet_loss_rate,
            jitter=self.jitter,
            available_bandwidth=self.available_bandwidth
        )


class VideoFrameInner(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("y_stride", ctypes.c_int),
        ("u_stride", ctypes.c_int),
        ("v_stride", ctypes.c_int),
        ("y_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("u_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("v_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("rotation", ctypes.c_int),
        ("render_time_ms", ctypes.c_int64),
        ("avsync_type", ctypes.c_int),
        ("metadata_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("metadata_size", ctypes.c_int),
        ("shared_context", ctypes.c_void_p),
        ("texture_id", ctypes.c_int),
        ("matrix", ctypes.c_float * 16),
        ("alpha_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("alpha_mode", ctypes.c_int)
    ]

    def get(self):
        return VideoFrame(
            type=self.type,
            width=self.width,
            height=self.height,
            y_stride=self.y_stride,
            u_stride=self.u_stride,
            v_stride=self.v_stride,
            y_buffer=ctypes.string_at(self.y_buffer, self.y_stride * self.height) if self.y_buffer else None,
            u_buffer=ctypes.string_at(self.u_buffer, self.u_stride * self.height // 2) if self.u_buffer else None,
            v_buffer=ctypes.string_at(self.v_buffer, self.v_stride * self.height // 2) if self.v_buffer else None,
            rotation=self.rotation,
            render_time_ms=self.render_time_ms,
            avsync_type=self.avsync_type,
            metadata=ctypes.string_at(self.metadata_buffer, self.metadata_size) if self.metadata_buffer else None,
            shared_context=self.shared_context.decode() if self.shared_context else None,
            texture_id=self.texture_id,
            matrix=self.matrix,
            alpha_buffer=ctypes.string_at(self.alpha_buffer, self.width * self.height) if self.alpha_buffer else None,
            alpha_mode=self.alpha_mode
        )


class EncodedVideoFrameInfoInner(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("frames_per_second", ctypes.c_int),
        ("frame_type", ctypes.c_int),
        ("rotation", ctypes.c_int),
        ("track_id", ctypes.c_int),
        ("capture_time_ms", ctypes.c_int64),
        ("decode_time_ms", ctypes.c_int64),
        ("uid", ctypes.c_uint),
        ("stream_type", ctypes.c_int)
    ]

    def get(self):
        return EncodedVideoFrameInfo(
            codec_type=self.codec_type,
            width=self.width,
            height=self.height,
            frames_per_second=self.frames_per_second,
            frame_type=self.frame_type,
            rotation=self.rotation,
            track_id=self.track_id,
            capture_time_ms=self.capture_time_ms,
            decode_time_ms=self.decode_time_ms,
            uid=self.uid,
            stream_type=self.stream_type
        )


class LastmileProbeResultInner(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_int),
        ("uplink_report", LastmileProbeOneWayResultInner),
        ("downlink_report", LastmileProbeOneWayResultInner),
        ("rtt", ctypes.c_uint)
    ]

    def get(self):
        return LastmileProbeResult(
            state=self.state,
            uplink_report=self.uplink_report.contents.get(),
            downlink_report=self.downlink_report.contents.get(),
            rtt=self.rtt
        )


class VideoSubscriptionOptionsInner(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("encodedFrameOnly", ctypes.c_bool)
    ]

    def get(self):
        return VideoSubscriptionOptions(
            type=self.type,
            encodedFrameOnly=self.encodedFrameOnly
        )

    @staticmethod
    def create(options: VideoSubscriptionOptions) -> 'VideoSubscriptionOptionsInner':
        return VideoSubscriptionOptionsInner(
            options.type.value,
            options.encodedFrameOnly
        )


class AudioPcmDataInfoInner(ctypes.Structure):
    _fields_ = [
        ("samplesPerChannel", ctypes.c_size_t),
        ("channelNum", ctypes.c_int16),
        ("samplesOut", ctypes.c_size_t),
        ("elapsedTimeMs", ctypes.c_int64),
        ("ntpTimeMs", ctypes.c_int64)
    ]

    def get(self):
        return AudioPcmDataInfo(
            samplesPerChannel=self.samplesPerChannel,
            channelNum=self.channelNum,
            samplesOut=self.samplesOut,
            elapsedTimeMs=self.elapsedTimeMs,
            ntpTimeMs=self.ntpTimeMs
        )

    @staticmethod
    def create(info: AudioPcmDataInfo) -> 'AudioPcmDataInfoInner':
        return AudioPcmDataInfoInner(
            info.samplesPerChannel,
            info.channelNum,
            info.samplesOut,
            info.elapsedTimeMs,
            info.ntpTimeMs
        )


class LocalAudioStatsInner(ctypes.Structure):
    _fields_ = [
        ("num_channels", ctypes.c_int),
        ("sent_sample_rate", ctypes.c_int),
        ("sent_bitrate", ctypes.c_int),
        ("internal_codec", ctypes.c_int),
        ("voice_pitch", ctypes.c_double)
    ]

    def get(self):
        return LocalAudioTrackStats(
            num_channels=self.num_channels,
            sent_sample_rate=self.sent_sample_rate,
            sent_bitrate=self.sent_bitrate,
            internal_codec=self.internal_codec,
            voice_pitch=self.voice_pitch
        )

    @staticmethod
    def create(stats: LocalAudioTrackStats) -> 'LocalAudioStatsInner':
        return LocalAudioStatsInner(
            stats.num_channels,
            stats.sent_sample_rate,
            stats.sent_bitrate,
            stats.internal_codec,
            stats.voice_pitch
        )


class SenderOptionsInner(ctypes.Structure):
    _fields_ = [
        ("cc_mode", ctypes.c_int),
        ("codec_type", ctypes.c_int),
        ("target_bitrate", ctypes.c_int)
    ]

    def get(self):
        return SenderOptions(
            cc_mode=self.cc_mode,
            codec_type=self.codec_type,
            target_bitrate=self.target_bitrate
        )

    @staticmethod
    def create(options: SenderOptions) -> 'SenderOptionsInner':
        return SenderOptionsInner(
            options.cc_mode.value,
            options.codec_type.value,
            options.target_bitrate
        )


class VideoDimensionsInner(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int)
    ]

    def get(self):
        return VideoDimensions(
            width=self.width,
            height=self.height
        )

    @staticmethod
    def create(dimensions: VideoDimensions) -> 'VideoDimensionsInner':
        return VideoDimensionsInner(
            dimensions.width,
            dimensions.height
        )


class VideoEncoderConfigurationInner(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("dimensions", VideoDimensionsInner),
        ("frame_rate", ctypes.c_int),
        ("bitrate", ctypes.c_int),
        ("min_bitrate", ctypes.c_int),
        ("orientation_mode", ctypes.c_int),
        ("degradation_preference", ctypes.c_int),
        ("mirror_mode", ctypes.c_int),
        ("encode_alpha", ctypes.c_int)
    ]

    def get(self):
        return VideoEncoderConfiguration(
            codec_type=self.codec_type,
            dimensions=self.dimensions.contents.get(),
            frame_rate=self.frame_rate,
            bitrate=self.bitrate,
            min_bitrate=self.min_bitrate,
            orientation_mode=self.orientation_mode,
            degradation_preference=self.degradation_preference,
            mirror_mode=self.mirror_mode,
            encode_alpha=self.encode_alpha
        )

    @staticmethod
    def create(config: VideoEncoderConfiguration) -> 'VideoEncoderConfigurationInner':
        return VideoEncoderConfigurationInner(
            config.codec_type,
            VideoDimensionsInner.create(config.dimensions),
            config.frame_rate,
            config.bitrate,
            config.min_bitrate,
            config.orientation_mode,
            config.degradation_preference,
            config.mirror_mode,
            config.encode_alpha
        )


class LocalVideoTrackStatsInner(ctypes.Structure):
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

    def get(self):
        return LocalVideoTrackStats(
            number_of_streams=self.number_of_streams,
            bytes_major_stream=self.bytes_major_stream,
            bytes_minor_stream=self.bytes_minor_stream,
            frames_encoded=self.frames_encoded,
            ssrc_major_stream=self.ssrc_major_stream,
            ssrc_minor_stream=self.ssrc_minor_stream,
            capture_frame_rate=self.capture_frame_rate,
            regulated_capture_frame_rate=self.regulated_capture_frame_rate,
            input_frame_rate=self.input_frame_rate,
            encode_frame_rate=self.encode_frame_rate,
            render_frame_rate=self.render_frame_rate,
            target_media_bitrate_bps=self.target_media_bitrate_bps,
            media_bitrate_bps=self.media_bitrate_bps,
            total_bitrate_bps=self.total_bitrate_bps,
            capture_width=self.capture_width,
            capture_height=self.capture_height,
            regulated_capture_width=self.regulated_capture_width,
            regulated_capture_height=self.regulated_capture_height,
            width=self.width,
            height=self.height,
            encoder_type=self.encoder_type,
            uplink_cost_time_ms=self.uplink_cost_time_ms,
            quality_adapt_indication=self.quality_adapt_indication
        )

    @staticmethod
    def create(stats: LocalVideoTrackStats) -> 'LocalVideoTrackStatsInner':
        return LocalVideoTrackStatsInner(
            stats.number_of_streams,
            stats.bytes_major_stream,
            stats.bytes_minor_stream,
            stats.frames_encoded,
            stats.ssrc_major_stream,
            stats.ssrc_minor_stream,
            stats.capture_frame_rate,
            stats.regulated_capture_frame_rate,
            stats.input_frame_rate,
            stats.encode_frame_rate,
            stats.render_frame_rate,
            stats.target_media_bitrate_bps,
            stats.media_bitrate_bps,
            stats.total_bitrate_bps,
            stats.capture_width,
            stats.capture_height,
            stats.regulated_capture_width,
            stats.regulated_capture_height,
            stats.width,
            stats.height,
            stats.encoder_type,
            stats.uplink_cost_time_ms,
            stats.quality_adapt_indication
        )


class SimulcastStreamConfigInner(ctypes.Structure):
    _fields_ = [
        ("dimensions", VideoDimensionsInner),
        ("bitrate", ctypes.c_int),
        ("framerate", ctypes.c_int)
    ]

    def get(self):
        return SimulcastStreamConfig(
            dimensions=self.dimensions.contents.get(),
            bitrate=self.bitrate,
            framerate=self.framerate
        )

    @staticmethod
    def create(config: SimulcastStreamConfig) -> 'SimulcastStreamConfigInner':
        return SimulcastStreamConfigInner(
            VideoDimensionsInner.create(config.dimensions),
            config.bitrate,
            config.framerate
        )


class AnaStatsInner(ctypes.Structure):
    _fields_ = [
        ("bitrate_action_counter", ctypes.c_uint32),
        ("channel_action_counter", ctypes.c_uint32),
        ("dtx_action_counter", ctypes.c_uint32),
        ("fec_action_counter", ctypes.c_uint32),
        ("frame_length_increase_counter", ctypes.c_uint32),
        ("frame_length_decrease_counter", ctypes.c_uint32),
        ("uplink_packet_loss_fraction", ctypes.c_float)
    ]

    def get(self):
        return AnaStats(
            bitrate_action_counter=self.bitrate_action_counter,
            channel_action_counter=self.channel_action_counter,
            dtx_action_counter=self.dtx_action_counter,
            fec_action_counter=self.fec_action_counter,
            frame_length_increase_counter=self.frame_length_increase_counter,
            frame_length_decrease_counter=self.frame_length_decrease_counter,
            uplink_packet_loss_fraction=self.uplink_packet_loss_fraction
        )

    @staticmethod
    def create(stats: AnaStats) -> 'AnaStatsInner':
        return AnaStatsInner(
            stats.bitrate_action_counter,
            stats.channel_action_counter,
            stats.dtx_action_counter,
            stats.fec_action_counter,
            stats.frame_length_increase_counter,
            stats.frame_length_decrease_counter,
            stats.uplink_packet_loss_fraction
        )


class AudioProcessingStatsInner(ctypes.Structure):
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

    def get(self):
        return AudioProcessingStats(
            echo_return_loss=self.echo_return_loss,
            echo_return_loss_enhancement=self.echo_return_loss_enhancement,
            divergent_filter_fraction=self.divergent_filter_fraction,
            delay_median_ms=self.delay_median_ms,
            delay_standard_deviation_ms=self.delay_standard_deviation_ms,
            residual_echo_likelihood=self.residual_echo_likelihood,
            residual_echo_likelihood_recent_max=self.residual_echo_likelihood_recent_max,
            delay_ms=self.delay_ms
        )

    @staticmethod
    def create(stats: AudioProcessingStats) -> 'AudioProcessingStatsInner':
        return AudioProcessingStatsInner(
            stats.echo_return_loss,
            stats.echo_return_loss_enhancement,
            stats.divergent_filter_fraction,
            stats.delay_median_ms,
            stats.delay_standard_deviation_ms,
            stats.residual_echo_likelihood,
            stats.residual_echo_likelihood_recent_max,
            stats.delay_ms
        )


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
        ("ana_statistics", AnaStatsInner),
        ("apm_statistics", AudioProcessingStatsInner)
    ]

    def get(self):
        return LocalAudioDetailedStats(
            local_ssrc=self.local_ssrc,
            bytes_sent=self.bytes_sent,
            packets_sent=self.packets_sent,
            packets_lost=self.packets_lost,
            fraction_lost=self.fraction_lost,
            codec_name=self.codec_name.decode(),
            codec_payload_type=self.codec_payload_type,
            ext_seqnum=self.ext_seqnum,
            jitter_ms=self.jitter_ms,
            rtt_ms=self.rtt_ms,
            audio_level=self.audio_level,
            total_input_energy=self.total_input_energy,
            total_input_duration=self.total_input_duration,
            typing_noise_detected=self.typing_noise_detected,
            ana_statistics=self.ana_statistics.contents.get(),
            apm_statistics=self.apm_statistics.contents.get()
        )

    @staticmethod
    def create(stats: LocalAudioDetailedStats) -> 'LocalAudioDetailedStatsInner':
        return LocalAudioDetailedStatsInner(
            stats.local_ssrc,
            stats.bytes_sent,
            stats.packets_sent,
            stats.packets_lost,
            stats.fraction_lost,
            stats.codec_name.encode(),
            stats.codec_payload_type,
            stats.ext_seqnum,
            stats.jitter_ms,
            stats.rtt_ms,
            stats.audio_level,
            stats.total_input_energy,
            stats.total_input_duration,
            stats.typing_noise_detected,
            AnaStatsInner.create(stats.ana_statistics),
            AudioProcessingStatsInner.create(stats.apm_statistics)
        )


class VideoTrackInfoInner(ctypes.Structure):
    _fields_ = [
        ("is_local", ctypes.c_int),
        ("owner_uid", uid_t),
        ("track_id", track_id_t),
        ("channel_id", ctypes.c_char_p),
        ("stream_type", ctypes.c_int),
        ("codec_type", ctypes.c_int),
        ("encoded_frame_only", ctypes.c_int),
        ("source_type", ctypes.c_int),
        ("observation_position", ctypes.c_uint32)
    ]

    def get(self):
        return VideoTrackInfo(
            is_local=self.is_local,
            owner_uid=self.owner_uid,
            track_id=self.track_id,
            channel_id=self.channel_id.decode() if self.channel_id else '',
            stream_type=self.stream_type,
            codec_type=self.codec_type,
            encoded_frame_only=self.encoded_frame_only,
            source_type=self.source_type,
            observation_position=self.observation_position
        )

    @staticmethod
    def create(info: VideoTrackInfo) -> 'VideoTrackInfoInner':
        return VideoTrackInfoInner(
            info.is_local,
            info.owner_uid,
            info.track_id,
            info.channel_id.encode(),
            info.stream_type,
            info.codec_type,
            info.encoded_frame_only,
            info.source_type,
            info.observation_position
        )


class RemoteVideoTrackStatsInner(ctypes.Structure):
    _fields_ = [
        ("uid", uid_t),
        ("delay", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("received_bitrate", ctypes.c_int),
        ("decoder_output_frame_rate", ctypes.c_int),
        ("renderer_output_frame_rate", ctypes.c_int),
        ("frame_loss_rate", ctypes.c_int),
        ("packet_loss_rate", ctypes.c_int),
        ("rx_stream_type", ctypes.c_int),
        ("total_frozen_time", ctypes.c_int),
        ("frozen_rate", ctypes.c_int),
        ("total_decoded_frames", ctypes.c_uint32),
        ("av_sync_time_ms", ctypes.c_int),
        ("downlink_process_time_ms", ctypes.c_uint32),
        ("frame_render_delay_ms", ctypes.c_uint32),
        ("totalActiveTime", ctypes.c_uint64),
        ("publishDuration", ctypes.c_uint64)
    ]

    def get(self):
        return RemoteVideoTrackStats(
            uid=self.uid,
            delay=self.delay,
            width=self.width,
            height=self.height,
            received_bitrate=self.received_bitrate,
            decoder_output_frame_rate=self.decoder_output_frame_rate,
            renderer_output_frame_rate=self.renderer_output_frame_rate,
            frame_loss_rate=self.frame_loss_rate,
            packet_loss_rate=self.packet_loss_rate,
            rx_stream_type=self.rx_stream_type,
            total_frozen_time=self.total_frozen_time,
            frozen_rate=self.frozen_rate,
            total_decoded_frames=self.total_decoded_frames,
            av_sync_time_ms=self.av_sync_time_ms,
            downlink_process_time_ms=self.downlink_process_time_ms,
            frame_render_delay_ms=self.frame_render_delay_ms,
            total_active_time=self.totalActiveTime,
            publish_duration=self.publishDuration
        )

    @staticmethod
    def create(stats: RemoteVideoTrackStats) -> 'RemoteVideoTrackStatsInner':
        return RemoteVideoTrackStatsInner(
            stats.uid,
            stats.delay,
            stats.width,
            stats.height,
            stats.received_bitrate,
            stats.decoder_output_frame_rate,
            stats.renderer_output_frame_rate,
            stats.frame_loss_rate,
            stats.packet_loss_rate,
            stats.rx_stream_type,
            stats.total_frozen_time,
            stats.frozen_rate,
            stats.total_decoded_frames,
            stats.av_sync_time_ms,
            stats.downlink_process_time_ms,
            stats.frame_render_delay_ms,
            stats.total_active_time,
            stats.publish_duration
        )
    
class ColorSpaceTypeInner(ctypes.Structure):
    _fields_ = [
        ("primaries_id", ctypes.c_int),
        ("transfer_id", ctypes.c_int),
        ("matrix_id", ctypes.c_int),
        ("range_id", ctypes.c_int)
    ]
    def get(self):
        return ColorSpaceType(
            primaries_id=self.primaries_id,
            transfer_id=self.transfer_id,
            matrix_id=self.matrix_id,
            range_id=self.range_id
        )
    @staticmethod
    def create(colorspace:ColorSpaceType) -> 'ColorSpaceTypeInner':
        return ColorSpaceTypeInner(
            primaries_id=colorspace.primaries_id,
            transfer_id=colorspace.transfer_id,
            matrix_id=colorspace.matrix_id,
            range_id=colorspace.range_id
        )


class ExternalVideoFrameInner(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("format", ctypes.c_int),
        ("buffer", ctypes.c_void_p),
        ("stride", ctypes.c_int),
        ("height", ctypes.c_int),
        ("crop_left", ctypes.c_int),
        ("crop_top", ctypes.c_int),
        ("crop_right", ctypes.c_int),
        ("crop_bottom", ctypes.c_int),
        ("rotation", ctypes.c_int),
        ("timestamp", ctypes.c_longlong),
        ("egl_context", ctypes.c_void_p),
        ("egl_type", ctypes.c_int),
        ("texture_id", ctypes.c_int),
        ("matrix", ctypes.c_float * 16),
        ("metadata_buffer", ctypes.POINTER(ctypes.c_uint8)),
        ("metadata_size", ctypes.c_int),
        ("alpha_buffer", ctypes.c_void_p),
        ("fill_alpha_buffer", ctypes.c_uint8),
        ("alpha_mode", ctypes.c_int),
        ("color_space", ColorSpaceTypeInner)
    ]

    def get(self):
        return ExternalVideoFrame(
            type=self.type,
            format=self.format,
            buffer=ctypes.string_at(self.buffer, self.stride * self.height) if self.buffer else None,
            stride=self.stride,
            height=self.height,
            crop_left=self.crop_left,
            crop_top=self.crop_top,
            crop_right=self.crop_right,
            crop_bottom=self.crop_bottom,
            rotation=self.rotation,
            timestamp=self.timestamp,
            egl_context=self.egl_context,
            egl_type=self.egl_type,
            texture_id=self.texture_id,
            matrix=[self.matrix[i] for i in range(16)],
            metadata_buffer=ctypes.string_at(self.metadata_buffer, self.metadata_size) if self.metadata_buffer else None,
            metadata_size=self.metadata_size,
            alpha_buffer=self.alpha_buffer,
            fill_alpha_buffer=self.fill_alpha_buffer,
            alpha_mode=self.alpha_mode,
            color_space=self.color_space.get()
        )

    @staticmethod
    def create(frame: ExternalVideoFrame) -> 'ExternalVideoFrameInner':
        if frame.buffer is not None:
            c_buffer = (ctypes.c_uint8 * len(frame.buffer)).from_buffer(frame.buffer)
            c_buffer_ptr = ctypes.cast(c_buffer, ctypes.c_void_p)
        else:
            c_buffer_ptr = ctypes.c_void_p(0)
       

        #aplha_buffer and is_fill alpha_buffer 
        if (frame.fill_alpha_buffer >0) and (frame.alpha_buffer is not None):
            c_alpha_buffer = (ctypes.c_uint8 * len(frame.alpha_buffer)).from_buffer(frame.alpha_buffer)
            c_alpha_buffer_ptr = ctypes.cast(c_alpha_buffer, ctypes.c_void_p)
        else:
            c_alpha_buffer_ptr = ctypes.c_void_p(0)

        c_metadata_size = len (frame.metadata) if frame.metadata is not None else 0
        if frame.metadata is not None and c_metadata_size > 0:
            c_metadata_ptr = (ctypes.c_uint8 * len(frame.metadata)).from_buffer(frame.metadata)
            c_metadata_size = len(frame.metadata)
        else:
            #c_metadata_ptr = ctypes.c_void_p(0)
            c_metadata_ptr  = ctypes.POINTER(ctypes.c_uint8)()
            c_metadata_size = 0
       
        

        
        return ExternalVideoFrameInner(
            frame.type,
            frame.format,
            c_buffer_ptr,
            frame.stride,
            frame.height,
            frame.crop_left,
            frame.crop_top,
            frame.crop_right,
            frame.crop_bottom,
            frame.rotation,
            frame.timestamp,
            frame.egl_context,
            frame.egl_type,
            frame.texture_id,
            (ctypes.c_float * 16)(*frame.matrix),
            c_metadata_ptr,
            c_metadata_size,
            c_alpha_buffer_ptr,
            frame.fill_alpha_buffer,
            frame.alpha_mode,
            ColorSpaceTypeInner.create(frame.color_space)
        )


class RTCConnInfoInner(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint64),
        ("channel_id", ctypes.c_char_p),
        ("state", ctypes.c_int),
        ("local_user_id", ctypes.c_char_p),
        ("internal_uid", ctypes.c_uint)
    ]

    def get(self):
        return RTCConnInfo(
            id=self.id,
            channel_id=self.channel_id.decode(),
            state=self.state,
            local_user_id=self.local_user_id.decode(),
            internal_uid=self.internal_uid
        )

    @staticmethod
    def create(info: RTCConnInfo) -> 'RTCConnInfoInner':
        return RTCConnInfoInner(
            info.id,
            info.channel_id.encode(),
            info.state,
            info.local_user_id.encode(),
            info.internal_uid
        )


class AudioSubscriptionOptionsInner(ctypes.Structure):
    _fields_ = [
        ('packet_only', ctypes.c_int),
        ('pcm_data_only', ctypes.c_int),
        ('bytes_per_sample', ctypes.c_uint32),
        ('number_of_channels', ctypes.c_uint32),
        ('sample_rate_hz', ctypes.c_uint32),
    ]

    def get(self):
        return AudioSubscriptionOptions(
            packet_only=self.packet_only,
            pcm_data_only=self.pcm_data_only,
            bytes_per_sample=self.bytes_per_sample,
            number_of_channels=self.number_of_channels,
            sample_rate_hz=self.sample_rate_hz
        )

    @staticmethod
    def create(options: AudioSubscriptionOptions) -> 'AudioSubscriptionOptionsInner':
        return AudioSubscriptionOptionsInner(
            options.packet_only,
            options.pcm_data_only,
            options.bytes_per_sample,
            options.number_of_channels,
            options.sample_rate_hz
        )


class RTCConnConfigInner(ctypes.Structure):
    _fields_ = [
        ('auto_subscribe_audio', ctypes.c_int),
        ('auto_subscribe_video', ctypes.c_int),
        ('enable_audio_recording_or_playout', ctypes.c_int),
        ('max_send_bitrate', ctypes.c_int),
        ('min_port', ctypes.c_int),
        ('max_port', ctypes.c_int),
        ('audio_subs_options', AudioSubscriptionOptionsInner),
        ('client_role_type', ctypes.c_int),
        ('channel_profile', ctypes.c_int),
        ('audio_recv_media_packet', ctypes.c_int),
        ('audio_recv_encoded_frame', ctypes.c_int),
        ('video_recv_media_packet', ctypes.c_int),
    ]

    def get(self):
        return RTCConnConfig(
            auto_subscribe_audio=self.auto_subscribe_audio,
            auto_subscribe_video=self.auto_subscribe_video,
            enable_audio_recording_or_playout=self.enable_audio_recording_or_playout,
            max_send_bitrate=self.max_send_bitrate,
            min_port=self.min_port,
            max_port=self.max_port,
            audio_subs_options=self.audio_subs_options.contents.get(),
            client_role_type=self.client_role_type,
            channel_profile=self.channel_profile,
            audio_recv_media_packet=self.audio_recv_media_packet,
            audio_recv_encoded_frame=self.audio_recv_encoded_frame,
            video_recv_media_packet=self.video_recv_media_packet
        )

    @staticmethod
    def create(config: RTCConnConfig) -> 'RTCConnConfigInner':
        return RTCConnConfigInner(
            config.auto_subscribe_audio,
            config.auto_subscribe_video,
            config.enable_audio_recording_or_playout,
            config.max_send_bitrate,
            config.min_port,
            config.max_port,
            AudioSubscriptionOptionsInner.create(config.audio_subs_options),
            config.client_role_type,
            config.channel_profile,
            config.audio_recv_media_packet,
            config.audio_recv_encoded_frame,
            config.video_recv_media_packet
        )


class RemoteAudioTrackStatsInner(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("quality", ctypes.c_int),
        ("network_transport_delay", ctypes.c_int),
        ("jitter_buffer_delay", ctypes.c_int),
        ("audio_loss_rate", ctypes.c_int),
        ("num_channels", ctypes.c_int),
        ("received_sample_rate", ctypes.c_int),
        ("received_bitrate", ctypes.c_int),
        ("total_frozen_time", ctypes.c_int),
        ("frozen_rate", ctypes.c_int),
        ("received_bytes", ctypes.c_int64)
    ]

    def get(self):
        return RemoteAudioTrackStats(
            uid=self.uid,
            quality=self.quality,
            network_transport_delay=self.network_transport_delay,
            jitter_buffer_delay=self.jitter_buffer_delay,
            audio_loss_rate=self.audio_loss_rate,
            num_channels=self.num_channels,
            received_sample_rate=self.received_sample_rate,
            received_bitrate=self.received_bitrate,
            total_frozen_time=self.total_frozen_time,
            frozen_rate=self.frozen_rate,
            received_bytes=self.received_bytes
        )

    @staticmethod
    def create(stats: RemoteAudioTrackStats) -> 'RemoteAudioTrackStatsInner':
        return RemoteAudioTrackStatsInner(
            stats.uid,
            stats.quality,
            stats.network_transport_delay,
            stats.jitter_buffer_delay,
            stats.audio_loss_rate,
            stats.num_channels,
            stats.received_sample_rate,
            stats.received_bitrate,
            stats.total_frozen_time,
            stats.frozen_rate,
            stats.received_bytes
        )

class EncodedAudioFrameInfoInner(ctypes.Structure):
    _fields_ = [
        ('speech', ctypes.c_int),
        ('codec', ctypes.c_int),
        ('sample_rate_hz', ctypes.c_int),
        ('samples_per_channel', ctypes.c_int),
        ('send_even_if_empty', ctypes.c_int),
        ('number_of_channels', ctypes.c_int),
        ('capture_time_ms', ctypes.c_int64)
    ]

    @staticmethod
    def create(info: EncodedAudioFrameInfo) -> 'EncodedAudioFrameInfoInner':
        return EncodedAudioFrameInfoInner(
            info.speech,
            info.codec,
            info.sample_rate,
            info.samples_per_channel,
            info.send_even_if_empty,
            info.number_of_channels,
            info.capture_time_ms
        )


class AudioVolumeInfoInner(ctypes.Structure):
    _fields_ = [
        ("user_id", user_id_t),
        ("volume", ctypes.c_uint),
        ("vad", ctypes.c_uint),
        ("voicePitch", ctypes.c_double)
    ]

    def get(self):
        return AudioVolumeInfo(
            user_id=self.user_id.decode() if self.user_id else "",
            volume=self.volume,
            vad=self.vad,
            voice_pitch=self.voicePitch
        )


class RemoteVideoStreamInfoInner(ctypes.Structure):
    _fields_ = [
        ("uid", ctypes.c_uint),
        ("stream_type", ctypes.c_uint8),
        ("current_downscale_level", ctypes.c_uint8),
        ("total_downscale_level_counts", ctypes.c_uint8)
    ]

    def get(self):
        return RemoteVideoStreamInfo(
            uid=self.uid,
            stream_type=self.stream_type,
            current_downscale_level=self.current_downscale_level,
            total_downscale_level_counts=self.total_downscale_level_counts
        )


class AudioFrameInner(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("samples_per_channel", ctypes.c_int),
        ("bytes_per_sample", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("samples_per_sec", ctypes.c_int),
        ("buffer", ctypes.c_void_p),
        ("render_time_ms", ctypes.c_int64),
        ("avsync_type", ctypes.c_int),
        ("presentation_ms", ctypes.c_int64),
        ("audio_track_number", ctypes.c_int),
        ("rtp_timestamp", ctypes.c_uint32),
       
        ("far_field_flag", ctypes.c_int),
        ("rms", ctypes.c_int),
        ("voice_prob", ctypes.c_int),
        ("music_prob", ctypes.c_int),
        ("pitch", ctypes.c_int)
    ]

    def get(self):
        return AudioFrame(
            type=self.type,
            samples_per_channel=self.samples_per_channel,
            bytes_per_sample=self.bytes_per_sample,
            channels=self.channels,
            samples_per_sec=self.samples_per_sec,
            buffer=bytearray(ctypes.string_at(self.buffer, self.samples_per_channel * self.bytes_per_sample * self.channels)),
            render_time_ms=self.render_time_ms,
            avsync_type=self.avsync_type,
            presentation_ms=self.presentation_ms,
            audio_track_number=self.audio_track_number,
            rtp_timestamp=self.rtp_timestamp,
            far_field_flag=self.far_field_flag,
            rms=self.rms,
            voice_prob=self.voice_prob,
            music_prob=self.music_prob,
            pitch=self.pitch
        )

    @staticmethod
    def create(frame: AudioFrame) -> 'AudioFrameInner':
        return AudioFrameInner(
            frame.type,
            frame.samples_per_channel,
            frame.bytes_per_sample,
            frame.channels,
            frame.samples_per_sec,
            ctypes.cast(frame.buffer, ctypes.c_void_p),
            frame.render_time_ms,
            frame.avsync_type,
            frame.presentation_ms,
            frame.audio_track_number,
            frame.rtp_timestamp,
            frame.far_field_flag,
            frame.rms,
            frame.voice_prob,
            frame.music_prob,
            frame.pitch
        )


class AudioParamsInner(ctypes.Structure):
    _fields_ = [
        ("sample_rate", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("mode", ctypes.c_int),
        ("samples_per_call", ctypes.c_int)
    ]


class AgoraServiceConfigInner(ctypes.Structure):
    _fields_ = [
        ('enable_audio_processor', ctypes.c_int),
        ('enable_audio_device', ctypes.c_int),
        ('enable_video', ctypes.c_int),
        ('context', ctypes.c_void_p),

        ('app_id', ctypes.c_char_p),
        ('area_code', ctypes.c_uint),
        ('channel_profile', ctypes.c_int),
        ('audio_scenario', ctypes.c_int),

        ('use_string_uid', ctypes.c_int),
        ('domain_limit', ctypes.c_int),
        ('log_level', ctypes.c_int),
        ('log_file_path', ctypes.c_char_p),
        ('log_file_size_kb', ctypes.c_uint32),
        ('data_dir', ctypes.c_char_p),
        ('config_dir', ctypes.c_char_p),
    ]

    def get(self):
        return AgoraServiceConfig(
            enable_audio_processor=self.enable_audio_processor,
            enable_audio_device=self.enable_audio_device,
            enable_video=self.enable_video,
            context=self.context,
            app_id=self.app_id.decode(),
            area_code=self.area_code,
            channel_profile=self.channel_profile,
            audio_scenario=self.audio_scenario,
            use_string_uid=self.use_string_uid,
            domain_limit=self.domain_limit,
            log_level=self.log_level,
            log_path=self.log_file_path.decode() if self.log_file_path else "",
            log_file_size_kb=self.log_file_size_kb,
            data_dir=self.data_dir.decode() if self.data_dir else "",
            config_dir=self.config_dir.decode() if self.config_dir else ""
        )

    @staticmethod
    def create(config: AgoraServiceConfig) -> 'AgoraServiceConfigInner':
        return AgoraServiceConfigInner(
            config.enable_audio_processor,
            config.enable_audio_device,
            config.enable_video,
            config.context,
            config.appid.encode() if config.appid else None,
            config.area_code,
            config.channel_profile,
            config.audio_scenario,
            config.use_string_uid,
            config.domain_limit,
            config.log_level,
            config.log_path.encode() if config.log_path else None,
            config.log_file_size_kb,
            config.data_dir.encode() if config.data_dir else None,
            config.config_dir.encode() if config.config_dir else None
        )


class EncodedVideoFrameInfoInner(ctypes.Structure):
    _fields_ = [
        ("codec_type", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("frames_per_second", ctypes.c_int),
        ("frame_type", ctypes.c_int),
        ("rotation", ctypes.c_int),
        ("track_id", ctypes.c_int),
        ("capture_time_ms", ctypes.c_int64),
        ("decode_time_ms", ctypes.c_int64),
        ("uid", ctypes.c_uint),
        ("stream_type", ctypes.c_int),
        ("presentation_ms", ctypes.c_int64)
    ]

    def get(self):
        return EncodedVideoFrameInfo(
            codec_type=self.codec_type,
            width=self.width,
            height=self.height,
            frames_per_second=self.frames_per_second,
            frame_type=self.frame_type,
            rotation=self.rotation,
            track_id=self.track_id,
            capture_time_ms=self.capture_time_ms,
            decode_time_ms=self.decode_time_ms,
            uid=self.uid,
            stream_type=self.stream_type,
            presentation_ms=self.presentation_ms
        )

    @staticmethod
    def create(info: EncodedVideoFrameInfo) -> 'EncodedVideoFrameInfoInner':
        return EncodedVideoFrameInfoInner(
            info.codec_type,
            info.width,
            info.height,
            info.frames_per_second,
            info.frame_type,
            info.rotation,
            info.track_id,
            info.capture_time_ms,
            info.decode_time_ms,
            info.uid,
            info.stream_type,
            info.presentation_ms
        )
    


class EncryptionConfigInner(ctypes.Structure):
    _fields_ = [
        ("encryption_mode", ctypes.c_int),
        ("encryption_key", ctypes.c_char_p),
        ("encryption_kdf_salt", ctypes.c_uint8 * 32)
    ]

    def get(self):
        return EncryptionConfig(
            encryption_mode=self.encryption_mode,
            encryption_key=self.encryption_key.decode() if self.encryption_key else "",
            encryption_kdf_salt=bytearray(bytes(self.encryption_kdf_salt))
        )   

    @staticmethod
    def create(config: EncryptionConfig) -> 'EncryptionConfigInner':
        length = len(config.encryption_kdf_salt) if config.encryption_kdf_salt else 0
        #   如果length大于32，则设置为32
        if length > 32:
            length = 32
        #change bytearray to uint8 * length
        encryption_kdf_salt = (ctypes.c_uint8 * 32)() # 32 bytes,empty array
        # get min length of config.encryption_kdf_salt and 32
        min_length = min(length, 32)
        #copy config.encryption_kdf_salt to encryption_kdf_salt
        for i in range(min_length):
            encryption_kdf_salt[i] = config.encryption_kdf_salt[i]
      
        # change encryption_key to c_char_p
        encryption_key = config.encryption_key.encode('utf-8') if config.encryption_key else None
        #change None to c_char_p
        return EncryptionConfigInner(
            config.encryption_mode,
            encryption_key,
            encryption_kdf_salt
        )


class CapabilityItemInner(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint8),
        ("name", ctypes.c_char_p)
    ]

    def get(self):
        return CapabilityItem(
            id=self.id,
            name=self.name.decode() if self.name else ""
        )

    @staticmethod
    def create(item: CapabilityItem) -> 'CapabilityItemInner':
        return CapabilityItemInner(
            item.id,
            item.name.encode() if item.name else None
        )


class CapabilityItemMapInner(ctypes.Structure):
    _fields_ = [
        ("item", ctypes.POINTER(CapabilityItemInner)),
        ("size", ctypes.c_size_t)
    ]

    def get(self):
        items = []
        if self.item and self.size > 0:
            for i in range(self.size):
                items.append(self.item[i].get())
        return CapabilityItemMap(
            item=items,
            size=self.size
        )

    @staticmethod
    def create(item_map: CapabilityItemMap) -> 'CapabilityItemMapInner':
        if item_map.item and len(item_map.item) > 0:
            items_array = (CapabilityItemInner * len(item_map.item))()
            for i, item in enumerate(item_map.item):
                items_array[i] = CapabilityItemInner.create(item)
            items_ptr = ctypes.cast(items_array, ctypes.POINTER(CapabilityItemInner))
        else:
            items_ptr = ctypes.POINTER(CapabilityItemInner)()
        
        return CapabilityItemMapInner(
            items_ptr,
            len(item_map.item) if item_map.item else 0
        )


class CapabilitiesInner(ctypes.Structure):
    _fields_ = [
        ("item_map", ctypes.POINTER(CapabilityItemMapInner)),
        ("capability_type", ctypes.c_int)
    ]

    def get(self):
        return Capabilities(
            item_map=self.item_map.contents.get() if self.item_map else None,
            capability_type=self.capability_type
        )

    @staticmethod
    def create(capabilities: Capabilities) -> 'CapabilitiesInner':
        item_map_ptr = None
        if capabilities.item_map:
            item_map_inner = CapabilityItemMapInner.create(capabilities.item_map)
            item_map_ptr = ctypes.pointer(item_map_inner)
        
        return CapabilitiesInner(
            item_map_ptr,
            capabilities.capability_type
        )



class CapabilitiesItemMapInner(ctypes.Structure):
    _fields_ = [
        ("item", ctypes.POINTER(CapabilityItemInner)),
        ("size", ctypes.c_size_t)
    ]

    def get(self):
        return CapabilitiesItemMap(
            item=self.item,
            size=self.size
        )
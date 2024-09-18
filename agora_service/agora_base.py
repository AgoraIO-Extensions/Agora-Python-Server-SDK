import time
import ctypes
import os
import sys


from . import agora_lib

AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDL = ctypes.c_void_p
user_id_t = ctypes.c_char_p

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


agora_service_create_custom_audio_track_pcm = agora_lib.agora_service_create_custom_audio_track_pcm
agora_service_create_custom_audio_track_pcm.restype = AGORA_HANDLE
agora_service_create_custom_audio_track_pcm.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

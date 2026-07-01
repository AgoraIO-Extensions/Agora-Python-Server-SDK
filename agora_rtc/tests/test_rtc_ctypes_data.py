"""
author: Wei
date: 2026-07-01
"""

from agora.rtc.agora_base import (
    AudioEncoderConfiguration,
    AudioProfileType,
    AudioSubscriptionOptions,
    EncryptionConfig,
    EncodedVideoFrameInfo,
    RTCConnInfo,
    VideoCodecType,
    VideoDimensions,
)
from agora.rtc._ctypes_handle._ctypes_data import (
    AudioEncoderConfigurationInner,
    AudioSubscriptionOptionsInner,
    EncryptionConfigInner,
    EncodedVideoFrameInfoInner,
    RTCConnInfoInner,
    VideoDimensionsInner,
)


def test_audio_encoder_configuration_inner_create():
    config = AudioEncoderConfiguration(audioProfile=AudioProfileType.AUDIO_PROFILE_MUSIC_STANDARD)
    inner = AudioEncoderConfigurationInner.create(config)
    assert inner.audioProfile == AudioProfileType.AUDIO_PROFILE_MUSIC_STANDARD


def test_rtc_conn_info_inner_create_and_get():
    info = RTCConnInfo(
        id=1,
        channel_id="channel_a",
        state=2,
        local_user_id="user_1",
        internal_uid=10086,
    )
    inner = RTCConnInfoInner.create(info)
    assert inner.channel_id == b"channel_a"
    assert inner.local_user_id == b"user_1"

    restored = inner.get()
    assert restored.channel_id == "channel_a"
    assert restored.local_user_id == "user_1"
    assert restored.internal_uid == 10086


def test_audio_subscription_options_inner_create_and_get():
    options = AudioSubscriptionOptions(
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=2,
        sample_rate_hz=48000,
    )
    inner = AudioSubscriptionOptionsInner.create(options)
    assert inner.pcm_data_only == 1
    assert inner.sample_rate_hz == 48000

    restored = inner.get()
    assert restored.number_of_channels == 2
    assert restored.sample_rate_hz == 48000


def test_encryption_config_inner_create_and_get():
    config = EncryptionConfig(
        encryption_mode=1,
        encryption_key="secret",
        encryption_kdf_salt=bytearray(b"salt"),
        datastream_encryption_enabled=True,
    )
    inner = EncryptionConfigInner.create(config)
    assert inner.encryption_key == b"secret"
    assert inner.encryption_kdf_salt[0] == ord("s")

    restored = inner.get()
    assert restored.encryption_key == "secret"
    assert restored.datastream_encryption_enabled is True


def test_video_dimensions_and_encoded_frame_info_inner():
    dimensions = VideoDimensions(width=1280, height=720)
    dim_inner = VideoDimensionsInner.create(dimensions)
    assert dim_inner.width == 1280
    assert dim_inner.height == 720
    assert dim_inner.get().height == 720

    info = EncodedVideoFrameInfo(
        codec_type=VideoCodecType.VIDEO_CODEC_H264,
        width=1280,
        height=720,
        frames_per_second=30,
    )
    info_inner = EncodedVideoFrameInfoInner.create(info)
    assert info_inner.codec_type == VideoCodecType.VIDEO_CODEC_H264
    assert info_inner.get().frames_per_second == 30

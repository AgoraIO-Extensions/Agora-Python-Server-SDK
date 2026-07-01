"""
author: Wei
date: 2026-07-01
"""

from agora.rtc.agora_base import (
    AreaCode,
    ChannelProfileType,
    ClientRoleType,
    RTCConnInfo,
    VideoCodecType,
    APMConfig,
)


def test_channel_profile_enum():
    assert ChannelProfileType.CHANNEL_PROFILE_COMMUNICATION == 0
    assert ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING == 1


def test_client_role_enum():
    assert ClientRoleType.CLIENT_ROLE_BROADCASTER == 1
    assert ClientRoleType.CLIENT_ROLE_AUDIENCE == 2


def test_video_codec_enum():
    assert VideoCodecType.VIDEO_CODEC_H264 == 2
    assert VideoCodecType.VIDEO_CODEC_AV1 == 12


def test_area_code_enum():
    assert AreaCode.AREA_CODE_GLOB == 0xFFFFFFFF


def test_rtc_conn_info_dataclass():
    info = RTCConnInfo(
        id=1,
        channel_id="test_channel",
        state=2,
        local_user_id="user_1",
        internal_uid=10086,
    )
    assert info.channel_id == "test_channel"
    assert info.internal_uid == 10086


def test_apm_config_to_json_string():
    config = APMConfig()
    json_str = config._to_json_string()
    assert '"enabled":false' in json_str
    assert '"ainsModelPref":10' in json_str

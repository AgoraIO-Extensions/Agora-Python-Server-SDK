"""
author: Wei
date: 2026-07-01
"""

import ctypes

from agora.rtm.rtm_base import (
    PublishOptions,
    RtmEncryptionConfig,
    RtmLogConfig,
    RtmLogLevel,
    SubscribeOptions,
)
from agora.rtm._ctypes_handle._ctypes_data import (
    MessageEventInner,
    PublishOptionsInner,
    RtmEncryptionConfigInner,
    RtmLogConfigInner,
    SubscribeOptionsInner,
)


def test_subscribe_options_inner_create():
    options = SubscribeOptions(with_message=False, with_presence=True)
    inner = SubscribeOptionsInner.create(options)
    assert inner.withMessage is False
    assert inner.withPresence is True


def test_rtm_encryption_config_inner_create():
    config = RtmEncryptionConfig(encryption_key="secret", encryption_salt="salt")
    inner = RtmEncryptionConfigInner.create(config)
    assert inner.encryptionKey == b"secret"
    assert inner.encryptionSalt[0] == ord("s")


def test_rtm_log_config_inner_create():
    config = RtmLogConfig(
        file_path="/tmp/rtm.log",
        file_size_kb=1024,
        log_level=RtmLogLevel.RTM_LOG_LEVEL_INFO,
    )
    inner = RtmLogConfigInner.create(config)
    assert inner.filePath == b"/tmp/rtm.log"
    assert inner.fileSizeInKB == 1024
    assert inner.level == RtmLogLevel.RTM_LOG_LEVEL_INFO


def test_publish_options_inner_create():
    options = PublishOptions(custom_type="demo", store_in_history=True)
    inner = PublishOptionsInner.create(options)
    assert inner.customType == b"demo"
    assert inner.storeInHistory is True


def test_message_event_inner_get():
    payload = b"hello"
    inner = MessageEventInner(
        channelType=1,
        messageType=0,
        channelName=b"channel_a",
        channelTopic=b"topic_a",
        message=ctypes.c_char_p(payload),
        messageLength=len(payload),
        publisher=b"user_1",
        customType=b"text",
    )
    event = inner.get()
    assert event.channel_name == "channel_a"
    assert event.message == payload
    assert event.publisher == "user_1"

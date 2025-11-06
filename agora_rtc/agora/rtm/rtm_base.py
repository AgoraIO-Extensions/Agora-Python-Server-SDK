
from dataclasses import dataclass
import time
import ctypes
from enum import IntEnum


#from agora.rtm.rtm_event_handler import RtmEventHandler


import logging

from . import rtm_lib
logger = logging.getLogger(__name__)

#ennum define
class RtmAreaCode(IntEnum):
    RTM_AREA_CODE_CN = 0x00000001
    RTM_AREA_CODE_NA = 0x00000002
    RTM_AREA_CODE_EU = 0x00000004
    RTM_AREA_CODE_AS = 0x00000008
    RTM_AREA_CODE_JP = 0x00000010
    RTM_AREA_CODE_IN = 0x00000020
    RTM_AREA_CODE_GLOB = 0xFFFFFFFF

class RtmLogLevel(IntEnum):
  RTM_LOG_LEVEL_NONE = 0x0000,
  RTM_LOG_LEVEL_INFO = 0x0001,
  RTM_LOG_LEVEL_WARN = 0x0002,
  RTM_LOG_LEVEL_ERROR = 0x0004,
  RTM_LOG_LEVEL_FATAL = 0x0008,

class RtmEncryptionMode(IntEnum):
  RTM_ENCRYPTION_MODE_NONE = 0
  RTM_ENCRYPTION_MODE_AES_128_GCM = 1
  RTM_ENCRYPTION_MODE_AES_256_GCM = 2

class RtmServiceType(IntEnum):
    RTM_SERVICE_TYPE_NONE = 0x00000000,
    RTM_SERVICE_TYPE_MESSAGE = 0x00000001,
    RTM_SERVICE_TYPE_STREAM = 0x00000002,




class RtmChannelType(IntEnum):
  RTM_CHANNEL_TYPE_NONE = 0
  RTM_CHANNEL_TYPE_MESSAGE = 1
  RTM_CHANNEL_TYPE_STREAM = 2
  RTM_CHANNEL_TYPE_USER = 3

class RtmMessageType(IntEnum):
  RTM_MESSAGE_TYPE_BINARY = 0,
  RTM_MESSAGE_TYPE_STRING = 1,


class RtmStorageType(IntEnum):
    RTM_STORAGE_TYPE_NONE = 0
    RTM_STORAGE_TYPE_USER = 1
    RTM_STORAGE_TYPE_CHANNEL = 2

class RtmStorageEventType(IntEnum):
    RTM_STORAGE_EVENT_TYPE_NONE = 0,
    RTM_STORAGE_EVENT_TYPE_SNAPSHOT = 1
    RTM_STORAGE_EVENT_TYPE_SET = 2
    RTM_STORAGE_EVENT_TYPE_UPDATE = 3
    RTM_STORAGE_EVENT_TYPE_REMOVE = 4
 

class RtmLockEventType(IntEnum):
    RTM_LOCK_EVENT_TYPE_NONE = 0,
    RTM_LOCK_EVENT_TYPE_SNAPSHOT = 1,
    RTM_LOCK_EVENT_TYPE_LOCK_SET = 2,
    RTM_LOCK_EVENT_TYPE_LOCK_REMOVED = 3,
    RTM_LOCK_EVENT_TYPE_LOCK_ACQUIRED = 4,
    RTM_LOCK_EVENT_TYPE_LOCK_RELEASED = 5,
    RTM_LOCK_EVENT_TYPE_LOCK_EXPIRED = 6,

class RtmProxyType(IntEnum):
  RTM_PROXY_TYPE_NONE = 0,
  RTM_PROXY_TYPE_HTTP = 1,
  RTM_PROXY_TYPE_CLOUD_TCP = 2,

class RtmTopicEventType(IntEnum):
  RTM_TOPIC_EVENT_TYPE_NONE = 0,
  RTM_TOPIC_EVENT_TYPE_SNAPSHOT = 1,
  RTM_TOPIC_EVENT_TYPE_REMOTE_JOIN_TOPIC = 2,
  RTM_TOPIC_EVENT_TYPE_REMOTE_LEAVE_TOPIC = 3,

class RtmPresenceEventType(IntEnum):
  RTM_PRESENCE_EVENT_TYPE_NONE = 0,
  RTM_PRESENCE_EVENT_TYPE_SNAPSHOT = 1,
  RTM_PRESENCE_EVENT_TYPE_INTERVAL = 2,
  RTM_PRESENCE_EVENT_TYPE_REMOTE_JOIN_CHANNEL = 3,
  RTM_PRESENCE_EVENT_TYPE_REMOTE_LEAVE_CHANNEL = 4,
  RTM_PRESENCE_EVENT_TYPE_REMOTE_TIMEOUT = 5,
  RTM_PRESENCE_EVENT_TYPE_REMOTE_STATE_CHANGED = 6,
  RTM_PRESENCE_EVENT_TYPE_ERROR_OUT_OF_SERVICE = 7,


@dataclass
class RtmLogConfig:
    file_path: str = ""
    file_size_kb: int = 5*1024
    log_level: RtmLogLevel = RtmLogLevel.RTM_LOG_LEVEL_INFO #default to info


@dataclass(kw_only=True)
class RtmProxyConfig:
    proxy_type: int = RtmProxyType.RTM_PROXY_TYPE_NONE
    proxy_server: str = ""
    proxy_port: int = 0
    proxy_username: str = ""
    proxy_password: str = ""

@dataclass(kw_only=True)
class RtmPrivateConfig:
    service_type: RtmServiceType = RtmServiceType.RTM_SERVICE_TYPE_NONE
    access_point_hosts: list[str] = None
    
    def __post_init__(self):
        if self.access_point_hosts is None:
            self.access_point_hosts = []
    
@dataclass(kw_only=True)
class RtmEncryptionConfig:
    encryption_mode: int = RtmEncryptionMode.RTM_ENCRYPTION_MODE_NONE
    encryption_key: str = ""
    encryption_salt: str = ""







class StateItem:
    pass
class IntervalInfo:
    pass
class SnapshotInfo:
    pass
class TopicInfo:
    pass
class LockDetail:
    pass
class Metadata:
    pass
class UserState:
    pass

@dataclass
class LinkStateEvent:
    current_state: int
    previous_state: int
    service_type: int
    operation: int
    reason_code: int
    reason: str
    affected_channels: list[str]
    unrestored_channels: list[str]
    is_resumed: bool
    timestamp: int

class HistoryMessage:
    pass
class User:
    pass
class ChannelInfo:
    pass
class ChannelInfoList:
    pass

@dataclass
class MessageEvent:
    channel_type: int
    message_type: int
    channel_name: str
    channel_topic: str
    message: str
    message_length: int
    publisher: str
    custom_type: str



@dataclass
class PresenceEvent:
    type: int
    channel_type: int
    channel_name: str
    publisher: str
    state_items: list[StateItem]
    state_item_count: int
    interval: IntervalInfo
    snapshot: SnapshotInfo

@dataclass
class TopicEvent:
    type: int
    channel_name: str
    publisher: str
    topic_infos: list[TopicInfo]
    topic_info_count: int

@dataclass
class LockEvent:
    channel_type: int
    event_type: int
    channel_name: str
    lock_detail_list: list[LockDetail]
    count: int
  
@dataclass
class StorageEvent:
    channel_type: int
    storage_type: int
    event_type: int
    target: str
    data: Metadata

@dataclass
class PublishOptions:
    channel_type: int = RtmChannelType.RTM_CHANNEL_TYPE_NONE
    message_type: int = RtmMessageType.RTM_MESSAGE_TYPE_BINARY
    custom_type: str = ""
    store_in_history: bool = False

@dataclass
class SubscribeOptions:
    with_message: bool = True
    with_metadata: bool = False
    with_presence: bool = False
    with_lock: bool = False
    be_quiet: bool = True


class IRtmEventHandler:
    def on_message_event(self, event: MessageEvent):
        pass
    def on_presence_event(self, event: PresenceEvent):
        pass
    def on_topic_event(self, event: TopicEvent):
        pass
    def on_lock_event(self, event: LockEvent):
        pass
    def on_storage_event(self, event: StorageEvent):
        pass
    def on_join_result(self, request_id: int, channel_name: str, user_id: str, error_code: int):
        pass
    def on_leave_result(self, request_id: int, channel_name: str, user_id: str, error_code: int):
        pass
    def on_join_topic_result(self, request_id: int, channel_name: str, user_id: str, topic: str, meta: str, error_code: int):
        pass
    def on_leave_topic_result(self, request_id: int, channel_name: str, user_id: str, topic: str, meta: str, error_code: int):
        pass
    def on_subscribe_topic_result(self, request_id: int, channel_name: str, user_id: str, topic: str, succeed_users: list[str], failed_users: list[str], error_code: int):
        pass
    def on_connection_state_changed(self, channel_name: str, state: int, reason: int):
        pass
    def on_token_privilege_will_expire(self, channel_name: str):
        pass
    def on_subscribe_result(self, request_id: int, channel_name: str, error_code: int):
        pass
    def on_unsubscribe_result(self, request_id: int, channel_name: str, error_code: int):
        pass
    def on_publish_result(self, request_id: int, error_code: int):
        pass
    def on_login_result(self, request_id: int, error_code: int):
        pass
    def on_set_channel_metadata_result(self, request_id: int, channel_name: str, channel_type: int, error_code: int):
        pass
    def on_update_channel_metadata_result(self, request_id: int, channel_name: str, channel_type: int, error_code: int):
        pass
    def on_remove_channel_metadata_result(self, request_id: int, channel_name: str, channel_type: int, error_code: int):
        pass
    def on_get_channel_metadata_result(self, request_id: int, channel_name: str, channel_type: int, data: str, error_code: int):
        pass
    def on_set_user_metadata_result(self, request_id: int, user_id: str, error_code: int):
        pass
    def on_update_user_metadata_result(self, request_id: int, user_id: str, error_code: int):
        pass
    def on_remove_user_metadata_result(self, request_id: int, user_id: str, error_code: int):
        pass
    def on_get_user_metadata_result(self, request_id: int, user_id: str, data: str, error_code: int):
        pass
    def on_subscribe_user_metadata_result(self, request_id: int, user_id: str, error_code: int):
        pass
    def on_set_lock_result(self, request_id: int, channel_name: str, channel_type: int, lock_name: str, error_code: int):
        pass
    def on_remove_lock_result(self, request_id: int, channel_name: str, channel_type: int, lock_name: str, error_code: int):
        pass
    def on_release_lock_result(self, request_id: int, channel_name: str, channel_type: int, lock_name: str, error_code: int):
        pass
    def on_acquire_lock_result(self, request_id: int, channel_name: str, channel_type: int, lock_name: str, error_code: int, error_details: str):
        pass
    def on_revoke_lock_result(self, request_id: int, channel_name: str, channel_type: int, lock_name: str, error_code: int):
        pass
    def on_get_locks_result(self, request_id: int, channel_name: str, channel_type: int, lock_detail_list: list[LockDetail], count: int, error_code: int):
        pass
    def on_who_now_result(self, request_id: int, user_state_list: list[UserState], next_page: str, error_code: int):
        pass
    def on_get_online_users_result(self, request_id: int, user_state_list: list[UserState], next_page: str, error_code: int):
        pass
    def on_where_now_result(self, request_id: int, channels: list[ChannelInfo], count: int, error_code: int):
        pass
    def on_get_user_channels_result(self, request_id: int, channels: list[ChannelInfo], count: int, error_code: int):
        pass
    def on_presence_set_state_result(self, request_id: int, error_code: int):
        pass
    def on_presence_remove_state_result(self, request_id: int, error_code: int):
        pass
    def on_presence_get_state_result(self, request_id: int, state: UserState, error_code: int):
        pass
    def on_link_state_event(self, event: LinkStateEvent):
        pass
    def on_get_history_messages_result(self, request_id: int, message_list: list[HistoryMessage], count: int, new_start: int, error_code: int):
        pass
    def on_logout_result(self, request_id: int, error_code: int):
        pass
    def on_renew_token_result(self, request_id: int, server_type: int, channel_name: str, error_code: int):
        pass
    def on_renew_token_result(self, request_id: int, server_type: int, channel_name: str, error_code: int):
        pass
    def on_unsubscribe_topic_result(self, request_id: int, channel_name: str, topic: str, error_code: int):
        pass
    def on_get_subscribed_user_list_result(self, request_id: int, channel_name: str, topic: str, users: list[User], error_code: int):
        pass
    def on_unsubscribe_user_metadata_result(self, request_id: int, user_id: str, error_code: int):
        pass

    
    
@dataclass(kw_only=True)
class RtmConfig:
    app_id: str = ""
    user_id: str = ""
    area_code: RtmAreaCode = RtmAreaCode.RTM_AREA_CODE_GLOB
    protocol_type: int = 0
    presence_timeout: int = 0
    heartbeat_interval: int = 0
    context: object = None
    use_string_user_id: int = 0
    multipath: int = 0
    isp_policy_enabled: int = 0
    event_handler: IRtmEventHandler = None
    log_config: RtmLogConfig = None
    proxy_config: RtmProxyConfig = None
    encryption_config: RtmEncryptionConfig = None
    private_config: RtmPrivateConfig = None
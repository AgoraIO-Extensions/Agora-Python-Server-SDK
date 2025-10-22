import ctypes


from agora.rtm import rtm_lib


AGORA_HANDLE = ctypes.c_void_p
AGORA_API_C_INT = ctypes.c_int
AGORA_API_C_HDL = ctypes.c_void_p
AGORA_API_C_VOID = None
user_id_t = ctypes.c_char_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint
uint64_t = ctypes.c_uint64
k_max_codec_name_len = 100

from ..rtm_base import *

#global api
#convert python instance to ctypes pointer
def convert_python_to_ctypes_pointer(python_instance):
    void_ptr = ctypes.cast(ctypes.py_object(python_instance), ctypes.POINTER(ctypes.c_void_p))
    return void_ptr
#convert ctypes pointer to python instance
def convert_ctypes_pointer_to_python_instance(ctypes_pointer):
    python_instance = ctypes.cast(ctypes_pointer, ctypes.py_object).value
    return python_instance

class RtmLogConfigInner(ctypes.Structure):
    _fields_ = [
        ("filePath", ctypes.c_char_p),
        ("fileSizeInKB", ctypes.c_uint32),
        ("level", ctypes.c_int)
    ]
    @staticmethod
    def create(config: RtmLogConfig) -> 'RtmLogConfigInner':
        return RtmLogConfigInner(
            filePath=config.file_path.encode(),
            fileSizeInKB=config.file_size_kb,
            level=config.log_level
        )
class RtmProxyConfigInner(ctypes.Structure):
    _fields_ = [
        ("proxyType", ctypes.c_int),
        ("server", ctypes.c_char_p),
        ("port", ctypes.c_uint16),
        ("account", ctypes.c_char_p),
        ("password", ctypes.c_char_p)
    ]
    @staticmethod
    def create(config: RtmProxyConfig) -> 'RtmProxyConfigInner':
        return RtmProxyConfigInner(
            proxyType=config.proxy_type,
            server=config.proxy_server.encode() if config.proxy_server else b"",
            port=config.proxy_port,
            account=config.proxy_username.encode() if config.proxy_username else b"",
            password=config.proxy_password.encode() if config.proxy_password else b""
        )
class RtmEncryptionConfigInner(ctypes.Structure):
    _fields_ = [    
        ("encryptionMode", ctypes.c_int),
        ("encryptionKey", ctypes.c_char_p),
        ("encryptionSalt", ctypes.c_uint8 * 32)
    ]
    @staticmethod
    def create(config: RtmEncryptionConfig) -> 'RtmEncryptionConfigInner':
        # 创建32字节的salt数组
        salt_array = (ctypes.c_uint8 * 32)()
        if config.encryption_salt:
            salt_bytes = config.encryption_salt.encode() if isinstance(config.encryption_salt, str) else config.encryption_salt
            for i, byte in enumerate(salt_bytes[:32]):
                salt_array[i] = byte
        
        return RtmEncryptionConfigInner(
            encryptionMode=config.encryption_mode,
            encryptionKey=config.encryption_key.encode() if config.encryption_key else b"",
            encryptionSalt=salt_array
        )

class RtmPrivateConfigInner(ctypes.Structure):
    _fields_ = [
        ("serviceType", ctypes.c_int),
        ("accessPointHosts", ctypes.c_char_p),
        ("accessPointHostsCount", ctypes.c_size_t)
    ]
    @staticmethod
    def create(config: RtmPrivateConfig) -> 'RtmPrivateConfigInner':
        # 将列表转换为逗号分隔的字符串
        hosts_str = ",".join(config.access_point_hosts) if config.access_point_hosts else ""
        return RtmPrivateConfigInner(
            serviceType=config.service_type,
            accessPointHosts=ctypes.c_char_p(0),
            accessPointHostsCount=ctypes.c_size_t(0)
        )
    

class RtmConfigInner(ctypes.Structure):
    _fields_ = [
        ("appId", ctypes.c_char_p),
        ("userId", ctypes.c_char_p),
        ("areaCode", ctypes.c_int),
        ("protocolType", ctypes.c_int),
        ("presenceTimeout", ctypes.c_uint32),
        ("heartbeatInterval", ctypes.c_uint32),
        ("context", ctypes.c_void_p),
        ("useStringUserId", ctypes.c_bool),
        ("multipath", ctypes.c_bool),
        ("ispPolicyEnabled", ctypes.c_bool),
        ("eventHandler", ctypes.c_void_p),
        ("logConfig", RtmLogConfigInner),
        ("proxyConfig", RtmProxyConfigInner),
        ("encryptionConfig", RtmEncryptionConfigInner),
        ("privateConfig", RtmPrivateConfigInner)
    ]
    @staticmethod
    def create(config: RtmConfig) -> 'RtmConfigInner':
        inner_log_config = RtmLogConfigInner.create(config.log_config)
        inner_private_config = RtmPrivateConfigInner.create(config.private_config)
        inner_proxy_config = RtmProxyConfigInner.create(config.proxy_config)
        inner_encryption_config = RtmEncryptionConfigInner.create(config.encryption_config)
        
        inner_config = RtmConfigInner(
            appId=config.app_id.encode() if config.app_id else b"",
            userId=config.user_id.encode() if config.user_id else b"",
            areaCode=config.area_code,
            protocolType=config.protocol_type,
            presenceTimeout=config.presence_timeout,
            heartbeatInterval=config.heartbeat_interval,
            context=ctypes.c_void_p(config.context) if config.context else ctypes.c_void_p(0),
            useStringUserId=config.use_string_user_id,
            multipath=config.multipath,
            ispPolicyEnabled=config.isp_policy_enabled,
            eventHandler=ctypes.c_void_p(id(config.event_handler)) if config.event_handler else ctypes.c_void_p(0),
            logConfig=inner_log_config,
            proxyConfig=inner_proxy_config,
            encryptionConfig=inner_encryption_config,
            privateConfig=inner_private_config
        )
        return inner_config
class PublishOptionsInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("customType", ctypes.c_char_p),
        ("storeInHistory", ctypes.c_bool)
    ]
    @staticmethod
    def create(options: PublishOptions) -> 'PublishOptionsInner':
        return PublishOptionsInner(
            channelType=options.channel_type,
            messageType=options.message_type,
            customType=options.custom_type.encode() if options.custom_type else b"",
            storeInHistory=options.store_in_history
        )

class SubscribeOptionsInner(ctypes.Structure):
    _fields_ = [
        ("withMessage", ctypes.c_bool),
        ("withMetadata", ctypes.c_bool),
        ("withPresence", ctypes.c_bool),
        ("withLock", ctypes.c_bool),
        ("beQuiet", ctypes.c_bool)
    ]
    @staticmethod
    def create(options: SubscribeOptions) -> 'SubscribeOptionsInner':
        return SubscribeOptionsInner(
            withMessage=options.with_message,
            withMetadata=options.with_metadata,
            withPresence=options.with_presence,
            withLock=options.with_lock,
            beQuiet=options.be_quiet
        )
class MessageEventInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("channelName", ctypes.c_char_p),
        ("channelTopic", ctypes.c_char_p),
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p)
    ]
    def get(self) -> MessageEvent:
        return MessageEvent(
            channel_type=self.channelType,
            message_type=self.messageType,
            channel_name=self.channelName.decode('utf-8') if self.channelName else "",
            channel_topic=self.channelTopic.decode('utf-8') if self.channelTopic else "",
            message=self.message.decode('utf-8') if self.message else "",
            message_length=self.messageLength,
            publisher=self.publisher.decode('utf-8') if self.publisher else "",
            custom_type=self.customType.decode('utf-8') if self.customType else "",
        )
class PresenceEventInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("channelName", ctypes.c_char_p),
        ("channelTopic", ctypes.c_char_p),
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p)
    ]
class TopicEventInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("channelName", ctypes.c_char_p),
        ("channelTopic", ctypes.c_char_p),
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p)
    ]
class LockEventInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("channelName", ctypes.c_char_p),
        ("channelTopic", ctypes.c_char_p),
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p)
    ]
class StorageEventInner(ctypes.Structure):
    _fields_ = [
        ("channelType", ctypes.c_int),
        ("messageType", ctypes.c_int),
        ("channelName", ctypes.c_char_p),
        ("channelTopic", ctypes.c_char_p),
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p)
    ]
class JoinResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class LeaveResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class JoinTopicResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("userId", ctypes.c_char_p),
        ("topic", ctypes.c_char_p),
        ("meta", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class LeaveTopicResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("userId", ctypes.c_char_p),
        ("topic", ctypes.c_char_p),
        ("meta", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]

class ConnectionStateChangedInner(ctypes.Structure):
    _fields_ = [
        ("channelName", ctypes.c_char_p),
        ("state", ctypes.c_int),
        ("reason", ctypes.c_int)
    ]
class TokenPrivilegeWillExpireInner(ctypes.Structure):
    _fields_ = [
        ("channelName", ctypes.c_char_p)
    ]
class SubscribeResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class PublishResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("errorCode", ctypes.c_int)
    ]
class LoginResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("errorCode", ctypes.c_int)
    ]
class SetChannelMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
class UpdateChannelMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
class RemoveChannelMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
class GetChannelMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("data", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class SetUserMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class UpdateUserMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class RemoveUserMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class GetUserMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userId", ctypes.c_char_p),
        ("data", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class SubscribeUserMetadataResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userId", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class SetLockResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class RemoveLockResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class ReleaseLockResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class AcquireLockResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int),
        ("errorDetails", ctypes.c_char_p)
    ]
class RevokeLockResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockName", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]

class UserStateInner(ctypes.Structure):
    _fields_ = [
        ("userId", ctypes.c_char_p),
        ("userData", ctypes.c_char_p),
        ("userDataLength", ctypes.c_size_t),
    ]
class ChannelInfoInner(ctypes.Structure):
    _fields_ = [
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("channelTopic", ctypes.c_char_p),
        ("channelTopicLength", ctypes.c_size_t),
    ]
class LockDetailInner(ctypes.Structure):
    _fields_ = [
        ("lockName", ctypes.c_char_p),
        ("lockType", ctypes.c_int),
        ("lockData", ctypes.c_char_p),
        ("lockDataLength", ctypes.c_size_t),
    ]
class HistoryMessageInner(ctypes.Structure):
    _fields_ = [
        ("message", ctypes.c_char_p),
        ("messageLength", ctypes.c_size_t),
        ("publisher", ctypes.c_char_p),
        ("customType", ctypes.c_char_p),
    ]
class LinkStateEventInner(ctypes.Structure):
    _fields_ = [
        ("currentState", ctypes.c_int),
        ("previousState", ctypes.c_int),
        ("serviceType", ctypes.c_int),
        ("operation", ctypes.c_int),
        ("reasonCode", ctypes.c_int),
        ("reason", ctypes.c_char_p),
        ("affectedChannels", ctypes.POINTER(ctypes.c_char_p)),
        ("affectedChannelCount", ctypes.c_size_t),
        ("unrestoredChannels", ctypes.POINTER(ctypes.c_char_p)),
        ("unrestoredChannelCount", ctypes.c_size_t),
        ("isResumed", ctypes.c_bool),
        ("timestamp", ctypes.c_uint64),
    ]
  
    def get(self) -> LinkStateEvent:
        # convert affectedChannels and unrestoredChannels to list[str]
        affected_channels = []
        unrestored_channels = []
        if self.affectedChannels and self.affectedChannelCount > 0:
            for i in range(self.affectedChannelCount):
                affected_channels.append(self.affectedChannels[i].decode('utf-8'))
        if self.unrestoredChannels and self.unrestoredChannelCount > 0:
            for i in range(self.unrestoredChannelCount):
                unrestored_channels.append(self.unrestoredChannels[i].decode('utf-8'))
        return LinkStateEvent(
            current_state=self.currentState,
            previous_state=self.previousState,
            service_type=self.serviceType,
            operation=self.operation,
            reason_code=self.reasonCode,
            reason=self.reason.decode('utf-8') if self.reason is not None else "",
            affected_channels=affected_channels,
            unrestored_channels=unrestored_channels,
            is_resumed=self.isResumed,
            timestamp=self.timestamp,
        )
class UserListInner(ctypes.Structure):
    _fields_ = [
        ("userIds", ctypes.POINTER(ctypes.c_char_p)),
        ("count", ctypes.c_int),
    ]
class UserStateListInner(ctypes.Structure):
    _fields_ = [
        ("userStates", ctypes.POINTER(UserStateInner)),
        ("count", ctypes.c_int),
    ]
class ChannelInfoListInner(ctypes.Structure):
    _fields_ = [
        ("channelInfos", ctypes.POINTER(ChannelInfoInner)),
        ("count", ctypes.c_int),
    ]
class LockDetailListInner(ctypes.Structure):
    _fields_ = [
        ("lockDetails", ctypes.POINTER(LockDetailInner)),
        ("count", ctypes.c_int),
    ]
class HistoryMessageListInner(ctypes.Structure):
    _fields_ = [
        ("historyMessages", ctypes.POINTER(HistoryMessageInner)),
        ("count", ctypes.c_int),
    ]

class GetLocksResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channelName", ctypes.c_char_p),
        ("channelType", ctypes.c_int),
        ("lockDetailList", ctypes.POINTER(LockDetailInner)),
        ("count", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
class WhoNowResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userStateList", ctypes.POINTER(UserStateInner)),
        ("count", ctypes.c_int),
        ("nextPage", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class GetOnlineUsersResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("userStateList", ctypes.POINTER(UserStateInner)),
        ("count", ctypes.c_int),
        ("nextPage", ctypes.c_char_p),
        ("errorCode", ctypes.c_int)
    ]
class WhereNowResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channels", ctypes.POINTER(ChannelInfoInner)),
        ("count", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
class GetUserChannelsResultInner(ctypes.Structure):
    _fields_ = [
        ("requestId", ctypes.c_uint64),
        ("channels", ctypes.POINTER(ChannelInfoInner)),
        ("count", ctypes.c_int),
        ("errorCode", ctypes.c_int)
    ]
 
#envent handler call type c declare
ON_MESSAGE_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(MessageEventInner))
ON_PRESENCE_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(PresenceEventInner))
ON_TOPIC_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(TopicEventInner))
ON_LOCK_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LockEventInner))
ON_STORAGE_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(StorageEventInner))
ON_JOIN_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_LEAVE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_JOIN_TOPIC_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_LEAVE_TOPIC_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_SUBSCRIBE_TOPIC_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(UserListInner), ctypes.POINTER(UserListInner), ctypes.c_int)
ON_CONNECTION_STATE_CHANGED = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_TOKEN_PRIVILEGE_WILL_EXPIRE = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p)
ON_SUBSCRIBE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int)
ON_UNSUBSCRIBE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int)
ON_PUBLISH_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int)
ON_LOGIN_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int)
ON_SET_CHANNEL_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_UPDATE_CHANNEL_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_REMOVE_CHANNEL_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_GET_CHANNEL_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_SET_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_UPDATE_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_REMOVE_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_GET_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_SUBSCRIBE_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_SET_LOCK_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_REMOVE_LOCK_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_RELEASE_LOCK_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_ACQUIRE_LOCK_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_REVOKE_LOCK_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_GET_LOCKS_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
ON_WHO_NOW_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(UserStateInner), ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
ON_GET_ONLINE_USERS_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(UserStateInner), ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
ON_WHERE_NOW_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(ChannelInfoInner), ctypes.c_int, ctypes.c_int)
ON_GET_USER_CHANNELS_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(ChannelInfoInner), ctypes.c_int, ctypes.c_int)
ON_PRESENCE_SET_STATE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int)
ON_PRESENCE_REMOVE_STATE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int)
ON_PRESENCE_GET_STATE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(UserStateInner), ctypes.c_int, ctypes.c_int)
ON_LINK_STATE_EVENT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LinkStateEventInner))
ON_GET_HISTORY_MESSAGES_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.POINTER(HistoryMessageInner), ctypes.c_size_t, ctypes.c_uint64, ctypes.c_int)
ON_LOGOUT_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int)
ON_RENEW_TOKEN_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
ON_PUBLISH_TOPIC_MESSAGE_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_UNSUBSCRIBE_TOPIC_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
ON_GET_SUBSCRIBED_USER_LIST_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(UserListInner), ctypes.c_int, ctypes.c_int)
ON_UNSUBSCRIBE_USER_METADATA_RESULT = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)

class RtmEventHandlerInner(ctypes.Structure):
    _fields_ = [
        ("onMessageEvent", ON_MESSAGE_EVENT),
        ("onPresenceEvent", ON_PRESENCE_EVENT),
        ("onTopicEvent", ON_TOPIC_EVENT),
        ("onLockEvent", ON_LOCK_EVENT),
        ("onStorageEvent", ON_STORAGE_EVENT),
        ("onJoinResult", ON_JOIN_RESULT),
        ("onLeaveResult", ON_LEAVE_RESULT),
        ("onJoinTopicResult", ON_JOIN_TOPIC_RESULT),
        ("onLeaveTopicResult", ON_LEAVE_TOPIC_RESULT),
        ("onSubscribeTopicResult", ON_SUBSCRIBE_TOPIC_RESULT),
        ("onConnectionStateChanged", ON_CONNECTION_STATE_CHANGED),
        ("onTokenPrivilegeWillExpire", ON_TOKEN_PRIVILEGE_WILL_EXPIRE),
        ("onSubscribeResult", ON_SUBSCRIBE_RESULT),
        ("onUnsubscribeResult", ON_UNSUBSCRIBE_RESULT),
        ("onPublishResult", ON_PUBLISH_RESULT),
        ("onLoginResult", ON_LOGIN_RESULT),
        ("onSetChannelMetadataResult", ON_SET_CHANNEL_METADATA_RESULT),
        ("onUpdateChannelMetadataResult", ON_UPDATE_CHANNEL_METADATA_RESULT),
        ("onRemoveChannelMetadataResult", ON_REMOVE_CHANNEL_METADATA_RESULT),
        ("onGetChannelMetadataResult", ON_GET_CHANNEL_METADATA_RESULT),
        ("onSetUserMetadataResult", ON_SET_USER_METADATA_RESULT),
        ("onUpdateUserMetadataResult", ON_UPDATE_USER_METADATA_RESULT),
        ("onRemoveUserMetadataResult", ON_REMOVE_USER_METADATA_RESULT),
        ("onGetUserMetadataResult", ON_GET_USER_METADATA_RESULT),
        ("onSubscribeUserMetadataResult", ON_SUBSCRIBE_USER_METADATA_RESULT),
        ("onSetLockResult", ON_SET_LOCK_RESULT),
        ("onRemoveLockResult", ON_REMOVE_LOCK_RESULT),
        ("onReleaseLockResult", ON_RELEASE_LOCK_RESULT),
        ("onAcquireLockResult", ON_ACQUIRE_LOCK_RESULT),
        ("onRevokeLockResult", ON_REVOKE_LOCK_RESULT),
        ("onGetLocksResult", ON_GET_LOCKS_RESULT),
        ("onWhoNowResult", ON_WHO_NOW_RESULT),
        ("onGetOnlineUsersResult", ON_GET_ONLINE_USERS_RESULT),
        ("onWhereNowResult", ON_WHERE_NOW_RESULT),
        ("onGetUserChannelsResult", ON_GET_USER_CHANNELS_RESULT),
        ("onPresenceSetStateResult", ON_PRESENCE_SET_STATE_RESULT),
        ("onPresenceRemoveStateResult", ON_PRESENCE_REMOVE_STATE_RESULT),
        ("onPresenceGetStateResult", ON_PRESENCE_GET_STATE_RESULT),
        ("onLinkStateEvent", ON_LINK_STATE_EVENT),
        ("onGetHistoryMessagesResult", ON_GET_HISTORY_MESSAGES_RESULT),
        ("onLogoutResult", ON_LOGOUT_RESULT),
        ("onRenewTokenResult", ON_RENEW_TOKEN_RESULT),
        ("onPublishTopicMessageResult", ON_PUBLISH_TOPIC_MESSAGE_RESULT),
        ("onUnsubscribeTopicResult", ON_UNSUBSCRIBE_TOPIC_RESULT),
        ("onGetSubscribedUserListResult", ON_GET_SUBSCRIBED_USER_LIST_RESULT),
        ("onUnsubscribeUserMetadataResult", ON_UNSUBSCRIBE_USER_METADATA_RESULT),
        ("userData", ctypes.c_void_p),
    ]
    def __init__(self, event_handler: IRtmEventHandler, rtm_client):
        self.event_handler = event_handler
        self.userData = ctypes.c_void_p(id(rtm_client))
        self.onMessageEvent = ON_MESSAGE_EVENT(self._on_message_event)
        self.onPresenceEvent = ON_PRESENCE_EVENT(self._on_presence_event)
        self.onTopicEvent = ON_TOPIC_EVENT(self._on_topic_event)
        self.onLockEvent = ON_LOCK_EVENT(self._on_lock_event)
        self.onStorageEvent = ON_STORAGE_EVENT(self._on_storage_event)
        self.onJoinResult = ON_JOIN_RESULT(self._on_join_result)
        self.onLeaveResult = ON_LEAVE_RESULT(self._on_leave_result)
        self.onJoinTopicResult = ON_JOIN_TOPIC_RESULT(self._on_join_topic_result)
        self.onLeaveTopicResult = ON_LEAVE_TOPIC_RESULT(self._on_leave_topic_result)
        self.onSubscribeTopicResult = ON_SUBSCRIBE_TOPIC_RESULT(self._on_subscribe_topic_result)
        self.onConnectionStateChanged = ON_CONNECTION_STATE_CHANGED(self._on_connection_state_changed)
        self.onTokenPrivilegeWillExpire = ON_TOKEN_PRIVILEGE_WILL_EXPIRE(self._on_token_privilege_will_expire)
        self.onSubscribeResult = ON_SUBSCRIBE_RESULT(self._on_subscribe_result)
        self.onUnsubscribeResult = ON_UNSUBSCRIBE_RESULT(self._on_unsubscribe_result)
        self.onPublishResult = ON_PUBLISH_RESULT(self._on_publish_result)
        self.onLoginResult = ON_LOGIN_RESULT(self._on_login_result)
        self.onSetChannelMetadataResult = ON_SET_CHANNEL_METADATA_RESULT(self._on_set_channel_metadata_result)
        self.onUpdateChannelMetadataResult = ON_UPDATE_CHANNEL_METADATA_RESULT(self._on_update_channel_metadata_result)
        self.onRemoveChannelMetadataResult = ON_REMOVE_CHANNEL_METADATA_RESULT(self._on_remove_channel_metadata_result)
        self.onGetChannelMetadataResult = ON_GET_CHANNEL_METADATA_RESULT(self._on_get_channel_metadata_result)
        self.onSetUserMetadataResult = ON_SET_USER_METADATA_RESULT(self._on_set_user_metadata_result)
        self.onUpdateUserMetadataResult = ON_UPDATE_USER_METADATA_RESULT(self._on_update_user_metadata_result)
        self.onRemoveUserMetadataResult = ON_REMOVE_USER_METADATA_RESULT(self._on_remove_user_metadata_result)
        self.onGetUserMetadataResult = ON_GET_USER_METADATA_RESULT(self._on_get_user_metadata_result)
        self.onSubscribeUserMetadataResult = ON_SUBSCRIBE_USER_METADATA_RESULT(self._on_subscribe_user_metadata_result)
        self.onSetLockResult = ON_SET_LOCK_RESULT(self._on_set_lock_result)
        self.onRemoveLockResult = ON_REMOVE_LOCK_RESULT(self._on_remove_lock_result)
        self.onReleaseLockResult = ON_RELEASE_LOCK_RESULT(self._on_release_lock_result)
        self.onAcquireLockResult = ON_ACQUIRE_LOCK_RESULT(self._on_acquire_lock_result)
        self.onRevokeLockResult = ON_REVOKE_LOCK_RESULT(self._on_revoke_lock_result)
        self.onGetLocksResult = ON_GET_LOCKS_RESULT(self._on_get_locks_result)
        self.onWhoNowResult = ON_WHO_NOW_RESULT(self._on_who_now_result)
        self.onGetOnlineUsersResult = ON_GET_ONLINE_USERS_RESULT(self._on_get_online_users_result)
        self.onWhereNowResult = ON_WHERE_NOW_RESULT(self._on_where_now_result)
        self.onGetUserChannelsResult = ON_GET_USER_CHANNELS_RESULT(self._on_get_user_channels_result)
        self.onPresenceSetStateResult = ON_PRESENCE_SET_STATE_RESULT(self._on_presence_set_state_result)
        self.onPresenceRemoveStateResult = ON_PRESENCE_REMOVE_STATE_RESULT(self._on_presence_remove_state_result)
        self.onPresenceGetStateResult = ON_PRESENCE_GET_STATE_RESULT(self._on_presence_get_state_result)
        self.onLinkStateEvent = ON_LINK_STATE_EVENT(self._on_link_state_event)
        self.onGetHistoryMessagesResult = ON_GET_HISTORY_MESSAGES_RESULT(self._on_get_history_messages_result)
        self.onLogoutResult = ON_LOGOUT_RESULT(self._on_logout_result)
        self.onRenewTokenResult = ON_RENEW_TOKEN_RESULT(self._on_renew_token_result)
        self.onPublishTopicMessageResult = ON_PUBLISH_TOPIC_MESSAGE_RESULT(self._on_publish_topic_message_result)
        self.onUnsubscribeTopicResult = ON_UNSUBSCRIBE_TOPIC_RESULT(self._on_unsubscribe_topic_result)
        self.onGetSubscribedUserListResult = ON_GET_SUBSCRIBED_USER_LIST_RESULT(self._on_get_subscribed_user_list_result)
        self.onUnsubscribeUserMetadataResult = ON_UNSUBSCRIBE_USER_METADATA_RESULT(self._on_unsubscribe_user_metadata_result)
        self.userData = ctypes.c_void_p(id(event_handler))
    def _on_message_event(self, event_handle, message_event_ptr):
        message_event_inner = message_event_ptr.contents if message_event_ptr is not None else None
        if message_event_inner is not None and message_event_inner.get() is not None:
            message_event = message_event_inner.get()
            self.event_handler.on_message_event(message_event)
    def _on_presence_event(self, event_handle, presence_event_ptr):
        presence_event_inner = presence_event_ptr.contents if presence_event_ptr is not None else None
        if presence_event_inner is not None and presence_event_inner.get() is not None:
            presence_event = presence_event_inner.get()
            self.event_handler.on_presence_event(presence_event)
    def _on_topic_event(self, event_handle, topic_event_ptr):
        topic_event_inner = topic_event_ptr.contents if topic_event_ptr is not None else None
        if topic_event_inner is not None and topic_event_inner.get() is not None:
            topic_event = topic_event_inner.get()
            self.event_handler.on_topic_event(topic_event)
    def _on_lock_event(self, event_handle, lock_event_ptr):
        lock_event_inner = lock_event_ptr.contents if lock_event_ptr is not None else None
        if lock_event_inner is not None:
            lock_event = lock_event_inner.get()
            print(f"on_lock_event: {lock_event}")
            self.event_handler.on_lock_event(lock_event)
        else:
            print(f"on_lock_event: event is None")
            self.event_handler.on_lock_event(None)
    def _on_storage_event(self, event_handle, storage_event_ptr):
        storage_event_inner = storage_event_ptr.contents if storage_event_ptr is not None else None
        if storage_event_inner is not None:
            storage_event = storage_event_inner.get()
            print(f"on_storage_event: {storage_event}")
            self.event_handler.on_storage_event(storage_event)
        else:
            print(f"on_storage_event: event is None")
            self.event_handler.on_storage_event(None)
    def _on_join_result(self, event_handle, request_id, channel_name, user_id, error_code):
        print(f"on_join_result: request_id: {request_id}, channel_name: {channel_name}, user_id: {user_id}, error_code: {error_code}")
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        self.event_handler.on_join_result(request_id, str_channel_name, str_user_id, error_code)
    def _on_leave_result(self, event_handle, request_id, channel_name, user_id, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        self.event_handler.on_leave_result(request_id, str_channel_name, str_user_id, error_code)
    def _on_join_topic_result(self, event_handle, request_id, channel_name, user_id, topic, meta, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        str_meta = meta.decode('utf-8') if meta is not None else ""
        self.event_handler.on_join_topic_result(request_id, str_channel_name, str_user_id, str_topic, str_meta, error_code)
    def _on_leave_topic_result(self, event_handle, request_id, channel_name, user_id, topic, meta, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        str_meta = meta.decode('utf-8') if meta is not None else ""
        self.event_handler.on_leave_topic_result(request_id, str_channel_name, str_user_id, str_topic, str_meta, error_code)
    def _on_subscribe_topic_result(self, event_handle, request_id, channel_name, user_id, topic, succeed_users, failed_users, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        str_succeed_users = succeed_users.decode('utf-8') if succeed_users is not None else ""
        str_failed_users = failed_users.decode('utf-8') if failed_users is not None else ""
        self.event_handler.on_subscribe_topic_result(request_id, str_channel_name, str_user_id, str_topic, str_succeed_users, str_failed_users, error_code)
    def _on_connection_state_changed(self, event_handle, channel_name, state, reason):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        self.event_handler.on_connection_state_changed(str_channel_name, state, reason)
    def _on_token_privilege_will_expire(self, event_handle, channel_name):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        self.event_handler.on_token_privilege_will_expire(str_channel_name)

    def _on_subscribe_result(self, event_handle, request_id, channel_name, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        self.event_handler.on_subscribe_result(request_id, str_channel_name, error_code)
    def _on_unsubscribe_result(self, event_handle, request_id, channel_name, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        self.event_handler.on_unsubscribe_result(request_id, str_channel_name, error_code)
    def _on_publish_result(self, event_handle, request_id, error_code):
        print(f"on publish result: request_id {request_id}, {error_code}")
        self.event_handler.on_publish_result(request_id, error_code)
    def _on_login_result(self, event_handle, request_id, error_code):
        print(f"on login result:request_id {request_id}, {error_code}")
        self.event_handler.on_login_result(request_id, error_code)
    def _on_set_channel_metadata_result(self, event_handle, request_id, channel_name, channel_type, error_code):
        self.event_handler.on_set_channel_metadata_result(request_id, channel_name, channel_type, error_code)
    def _on_update_channel_metadata_result(self, event_handle, request_id, channel_name, channel_type, error_code):
        self.event_handler.on_update_channel_metadata_result(request_id, channel_name, channel_type, error_code)
    def _on_remove_channel_metadata_result(self, event_handle, request_id, channel_name, channel_type, error_code):   
        self.event_handler.on_remove_channel_metadata_result(request_id, channel_name, channel_type, error_code)
    def _on_get_channel_metadata_result(self, event_handle, request_id, channel_name, channel_type, meta, error_code):
        self.event_handler.on_get_channel_metadata_result(request_id, channel_name, channel_type, meta, error_code)
    def _on_set_user_metadata_result(self, event_handle, request_id, user_id, error_code):
        self.event_handler.on_set_user_metadata_result(request_id, user_id, error_code)
    def _on_update_user_metadata_result(self, event_handle, request_id, user_id, error_code):
        self.event_handler.on_update_user_metadata_result(request_id, user_id, error_code)
    def _on_remove_user_metadata_result(self, event_handle, request_id, user_id, error_code):
        self.event_handler.on_remove_user_metadata_result(request_id, user_id, error_code)
    def _on_get_user_metadata_result(self, event_handle, request_id, user_id, meta, error_code):
        self.event_handler.on_get_user_metadata_result(request_id, user_id, meta, error_code)
    def _on_subscribe_user_metadata_result(self, event_handle, request_id, user_id, error_code):
        self.event_handler.on_subscribe_user_metadata_result(request_id, user_id, error_code)
    def _on_set_lock_result(self, event_handle, request_id, channel_name, channel_type, lock_name, error_code):
        self.event_handler.on_set_lock_result(request_id, channel_name, channel_type, lock_name, error_code)
    def _on_remove_lock_result(self, event_handle, request_id, channel_name, channel_type, lock_name, error_code):
        self.event_handler.on_remove_lock_result(request_id, channel_name, channel_type, lock_name, error_code)
    def _on_release_lock_result(self, event_handle, request_id, channel_name, channel_type, lock_name, error_code):
        self.event_handler.on_release_lock_result(request_id, channel_name, channel_type, lock_name, error_code)
    def _on_acquire_lock_result(self, event_handle, request_id, channel_name, channel_type, lock_name, error_code, error_details):
        self.event_handler.on_acquire_lock_result(request_id, channel_name, channel_type, lock_name, error_code, error_details)
    def _on_revoke_lock_result(self, event_handle, request_id, channel_name, channel_type, lock_name, error_code):
        self.event_handler.on_revoke_lock_result(request_id, channel_name, channel_type, lock_name, error_code)
    def _on_get_locks_result(self, event_handle, request_id, channel_name, channel_type, lock_detail_list, count, error_code):
        self.event_handler.on_get_locks_result(request_id, channel_name, channel_type, lock_detail_list, count, error_code)
    def _on_who_now_result(self, event_handle, request_id, user_state_list, count, next_page, error_code):
        self.event_handler.on_who_now_result(request_id, user_state_list, next_page, error_code)
    def _on_get_online_users_result(self, event_handle, request_id, user_state_list, count, next_page, error_code):
        self.event_handler.on_get_online_users_result(request_id, user_state_list, next_page, error_code)
    def _on_where_now_result(self, event_handle, request_id, channels, count, error_code):
        self.event_handler.on_where_now_result(request_id, channels, count, error_code)
    def _on_get_user_channels_result(self, event_handle, request_id, channels, count, error_code):
        self.event_handler.on_get_user_channels_result(request_id, channels, count, error_code)
    def _on_presence_set_state_result(self, event_handle, request_id, error_code):
        self.event_handler.on_presence_set_state_result(request_id, error_code)
    def _on_presence_remove_state_result(self, event_handle, request_id, error_code):
        self.event_handler.on_presence_remove_state_result(request_id, error_code)
    def _on_presence_get_state_result(self, event_handle, request_id, state, error_code):
        self.event_handler.on_presence_get_state_result(request_id, state, error_code)
    def _on_link_state_event(self, event_handle, link_state_event_ptr):
        #convert link_state_event_ptr to LinkStateEvent
        #print(f"on_link_state_event: {link_state_event_ptr}")
        event_inner = link_state_event_ptr.contents if link_state_event_ptr is not None else None
        if event_inner is not None and event_inner.get() is not None:
            link_state_event = event_inner.get()
            #print(f"on_link_state_event: {link_state_event}")
            self.event_handler.on_link_state_event(link_state_event)
        else:
            #print(f"on_link_state_event: event is None")
            self.event_handler.on_link_state_event(None)
    def _on_get_history_messages_result(self, event_handle, request_id, history_messages, count, new_start, error_code):
        history_messages_inner = history_messages.contents if history_messages is not None else None
        if history_messages_inner is not None:
            history_messages_list = []
            for i in range(count):
                history_message_inner = history_messages_inner.historyMessages[i].contents if history_messages_inner.historyMessages[i] is not None else None
                if history_message_inner is not None:
                    history_message = history_message_inner.get()
                    history_messages_list.append(history_message)
            self.event_handler.on_get_history_messages_result(request_id, history_messages_list, count, new_start, error_code)
        else:
            self.event_handler.on_get_history_messages_result(request_id, [], count, new_start, error_code)
    def _on_logout_result(self, event_handle, request_id, error_code):
        print(f"on logout result: request_id {request_id}, {error_code}")
        self.event_handler.on_logout_result(request_id, error_code)
    def _on_renew_token_result(self, event_handle, request_id, server_type, channel_name, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        self.event_handler.on_renew_token_result(request_id, server_type, str_channel_name, error_code)
    def _on_publish_topic_message_result(self, event_handle, request_id, channel_name, topic, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        self.event_handler.on_publish_topic_message_result(request_id, str_channel_name, str_topic, error_code)
    def _on_unsubscribe_topic_result(self, event_handle, request_id, channel_name, topic, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        self.event_handler.on_unsubscribe_topic_result(request_id, str_channel_name, str_topic, error_code)
    def _on_get_subscribed_user_list_result(self, event_handle, request_id, channel_name, topic, users, error_code):
        str_channel_name = channel_name.decode('utf-8') if channel_name is not None else ""
        str_topic = topic.decode('utf-8') if topic is not None else ""
        user_list_inner = users.contents if users is not None else None
        user_list = []
        if user_list_inner is not None:
            for i in range(user_list_inner.count):
                user_id = user_list_inner.userIds[i].decode('utf-8') if user_list_inner.userIds[i] is not None else ""
                user_list.append(user_id)
        self.event_handler.on_get_subscribed_user_list_result(request_id, str_channel_name, str_topic, user_list, error_code)
    def _on_unsubscribe_user_metadata_result(self, event_handle, request_id, user_id, error_code):
        str_user_id = user_id.decode('utf-8') if user_id is not None else ""
        self.event_handler.on_unsubscribe_user_metadata_result(request_id, str_user_id, error_code)
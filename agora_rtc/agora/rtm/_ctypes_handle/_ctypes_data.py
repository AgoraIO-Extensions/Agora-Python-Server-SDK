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
            server=config.server.encode(),
            port=config.port,
            account=config.account.encode(),
            password=config.password.encode()
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
    def create(config: RtmEncryptionConfig) -> 'RtmEncryptionConfigInner':
        return RtmEncryptionConfigInner(
            encryptionMode=config.encryption_mode,
            encryptionKey=config.encryption_key.encode(),
            encryptionSalt=config.encryption_salt
        )

class RtmEncryptionConfigInner(ctypes.Structure):
    _fields_ = [    
        ("encryptionMode", ctypes.c_int),
        ("encryptionKey", ctypes.c_char_p),
        ("encryptionSalt", ctypes.c_uint8 * 32)
    ]
    @staticmethod
    def create(config: RtmEncryptionConfig) -> 'RtmEncryptionConfigInner':
        return RtmEncryptionConfigInner(
            encryptionMode=config.encryption_mode,
            encryptionKey=config.encryption_key.encode(),
            encryptionSalt=config.encryption_salt
        )

class RtmPrivateConfigInner(ctypes.Structure):
    _fields_ = [
        ("serviceType", ctypes.c_int),
        ("accessPointHosts", ctypes.c_char_p),
        ("accessPointHostsCount", ctypes.c_size_t)
    ]
    @staticmethod
    def create(config: RtmPrivateConfig) -> 'RtmPrivateConfigInner':
        return RtmPrivateConfigInner(
            serviceType=config.service_type,
            accessPointHosts=config.access_point_hosts.encode(),
            accessPointHostsCount=config.access_point_hosts_count
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
        return RtmConfigInner(
            appId=config.app_id.encode(),
            userId=config.user_id.encode(),
            areaCode=config.area_code,
            protocolType=config.protocol_type,
            presenceTimeout=config.presence_timeout,
            heartbeatInterval=config.heartbeat_interval,
            context=config.context,
            useStringUserId=config.use_string_user_id,
            multipath=config.multipath,
            ispPolicyEnabled=config.isp_policy_enabled,
            eventHandler=config.event_handler,
            logConfig=RtmLogConfigInner.create(config.log_config) if config.log_config else RtmLogConfigInner(),
            proxyConfig=RtmProxyConfigInner.create(config.proxy_config) if config.proxy_config else RtmProxyConfigInner(),
            encryptionConfig=RtmEncryptionConfigInner.create(config.encryption_config) if config.encryption_config else RtmEncryptionConfigInner(),
            privateConfig=RtmPrivateConfigInner.create(config.private_config) if config.private_config else RtmPrivateConfigInner()
        )
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
            customType=options.custom_type,
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
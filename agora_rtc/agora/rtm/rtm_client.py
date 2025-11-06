from dataclasses import dataclass
import time
import ctypes
from ._ctypes_handle._ctypes_data import *
from .rtm_base import *


import logging

from . import rtm_lib
logger = logging.getLogger(__name__)


agora_rtm_client_create = rtm_lib.agora_rtm_client_create
agora_rtm_client_create.restype = AGORA_HANDLE
agora_rtm_client_create.argtypes = [ctypes.POINTER(RtmConfigInner), ctypes.POINTER(ctypes.c_int)]

agora_rtm_client_release = rtm_lib.agora_rtm_client_release
agora_rtm_client_release.restype = AGORA_API_C_INT
agora_rtm_client_release.argtypes = [AGORA_HANDLE]

agora_rtm_client_login = rtm_lib.agora_rtm_client_login
agora_rtm_client_login.restype = AGORA_API_C_INT
agora_rtm_client_login.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

agora_rtm_client_logout = rtm_lib.agora_rtm_client_logout
agora_rtm_client_logout.restype = AGORA_API_C_INT
agora_rtm_client_logout.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_uint64)]

agora_rtm_client_renew_token = rtm_lib.agora_rtm_client_renew_token
agora_rtm_client_renew_token.restype = AGORA_API_C_INT
agora_rtm_client_renew_token.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

#int agora_rtm_client_publish(C_IRtmClient *this_, const char *channelName, const char *message, const size_t length, const struct C_PublishOptions *option, uint64_t *requestId);
agora_rtm_client_publish = rtm_lib.agora_rtm_client_publish
agora_rtm_client_publish.restype = AGORA_API_C_INT
agora_rtm_client_publish.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(PublishOptionsInner), ctypes.POINTER(ctypes.c_uint64)]

#int agora_rtm_client_subscribe(C_IRtmClient *this_, const char *channelName, const struct C_SubscribeOptions *options, uint64_t *requestId);
agora_rtm_client_subscribe = rtm_lib.agora_rtm_client_subscribe
agora_rtm_client_subscribe.restype = AGORA_API_C_INT
agora_rtm_client_subscribe.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(SubscribeOptionsInner), ctypes.POINTER(ctypes.c_uint64)]

#int agora_rtm_client_unsubscribe(C_IRtmClient *this_, const char *channelName, uint64_t *requestId);
agora_rtm_client_unsubscribe = rtm_lib.agora_rtm_client_unsubscribe
agora_rtm_client_unsubscribe.restype = AGORA_API_C_INT
agora_rtm_client_unsubscribe.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

agora_rtm_client_get_version = rtm_lib.agora_rtm_client_get_version
agora_rtm_client_get_version.restype = ctypes.c_char_p
agora_rtm_client_get_version.argtypes = [AGORA_HANDLE]

agora_rtm_client_get_error_reason = rtm_lib.agora_rtm_client_get_error_reason
agora_rtm_client_get_error_reason.restype = ctypes.c_char_p
agora_rtm_client_get_error_reason.argtypes = [ctypes.c_int]

def create_rtm_client(config: RtmConfig):
     return RTMClient(config)



class RTMClient:
    def __init__(self, config: RtmConfig) -> None:
        self.client_handle = None
        self.config = config
        self.is_valid = False
        #check config
        if config.log_config is None:
            config.log_config = RtmLogConfig(
                file_path="./logs/rtm.log",
                file_size_kb=1024,
                log_level=RtmLogLevel.RTM_LOG_LEVEL_INFO
            )
        if config.private_config is None:
            config.private_config = RtmPrivateConfig(
                service_type=RtmServiceType.RTM_SERVICE_TYPE_NONE,
                access_point_hosts=None,
            )
        if config.proxy_config is None:
            config.proxy_config = RtmProxyConfig(
                proxy_type=RtmProxyType.RTM_PROXY_TYPE_NONE,
                proxy_server="",
                proxy_port=0,
                proxy_username="",
                proxy_password=""
            )
        if config.encryption_config is None:
            config.encryption_config = RtmEncryptionConfig(
                encryption_mode=RtmEncryptionMode.RTM_ENCRYPTION_MODE_NONE,
                encryption_key=None,
                encryption_salt=None
            )
        # realy create client
        inner_log_config = RtmLogConfigInner.create(config.log_config)
        inner_private_config = RtmPrivateConfigInner.create(config.private_config)
        inner_proxy_config = RtmProxyConfigInner.create(config.proxy_config)
        inner_encryption_config = RtmEncryptionConfigInner.create(config.encryption_config)
        ret = ctypes.c_int(0)

        #register event handler from python to ctypes
        
        config_inner = RtmConfigInner.create(config)
        c_event_handler = RtmEventHandlerInner(config.event_handler, self)
        config_inner.eventHandler = ctypes.cast(ctypes.byref(c_event_handler), ctypes.c_void_p)
        self.client_handle = agora_rtm_client_create(ctypes.byref(config_inner), ctypes.byref(ret))
        print(f"create_rtm_client ret: {ret.value}, client_handle: {self.client_handle}")
        print(f"error reason: {self.get_error_reason(ret.value)}")
        self.is_valid = self.client_handle is not None and ret.value == 0
    def _is_valid(self)->bool:
        return self.is_valid
       
        
    def release(self):
        if self.client_handle:
            ret = agora_rtm_client_release(self.client_handle)
            if ret == 0:
                self.client_handle = None
                self.config = None
    def login(self, token: str)->(int, int):
        #convert from str to c_char_p without memory copy
        bytes_data = token.encode('utf-8')
        c_data = ctypes.c_char_p(bytes_data)
        request_id = ctypes.c_uint64(0)
        ret = agora_rtm_client_login(self.client_handle, c_data, ctypes.byref(request_id))
        return ret, int(request_id.value)
       
    def logout(self)->(int, int):
        request_id = ctypes.c_uint64(0)
        ret = agora_rtm_client_logout(self.client_handle, ctypes.byref(request_id))
        return ret, int(request_id.value)
    def renew_token(self, token: str)->(int, int):
        request_id = ctypes.c_uint64(0)
        ret = agora_rtm_client_renew_token(self.client_handle, token.encode(), ctypes.byref(request_id))
        return ret, int(request_id.value)
    def publish(self, channel_name: str, message: str, options: PublishOptions) ->(int, uint64_t):
        inner_options = PublishOptionsInner.create(options)
        request_id = ctypes.c_uint64(0) 
        ret = agora_rtm_client_publish(self.client_handle, channel_name.encode(), message.encode(), len(message), ctypes.byref(inner_options), ctypes.byref(request_id))
        return ret, int(request_id.value)
     
    def send_channel_message(self, channel_name: str, message: str) ->(int, uint64_t):
        publish_options = PublishOptions(
            channel_type=RtmChannelType.RTM_CHANNEL_TYPE_MESSAGE,
            message_type=RtmMessageType.RTM_MESSAGE_TYPE_BINARY,
            custom_type="",
            store_in_history=False
        )
        ret, request_id = self.publish(channel_name, message, publish_options)
        return ret, request_id
    def send_user_message(self, user_id: str, message: str) ->(int, uint64_t):
        publish_options = PublishOptions(
            channel_type=RtmChannelType.RTM_CHANNEL_TYPE_USER,
            message_type=RtmMessageType.RTM_MESSAGE_TYPE_BINARY,
            custom_type="",
            store_in_history=False
        )
        ret, request_id = self.publish(user_id, message, publish_options)
        return ret, request_id
    def subscribe(self, channel_name: str, options: SubscribeOptions) ->(int, uint64_t):
        inner_options = SubscribeOptionsInner.create(options)
        request_id = ctypes.c_uint64(0) 
        ret = agora_rtm_client_subscribe(self.client_handle, channel_name.encode(), ctypes.byref(inner_options), ctypes.byref(request_id))
        return ret, int(request_id.value)
       
    def unsubscribe(self, channel_name: str)->(int, uint64_t):
        request_id = ctypes.c_uint64(0)
        ret = agora_rtm_client_unsubscribe(self.client_handle, channel_name.encode(), ctypes.byref(request_id))
        return ret, int(request_id.value)

    
    def get_version(self)->str:
        ret = agora_rtm_client_get_version(self.client_handle)
        return ret.decode('utf-8')
    def get_error_reason(self, error_code: int)->str:
        ret = agora_rtm_client_get_error_reason(error_code)
        if ret is None:
            return ""
        return ret.decode('utf-8')
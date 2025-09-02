
import ctypes
from ..agora_base import *
from ..local_user import *
from .._utils.globals import *
from ..rtc_connection_observer import *
import logging
logger = logging.getLogger(__name__)


ON_CONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_DISCONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_CONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_RECONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_RECONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)

ON_CONNECTION_LOST_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner))
ON_LASTMILE_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_LASTMILE_PROBE_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LastmileProbeResultInner))
ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p)
ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE)

ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_CONNECTION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_USER_JOINED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t)
ON_USER_LEFT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)
ON_TRANSPORT_STATS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCStatsInner))

ON_CHANGE_ROLE_SUCCESS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_CHANGE_ROLE_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)
ON_USER_NETWORK_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int)
ON_NETWORK_TYPE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_API_CALL_EXECUTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)

ON_CONTENT_INSPECT_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_SNAPSHOT_TAKEN_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, uid_t, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p)
ON_WARNING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p)
ON_CHANNEL_MEDIA_RELAY_STATE_CHANGED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int, ctypes.c_int)

ON_LOCAL_USER_REGISTERED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, uid_t, ctypes.c_char_p)
ON_USER_ACCOUNT_UPDATED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, uid_t, ctypes.c_char_p)
ON_STREAM_MESSAGE_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
ON_ENCRYPTION_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_UPLOAD_LOG_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)

ON_ENCRYPTION_ERROR_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)  
ON_CAPABILITIES_CHANGED_CALLBACK = ctypes.CFUNCTYPE(
    None,  # return type
    AGORA_HANDLE,  # agora_capabilities_observer
    ctypes.POINTER(CapabilitiesInner),  # caps
    ctypes.c_int  # size
) 

class RTCConnectionObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_connected", ON_CONNECTED_CALLBACK),
        ("on_disconnected", ON_DISCONNECTED_CALLBACK),
        ("on_connecting", ON_CONNECTING_CALLBACK),
        ("on_reconnecting", ON_RECONNECTING_CALLBACK),
        ("on_reconnected", ON_RECONNECTED_CALLBACK),

        ("on_connection_lost", ON_CONNECTION_LOST_CALLBACK),
        ("on_lastmile_quality", ON_LASTMILE_QUALITY_CALLBACK),
        ("on_lastmile_probe_result", ON_LASTMILE_PROBE_RESULT_CALLBACK),
        ("on_token_privilege_will_expire", ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK),
        ("on_token_privilege_did_expire", ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK),

        ("on_connection_license_validation_failure", ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK),
        ("on_connection_failure", ON_CONNECTION_FAILURE_CALLBACK),
        ("on_user_joined", ON_USER_JOINED_CALLBACK),
        ("on_user_left", ON_USER_LEFT_CALLBACK),
        ("on_transport_stats", ON_TRANSPORT_STATS_CALLBACK),

        ("on_change_role_success", ON_CHANGE_ROLE_SUCCESS_CALLBACK),
        ("on_change_role_failure", ON_CHANGE_ROLE_FAILURE_CALLBACK),
        ("on_user_network_quality", ON_USER_NETWORK_QUALITY_CALLBACK),
        ("on_network_type_changed", ON_NETWORK_TYPE_CHANGED_CALLBACK),
        ("on_api_call_executed", ON_API_CALL_EXECUTED_CALLBACK),

        ("on_content_inspect_result", ON_CONTENT_INSPECT_RESULT_CALLBACK),
        ("on_snapshot_taken", ON_SNAPSHOT_TAKEN_CALLBACK),
        ("on_error", ON_ERROR_CALLBACK),
        ("on_warning", ON_WARNING_CALLBACK),
        ("on_channel_media_relay_state_changed", ON_CHANNEL_MEDIA_RELAY_STATE_CHANGED_CALLBACK),

        ("on_local_user_registered", ON_LOCAL_USER_REGISTERED_CALLBACK),
        ("on_user_account_updated", ON_USER_ACCOUNT_UPDATED_CALLBACK),
        ("on_stream_message_error", ON_STREAM_MESSAGE_ERROR_CALLBACK),
        ("on_encryption_error", ON_ENCRYPTION_ERROR_CALLBACK),
        ("on_upload_log_result", ON_UPLOAD_LOG_RESULT_CALLBACK),
        ("on_encryption_error", ON_ENCRYPTION_ERROR_CALLBACK)
    ]

    def __init__(self, conn_observer: IRTCConnectionObserver, connection: 'RTCConnection') -> None:
        from ..rtc_connection import RTCConnection  # Moved import here to avoid circular import
        self.conn_observer = conn_observer
        self.conn = connection
        self.on_connected = ON_CONNECTED_CALLBACK(self._on_connected)
        self.on_disconnected = ON_DISCONNECTED_CALLBACK(self._on_disconnected)
        self.on_connecting = ON_CONNECTING_CALLBACK(self._on_connecting)
        self.on_reconnecting = ON_RECONNECTING_CALLBACK(self._on_reconnecting)
        self.on_reconnected = ON_RECONNECTED_CALLBACK(self._on_reconnected)
        self.on_connection_lost = ON_CONNECTION_LOST_CALLBACK(self._on_connection_lost)
        self.on_lastmile_quality = ON_LASTMILE_QUALITY_CALLBACK(self._on_lastmile_quality)
        self.on_lastmile_probe_result = ON_LASTMILE_PROBE_RESULT_CALLBACK(self._on_lastmile_probe_result)
        self.on_token_privilege_will_expire = ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK(self._on_token_privilege_will_expire)
        self.on_token_privilege_did_expire = ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK(self._on_token_privilege_did_expire)
        self.on_connection_license_validation_failure = ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK(self._on_connection_license_validation_failure)
        self.on_connection_failure = ON_CONNECTION_FAILURE_CALLBACK(self._on_connection_failure)
        self.on_user_joined = ON_USER_JOINED_CALLBACK(self._on_user_joined)
        self.on_user_left = ON_USER_LEFT_CALLBACK(self._on_user_left)
        self.on_transport_stats = ON_TRANSPORT_STATS_CALLBACK(self._on_transport_stats)
        self.on_change_role_success = ON_CHANGE_ROLE_SUCCESS_CALLBACK(self._on_change_role_success)
        self.on_change_role_failure = ON_CHANGE_ROLE_FAILURE_CALLBACK(self._on_change_role_failure)
        self.on_user_network_quality = ON_USER_NETWORK_QUALITY_CALLBACK(self._on_user_network_quality)
        self.on_network_type_changed = ON_NETWORK_TYPE_CHANGED_CALLBACK(self._on_network_type_changed)
        self.on_api_call_executed = ON_API_CALL_EXECUTED_CALLBACK(self._on_api_call_executed)
        self.on_content_inspect_result = ON_CONTENT_INSPECT_RESULT_CALLBACK(self._on_content_inspect_result)
        self.on_snapshot_taken = ON_SNAPSHOT_TAKEN_CALLBACK(self._on_snapshot_taken)
        self.on_error = ON_ERROR_CALLBACK(self._on_error)
        self.on_warning = ON_WARNING_CALLBACK(self._on_warning)
        self.on_channel_media_relay_state_changed = ON_CHANNEL_MEDIA_RELAY_STATE_CHANGED_CALLBACK(self._on_channel_media_relay_state_changed)
        self.on_local_user_registered = ON_LOCAL_USER_REGISTERED_CALLBACK(self._on_local_user_registered)
        self.on_user_account_updated = ON_USER_ACCOUNT_UPDATED_CALLBACK(self._on_user_account_updated)
        self.on_stream_message_error = ON_STREAM_MESSAGE_ERROR_CALLBACK(self._on_stream_message_error)
        self.on_encryption_error = ON_ENCRYPTION_ERROR_CALLBACK(self._on_encryption_error)
        self.on_upload_log_result = ON_UPLOAD_LOG_RESULT_CALLBACK(self._on_upload_log_result)
        self.on_encryption_error = ON_ENCRYPTION_ERROR_CALLBACK(self._on_encryption_error)

    def _on_connected(self, agora_rtc_conn, conn_info_inner, reason):
        logger.debug(f"ConnCB _on_connected: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_connected(self.conn, conn_info, reason)

    def _on_disconnected(self, agora_rtc_conn, conn_info_inner, reason):
        logger.debug(f"ConnCB _on_disconnected: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_disconnected(self.conn, conn_info, reason)

    def _on_connecting(self, agora_rtc_conn, conn_info_inner: ctypes.POINTER(RTCConnInfoInner), reason):
        logger.debug(f"ConnCB _on_connecting: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        # conn_info = conn_info_inner.contents.get()
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_connecting(self.conn, conn_info, reason)

    def _on_reconnecting(self, agora_rtc_conn, conn_info_inner, reason):
        logger.debug(f"ConnCB _on_reconnecting: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_reconnecting(self.conn, conn_info, reason)

    def _on_reconnected(self, agora_rtc_conn, conn_info_inner, reason):
        logger.debug(f"ConnCB _on_reconnected: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_reconnected(self.conn, conn_info, reason)

    def _on_connection_lost(self, agora_rtc_conn, conn_info_inner):
        logger.debug(f"ConnCB _on_connection_lost: {agora_rtc_conn}, {conn_info_inner}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_connection_lost(self.conn, conn_info)

    def _on_lastmile_quality(self, agora_rtc_conn, quality):
        logger.debug(f"ConnCB _on_lastmile_quality: {agora_rtc_conn}, {quality}")
        self.conn_observer.on_lastmile_quality(self.conn, quality)

    def _on_lastmile_probe_result(self, agora_rtc_conn, last_mile_prob_result_ptr):
        logger.debug(f"ConnCB _on_lastmile_probe_result: {agora_rtc_conn}, {last_mile_prob_result_ptr}")
        last_mile_result = last_mile_prob_result_ptr.contents
        self.conn_observer.on_lastmile_probe_result(self.conn, last_mile_result)

    def _on_token_privilege_will_expire(self, agora_rtc_conn, token):
        logger.debug(f"ConnCB _on_token_privilege_will_expire: {agora_rtc_conn}, {token}")
        token_str = token.decode('utf-8')  # decode will generate a new object
        self.conn_observer.on_token_privilege_will_expire(self.conn, token_str)

    def _on_token_privilege_did_expire(self, agora_rtc_conn):
        logger.debug(f"ConnCB _on_token_privilege_did_expire: {agora_rtc_conn}")
        self.conn_observer.on_token_privilege_did_expire(self.conn)

    def _on_connection_license_validation_failure(self, agora_rtc_conn, reason):
        logger.debug(f"ConnCB _on_connection_license_validation_failure: {agora_rtc_conn}, {reason}")
        self.conn_observer.on_connection_license_validation_failure(self.conn, reason)

    def _on_connection_failure(self, agora_rtc_conn, conn_info_inner, reason):
        logger.debug(f"ConnCB _on_connection_failure: {agora_rtc_conn}, {conn_info_inner}, {reason}")
        conn_info = conn_info_inner.contents.get()
        self.conn_observer.on_connection_failure(self.conn, conn_info, reason)

    def _on_user_joined(self, agora_rtc_conn, user_id):
        logger.debug(f"ConnCB _on_user_joined: {agora_rtc_conn}, {user_id}")
        userid_str = user_id.decode('utf-8')
        self.conn_observer.on_user_joined(self.conn, userid_str)

    def _on_user_left(self, agora_rtc_conn, user_id, reason):
        logger.debug(f"ConnCB _on_user_left: {agora_rtc_conn}, {user_id}, {reason}")
        userid_str = user_id.decode('utf-8')
        self.conn_observer.on_user_left(self.conn, userid_str, reason)

    def _on_transport_stats(self, agora_rtc_conn, stats):
        logger.debug(f"ConnCB _on_transport_stats: {agora_rtc_conn}, {stats}")
        rtc_stats = stats.contents
        self.conn_observer.on_transport_stats(self.conn, rtc_stats)

    def _on_change_role_success(self, agora_rtc_conn, old_role, new_role):
        logger.debug(f"ConnCB _on_change_role_success: {agora_rtc_conn}, {old_role}, {new_role}")
        self.conn_observer.on_change_role_success(self.conn, old_role, new_role)

    def _on_change_role_failure(self, agora_rtc_conn, reason, cur_role):
        logger.debug(f"ConnCB _on_change_role_failure: {agora_rtc_conn}, {reason}, {cur_role}")
        self.conn_observer.on_change_role_failure(self.conn, reason, cur_role)

    def _on_user_network_quality(self, agora_rtc_conn, user_id, tx_quality, rx_quality):
        logger.debug(f"ConnCB _on_user_network_quality: {agora_rtc_conn}, {user_id}, {tx_quality}, {rx_quality}")
        userid_str = user_id.decode('utf-8') if user_id else ""
        self.conn_observer.on_user_network_quality(self.conn, userid_str, tx_quality, rx_quality)

    def _on_network_type_changed(self, agora_rtc_conn, network_type):
        logger.debug(f"ConnCB _on_network_type_changed: {agora_rtc_conn}, {network_type}")
        self.conn_observer.on_network_type_changed(self.conn, network_type)

    def _on_api_call_executed(self, agora_rtc_conn, error, api_type, api_params):
        logger.debug(f"ConnCB _on_api_call_executed: {agora_rtc_conn}, {error}, {api_type}, {api_params}")
        _api_type_str = api_type.decode('utf-8') if api_type else ""
        _api_param_str = api_params.decode('utf-8') if api_params else ""
        self.conn_observer.on_api_call_executed(self.conn, error, _api_type_str, _api_param_str)

    def _on_content_inspect_result(self, agora_rtc_conn, result):
        logger.debug(f"ConnCB _on_content_inspect_result: {agora_rtc_conn}, {result}")
        self.conn_observer.on_content_inspect_result(self.conn, result)

    def _on_snapshot_taken(self, agora_rtc_conn, channel, uid, filepath, width, height, errCode):
        logger.debug(f"ConnCB _on_snapshot_taken: {agora_rtc_conn}, {channel}, {uid}, {filepath}, {width}, {height}, {errCode}")
        _channel_str = channel.decode('utf-8') if channel else ""
        _file_path_str = filepath.decode('utf-8') if filepath else ""
        self.conn_observer.on_snapshot_taken(self.conn, _channel_str, uid, _file_path_str, width, height, errCode)

    def _on_error(self, agora_rtc_conn, error_code, error_msg):
        logger.debug(f"ConnCB _on_error: {agora_rtc_conn}, {error_code}, {error_msg}")
        _error_msg_str = error_msg.decode('utf-8') if error_msg else ""
        self.conn_observer.on_error(self.conn, error_code, _error_msg_str)

    def _on_warning(self, agora_rtc_conn, warn_code, warn_msg):
        logger.debug(f"ConnCB _on_warning: {agora_rtc_conn}, {warn_code}, {warn_msg}")
        _warn_msg_str = warn_msg.decode('utf-8') if warn_msg else ""
        self.conn_observer.on_warning(self.conn, warn_code, _warn_msg_str)

    def _on_channel_media_relay_state_changed(self, agora_rtc_conn, state, code):
        logger.debug(f"ConnCB _on_channel_media_relay_state_changed: {agora_rtc_conn}, {state}, {code}")
        self.conn_observer.on_channel_media_relay_state_changed(self.conn, state, code)

    def _on_local_user_registered(self, agora_rtc_conn, uid, user_account):
        logger.debug(f"ConnCB _on_local_user_registered: {agora_rtc_conn}, {uid}, {user_account}")
        # uid: ctype.int, user_account: ctype.c_char_p
        _user_account_str = user_account.decode('utf-8') if user_account else ""
        self.conn_observer.on_local_user_registered(self.conn, uid, _user_account_str)

    def _on_user_account_updated(self, agora_rtc_conn, uid, user_account):
        logger.debug(f"ConnCB _on_user_account_updated: {agora_rtc_conn}, {uid}, {user_account}")
        _user_account_str = user_account.decode('utf-8') if user_account else ""
        self.conn_observer.on_user_account_updated(self.conn, uid, _user_account_str)

    def _on_stream_message_error(self, agora_rtc_conn, user_id, stream_id, code, missed, cached):
        logger.debug(f"ConnCB _on_stream_message_error: {agora_rtc_conn}, {user_id}, {stream_id}, {code}, {missed}, {cached}")
        _user_id_str = user_id.decode('utf-8') if user_id else ""
        self.conn_observer.on_stream_message_error(self.conn, _user_id_str, stream_id, code, missed, cached)

    def _on_encryption_error(self, agora_rtc_conn, error_type):
        logger.debug(f"ConnCB _on_encryption_error: {agora_rtc_conn}, {error_type}")
        self.conn_observer.on_encryption_error(self.conn, error_type)

    def _on_upload_log_result(self, agora_rtc_conn, request_id, success, reason):
        logger.debug(f"ConnCB _on_upload_log_result: {agora_rtc_conn}, {request_id}, {success}, {reason}")
        _request_id_str = request_id.decode("utf-8") if request_id else ""
        self.conn_observer.on_upload_log_result(self.conn, _request_id_str, success, reason)

    def _on_encryption_error(self, agora_rtc_conn, error_type):
        logger.debug(f"ConnCB _on_encryption_error: {agora_rtc_conn}, {error_type}")
        self.conn_observer.on_encryption_error(self.conn, error_type)



class CapabilitiesObserverInner(ctypes.Structure):
    _fields_ = [
        ("on_capabilities_changed", ON_CAPABILITIES_CHANGED_CALLBACK)
    ]
    def __init__(self, conn:'RtcConnection'):
        self.conn = conn
        self.on_capabilities_changed = ON_CAPABILITIES_CHANGED_CALLBACK(self._on_capabilities_changed)
        
    def _on_capabilities_changed(self, agora_capabilities_observer, ptr_caps_inner, size):
        print(f"ConnCB _on_capabilities_changed: {agora_capabilities_observer}, {ptr_caps_inner}, {size}")
        
        # 正确解析C指针数组
        # 方法1: 使用ctypes.cast将指针转换为数组
        caps_list = []
        for i in range(size):
            cur_ptr = ptr_caps_inner[i]
            cur_cap = cur_ptr.get()
            caps_list.append(cur_cap)
        self.conn._on_capabilities_changed(caps_list)
        
        
        # 方法2: 直接使用指针算术（更安全的方式）
        # caps_list = []
        # for i in range(size.value):
        #     cap_ptr = ctypes.pointer(ptr_caps_inner.contents)
        #     cap_ptr = ctypes.cast(cap_ptr, ctypes.POINTER(ctypes.c_void_p))
        #     cap_ptr.value = ctypes.addressof(ptr_caps_inner.contents) + i * ctypes.sizeof(CapabilitiesInner)
        #     cap_ptr = ctypes.cast(cap_ptr, ctypes.POINTER(CapabilitiesInner))
        #     cap_inner = cap_ptr.contents
        #     cap = cap_inner.get()
        #     caps_list.append(cap)
        
        # 调用回调函数


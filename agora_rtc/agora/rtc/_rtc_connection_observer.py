
import ctypes
from .agora_base import *
from .local_user import *
from .globals import *
# from  .rtc_connection import *
from .rtc_connection_observer import *

class RTCConnInfoInner(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint64),
        ("channel_id", ctypes.c_char_p),
        ("state", ctypes.c_int),
        ("local_user_id", ctypes.c_char_p),
        ("internal_uid", ctypes.c_uint)
    ]
    def _convert_to_rtc_conn_info(self):
        from .rtc_connection import RTCConnInfo
        con_info = RTCConnInfo()

        # 直接访问字段
        con_info.id = self.id
        con_info.channel_id = self.channel_id.decode('utf-8') if self.channel_id else ''
        con_info.state = self.state
        con_info.local_user_id = self.local_user_id.decode('utf-8') if self.local_user_id else ''
        con_info.internal_uid = self.internal_uid

        return con_info
    
    

uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

ON_CONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_DISCONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_CONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_RECONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_RECONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)

ON_CONNECTION_LOST_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner))
ON_LASTMILE_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_LASTMILE_PROBE_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LastmileProbeResult))
ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p)
ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE)

ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_CONNECTION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfoInner), ctypes.c_int)
ON_USER_JOINED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t)
ON_USER_LEFT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, user_id_t, ctypes.c_int)
ON_TRANSPORT_STATS_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCStats))

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
        ("on_upload_log_result", ON_UPLOAD_LOG_RESULT_CALLBACK)
    ]

    def __init__(self, conn_observer:IRTCConnectionObserver, connection: 'RTCConnection') -> None:
        from .rtc_connection import RTCConnection  # Moved import here to avoid circular import
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


        #agora_rtc_conn： handle of RTCConnection; conn_info_inner:pointer to RTCConnInfoInner 
        #reason: int type
        #
        """
        parameter type desp:
        agora_rtc_conn： handle of RTCConnection; 
        conn_info_inner:pointer to RTCConnInfoInner 
        reason: int type
        quality:int type

        # note: sumary for ctypes.POINTER
        #note: conn_info_inner is a pointer to RTCConnInfoInner, so we should do like following to ensure
        # conn_info is a RTCConnInfo
        # we make sure: conn_info_inner is a pointer to RTCConnInfoInner from ctypes, so 
        # no need to do type check like isinstance(xx),just use dereferencing method to get the contents
        if isinstance(conn_info_inner, ctypes.POINTER(RTCConnInfoInner)):
            conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        else:
            conn_info = conn_info_inner._convert_to_rtc_conn_info()

        just use: 
        conn_info = conn_info_inner.contents.()
        
        to 
        """
    def _on_connected(self, agora_rtc_conn, conn_info_inner, reason):
        print("ConnCB _on_connected:", agora_rtc_conn, conn_info_inner, reason)
       
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_connected(self.conn, conn_info, reason)

    def _on_disconnected(self, agora_rtc_conn, conn_info_inner, reason):
        #print("ConnCB _on_disconnected:", agora_rtc_conn, conn_info_inner, reason)
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_disconnected(self.conn, conn_info, reason)

    def _on_connecting(self, agora_rtc_conn, conn_info_inner, reason):
        #print("ConnCB _on_connecting:", agora_rtc_conn, conn_info_inner, reason)
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_connecting(self.conn, conn_info, reason)

    def _on_reconnecting(self, agora_rtc_conn, conn_info_inner, reason):
        #print("ConnCB _on_reconnecting:", agora_rtc_conn, conn_info_inner, reason)
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_reconnecting(self.conn, conn_info, reason)

    def _on_reconnected(self, agora_rtc_conn, conn_info_inner, reason):
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_reconnected(self.conn, conn_info, reason)

    def _on_connection_lost(self, agora_rtc_conn, conn_info_inner):
        #print("ConnCB _on_connection_lost:", agora_rtc_conn, conn_info_inner)
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_connection_lost(self.conn, conn_info)

    def _on_lastmile_quality(self, agora_rtc_conn, quality):
        #print("ConnCB _on_lastmile_quality:", agora_rtc_conn, quality)
        self.conn_observer.on_lastmile_quality(self.conn, quality)

    #last_mile_prob_result_ptr: ctypes.POINTER(LastmileProbeResult)) type
    def _on_lastmile_probe_result(self, agora_rtc_conn, last_mile_prob_result_ptr):
        #print("ConnCB _on_lastmile_probe_result:", agora_rtc_conn, last_mile_prob_result_ptr)
        # result is a pointer to LastmileProbeResult
        # we should dereference the pointer to get the LastmileProbeResult, thus we can access its fields
        last_mile_result = last_mile_prob_result_ptr.contents
        
        self.conn_observer.on_lastmile_probe_result(self.conn, last_mile_result)

    #token: ctypes.char_p
    def _on_token_privilege_will_expire(self, agora_rtc_conn, token):
        #print("ConnCB _on_token_privilege_will_expire:", agora_rtc_conn, token)
        token_str = token.decode('utf-8') #decode will generate a new object
        self.conn_observer.on_token_privilege_will_expire(self.conn, token_str)

    def _on_token_privilege_did_expire(self, agora_rtc_conn):
        #print("ConnCB _on_token_privilege_did_expire:", agora_rtc_conn)
        self.conn_observer.on_token_privilege_did_expire(self.conn)

    def _on_connection_license_validation_failure(self, agora_rtc_conn, reason):
        #print("ConnCB _on_connection_license_validation_failure:", agora_rtc_conn, reason)
        self.conn_observer.on_connection_license_validation_failure(self.conn, reason)

    def _on_connection_failure(self, agora_rtc_conn, conn_info_inner, reason):
        #print("ConnCB _on_connection_failure:", agora_rtc_conn, conn_info_inner, reason)
        conn_info = conn_info_inner.contents._convert_to_rtc_conn_info()
        self.conn_observer.on_connection_failure(self.conn, conn_info, reason)
    #userid: ctyps.char_p   
    def _on_user_joined(self, agora_rtc_conn, user_id):
        print("ConnCB _on_user_joined:", agora_rtc_conn, user_id)
        userid_str = user_id.decode('utf-8')
        self.conn_observer.on_user_joined(self.conn, userid_str)

    def _on_user_left(self, agora_rtc_conn, user_id, reason):
        print("ConnCB _on_user_left:", agora_rtc_conn, user_id, reason)
        userid_str = user_id.decode('utf-8')
        self.conn_observer.on_user_left(self.conn, userid_str, reason)
    #stats: ctypes.POINTER(RTCStats)
    def _on_transport_stats(self, agora_rtc_conn, stats):
        #print("ConnCB _on_transport_stats:", agora_rtc_conn, stats)
        #stats is a pointer to RTCStats
        #should dereference the pointer to get the RTCStats, thus we can access its fields
        rtc_stats = stats.contents
        """
        if isinstance(stats, ctypes.POINTER(RTCStats)):
            rtc_stats = stats.contents
        else:
            rtc_stats = stats
        """
        
        self.conn_observer.on_transport_stats(self.conn, rtc_stats)
    #old_role/new_role: ctypes.int
    def _on_change_role_success(self, agora_rtc_conn, old_role, new_role):
        #print("ConnCB _on_change_role_success:", agora_rtc_conn, old_role, new_role)
        self.conn_observer.on_change_role_success(self.conn, old_role, new_role)

    def _on_change_role_failure(self, agora_rtc_conn, reason, cur_role):
        #print("ConnCB _on_change_role_failure:", agora_rtc_conn, reason, cur_role)
        self.conn_observer.on_change_role_failure(self.conn, reason, cur_role)

    def _on_user_network_quality(self, agora_rtc_conn, user_id, tx_quality, rx_quality):
        #print("ConnCB _on_user_network_quality:", agora_rtc_conn, user_id, tx_quality, rx_quality)
        #user_id: ctypes.char_p
        #tx_quality: ctypes.int
        #rx_quality: ctypes.int
        userid_str = user_id.decode('utf-8') if user_id else ""
        self.conn_observer.on_user_network_quality(self.conn, userid_str, tx_quality, rx_quality)

    def _on_network_type_changed(self, agora_rtc_conn, network_type):
        #print("ConnCB _on_network_type_changed:", agora_rtc_conn, network_type)
        #network_type: ctypes.int
        self.conn_observer.on_network_type_changed(self.conn, network_type)

    def _on_api_call_executed(self, agora_rtc_conn, error, api_type, api_params):
        #print("ConnCB _on_api_call_executed:", agora_rtc_conn, error, api_type, api_params)
        #error: ctypes.int; api_type: ctypes.char_p; api_params: ctypes.char_p
        _api_type_str = api_type.decode('utf-8') if api_type else ""
        _api_param_str = api_params.decode('utf-8') if api_params else ""
        self.conn_observer.on_api_call_executed(self.conn, error, _api_type_str, _api_param_str)

    def _on_content_inspect_result(self, agora_rtc_conn, result):
        #print("ConnCB _on_content_inspect_result:", agora_rtc_conn, result)
        #result: ctypes.int
        self.conn_observer.on_content_inspect_result(self.conn, result)

    def _on_snapshot_taken(self, agora_rtc_conn, channel, uid, filepath, width, height, errCode):
        #print("ConnCB _on_snapshot_taken:", agora_rtc_conn, channel, uid, filepath, width, height, errCode)
        #channel: ctypes.c_char_p; uid: ctypes.c_uint32; filepath: ctypes.c_char_p; width: ctypes.c_int32; height: ctypes.c_int32; errCode: ctypes.c_int32
        _channel_str = channel.decode('utf-8') if channel else ""
        _file_path_str = filepath.decode('utf-8') if filepath else ""
        self.conn_observer.on_snapshot_taken(self.conn, _channel_str, uid, _file_path_str, width, height, errCode)

    def _on_error(self, agora_rtc_conn, error_code, error_msg):
        #print("ConnCB _on_error:", agora_rtc_conn, error_code, error_msg)
        _error_msg_str = error_msg.decode('utf-8') if error_msg else ""
        self.conn_observer.on_error(self.conn, error_code, _error_msg_str)

    def _on_warning(self, agora_rtc_conn, warn_code, warn_msg):
        #print("ConnCB _on_warning:", agora_rtc_conn, warn_code, warn_msg)
        _warn_msg_str = warn_msg.decode('utf-8') if warn_msg else ""
        self.conn_observer.on_warning(self.conn, warn_code, _warn_msg_str)

    def _on_channel_media_relay_state_changed(self, agora_rtc_conn, state, code):
        #print("ConnCB _on_channel_media_relay_state_changed:", agora_rtc_conn, state, code)
        self.conn_observer.on_channel_media_relay_state_changed(self.conn, state, code)

    def _on_local_user_registered(self, agora_rtc_conn, uid, user_account):
        #print("ConnCB _on_local_user_registered:", agora_rtc_conn, uid, user_account)
        #uid: ctype.int, user_account: ctype.c_char_p
        _user_account_str = user_account.decode('utf-8') if user_account else ""
        self.conn_observer.on_local_user_registered(self.conn, uid, _user_account_str)

    def _on_user_account_updated(self, agora_rtc_conn, uid, user_account):
        #print("ConnCB _on_user_account_updated:", agora_rtc_conn, uid, user_account)
        _user_account_str = user_account.decode('utf-8') if user_account else ""
        self.conn_observer.on_user_account_updated(self.conn, uid, _user_account_str)

    def _on_stream_message_error(self, agora_rtc_conn, user_id, stream_id, code, missed, cached):
        print("ConnCB _on_stream_message_error:", agora_rtc_conn, user_id, stream_id, code, missed, cached)
        _user_id_str = user_id.decode('utf-8') if user_id else ""
        self.conn_observer.on_stream_message_error(self.conn, _user_id_str, stream_id, code, missed, cached)

    def _on_encryption_error(self, agora_rtc_conn, error_type):
        #print("ConnCB _on_encryption_error:", agora_rtc_conn, error_type)
        self.conn_observer.on_encryption_error(self.conn, error_type)

    #request_id: ctypes.c_char_p; success/reason: ctypes.int
    def _on_upload_log_result(self, agora_rtc_conn, request_id, success, reason):
        #print("ConnCB _on_upload_log_result:", agora_rtc_conn, request_id, success, reason)
        _request_id_str = request_id.decode("utf-8") if request_id else ""
        self.conn_observer.on_upload_log_result(self.conn, _request_id_str, success, reason)
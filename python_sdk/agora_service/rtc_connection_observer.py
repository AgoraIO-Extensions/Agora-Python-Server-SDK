import ctypes
from .agora_base import *
from .local_user import *

class RTCConnInfo(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint64),
        ("channel_id", ctypes.c_char_p),
        ("state", ctypes.c_int),
        ("local_user_id", ctypes.c_char_p),
        ("internal_uid", ctypes.c_uint)
    ]

user_id_t = ctypes.c_char_p
uid_t = ctypes.c_uint
track_id_t = ctypes.c_uint

ON_CONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_DISCONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_CONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_RECONNECTING_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
ON_RECONNECTED_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)

ON_CONNECTION_LOST_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo))
ON_LASTMILE_QUALITY_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_LASTMILE_PROBE_RESULT_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(LastmileProbeResult))
ON_TOKEN_PRIVILEGE_WILL_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_char_p)
ON_TOKEN_PRIVILEGE_DID_EXPIRE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE)

ON_CONNECTION_LICENSE_VALIDATION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.c_int)
ON_CONNECTION_FAILURE_CALLBACK = ctypes.CFUNCTYPE(None, AGORA_HANDLE, ctypes.POINTER(RTCConnInfo), ctypes.c_int)
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

class RTCConnectionObserver(ctypes.Structure):
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

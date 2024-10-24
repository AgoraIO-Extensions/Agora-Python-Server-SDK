import time
import ctypes
from .agora_base import *
from .local_user import LocalUser
from .rtc_connection_observer import IRTCConnectionObserver
from ._ctypes_handle._audio_frame_observer import AudioFrameObserverInner
from .agora_parameter import AgoraParameter
from ._utils.globals import AgoraHandleInstanceMap
from ._ctypes_handle._rtc_connection_observer import RTCConnectionObserverInner
from ._ctypes_handle._ctypes_data import *
import logging
logger = logging.getLogger(__name__)

agora_rtc_conn_get_local_user = agora_lib.agora_rtc_conn_get_local_user
agora_rtc_conn_get_local_user.restype = AGORA_HANDLE
agora_rtc_conn_get_local_user.argtypes = [AGORA_HANDLE]

agora_rtc_conn_connect = agora_lib.agora_rtc_conn_connect
agora_rtc_conn_connect.restype = AGORA_API_C_INT
agora_rtc_conn_connect.argtypes = [AGORA_HANDLE, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

agora_rtc_conn_disconnect = agora_lib.agora_rtc_conn_disconnect
agora_rtc_conn_disconnect.restype = AGORA_API_C_INT
agora_rtc_conn_disconnect.argtypes = [AGORA_HANDLE]

agora_rtc_conn_register_observer = agora_lib.agora_rtc_conn_register_observer
agora_rtc_conn_register_observer.restype = AGORA_API_C_INT
agora_rtc_conn_register_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(RTCConnectionObserverInner)]

agora_rtc_conn_unregister_observer = agora_lib.agora_rtc_conn_unregister_observer
agora_rtc_conn_unregister_observer.restype = AGORA_API_C_INT
agora_rtc_conn_unregister_observer.argtypes = [AGORA_HANDLE]

agora_rtc_conn_release = agora_lib.agora_rtc_conn_destroy
agora_rtc_conn_release.restype = AGORA_API_C_VOID
agora_rtc_conn_release.argtypes = [AGORA_HANDLE]

agora_rtc_conn_create_data_stream = agora_lib.agora_rtc_conn_create_data_stream
agora_rtc_conn_create_data_stream.restype = AGORA_API_C_INT
agora_rtc_conn_create_data_stream.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]

agora_rtc_conn_send_stream_message = agora_lib.agora_rtc_conn_send_stream_message
agora_rtc_conn_send_stream_message.restype = AGORA_API_C_INT
agora_rtc_conn_send_stream_message.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]

agora_rtc_conn_get_agora_parameter = agora_lib.agora_rtc_conn_get_agora_parameter
agora_rtc_conn_get_agora_parameter.restype = ctypes.c_void_p
agora_rtc_conn_get_agora_parameter.argtypes = [AGORA_HANDLE]

agora_rtc_conn_renew_token = agora_lib.agora_rtc_conn_renew_token
agora_rtc_conn_renew_token.restype = AGORA_API_C_INT
agora_rtc_conn_renew_token.argtypes = [AGORA_HANDLE, ctypes.c_char_p]


class RTCConnection:
    def __init__(self, conn_handle) -> None:
        self.conn_handle = conn_handle
        self.con_observer = None
        self.local_user = None
        self.local_user_handle = agora_rtc_conn_get_local_user(conn_handle)
        if self.local_user_handle:
            self.local_user = LocalUser(self.local_user_handle, self)
        # add to map
        AgoraHandleInstanceMap().set_local_user_map(self.conn_handle, self)
        AgoraHandleInstanceMap().set_con_map(self.conn_handle, self)

    #
    def connect(self, token: str, chan_id: str, user_id: str) -> int:
        ret = agora_rtc_conn_connect(self.conn_handle, ctypes.create_string_buffer(token.encode('utf-8')), ctypes.create_string_buffer(chan_id.encode('utf-8')), ctypes.create_string_buffer(user_id.encode('utf-8')))
        return ret

    #
    def disconnect(self) -> int:
        ret = agora_rtc_conn_disconnect(self.conn_handle)
        return ret

    # update token when token expired
    def renew_token(self, token) -> int:
        ret = agora_rtc_conn_renew_token(self.conn_handle, token.encode('utf-8'))
        return ret

    #
    def register_observer(self, conn_observer: IRTCConnectionObserver) -> int:
        if self.con_observer:
            self.unregister_observer()
        self.con_observer = RTCConnectionObserverInner(conn_observer, self)
        ret = agora_rtc_conn_register_observer(self.conn_handle, self.con_observer)
        return ret

    #
    def unregister_observer(self) -> int:
        ret = 0
        if self.con_observer:
            ret = agora_rtc_conn_unregister_observer(self.conn_handle)
        self.con_observer = None
        return ret

    # create a data stream
    def create_data_stream(self, reliable, ordered) -> int:
        stream_id = ctypes.c_int(0)
        ret = agora_rtc_conn_create_data_stream(self.conn_handle, ctypes.byref(stream_id), int(reliable), int(ordered))
        if ret < 0:
            return None
        return stream_id.value

    # send data stream message to connection
    def send_stream_message(self, stream_id, data) -> int:
        encoded_data = data.encode('utf-8')
        length = len(encoded_data)
        ret = agora_rtc_conn_send_stream_message(
            self.conn_handle,
            stream_id,
            encoded_data,
            length
        )
        return ret

    #
    def get_agora_parameter(self):
        agora_parameter = agora_rtc_conn_get_agora_parameter(self.conn_handle)
        if not agora_parameter:
            return None
        return AgoraParameter(agora_parameter)

    #

    def get_local_user(self):
        return self.local_user

    def release(self):
        # release local user map
        if self.conn_handle:
            AgoraHandleInstanceMap().del_local_user_map(self.conn_handle)
            agora_rtc_conn_release(self.conn_handle)
        self.conn_handle = None
        self.local_user = None

import time
import ctypes
from .agora_base import *
from .local_user import LocalUser
from .rtc_connection_observer import IRTCConnectionObserver
from ._audio_frame_observer import AudioFrameObserverInner
from .agora_parameter import AgoraParameter
from .globals import AgoraHandleInstanceMap
from ._rtc_connection_observer import RTCConnectionObserverInner
from ._ctypes_data import *
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
# unregister
agora_rtc_conn_unregister_observer = agora_lib.agora_rtc_conn_unregister_observer
agora_rtc_conn_unregister_observer.restype = AGORA_API_C_INT
agora_rtc_conn_unregister_observer.argtypes = [AGORA_HANDLE]

# release
agora_rtc_conn_release = agora_lib.agora_rtc_conn_destroy
# note: for c void return type, we use default
agora_rtc_conn_release.restype = AGORA_API_C_VOID
agora_rtc_conn_release.argtypes = [AGORA_HANDLE]

agora_media_node_factory_create_audio_pcm_data_sender = agora_lib.agora_media_node_factory_create_audio_pcm_data_sender
agora_media_node_factory_create_audio_pcm_data_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_pcm_data_sender.argtypes = [AGORA_HANDLE]

agora_local_user_subscribe_audio = agora_lib.agora_local_user_subscribe_audio
agora_local_user_subscribe_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_audio.argtypes = [AGORA_HANDLE, user_id_t]

agora_local_user_unsubscribe_audio = agora_lib.agora_local_user_unsubscribe_audio
agora_local_user_unsubscribe_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_audio.argtypes = [AGORA_HANDLE, user_id_t]

# sub&unsub all audio
agora_local_user_subscribe_all_audio = agora_lib.agora_local_user_subscribe_all_audio
agora_local_user_subscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_subscribe_all_audio.argtypes = [AGORA_HANDLE]

agora_local_user_unsubscribe_all_audio = agora_lib.agora_local_user_unsubscribe_all_audio
agora_local_user_unsubscribe_all_audio.restype = AGORA_API_C_INT
agora_local_user_unsubscribe_all_audio.argtypes = [AGORA_HANDLE]

agora_media_node_factory_create_video_frame_sender = agora_lib.agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_frame_sender.argtypes = [AGORA_HANDLE]

agora_service_create_custom_video_track_frame = agora_lib.agora_service_create_custom_video_track_frame
agora_service_create_custom_video_track_frame.restype = AGORA_HANDLE
agora_service_create_custom_video_track_frame.argtypes = [AGORA_HANDLE, AGORA_HANDLE]

agora_local_video_track_destroy = agora_lib.agora_local_video_track_destroy
agora_local_video_track_destroy.restype = AGORA_HANDLE
agora_local_video_track_destroy.argtypes = [AGORA_HANDLE]

agora_video_frame_sender_destroy = agora_lib.agora_video_frame_sender_destroy
agora_video_frame_sender_destroy.restype = AGORA_HANDLE
agora_video_frame_sender_destroy.argtypes = [AGORA_HANDLE]


agora_local_user_register_audio_frame_observer = agora_lib.agora_local_user_register_audio_frame_observer
agora_local_user_register_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_register_audio_frame_observer.argtypes = [AGORA_HANDLE, ctypes.POINTER(AudioFrameObserverInner)]

agora_local_user_unregister_audio_frame_observer = agora_lib.agora_local_user_unregister_audio_frame_observer
agora_local_user_unregister_audio_frame_observer.restype = AGORA_API_C_INT
agora_local_user_unregister_audio_frame_observer.argtypes = [AGORA_HANDLE]


agora_local_user_set_playback_audio_frame_before_mixing_parameters = agora_lib.agora_local_user_set_playback_audio_frame_before_mixing_parameters
agora_local_user_set_playback_audio_frame_before_mixing_parameters.restype = AGORA_API_C_INT
agora_local_user_set_playback_audio_frame_before_mixing_parameters.argtypes = [AGORA_HANDLE, ctypes.c_uint32, ctypes.c_uint32]

# 定义datastream 有关的函数
agora_rtc_conn_create_data_stream = agora_lib.agora_rtc_conn_create_data_stream
agora_rtc_conn_create_data_stream.restype = AGORA_API_C_INT
agora_rtc_conn_create_data_stream.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]

agora_rtc_conn_send_stream_message = agora_lib.agora_rtc_conn_send_stream_message
agora_rtc_conn_send_stream_message.restype = AGORA_API_C_INT
agora_rtc_conn_send_stream_message.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]


# set paramter
# AGORA_API_C_HDL agora_rtc_conn_get_agora_parameter(AGORA_HANDLE agora_rtc_conn);
agora_rtc_conn_get_agora_parameter = agora_lib.agora_rtc_conn_get_agora_parameter
agora_rtc_conn_get_agora_parameter.restype = ctypes.c_void_p
agora_rtc_conn_get_agora_parameter.argtypes = [AGORA_HANDLE]

# AGORA_API_C_INT agora_parameter_set_parameters(AGORA_HANDLE agora_parameter, const char* json_src);
agora_parameter_set_parameters = agora_lib.agora_parameter_set_parameters
agora_parameter_set_parameters.restype = AGORA_API_C_INT
agora_parameter_set_parameters.argtypes = [AGORA_HANDLE, ctypes.c_char_p]

# renew token
# AGORA_API_C_INT agora_rtc_conn_renew_token(AGORA_HANDLE agora_rtc_conn, const char* token);
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
        self.con_observer = conn_observer
        con_observer_inner = RTCConnectionObserverInner(self.con_observer, self)
        self.con_observer_inner = con_observer_inner
        ret = agora_rtc_conn_register_observer(self.conn_handle, con_observer_inner)
        return ret

    #
    def unregister_observer(self) -> int:
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

        # release local handle

        self.local_user = None

        agora_rtc_conn_release(self.conn_handle)
        self.conn_handle = None

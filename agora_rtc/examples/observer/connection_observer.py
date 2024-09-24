#!env python
import logging
logger = logging.getLogger(__name__)

from agora.rtc.rtc_connection_observer import IRTCConnectionObserver
class DYSConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super(DYSConnectionObserver, self).__init__()

    def on_connected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_disconnected, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")


    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        logger.info(f"on_connecting, agora_rtc_conn={agora_rtc_conn}, local_user_id={conn_info.local_user_id}, state={conn_info.state}, internal_uid={conn_info.internal_uid} ,reason={reason}")

    def on_user_joined(self, agora_rtc_conn, user_id):
        logger.info(f"on_user_joined, agora_rtc_conn={agora_rtc_conn}, user_id={user_id}")

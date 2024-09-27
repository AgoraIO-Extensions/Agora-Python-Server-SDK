#!env python
import logging
logger = logging.getLogger(__name__)

from agora.rtc.local_user_observer import IRTCLocalUserObserver
class SampleLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(SampleLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        logger.info(f"on_stream_message, user_id={user_id}, stream_id={stream_id}, data={data}, length={length}")
        return 0

    def on_user_info_updated(self, local_user, user_id, msg, val):
        logger.info(f"on_user_info_updated, user_id={user_id}, msg={msg}, val={val}")
        return 0

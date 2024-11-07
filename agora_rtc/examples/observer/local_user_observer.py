#!env python
from agora.rtc.local_user_observer import IRTCLocalUserObserver
import logging
logger = logging.getLogger(__name__)


class ExampleLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(ExampleLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        logger.info(f"on_stream_message, user_id={user_id}, stream_id={stream_id}, data={data}, length={length}")
        pass

    def on_user_info_updated(self, local_user, user_id, msg, val):
        logger.info(f"on_user_info_updated, user_id={user_id}, msg={msg}, val={val}")
        pass
    
    def on_audio_volume_indication(self, agora_local_user, speakers_list, speaker_number, total_volume):
        print(f"xxxxxx xxxx on_audio_volume_indication: number = {speaker_number },totoal volume = {total_volume}")
        for i in range(speaker_number):
            speaker = speakers_list[i]
            print("on vulume indication: ", speaker)
        pass

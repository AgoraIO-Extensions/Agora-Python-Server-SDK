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
        #print(f"xxxxxx xxxx on_audio_volume_indication: number = {speaker_number },totoal volume = {total_volume}")
        for i in range(speaker_number):
            speaker = speakers_list[i]
            #print("on vulume indication: ", speaker)
        pass
    """
    # how to define remote user's Mute /UnMute state:
    for (reason ==5 and state ==0) : remote user is Muted
    for (reason ==6 and state ==1 ) : remote user is UnMuted

    #on_user_audio_track_state_changed
    # if reason==5, indicate the remote user is muted by self
    # if reason==6, indicate the remote user is unmuted by self
    # an sample for state change activity:
    # 1. when remote user call MuteAudio: the state is :(will trigger only once)
    on_user_audio_track_state_changed: user_id=182883922,state=0, reason=5, elapsed=275780
    # 2. when remote user call UnmuteAudio: the state is : (will trigger twice)
    on_user_audio_track_state_changed: user_id=182883922,state=1, reason=6, elapsed=275780
    on_user_audio_track_state_changed: user_id=182883922,state=2, reason=6, elapsed=290281
    """
    def on_user_audio_track_state_changed(self, agora_local_user, user_id, agora_remote_audio_track, state, reason, elapsed):
        print(f"on_user_audio_track_state_changed: user_id={user_id},state={state}, reason={reason}, elapsed={elapsed}")
        pass
    

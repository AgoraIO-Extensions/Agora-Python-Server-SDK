# coding=utf-8

import time
import datetime
import ctypes
from common.path_utils import get_log_path_with_filename
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame

from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora.rtc.rtc_connection import *
from agora.rtc.media_node_factory import *
from agora.rtc.audio_pcm_data_sender import *
from agora.rtc.audio_frame_observer import *
import signal
from agora.rtc.audio_vad import *
from agora.rtc.local_user import *
from agora.rtc.local_user_observer import *
import threading
from collections import deque

# import voicesentencedetection
from agora.rtc.voice_detection import *
from agora.rtc.audio_vad import *

import gc
import asyncio


# connection observer

def local_get_log_path_with_filename():
    example_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(example_dir, 'agorasdk.log')
    return log_path


# observer
class MyAudioFrameObserver(IAudioFrameObserver):
    def __init__(self):
        super(MyAudioFrameObserver, self).__init__()
        self._source_file = open("./vad_source.pcm", "wb")
        self._case1_file = open("./vad_case1.pcm", "wb")
        self._case2_file = open("./vad_case2.pcm", "wb")
        self._case3_file = open("./vad_case3.pcm", "wb")
        self._silence_pack = bytearray(320)
        self._vad_file = None  # open("./vad_file.pcm", "wb")
        self._log_file = None  # open("./vad_log.txt", "w")
        """
        # Recommended  configurations:  
            # For not-so-noisy environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -50)  
            # For noisy environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -40)  
            # For high-noise environments, use this configuration: (16, 30, 20, 0.7, 0.5, 70, 70, -30)

         """

        self._vad_instance = AudioVadV2(AudioVadConfigV2(16, 30, 20, 0.7, 0.5, 70, 70, -50))
        self._vad_counts = 0
        # vad v1 related
        self.v1_configure = VadConfig()
        # modify v1 vad configure
        self.v1_configure.voiceProbThr = 0.5
        self.v1_configure.rmsThr = -40
        self.v1_configure.aggressive = 2.0
        self.v1_configure.preStartRecognizeCount = 18
        self.v1_configure.startRecognizeCount = 16
        self.v1_configure.stopRecognizeCount = 20
        self.v1_configure.activePercent = 0.6
        self.v1_configure.inactivePercent = 0.2

        self._vad_v1_instance = AudioVad()
        self._vad_v1_instance.Create(self.v1_configure)
        self._vad_v1_counts = 0
        self._vad_v1_file = None  # open("./vad_file_v1.pcm", "wb")

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     audio_params_instance = AudioParams()
    #     return audio_params_instance

    def on_record_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_record_audio_frame")
        return 0

    def on_playback_audio_frame(self, agora_local_user, channelId, frame):
        logger.info(f"on_playback_audio_frame")
        return 0

    def on_ear_monitoring_audio_frame(self, agora_local_user, frame):
        logger.info(f"on_ear_monitoring_audio_frame")
        return 0

    def _dump_to_file(self, fd, audio_frame: AudioFrame):
        fd.write(audio_frame.buffer)

    def on_playback_audio_frame_before_mixing(self, agora_local_user, channelId, uid, audio_frame: AudioFrame):
        # logger.info(f"on_playback_audio_frame_before_mixing, channelId={channelId}, uid={uid}, type={audio_frame.type}, samples_per_sec={audio_frame.samples_per_sec}, samples_per_channel={audio_frame.samples_per_channel}, bytes_per_sample={audio_frame.bytes_per_sample}, channels={audio_frame.channels}, len={len(audio_frame.buffer)}")
        print(f"before_mixing: far = {audio_frame.far_field_flag },rms = {audio_frame.rms}, voice = {audio_frame.voice_prob}, music ={audio_frame.music_prob},pith = {audio_frame.pitch}")
        # strategies
        # anyway, dump source file
        # if audio_frame.buffer:
        self._source_file.write(audio_frame.buffer)
        v1_datas = audio_frame.buffer

        # vad v2
        state, bytes = self._vad_instance.process(audio_frame)
        print("state = ", state, len(bytes) if bytes != None else 0)
        # save and append to file
        if bytes != None:
            if state == 1:
                # open and write to file
                print("vad v2 start speaking:", self._vad_counts)
                cur_time = int(time.time()*1000)
                name = f"./vad_{self._vad_counts}.pcm"
                self._vad_file = open(name, "wb")
                self._vad_file.write(bytes)
            elif state == 2:
                self._vad_file.write(bytes)
            elif state == 3:
                self._vad_file.write(bytes)
                self._vad_file.close()
                self._vad_counts += 1
                print("vad v2 stop speaking:", self._vad_counts-1)
            else:
                logger.info("unknown state")
        # vad v1
        ret, frameout, flag = self._vad_v1_instance.Proc(v1_datas)
        print(f"vad v1 ret = {ret}, flag = {flag}")
        if ret == 0 and flag == 1:
            # start speaking
            print("vad v1 start speaking:", self._vad_v1_counts)
            cur_time = int(time.time()*1000)
            name = f"./vad1_{self._vad_v1_counts}.pcm"
            self._vad_v1_file = open(name, "wb")
            self._vad_v1_file.write(frameout)
        elif ret == 0 and flag == 2:
            # speaking:
            self._vad_v1_file.write(frameout)
        elif ret == 0 and flag == 3:
            # stop speaking
            self._vad_v1_file.write(frameout)
            self._vad_v1_file.close()
            self._vad_v1_counts += 1
            print("vad v1 stop speaking:", self._vad_v1_counts-1)

        """
        
        """

        # case 1
        if audio_frame.far_field_flag == 1:
            self._case1_file.write(audio_frame.buffer)
        else:
            self._case1_file.write(self._silence_pack)

        # case2
        if audio_frame.far_field_flag == 1 and audio_frame.voice_prob > 75:
            self._case2_file.write(audio_frame.buffer)
        else:
            self._case2_file.write(self._silence_pack)

        # case3
        if audio_frame.far_field_flag == 1 and audio_frame.voice_prob > 75 and audio_frame.rms > -35:
            self._case3_file.write(audio_frame.buffer)
        else:
            self._case3_file.write(self._silence_pack)

        return 1

    def on_get_audio_frame_position(self, agora_local_user):
        logger.info(f"on_get_audio_frame_position")
        return 0
    # def on_get_audio_frame_position(self, agora_local_user):
    #     logger.info("CCC on_get_audio_frame_position")
    #     return 0

    # def on_get_playback_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_playback_audio_frame_param")
    #     return 0
    # def on_get_record_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_record_audio_frame_param")
    #     return 0
    # def on_get_mixed_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_mixed_audio_frame_param")
    #     return 0
    # def on_get_ear_monitoring_audio_frame_param(self, agora_local_user):
    #     logger.info("CCC on_get_ear_monitoring_audio_frame_param")
    #     return 0




# sig handleer


def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True


def main():

    # signal handler

    signal.signal(signal.SIGINT, signal_handler)

    # run this example
    # 例如： python examples/example.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
    appid = sys.argv[1]
    token = sys.argv[2]
    channel_id = sys.argv[3]
    pcm_file_path = sys.argv[4]
    # check argv len
    if len(sys.argv) > 5:
        uid = sys.argv[5]
    else:
        uid = "0"

    # send stream or not
    if len(sys.argv) > 7:
        send_stream = int(sys.argv[7])
    else:
        send_stream = 0
    if len(sys.argv) > 8:
        role_type = int(sys.argv[8])
    else:
        role_type = 2

    """
    #check vad sample file
    if len(sys.argv) > 6:
        DoVadTest(sys.argv[6])
    """
    print("appid:", appid, "token:", token, "channel_id:", channel_id, "pcm_file_path:", pcm_file_path, "uid:", uid, "send_stream:", send_stream)

    config = AgoraServiceConfig()
    config.appid = appid
    # config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
    config.log_path = local_get_log_path_with_filename()  # get_log_path_with_filename(os.path.splitext(__file__)[0])

    agora_service = AgoraService()
    agora_service.initialize(config)

    sub_opt = AudioSubscriptionOptions(
        packet_only=0,
        pcm_data_only=1,
        bytes_per_sample=2,
        number_of_channels=1,
        sample_rate_hz=16000
    )

    con_config = RTCConnConfig(
        auto_subscribe_audio=1,
        auto_subscribe_video=0,
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER if role_type == 1 else ClientRoleType.CLIENT_ROLE_AUDIENCE,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        audio_recv_media_packet=0,
        audio_subs_options=sub_opt,
        enable_audio_recording_or_playout=0,
    )

    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = ExampleConnectionObserver()
    connection.register_observer(conn_observer)

    connection.connect(token, channel_id, uid)

    # step2:
    media_node_factory = agora_service.create_media_node_factory()
    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)

    # step3: localuser:must regiseter before connect
    localuser = connection.get_local_user()
    local_observer = ExampleLocalUserObserver()
    # enable volume indication
    localuser.set_audio_volume_indication_parameters(100, 3, 1)
    localuser.register_local_user_observer(local_observer)

    # note: set_playback_audio_frame_before_mixing_parameters must be call before register_audio_frame_observer
    localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
    audio_observer = MyAudioFrameObserver()
    localuser.register_audio_frame_observer(audio_observer)

    # ret = localuser.get_user_role()
    # localuser.set_user_role(con_config.client_role_type)

    # step4: pub
    audio_track.set_enabled(1)
    localuser.publish_audio(audio_track)
    localuser.subscribe_all_audio()



    # stream msg
    stream_id = connection.create_data_stream(0, 0)
    print(f"streamid: {stream_id}")

    # set paramter

    # nearindump = "{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}"
    # connection.SetParameter(nearindump)
    # agora_parameter = connection.get_agora_parameter()
    # agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

    sendinterval = 0.05  # 50ms

    packnum = int((sendinterval*1000)/10)

    global g_runing
    # recv mode
    while g_runing:
        time.sleep(0.05)

     # release resource
    
    localuser.unpublish_audio(audio_track)
    audio_track.set_enabled(0)

    localuser.unregister_audio_frame_observer()
    localuser.unregister_local_user_observer()

    connection.disconnect()
    connection.unregister_observer()

    localuser.release()
    connection.release()

    
    audio_track.release()
    pcm_data_sender.release()
    

    media_node_factory.release()
    agora_service.release()
    
    #set to None
    audio_track = None
    audio_observer = None
    local_observer = None
    localuser = None
    connection = None
    agora_service = None


if __name__ == "__main__":
    main()


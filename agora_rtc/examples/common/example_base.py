#!env python
import asyncio
import signal
from common.parse_args import ExampleOptions
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig   
from agora.rtc.rtc_connection import RTCConnection
from agora.rtc.local_user import LocalUser
from agora.rtc.agora_base import *
import logging
logger = logging.getLogger(__name__)


class RTCBaseProcess():
    def __init__(self, conn_config: RTCConnConfig = None, publish_config: RtcConnectionPublishConfig = None):
        self._exit = asyncio.Event()
        self._conn_config = None
        self._publish_config = None
        if conn_config:
            self._conn_config = conn_config
        else:
            self._conn_config = RTCConnConfig(
                client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
                channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
            )
        if publish_config:
            self._publish_config = publish_config
        else:
            publish_config = RtcConnectionPublishConfig(
                audio_profile=AudioProfileType.AUDIO_PROFILE_DEFAULT,
                audio_scenario=AudioScenarioType.AUDIO_SCENARIO_AI_SERVER,
                is_publish_audio=True,
                is_publish_video=False,
                audio_publish_type=AudioPublishType.AUDIO_PUBLISH_TYPE_ENCODED_PCM,
                video_publish_type=VideoPublishType.VIDEO_PUBLISH_TYPE_YUV,
                video_encoded_image_sender_options=SenderOptions(
                    target_bitrate=6500,
                    cc_mode=TCcMode.CC_ENABLED,
                    codec_type=VideoCodecType.VIDEO_CODEC_H264,
                )
            )
            self._publish_config = publish_config
        self._serv_config = AgoraServiceConfig()
        self._serv_config.log_path = "./agora_rtc_log/agorasdk.log"
        self._serv_config.log_file_size_kb = 1024
        self._serv_config.data_dir = "./agora_rtc_log"
        self._serv_config.config_dir = "./agora_rtc_log"

    async def connect_and_release(self, agora_service: AgoraService, channel_id, sample_options: ExampleOptions):
        # ---------------2. Create Connection
        self.set_conn_config()
        logger.info(f"connect_and_release: {self._conn_config.auto_subscribe_video}, auto_subscribe_audio: {self._conn_config.auto_subscribe_audio}")
        #change role
        if sample_options.role == 0:
            self._conn_config.client_role_type = ClientRoleType.CLIENT_ROLE_AUDIENCE
        else:
            self._conn_config.client_role_type = ClientRoleType.CLIENT_ROLE_BROADCASTER 
        
        connection = agora_service.create_rtc_connection(self._conn_config, self._publish_config)
        conn_observer = ExampleConnectionObserver()
        connection.register_observer(conn_observer)
        connection.connect(sample_options.token, channel_id, sample_options.user_id)

        local_user = connection.get_local_user()
        local_user_observer = ExampleLocalUserObserver()
        connection.register_local_user_observer(local_user_observer)
        try:
            await self.setup_in_connection(agora_service, connection, local_user, sample_options)
        finally:
            connection.disconnect()
            connection.release()
            conn_observer = None
            local_user_observer = None
            connection = None
            logger.info("connection release")

    def set_conn_config(self):
        pass

    def set_serv_config(self):
        pass

    async def setup_in_connection(self, agora_service: AgoraService, connection: RTCConnection, local_user: LocalUser, sample_options: ExampleOptions):
        pass

    def handle_signal(self):
        self._exit.set()

    async def run(self, sample_options: ExampleOptions, log_path: str):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.handle_signal)
        loop.add_signal_handler(signal.SIGTERM, self.handle_signal)

        # config = AgoraServiceConfig()
        self._serv_config.appid = sample_options.app_id
        self._serv_config.log_path = log_path
        self.set_serv_config()
        agora_service = AgoraService()
        agora_service.initialize(self._serv_config)

        await self.create_connections(sample_options, agora_service)

        agora_service.release()
        logger.info("agora_service release")

    async def create_connections(self, sample_options: ExampleOptions, agora_service):
        tasks = []
        for i in range(int(sample_options.connection_number)):
            if i == 0:
                channel_id = sample_options.channel_id
            else:
                channel_id = sample_options.channel_id + str(i)
            #for audience, use same channel_id, and force uid to 0 for this case
            if sample_options.role == 0:
                channel_id = sample_options.channel_id
            logger.info(f"------channel_id: {channel_id}, uid: {sample_options.user_id}")
            tasks.append(asyncio.create_task(self.connect_and_release(agora_service, channel_id, sample_options)))
        await asyncio.gather(*tasks)

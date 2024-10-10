#!env python
import asyncio
import signal
from common.parse_args import ExampleOptions
from observer.connection_observer import ExampleConnectionObserver
from observer.local_user_observer import ExampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, RTCConnection, LocalUser
from agora.rtc.agora_base import *
import logging
logger = logging.getLogger(__name__)

class RTCBaseProcess():
    def __init__(self):
        self._exit = asyncio.Event()
        self._conn_config = RTCConnConfig(
            client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
            channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        )
        self._serv_config = AgoraServiceConfig()
    async def connect_and_release(self, agora_service:AgoraService, channel_id, sample_options:ExampleOptions):
        #---------------2. Create Connection
        self.set_conn_config()
        logger.info(f"connect_and_release: {self._conn_config.auto_subscribe_video}, auto_subscribe_audio: {self._conn_config.auto_subscribe_audio}")
        connection = agora_service.create_rtc_connection(self._conn_config)
        conn_observer = ExampleConnectionObserver()
        connection.register_observer(conn_observer)
        connection.connect(sample_options.token, channel_id, sample_options.user_id)

        local_user = connection.get_local_user()
        local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
        local_user_observer = ExampleLocalUserObserver()
        local_user.register_local_user_observer(local_user_observer)

        await self.setup_in_connection(agora_service, connection, local_user ,sample_options)        

        connection.unregister_observer()
        connection.disconnect()
        connection.release()

    def set_conn_config(self):
        pass
    def set_serv_config(self):
        pass
    async def setup_in_connection(self,agora_service:AgoraService, connection:RTCConnection, local_user:LocalUser, sample_options:ExampleOptions):
        pass

    def handle_signal(self):
        self._exit.set()
    async def run(self, sample_options:ExampleOptions, log_path:str):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.handle_signal)
        loop.add_signal_handler(signal.SIGTERM, self.handle_signal)

        # config = AgoraServiceConfig()
        self._serv_config.appid = sample_options.app_id
        self._serv_config.log_path = log_path
        self.set_serv_config()
        agora_service = AgoraService()
        agora_service.initialize(self._serv_config)

        async with asyncio.TaskGroup() as tg:
            for i in range(int(sample_options.connection_number)):
                if i == 0:
                    channel_id = sample_options.channel_id
                else:
                    channel_id = sample_options.channel_id + str(i)
                logger.info(f"------channel_id: {channel_id}, uid: {sample_options.user_id}")
                tg.create_task(self.connect_and_release(agora_service, channel_id, sample_options))

        agora_service.release()
        logger.info("agora_service.release")


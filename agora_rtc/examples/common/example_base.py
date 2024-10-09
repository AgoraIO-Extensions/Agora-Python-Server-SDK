#!env python
import asyncio
import signal
from common.parse_args import SampleOptions
from observer.connection_observer import SampleConnectionObserver
from observer.local_user_observer import SampleLocalUserObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig, RTCConnection, LocalUser
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RTCBaseProcess():
    def __init__(self):
        self._exit = asyncio.Event()    
    async def connect_and_release(self, agora_service:AgoraService, channel_id, sample_options:SampleOptions):
        #---------------2. Create Connection
        con_config = RTCConnConfig(
            client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
            channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        )
        connection = agora_service.create_rtc_connection(con_config)
        conn_observer = SampleConnectionObserver()
        connection.register_observer(conn_observer)
        connection.connect(sample_options.token, channel_id, sample_options.user_id)

        local_user = connection.get_local_user()
        local_user.set_audio_scenario(AudioScenarioType.AUDIO_SCENARIO_CHORUS)
        local_user_observer = SampleLocalUserObserver()
        local_user.register_local_user_observer(local_user_observer)

        await self.setup_sender(agora_service, local_user ,sample_options)        

        connection.unregister_observer()
        connection.disconnect()
        connection.release()

    async def setup_sender(self,agora_service:AgoraService, local_user:LocalUser, sample_options:SampleOptions):
        pass

    def handle_signal(self):
        self._exit.set()
    async def run(self, sample_options:SampleOptions, log_path:str):
        logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.handle_signal)
        loop.add_signal_handler(signal.SIGTERM, self.handle_signal)

        config = AgoraServiceConfig()
        config.appid = sample_options.app_id
        config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
        config.log_path = log_path
        agora_service = AgoraService()
        agora_service.initialize(config)

        async with asyncio.TaskGroup() as tg:
            for i in range(int(sample_options.connection_number)):
                logger.info(f"channel {i}")
                channel_id = sample_options.channel_id + str(i+1)
                tg.create_task(self.connect_and_release(agora_service, channel_id, sample_options))

        agora_service.release()
        logger.info("agora_service.release-coro")


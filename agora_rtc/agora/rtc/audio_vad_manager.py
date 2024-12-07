import ctypes
from .agora_base import *
import ctypes
from .audio_frame_observer import *
from .voice_detection import AudioVadV2, AudioVadConfigV2
import logging
from threading import Lock
logger = logging.getLogger(__name__)

# 需要考虑不同的vad configure：也就是说需要触发什么时候做设置？？
#可以做一个对外的接口：update（channel_id, user_id, vad_config）
# 然后一个总的configure接口：update_all(channel_id, vad_config)
# 默认配置用service 的configure
class AudioVadManager():
    def __init__(self, configure: AudioVadConfigV2) -> None:
        self._instance_map = {} # set to dict
        self._vad_config = configure
        self._lock = Lock()
        self._is_init = True
        pass
    def _make_key(self, channel_id: str, user_id: str) -> str:
        return channel_id + user_id
    def get_vad_instance(self, channel_id: str, user_id: str) -> AudioVadV2:
        key = self._make_key(channel_id, user_id)
        with self._lock:
            return self._instance_map.get(key, None)
    #note: inner function, not thread safe, but should be ok, since it is called by other thread safe function
    def _add_vad_instance(self, channel_id: str, user_id: str) -> int:
        key = self._make_key(channel_id, user_id)
        self._instance_map[key] = AudioVadV2(self._vad_config)
        return 0
        pass
    def del_vad_instance(self, channel_id: str, user_id: str) -> None:
        key = self._make_key(channel_id, user_id)
        with self._lock:
            self._instance_map.pop(key, None)
    def get_vad_instance(self, channel_id: str, user_id: str) -> AudioVadV2:
        key = self._make_key(channel_id, user_id)
        with self._lock:
            return self._instance_map.get(key, None)
    def process(self, channel_id: str, user_id: str, frame: AudioFrame) -> tuple[int, bytearray]:
        if self._is_init is False:
            return -2, None
        vad_instance = self.get_vad_instance(channel_id, user_id)
        if vad_instance is not None:
            return vad_instance.process(frame)
        else:
            #add new one
            self._add_vad_instance(channel_id, user_id)
            return -1, None
        pass
    def release(self) -> None:
        print("____release vad manager: ", len(self._instance_map))
        if self._is_init is False:
            return
        self._is_init = False
        with self._lock:
            self._instance_map.clear()
        pass
#!env python
import threading
import time
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame
from agora.rtc.audio_pcm_data_sender import AudioPcmDataSender
import logging
import asyncio
logger = logging.getLogger(__name__)



"""
# AudioConsumer
# 基础类，用于消费PCM数据，并将PCM数据推送到RTC频道中
# 在AI场景中：
#   当TTS有数据返回的时候：调用AudioConsumer::push_pcm_data方法，将返回的TTS数据直接push到AudioConsumer
#   在另外的一个“timer”的触发函数中，调用 AudioConsumer::consume()方法，将数据推送到rtc
    # 推荐：
    # “Timer”可以是asycio的模式；也可以是threading.Timer的模式；也可以和业务已有的timer结合在一起使用，都可以。只需要在timer 触发的函数中，调用 AudioConsumer::consume()即可
    # “Timer”的触发间隔，可以和业务已有的timer间隔一致，也可以根据业务需求调整，推荐在40～80ms之间  
 
AudioConsumer调用方式：
1. 使用该类的前提：
    - 需要客户在应用层自己实现一个timer，该timer间隔需要在[40ms,80ms]之间。这个timer的触发方法下面用app::TimeFunc表示。
    - 一个用户只能对应一个AudioConsumer对象，也就是保障一个生产者产生的内容对应一个消费者。
2. 使用方式：
    A 对每一个“生产pcm数据“的 userid 创建一个AudioConsumer对象，也就是保障一个生产者产生的内容对应一个消费者。
    B 当有pcm数据生成的时候，比如TTS的返回，调用 AudioConsumer::push_pcm_data(data)
    C 当需要消费的时候（通常用app::TimerFunc)，调用 AudioConsumer::consume()方法，会自动完成对数据的消费，也就是推送到rtc 频道中
    D 如果需要打断：也就是AI场景中，要停止播放当前AI的对话：调用 AudioConsumer::clear()方法,会自动清空当前buffer中的数据
    E 退出的时候，调用release()方法，释放资源
"""
class AudioConsumer:
    def __init__(self, pcm_sender: AudioPcmDataSender, sample_rate: int, channels: int) -> None:
        self._lock = threading.Lock()
        self._start_time = 0
        self._data = bytearray()
        self._consumed_packages = 0
        self._pcm_sender = pcm_sender
        self._frame = PcmAudioFrame()
        #init sample rate and channels
        self._frame.sample_rate = sample_rate
        self._frame.number_of_channels = channels

        #audio parame
        self._frame.bytes_per_sample = 2
        self._bytes_per_frame = sample_rate // 100 * channels * 2
        self._samples_per_channel = sample_rate // 100* channels
        #init pcmaudioframe
        self._frame.timestamp = 0

        self._init = True
        
        pass
    def push_pcm_data(self, data) ->None:
        if self._init == False:
            return
        # add to buffer, lock
        with self._lock:
            self._data += data
        pass
    def _reset(self):
        if self._init == False:
            return
        self._start_time = time.time()*1000
        self._consumed_packages = 0
        pass
 
    def consume(self):
        print("consume begin")
        if self._init == False:
            return -1
        now = time.time()*1000
        elapsed_time = int(now - self._start_time)
        expected_total_packages = int(elapsed_time//10)
        besent_packages = expected_total_packages - self._consumed_packages
        data_len = len(self._data)

        if besent_packages > 18 and data_len //self._bytes_per_frame < 18: #for fist time, if data_len is not enough, just return and wait for next time
            #print("-----underflow data")
            return -2
        if besent_packages > 18: #rest to start state, push 18 packs in Start_STATE
            self._reset()
            besent_packages = min(18, data_len//self._bytes_per_frame)
            self._consumed_packages = -besent_packages
            

        #get min packages
        act_besent_packages = (int)(min(besent_packages, data_len//self._bytes_per_frame))
        #print("consume 1:", act_besent_packages, data_len)
        if act_besent_packages < 1:
            return 0
       
        #construct an audio frame to push
        #frame = PcmAudioFrame()
        with self._lock:
            #frame = PcmAudioFrame()
            self._frame.data = self._data[:self._bytes_per_frame*act_besent_packages]
            self._frame.timestamp = 0
            self._frame.samples_per_channel = self._samples_per_channel*act_besent_packages
           
            #reset data
            self._data = self._data[self._bytes_per_frame*act_besent_packages:]
            self._consumed_packages += act_besent_packages

        self._pcm_sender.send_audio_pcm_data(self._frame)
        return act_besent_packages
        #print(f"act_besent_packages: {now},{now - self._start_time}, {besent_packages}, {act_besent_packages},{self._consumed_packages},{data_len}")
        pass

    def len(self) -> int:
        if self._init == False:
            return 0
        with self._lock:
            return len(self._data)
    def clear(self):
        if self._init == False:
            return
        with self._lock:
            self._data = bytearray()
        pass
    def release(self):
        if self._init == False:
            return
        
        self._init = False
        with self._lock:
            self._data = None
            self._frame = None
            self._pcm_sender = None
        self._lock = None
        pass



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
    MIN_BUFFER_SIZE = 10
    RTC_E2E_DELAY = 200 # e2e delay 90ms for iphone, 120ms for android;150ms for web. so we use 200ms here
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
        self._samples_per_channel = sample_rate // 100
        #init pcmaudioframe
        self._frame.timestamp = 0

        self._init = True
        self._last_consume_time = 0
        
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
        self._last_consume_time = self._start_time
        pass
 
    def consume(self):
        #print("consume begin")
        if self._init == False:
            return -1
        now = time.time()*1000
        elapsed_time = int(now - self._start_time)
        expected_total_packages = int(elapsed_time//10)
        besent_packages = expected_total_packages - self._consumed_packages
        data_len = len(self._data)
        #if data is not empty, to update last consume time
        if data_len > 0:
            self._last_consume_time = now

        if besent_packages > AudioConsumer.MIN_BUFFER_SIZE and data_len //self._bytes_per_frame < AudioConsumer.MIN_BUFFER_SIZE: #for fist time, if data_len is not enough, just return and wait for next time
            #print("-----underflow data")
            return -2
        if besent_packages > AudioConsumer.MIN_BUFFER_SIZE: #rest to start state, push 18 packs in Start_STATE
            self._reset()
            besent_packages = min(AudioConsumer.MIN_BUFFER_SIZE, data_len//self._bytes_per_frame)
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
        return self._consumed_packages
        #print(f"act_besent_packages: {now},{now - self._start_time}, {besent_packages}, {act_besent_packages},{self._consumed_packages},{data_len}")
        pass

    def len(self) -> int:
        if self._init == False:
            return 0
        with self._lock:
            return len(self._data)

    #判断AudioConsumer中的数据是否已经完全推送给了RTC 频道
    #因为audioconsumer内部有一定的缓存机制，所以当get_remaining_data_size 返回是0的时候，还有数据没有推送给
    #rtc 频道。如果要判断数据是否完全推送给了rtc 频道，需要调用这个api来做判断。
    #return value：1--push to rtc completed, 0--push to rtc not completed   -1--error
    def is_push_to_rtc_completed(self)->int:
        if self._init == False:
            return -1
        with self._lock:
            remain_size = len(self._data)
            if remain_size == 0:
                now = time.time()*1000
                diff = now - self._last_consume_time

                if diff > AudioConsumer.MIN_BUFFER_SIZE*10 + AudioConsumer.RTC_E2E_DELAY:
                    return 1
            
            return 0
        pass
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
class PcmConsumeStats:
    def __init__(self):
        self.startTime = 0
        self.totalLength = 0
        self.duration = 0
    def __str__(self):
        return f"PcmConsumeStats: startTime={self.startTime}, totalLength={self.totalLength}, duration={self.duration}"
    def __repr__(self):
        return self.__str__()
    def is_new_round(self) -> bool:
        if self.startTime == 0:
            return True
        now = int(time.time()*1000)
        if now - self.startTime > self.duration:
            return True
        return False
    def add_pcm_data(self, data_len: int,sample_rate: int,channels: int):
        if self.is_new_round():
            self.reset()
            self.startTime = int(time.time()*1000)
            self.totalLength = 0
            self.duration = 0

        self.totalLength += data_len
        #change duration to ms
        bytes_per_frame_in_ms = (sample_rate / 1000) * 2 * channels
        self.duration = self.totalLength / bytes_per_frame_in_ms

    def is_push_to_rtc_completed(self) -> bool:
        now = int(time.time()*1000)
        diff = now - self.startTime
        print(f"is_push_to_rtc_completed: {diff}, {self.duration}")
        if diff > self.duration + int(180):
            return True
        return False
        
    def reset(self):
        self.startTime = 0
        self.totalLength = 0
        self.duration = 0
    
    


import time
import ctypes

import os
import sys
from enum import Enum,IntEnum
from collections import deque
from .agora_base import AudioFrame, AudioParams
import logging
logger = logging.getLogger(__name__)
"""
思路：
设置一个队列，每次有音频数据过来，就放到队列里，然后根据队列里的数据，判断是否是说话状态
3个队列：
start：一个用来判断是否是说话状态；
stop：一个用来判断是否是停止说话状态；
trend：在用来判断结束的时候，用来判断趋势；就是说如果最近的趋势是要趋向开始说话，则不判断为结束。
用在这样的曲线：
+++0+++-----1----+++++++2+++++++----3-----+++++++4+++++++
在1部分结合部分2部分，就能达到stoprec count，然后也符合了inactivePercent，但这个时候2的趋势是要开始说话，所以针对这样的情况，应该
合并到说话队列中，所以需要trend队列，用来判断趋势。

趋势判断的目标：
我们的目标是在stop的范围内，如果发现趋势是active增加的，就不做stop。
所以总大小是stop大小；然后滑动窗体设定为stop大小的一半，然后判断这个滑动窗体里，是否是active增加的，如果是，则不判断为stop。

"""

class  VadConfigV2():
    def __init__(self, preStartRecognizeCount:int, startRecognizeCount:int, stopRecognizeCount:int, 
                 activePercent:float, inactivePercent:float, start_voiceprob: int, stop_voiceporb:int, rmsThreshold:float):
        self.startRecognizeCount = startRecognizeCount
        self.preStartRecognizeCount = preStartRecognizeCount
        self.stopRecognizeCount = stopRecognizeCount
        self.activePercent = activePercent #判断开始阶段的比例， float 类型，默认推荐是
        self.inactivePercent = inactivePercent
        self.start_voiceprob = start_voiceprob #int value, default to 50，这样就是快速启动，降低延迟
        self.stop_voiceprob = stop_voiceporb#int value, default to 70，这样就是快速停止，缩短结束时间的判断，整体降低延迟。避免长时间的非人声的静音数据，从而增大延迟
        self.start_rms = rmsThreshold #default to 0.0
        self.stop_rms = rmsThreshold #default to 0.0
        
        pass

class VadDataV2:
    def __init__(self, data: AudioFrame,   is_activity: bool):
        self._audio_frame = data
        #self.timestamp = time.time()
        self._is_activity = is_activity
        pass

class VoiceSentenceDetection():
    _kIntervalPerAudioFrameInMS = 10
    _kMaxChunkSizePer10MSFor16K = 320 #bytes, ??/ for diff sampleRate,its still 
    _kMaxChunkSizePer10MSFor32K = 640 #bytes, ??/ for diff sampleRate
    _kMaxChunkSizePer10MSFor48K = 960 #bytes, ??/ for diff sampleRate
    _vad_state_nonspeaking = 0
    _vad_state_startspeaking = 1
    _vad_state_speaking = 2
    _vad_state_stopspeaking = 3
    
    def __init__(self, config: VadConfigV2):
        self._vad_configure = config
        self._cur_state = self._vad_state_nonspeaking #0: non-speaking, 1-start speaking, 2-speaking, 3-stop speaking
        self._data = bytearray()
        self._start_size = self._vad_configure.preStartRecognizeCount + self._vad_configure.startRecognizeCount
        self._start_queue = deque(maxlen=self._start_size)
        self._stop_queue = deque(maxlen=self._vad_configure.stopRecognizeCount)
        #trend queue
        self._trend_queue = deque(maxlen=self._vad_configure.stopRecognizeCount)  # 600ms buffer,需要一定是整数，因为要计算趋势
        self._trend_window = self._vad_configure.stopRecognizeCount//2

 
        
        
    
    def _push_to_start(self, data: VadDataV2) -> tuple[int,bool]:
        self._start_queue.append(data)
        size = len(self._start_queue)
        return size, size >= self._start_size
    def _push_to_stop(self, data: VadDataV2) -> tuple[int,bool]:
        self._stop_queue.append(data)
        size = len(self._stop_queue)
        return size, size >= self._vad_configure.stopRecognizeCount
    def _push_to_trend(self, data: VadDataV2) -> tuple[int,bool]:
        self._trend_queue.append(data)
        size = len(self._trend_queue)
        return size, size >= self._trend_window
    def _sum(self,quue: deque) -> int:
        return sum(1 for item in quue if item._is_activity == True)
    def _calculate_sliding_window_ratio(self, arr:deque, window_size:int)-> list[float]:
        ratios = []  
        #不用严格的slide window 来计算,就计算前后的差异
        seperator_index = len(arr)//2
        count_ones = 0
        

        for i, item in enumerate(arr,start=0):
            if i  < seperator_index:
                count_ones +=  1 if item._is_activity == True else 0
            elif i == seperator_index:
                ratios.append(count_ones)
                count_ones = 0
            elif i > seperator_index:
                count_ones +=  1 if item._is_activity == True else 0
            
        ratios.append(count_ones)
              
        return ratios
        for start_index in range(len(arr) - window_size + 1):  
            count_ones = 0
            for i, item in enumerate(arr,start=start_index):
                if i >= start_index and i < start_index + window_size:
                    count_ones +=  1 if item._is_activity == True else 0
                ratio = count_ones / window_size  
                ratios.append(ratio)  
        return ratios  
    def _get_trend(self, queue: deque) -> int:
        if len(queue) < self._trend_window:
            return 0
        
        ratios = self._calculate_sliding_window_ratio(queue, self._trend_window)
        # 计算趋势
        print(ratios)
        return 1 if ratios[1] > ratios[0] else 0

    #get silence count from deque: totalcount, silenct_count
    def _get_silence_count(self, queue: deque, start_inx:int) -> tuple[int, int]:
        total = len(queue)
        silence_count = 0
        for i, item in enumerate(queue,start=0):
            if i > start_inx and item._is_activity == False:
                silence_count += 1
        return total, silence_count
        
    def _move_deque(self, data:bytearray, queue: deque) ->bytearray:
        
        for item in queue:  #是否有必要在这对inactive包替换为静音包？？？依赖实际测试
            data.extend(item._audio_frame.buffer)
        return data
    def _clear_queue(self, queue: deque):
        queue.clear()
        pass
    
    def _process_start(self, data: VadDataV2) -> tuple[int, bytearray]:
        size, full = self._push_to_start(data)
        state = self._cur_state
        bytes = bytearray()
       
        
        if full == True:
            #存在一定的问题：如果pre中就已经是开始在说话了，这个时候就会出现问题，或者漏掉的情况
            #检查start中的比例是否符合阈值,如果符合阈值，zhi，则将start中的数据全部送入到pre中，并且将pre清空，同时将start清空，同时将当前状态设置为speaking
            total, silence_count = self._get_silence_count(self._start_queue, self._vad_configure.preStartRecognizeCount)
            total -= self._vad_configure.preStartRecognizeCount
            if (total - silence_count) / total >= self._vad_configure.activePercent:
                state = self._vad_state_startspeaking
                #move pre & start to a new bytearray
                
                self._move_deque(bytes, self._start_queue)
                self._clear_queue(self._start_queue)
               
                #and clear pre &start
                self._clear_queue(self._stop_queue)
                print("start speaking:", len(self._stop_queue))
            
        return state, bytes
        
    def _process_speaking(self, data: VadDataV2) -> tuple[int, bytearray]:
        #将数据append 到stop中
        #如果数据满，怎判断是否触发stop
        state = self._cur_state
        size, full = self._push_to_stop(data)
        print(f"stop: {size}, {full}")

        
        if full == True:
            #trend check
            trend = self._get_trend(self._stop_queue)
            #检查stop中的比例是否符合阈值,
            #   如果符合阈值，同时清空stop 清空，并且将当前状态设置为non-speaking
            total, silence_count = self._get_silence_count(self._stop_queue,0)
            if (silence_count) / total >= (self._vad_configure.inactivePercent):
                state = self._vad_state_stopspeaking
                self._clear_queue(self._stop_queue)
                print(f"stop speaking: {len(self._start_queue)}, {silence_count}, {total}, {trend}")
        return state, data._audio_frame.buffer 
        
        
            

        
    def process(self, data:AudioFrame) -> tuple[int, bytearray]:
        is_activity = self._is_vad_active(data)
        vad_data = VadDataV2(data, is_activity)
        #判断当前的状态，
        # 我们的bufffer分为：pre、start 和stop 3个buffer
        # vad一共分3个状态，其实是2个大状态：静音，speaking
        # case1: 如果当前状态是non-speaking状态，
        #   就需要将数据保存在pre中；
        #   同时将数据保存在start 中
        #   如果start已经满，则判断是否触发speaking；
        #       如果触发speaking，则将start中的数据全部送入到pre中，并且将pre清空，同时将start清空，同时将当前状态设置为speaking
        #       如果没有触发speaking，则append 到start中
        # case2: 如果当前状态是speaking状态，
        #   就需要将数据保存在stop中；
        #   如果stop已经满，则判断是否触发stop
        #       如果触发stop，则将stop中的数据全部送出去；同时清空stop 清空，并且将当前状态设置为non-speaking
        #       如果没有触发stop，则append 到stop中
        state = self._cur_state
        if self._cur_state == self._vad_state_nonspeaking: #当前状态是静音
            state, data = self._process_start(vad_data)
            if state == self._vad_state_startspeaking:
                self._cur_state = self._vad_state_speaking
            
            return state, data
        if self._cur_state == self._vad_state_speaking:
            state, data = self._process_speaking(vad_data)
            if state == self._vad_state_stopspeaking:
                self._cur_state = self._vad_state_nonspeaking
            return state, data
        #default: shoud never happen
        return int(-100), bytearray()
    
    """
    找到一个v1和v2的异常点：
在v2中，有far=1， voice probe >70 但pitch=0。 但这个时候，还的确在说话中通过音频分析，v1判断出来也是在说话
    """
            
    def _is_vad_active(self, data: AudioFrame) -> bool:
        voice_prob = 0
        rms_prob = 0
        if self._cur_state == self._vad_state_speaking: #说话状态的时候，就是需要做stop 判断，所以参数用stop 的配置
            voice_prob = self._vad_configure.stop_voiceprob
            rms_prob = self._vad_configure.stop_rms
        else:
            voice_prob = self._vad_configure.start_voiceprob
            rms_prob = self._vad_configure.start_rms

        #case2
        #if data.far_field_flag == 1 and data.voice_prob > voice_prob :#and data.pitch > 0 : #voice: from 75 to 50
        #case4: rms > -40
        if data.far_field_flag == 1 and data.voice_prob > voice_prob and data.rms > rms_prob :#and data.pitch > 0 : #voice: from 75 to 50
            return True
        return False
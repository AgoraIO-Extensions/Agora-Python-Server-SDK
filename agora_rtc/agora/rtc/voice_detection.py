import time
import ctypes

import os
import sys
from enum import Enum,IntEnum
from collections import deque
from .agora_base import AudioFrame, AudioParams
import logging
logger = logging.getLogger(__name__)

class  AudioVadConfigV2():
    def __init__(self, preStartRecognizeCount:int=16, startRecognizeCount:int=30, stopRecognizeCount:int=50, 
                 activePercent:float=0.7, inactivePercent:float=0.5, start_voiceprob: int=70, stop_voiceporb:int=50, rmsThreshold:int=-50):
        self.start_recognize_count = startRecognizeCount
        self.pre_start_recognize_count = preStartRecognizeCount
        self.stop_recognize_count = stopRecognizeCount
        self.activePercent = activePercent #percent value = avtivity frames/ total_frames, to determine startspeaking, 
        self.inactivePercent = inactivePercent  #percent value = inactive_frames/ total_frames, to determine stopspeaking
        #voice prob:
        # The lower the gate threshold, the higher the probability that a frame is judged as activity,  
        # which allows the start phase to begin earlier.  
        #   
        # Conversely, the higher the gate threshold, the lower the probability that a frame is judged as activity,  
        # and the higher the probability of being judged as inactivity,  
        # which allows the end phase to begin earlier.
        self.start_voiceprob = start_voiceprob #defautl to 70
        self.stop_voiceprob = stop_voiceporb#default to 50

        #rms: for rmsThreshold, the higher the value, the more sensitive to voice activity.
        # In a quiet environment, it can be set to -50;   
        # in a noisy environment, it can be set to a value between -40 and -30.

        self.start_rms = rmsThreshold #default to -70
        self.stop_rms = rmsThreshold #default to -70
        # for apm mode:
        self.enable_adaptive_rms_threshold : bool = True
        self.adaptive_rms_threshold_factor : float = 0.67 #default to 0.67, and 2/3 to pass
        print(f"vadconfigure start_rms: {self.start_rms}, stop_rms: {self.stop_rms}")
        
        pass

class VadDataV2:
    def __init__(self, data: AudioFrame,   is_activity: bool):
        self._audio_frame = data
        #self.timestamp = time.time()
        self._is_activity = is_activity
        pass

class AudioVadV2():
    _kIntervalPerAudioFrameInMS = 10
    _kMaxChunkSizePer10MSFor16K = 320 #bytes, ??/ for diff sampleRate,its still 
    _kMaxChunkSizePer10MSFor32K = 640 #bytes, ??/ for diff sampleRate
    _kMaxChunkSizePer10MSFor48K = 960 #bytes, ??/ for diff sampleRate
    _vad_state_nonspeaking = 0
    _vad_state_startspeaking = 1
    _vad_state_speaking = 2
    _vad_state_stopspeaking = 3
    
    def __init__(self, config: AudioVadConfigV2):
        self._vad_configure = config
        self._cur_state = self._vad_state_nonspeaking #0: non-speaking, 1-start speaking, 2-speaking, 3-stop speaking
        self._data = bytearray()
        self._start_size = self._vad_configure.pre_start_recognize_count + self._vad_configure.start_recognize_count
        self._start_queue = deque(maxlen=self._start_size)
        self._stop_queue = deque(maxlen=self._vad_configure.stop_recognize_count)
        #trend queue: not impl in this version date: 2024-10-29
        self._trend_queue = None #deque(maxlen=self._vad_configure.stop_recognize_count)  
        self._trend_window = self._vad_configure.stop_recognize_count//2
        self._voice_count : int = 0
        self._silence_count : int = 0
        self._total_voice_rms : int = 0
        self._ref_avg_rms_in_last_session : int = 0

        #convert rms from -120, 0 to range from 0 to 127, respond to db: -127db, to 0db
        self._vad_configure.start_rms = 127 + self._vad_configure.start_rms
        self._vad_configure.stop_rms = 127 + self._vad_configure.stop_rms
        print(f"vad instance start_rms: {self._vad_configure.start_rms}, stop_rms: {self._vad_configure.stop_rms}")
        pass

    def _push_to_start(self, data: VadDataV2) -> tuple[int,bool]:
        self._start_queue.append(data)
        size = len(self._start_queue)
        return size, size >= self._start_size
    def _push_to_stop(self, data: VadDataV2) -> tuple[int,bool]:
        self._stop_queue.append(data)
        size = len(self._stop_queue)
        return size, size >= self._vad_configure.stop_recognize_count
    def _push_to_trend(self, data: VadDataV2) -> tuple[int,bool]:
        self._trend_queue.append(data)
        size = len(self._trend_queue)
        return size, size >= self._trend_window
    def _sum(self,quue: deque) -> int:
        return sum(1 for item in quue if item._is_activity == True)
    def _calculate_sliding_window_ratio(self, arr:deque, window_size:int)-> list[float]:
        ratios = []  
        #slide window
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
        #print(ratios)
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

        if data._is_activity == True:
            self._voice_count += 1
            self._total_voice_rms += data._audio_frame.rms
        else:
            self._voice_count = 0
            self._total_voice_rms = 0
        
        
       
        
        if full == True:
            if self._voice_count >= self._vad_configure.start_recognize_count:
                state = self._vad_state_startspeaking
                #move pre & start to a new bytearray
                
                self._move_deque(bytes, self._start_queue)
                self._clear_queue(self._start_queue)

                #update ref
                self._ref_avg_rms_in_last_session = int(self._total_voice_rms / self._voice_count)
                self._voice_count = 0
                self._total_voice_rms = 0
                self._silence_count = 0
               
                #and clear pre &start
                self._clear_queue(self._stop_queue)
                #print("start speaking:", len(self._stop_queue))
            
        return state, bytes
        
    def _process_speaking(self, data: VadDataV2) -> tuple[int, bytearray]:
        #将数据append 到stop中
        #如果数据满，怎判断是否触发stop
        state = self._cur_state
        size, full = self._push_to_stop(data)
        #print(f"stop: {size}, {full}")

        if data._is_activity == True:
            self._silence_count = 0
        else:
            self._silence_count += 1

        
        if full == True:    
            if self._silence_count >= (self._vad_configure.stop_recognize_count):
                state = self._vad_state_stopspeaking
                self._clear_queue(self._stop_queue)
                self._voice_count = 0
                self._total_voice_rms = 0
                self._silence_count = 0
                #print(f"stop speaking: {len(self._start_queue)}, {silence_count}, {total}, {trend}")
        return state, data._audio_frame.buffer 
        
        
            

        
    def process(self, data:AudioFrame) -> tuple[int, bytearray]:
        is_activity = self._is_vad_active(data)
        vad_data = VadDataV2(data, is_activity)
        # Determine the current state.  
            # The buffer  divided into three parts: pre, start, and stop.  
            # The Voice Activity Detection (VAD) has two major states: silent and speaking.  
            # Case 1: If the current state is non-speaking,  
            #   save the data into 'pre';  
            #   simultaneously save the data into 'start';  
            #   if 'start' is full, determine if speaking is triggered:  
            #       if speaking is triggered, move all data in pre and start to a new bytearray, and  clear both 'pre' and 'start',  
            #       then set the current state to speaking.  
            #       if speaking is not triggered, append the data to 'start'.  
            # Case 2: If the current state is speaking,  
            #   save the data in 'stop';  
            #   if 'stop' is full, determine if stop is triggered:  
            #       if stop is triggered, move all data in 'stop' to a new bytearray, and clear 'stop'
            #       and set the current state to non-speaking.  
            #       if stop is not triggered, append the data to 'stop'.
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
    
    def _get_ref_active_avg_rms(self) -> int:
        if self._vad_configure.enable_adaptive_rms_threshold and self._ref_avg_rms_in_last_session > 0:
            return int(float(self._ref_avg_rms_in_last_session)*self._vad_configure.adaptive_rms_threshold_factor) #half of avg as threshold value
        return self._vad_configure.start_rms
       
    """
    def _is_vad_active(self, data: AudioFrame) -> bool:
    """
            
    def _is_vad_active(self, data: AudioFrame) -> bool:
        voice_prob = 0
        rms_prob = 0
        if self._cur_state == self._vad_state_speaking: 
            voice_prob = self._vad_configure.stop_voiceprob
            rms_prob = self._vad_configure.stop_rms
        else:
            voice_prob = self._vad_configure.start_voiceprob
            rms_prob = self._vad_configure.start_rms

        #case2
        #if data.far_field_flag == 1 and data.voice_prob > voice_prob :#and data.pitch > 0 : #voice: from 75 to 50
        #case4: rms > -40
        #if data.far_field_flag == 1 and data.voice_prob > voice_prob and data.rms > rms_prob :#and data.pitch > 0 : #voice: from 75 to 50
        #date: 2025-10-29 for sdk which support apm filter, and in this version, we don't need to use farfield flag to detect speech, so we don't need to use farfield flag to detect speech
        refRms = self._get_ref_active_avg_rms()
        active = (data.voice_prob == 1) or (data.rms > refRms)
        #print(f"active: {active}, voice_prob: {data.voice_prob}, rms: {data.rms}, refRms: {refRms}")
        if active:
            return True
        return False
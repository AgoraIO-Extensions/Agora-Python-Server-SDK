#!env python
import threading
import time
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame
from agora.rtc.audio_pcm_data_sender import AudioPcmDataSender



class AudioStreamConsumer:
    def __init__(self,pcm_sender:AudioPcmDataSender) -> None:
        self._lock = threading.Lock()
        self._data = bytearray()
        self._interval = 0.05 #50ms 
        self._timer = threading.Timer(self._interval, self._consume)
        self._timer.start()
        self._start_time = 0
        self._consumed_packages = 0
        self._run = True
        self._event = threading.Event()
        self._pcm_sender = pcm_sender
        
    def push_pcm_data(self, data):
        #add to buffer, lock
        with self._lock:
            self._data += data
    def _consume(self):
        with self._lock:
            # cal current duration
            cur_time = time.time()*1000
            elapsed_time = cur_time - self._start_time
            wanted_packages = int(elapsed_time/10) - self._consumed_packages

            if wanted_packages > 18:  # 180ms, a new session
                wanted_packages = 18
                self._start_time = cur_time
                self._consumed_packages = -18
                print("audio_stream_consumer:new session")
            data_len = len(self._data)
            wanted_packages = min(wanted_packages, data_len//320)
            if self._data and wanted_packages > 0:
                #pop data
                frame_size = 320*wanted_packages
                frame_buf = bytearray(frame_size)
                frame_buf[:] = self._data[:frame_size]
                self._data = self._data[frame_size:]
                #print("pop data:", len(frame_buf))
                #send data
                frame = PcmAudioFrame()
                frame.data = frame_buf
                frame.timestamp = 0
                frame.samples_per_channel = 160*wanted_packages
                frame.bytes_per_sample = 2
                frame.number_of_channels = 1
                frame.sample_rate = 16000
                ret = self._pcm_sender.send_audio_pcm_data(frame)
                #print("second,ret=",wanted_packages, ret)
                self._consumed_packages += wanted_packages
                print("audio_stream_consumer:consumed_packages:", self._consumed_packages, wanted_packages)
                

            #restart timer
            if self._run:
                self._timer = threading.Timer(self._interval, self._consume)
                self._timer.start()
            else:
                self._event.set()
    def relase(self):
        print("audio_stream_consumer:release")
        self._run = False
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
            print("audio_stream_consumer:cancel timer")
        else:
            self._event.wait()
        self._timer = None
        self._data = None
        self._event = None
    def clear(self):
        with self._lock:
            self._data = bytearray()
            

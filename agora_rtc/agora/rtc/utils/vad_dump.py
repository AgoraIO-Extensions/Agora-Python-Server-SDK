#!env python
import time
from datetime import datetime
import logging
import os
import struct
from agora.rtc.agora_base import AudioFrame
logger = logging.getLogger(__name__)



"""
## VadDump helper class
"""
#buffer manager for vaddump: high performance buffer manager for vaddump

class BufferManager:
    """High-performance buffer manager using struct.pack
    
    Performance benchmarks (320 bytes, 100k iterations):
    - struct.pack: 0.016-0.019 seconds (FASTEST)
    - ctypes.memset: 0.107 seconds (5.6x slower)
    - ctypes loop: 0.686 seconds (36x slower)
    """
    
    def __init__(self, initial_size=320):
        self.size = initial_size
        self.buffer = bytearray(self.size)
    def resize(self, new_size: int):
        if new_size != self.size:
            self.size = new_size
            self.buffer = bytearray(self.size)
    def fill_zero(self):
        self.fill_int16(0)
    
    def fill_int16(self, value: int):
        """Fill buffer with int16 value using struct.pack (fastest method)
        
        Args:
            value: int16 value to fill (-32768 to 32767)
        
        Returns:
            bytearray: The filled buffer
        """
        # Pack value as little-endian int16 and repeat
        pattern = struct.pack('<h', value)
        self.buffer[:] = pattern * (self.size // 2)
        return self.buffer


class VadDump():
    def __init__(self, path: str) -> None:
        self._file_path = path
        self._count = 0
        self._frame_count = 0
        self._is_open = False
        self._source_file = None
        self._label_file = None
        self._vad_file = None
        self._voice_prob_file = None
        self._rms_file = None
        self._pitch_file = None
        self._buffer_manager = BufferManager(320)
        #check path is existed or not? if not, create new dir
        if self._check_directory_exists(path) is False:
            os.makedirs(path)
        # make suddirectory : ("%s/%04d%02d%02d%02d%02d%02d
        now = datetime.now()
        #format to YYYYMMDDHHMMSS
        self._file_path = "%s/%04d%02d%02d%02d%02d%02d" % (path, now.year, now.month, now.day, now.hour, now.minute, now.second)
        os.makedirs(self._file_path)


        pass
    def _check_directory_exists(self, path: str) -> bool:
        return os.path.exists(path) and os.path.isdir(path)
    def _create_vad_file(self) -> None:
        self._close_vad_file()
        #create a new one
        vad_file_path = "%s/vad_%d.pcm" % (self._file_path, self._count)
        self._vad_file = open(vad_file_path, "wb")
        #increment the count
        self._count += 1
        pass
    def _close_vad_file(self) -> None:
        if self._vad_file:
            self._vad_file.close()
            self._vad_file = None
        pass
    def open(self) -> int:
        if self._is_open is True:
            return 1
        self._is_open = True
        #open source file
        source_file_path = self._file_path + "/source.pcm"
        self._source_file = open(source_file_path, "wb") 
        #open label file
        label_file_path = self._file_path + "/label.txt"
        self._label_file = open(label_file_path, "w")
        #rms
        rms_file_path = self._file_path + "/rms.pcm"
        self._rms_file = open(rms_file_path, "wb")
        #pitch
        pitch_file_path = self._file_path + "/pitch.pcm"
        self._pitch_file = open(pitch_file_path, "wb")
        #voice prob
        voice_prob_file_path = self._file_path + "/voice_prob.pcm"
        self._voice_prob_file = open(voice_prob_file_path, "wb")

        #open vad file
        pass
    def write(self, frame:AudioFrame, vad_result_bytes: bytearray, vad_result_state : int) -> None:
        #write pcm to source
        if self._is_open is False:
            return
        if self._source_file:
            self._source_file.write(frame.buffer)
        # fomat frame 's label informaiton and write to label file
        if self._label_file:
            label_str = "ct:%d fct:%d state:%d far:%d vop:%d rms:%d pitch:%d mup:%d\n" % (self._count, self._frame_count,vad_result_state, frame.far_field_flag, frame.voice_prob, frame.rms, frame.pitch, frame.music_prob)
            self._label_file.write(label_str)
        #adjut buffer size if needed
        self._buffer_manager.resize(len(frame.buffer))
        #write rms to buffer
        self._buffer_manager.fill_int16(frame.rms*127)
        if self._rms_file:
            self._rms_file.write(self._buffer_manager.buffer)
        #write pitch to buffe
        self._buffer_manager.fill_int16(frame.pitch)
        if self._pitch_file:
            self._pitch_file.write(self._buffer_manager.buffer)
        #write voice prob to buffer
        self._buffer_manager.fill_int16(frame.voice_prob*127*127)
        if self._voice_prob_file:
            self._voice_prob_file.write(self._buffer_manager.buffer)
        #write to vad result
        if vad_result_state == 1: # start speaking
            #open new vad file and write header
            self._create_vad_file()
            if self._vad_file:
                self._vad_file.write(vad_result_bytes)
        if vad_result_state == 2:
            if self._vad_file:
                self._vad_file.write(vad_result_bytes)
        if vad_result_state == 3:
            if self._vad_file:
                self._vad_file.write(vad_result_bytes)
            self._close_vad_file()
        #increment frame counter
        self._frame_count += 1
        pass
    def close(self) -> None:
        if self._is_open == False:
            return 
        self._is_open = False
        if self._vad_file:
            self._close_vad_file()
            self._vad_file = None
        if self._label_file:
            self._label_file.close()
            self._label_file = None
        self._close_vad_file()

        if self._source_file:
            self._source_file.close()
            self._source_file = None
        if self._rms_file:
            self._rms_file.close()
            self._rms_file = None
        if self._pitch_file:
            self._pitch_file.close()
            self._pitch_file = None
        if self._voice_prob_file:
            self._voice_prob_file.close()
            self._voice_prob_file = None

        # assign to None
        self._count = 0
        self._frame_count = 0
        self._file_path = None

        pass
#!env python
import time
from datetime import datetime
import logging
import os
from agora.rtc.agora_base import AudioFrame
logger = logging.getLogger(__name__)



"""
## VadDump helper class
"""
class VadDump():
    def __init__(self, path: str) -> None:
        self._file_path = path
        self._count = 0
        self._frame_count = 0
        self._is_open = False
        self._source_file = None
        self._label_file = None
        self._vad_file = None
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

        # assign to None
        self._count = 0
        self._frame_count = 0
        self._file_path = None

        pass
#!env python
import pyaudio
import numpy as np
import time
import logging
import turtle

logger = logging.getLogger(__name__)




class AudioCollector:
    def __init__(self):
        # 音频参数设置
        self.FORMAT = pyaudio.paInt16        # 16位采样
        self.CHANNELS = 1                    # 单声道
        self.RATE = 48000                    # 采样率 48kHz
        self.CHUNK = int(self.RATE * 0.02)   # 20ms的数据量 = 48000 * 0.02 = 960个采样点
        self.MIC_INDEX = 0                   # 默认麦克风设备索引
        
        # 初始化 PyAudio
        self.audio = pyaudio.PyAudio()
        
        # 初始化音频流
        self.stream = None
        
    def list_devices(self):
        """列出所有可用的音频设备"""
        print("\n可用的音频设备：")
        for i in range(self.audio.get_device_count()):
            dev_info = self.audio.get_device_info_by_index(i)
            print(f"设备 {i}: {dev_info['name']}")
            
    def start_stream(self, device_index=None):
        """启动音频流"""
        if device_index is not None:
            self.MIC_INDEX = device_index
            
        try:
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=self.MIC_INDEX,
                frames_per_buffer=self.CHUNK
            )
            print(f"音频流已启动: {self.RATE}Hz, {self.CHANNELS}声道, {self.CHUNK}采样点/块")
            return True
        except Exception as e:
            print(f"启动音频流失败: {str(e)}")
            return False
            
    def read_chunk(self):
        """读取一个数据块"""
        if self.stream is None:
            return None
            
        try:
            # 读取原始数据
            raw_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            
            return raw_data
        except Exception as e:
            print(f"读取音频数据失败: {str(e)}")
            return None
            
    def stop_stream(self):
        """停止音频流"""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
    def cleanup(self):
        """清理资源"""
        self.stop_stream()
        if self.audio is not None:
            self.audio.terminate()
            self.audio = None
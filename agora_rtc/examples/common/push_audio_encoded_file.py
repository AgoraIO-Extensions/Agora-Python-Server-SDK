#!env python

import itertools
import av
from agora.rtc.agora_base import AudioCodecType, EncodedAudioFrameInfo
from agora.rtc.rtc_connection import RTCConnection
import asyncio
import ctypes

from asyncio import Event
import logging
logger = logging.getLogger(__name__)


async def push_encoded_audio_from_file(connection: RTCConnection, audio_file_path, _exit: Event):
    sendinterval = 0.1
    
    container = av.open(audio_file_path)
    sample_rate = 48000
    channels = 1
    for stream in container.streams:
        if stream.type == 'audio':
            sample_rate = stream.sample_rate
            channels = stream.channels
            logger.info(f"Audio stream: sample rate = {sample_rate}, channels = {channels}")
            break
    while True:
        for packet in itertools.cycle(container.demux()):
            if _exit.is_set():
                logger.info("exit")
                return
            if packet.stream.type == 'audio':
                frame = EncodedAudioFrameInfo()
                frame.speech = 0
                frame.codec = AudioCodecType.AUDIO_CODEC_AACLC  # https://doc.shengwang.cn/api-ref/rtc-server-sdk/cpp/structagora_1_1rtc_1_1_encoded_audio_frame_info.html
                frame.sample_rate = sample_rate
                frame.samples_per_channel = 1024
                frame.number_of_channels = channels
                frame.send_even_if_empty = 1
                '''
                NOTE: need convert cytpe.ptr ie. c++ memory pointer to python bytes or bytearray without copy
                mv = memoryview((ctypes.c_char * buffer_size).from_address(ctypes.addressof(buffer_ptr.contents)))

                # 转换为 bytes 或 bytearray（仍无拷贝）
                bytes_data = mv.tobytes()  # 如果需要不可变数据
                byte_array = bytearray(mv)  # 如果需要可变数据
                '''
                #cast from int to void_P_ptr
                #validity check
                if packet.buffer_ptr == 0:
                    logger.info("**** packet.buffer_ptr is 0 **********")
                    continue
                # cast from int to bytes without copy!!!!but user Must care the life cycle of the pointer
                # The pointer returned by packet.buffer_ptr has the same life cycle as the packet
                # In your case, packet might be freed when you've processed all packets, so the pointer is invalid.
                buffer_ptr = ctypes.cast(packet.buffer_ptr, ctypes.POINTER(ctypes.c_void_p))
                mv = memoryview((ctypes.c_char * packet.size).from_address(ctypes.addressof(buffer_ptr.contents)))
                bytes_data = mv.tobytes()
                ret = connection.push_audio_encoded_data(bytes_data, frame)
                time_base = packet.stream.time_base
                duration_in_seconds = packet.duration * time_base
                logger.info(f"Read audio packet with size {packet.size} bytes, PTS {packet.pts}, DTS {packet.dts}, duration_in_seconds={duration_in_seconds}")
                
                #note: 1. for send encoded audio, the frequency must be same  the package duration.  or in receive side, the audio will be played with a gap(caused by overflow and underflow)
                await asyncio.sleep(duration_in_seconds)

#!env python

import itertools
import av
from agora.rtc.agora_base import AudioCodecType, EncodedAudioFrameInfo
from agora.rtc.audio_encoded_frame_sender import AudioEncodedFrameSender

from asyncio import Event
import logging
logger = logging.getLogger(__name__)


async def push_encoded_audio_from_file(audio_sender: AudioEncodedFrameSender, audio_file_path, _exit: Event):
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
                ret = audio_sender.send_encoded_audio_frame(packet.buffer_ptr, packet.size, frame)
                time_base = packet.stream.time_base
                duration_in_seconds = packet.duration * time_base
                logger.info(f"Read audio packet with size {packet.size} bytes, PTS {packet.pts}, DTS {packet.dts}, duration_in_seconds={duration_in_seconds}")
                
                await asyncio.sleep(duration_in_seconds)

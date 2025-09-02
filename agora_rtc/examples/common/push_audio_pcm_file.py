#!env python

from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
from agora.rtc.utils.audio_consumer import AudioConsumer
from asyncio import Event
from agora.rtc.rtc_connection import RTCConnection
import asyncio
import datetime
import logging
import random
logger = logging.getLogger(__name__)

def file_to_consumer(file, buffer, consumer:AudioConsumer):
    while True:
        success = file.readinto(buffer)
        if not success:
            file.seek(0)
            return
        consumer.push_pcm_data(buffer)
    pass


async def push_pcm_data_from_file(sample_rate, num_of_channels, connection: RTCConnection, audio_file_path, _exit: Event):
    with open(audio_file_path, "rb") as audio_file:
        pcm_sendinterval = 5  #5s send one frame
        pcm_count = 0
        send_size = int(sample_rate*num_of_channels*pcm_sendinterval*2)
        frame_buf = bytearray(send_size)
        interval = 0.06 # 60ms
        bytes_in_ms = int(sample_rate * num_of_channels * 2 / 1000)

      
        while not _exit.is_set():
            # check rest len in consumer
            ret = connection.is_push_to_rtc_completed()
            if ret == True:
                read_len = audio_file.readinto(frame_buf)

                if read_len < bytes_in_ms*100: #at least 100 frames
                    audio_file.seek(0)
                    continue
                #round to multiple of bytes_in_ms
                #try memoryview and slice to avoid copy data
                read_len = int(read_len//bytes_in_ms)*bytes_in_ms
                mv = memoryview(frame_buf)
                slice_data = mv[:read_len]
                connection.push_audio_pcm_data(slice_data, sample_rate, num_of_channels)
            
            await asyncio.sleep(interval)
            
        frame_buf = None
       


async def my_conn_life_timer(cevent, delay):
    logger.info(f"conn_life_timer: {delay}")
    await asyncio.sleep(delay)
    logger.info(f"conn_life_timer: {delay} finish")
    cevent.set()

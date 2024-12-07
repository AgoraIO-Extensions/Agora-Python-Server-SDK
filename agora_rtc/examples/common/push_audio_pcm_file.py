#!env python

from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
from agora.rtc.utils.audio_consumer import AudioConsumer
from asyncio import Event
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


async def push_pcm_data_from_file(sample_rate, num_of_channels, pcm_data_sender: AudioPcmDataSender, audio_file_path, _exit: Event):
    with open(audio_file_path, "rb") as audio_file:
        pcm_sendinterval = 0.1
        pcm_count = 0
        send_size = int(sample_rate*num_of_channels*pcm_sendinterval*2)
        frame_buf = bytearray(send_size)
        interval = 0.06 # 60ms
        audio_consumer = AudioConsumer(pcm_data_sender,sample_rate, num_of_channels)
        # at begining:  read all data to consumer
        file_to_consumer(audio_file, frame_buf, audio_consumer)
        while not _exit.is_set():
            # check rest len in consumer
            remain_len = audio_consumer.len()
            if remain_len < send_size*interval*150: #interval*1000/10 *1.5. where 1.5 is the redundancy coeficient
                file_to_consumer(audio_file, frame_buf, audio_consumer)
            ret = audio_consumer.consume()
            logger.info(f"send pcm: count,ret={ret}")
            
            await asyncio.sleep(interval)
            
        frame_buf = None
        audio_consumer.release()


async def my_conn_life_timer(cevent, delay):
    logger.info(f"conn_life_timer: {delay}")
    await asyncio.sleep(delay)
    logger.info(f"conn_life_timer: {delay} finish")
    cevent.set()

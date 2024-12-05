#!env python

from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
from agora.rtc.utils.audio_consumer import AudioConsumer
from common.pacer import Pacer
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
        pacer_pcm = Pacer(pcm_sendinterval)
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


async def push_pcm_data_from_file2(sample_rate, num_of_channels, pcm_data_sender: AudioPcmDataSender, audio_file_path):

    timer_conn_exit = asyncio.Event()
    asyncio.create_task(my_conn_life_timer(timer_conn_exit, 5))

    with open(audio_file_path, "rb") as audio_file:
        pcm_sendinterval = 0.1
        pacer_pcm = Pacer(pcm_sendinterval)
        pcm_count = 0
        send_size = int(sample_rate*num_of_channels*pcm_sendinterval*2)
        frame_buf = bytearray(send_size)
        while not timer_conn_exit.is_set():
            success = audio_file.readinto(frame_buf)
            if not success:
                audio_file.seek(0)
                continue
            frame = PcmAudioFrame(
                data=frame_buf,
                timestamp=0,
                samples_per_channel=int(sample_rate*pcm_sendinterval),
                bytes_per_sample=2,
                number_of_channels=num_of_channels,
                sample_rate=sample_rate
            )
            ret = pcm_data_sender.send_audio_pcm_data(frame)
            pcm_count += 1
            logger.info(f"send pcm: count,ret={pcm_count}, {ret}, {send_size}, {pcm_sendinterval}")
            await pacer_pcm.apace_interval(0.1)
        frame_buf = None

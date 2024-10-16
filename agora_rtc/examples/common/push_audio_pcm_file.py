#!env python

from asyncio import Event
import logging
logger = logging.getLogger(__name__)
from common.pacer import Pacer
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame, AudioPcmDataSender
async def push_pcm_data_from_file(sample_rate, num_of_channels , pcm_data_sender:AudioPcmDataSender, audio_file_path, _exit:Event):
    with open(audio_file_path, "rb") as audio_file:
        pcm_sendinterval = 0.1
        pacer_pcm = Pacer(pcm_sendinterval)
        pcm_count = 0
        send_size = int(sample_rate*num_of_channels*pcm_sendinterval*2)
        frame_buf = bytearray(send_size)            
        while not _exit.is_set():
            success = audio_file.readinto(frame_buf)
            if not success:
                audio_file.seek(0)
                continue
            frame = PcmAudioFrame()
            frame.data = frame_buf
            frame.timestamp = 0
            frame.samples_per_channel = int(sample_rate * pcm_sendinterval)
            frame.bytes_per_sample = 2
            frame.number_of_channels = num_of_channels
            frame.sample_rate = sample_rate
            ret = pcm_data_sender.send_audio_pcm_data(frame)
            pcm_count += 1
            logger.info(f"send pcm: count,ret={pcm_count}, {ret}, {send_size}, {pcm_sendinterval}")
            await pacer_pcm.apace_interval(0.1)
        frame_buf = None
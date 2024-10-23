#!env python

from agora.rtc.video_frame_sender import ExternalVideoFrame, VideoFrameSender
from common.pacer import Pacer
from asyncio import Event
import asyncio
import datetime
import logging
import random
logger = logging.getLogger(__name__)


async def push_yuv_data_from_file(width, height, fps, video_sender: VideoFrameSender, video_file_path, _exit: Event):
    # logger.warning(f'push_yuv_data_from_file time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}')

    first_frame = None
    with open(video_file_path, "rb") as video_file:
        yuv_sendinterval = 1.0/fps
        pacer_yuv = Pacer(yuv_sendinterval)
        yuv_count = 0
        yuv_len = int(width*height*3/2)
        frame_buf = bytearray(yuv_len)
        while not _exit.is_set():
            success = video_file.readinto(frame_buf)
            if not success:
                video_file.seek(0)
                continue
            if first_frame is None:
                first_frame = frame_buf
            frame = ExternalVideoFrame()
            frame.buffer = frame_buf
            frame.type = 1
            frame.format = 1
            frame.stride = width
            frame.height = height
            frame.timestamp = 0
            frame.metadata = "hello metadata"
            frame.alpha_buffer = first_frame
            ret = video_sender.send_video_frame(frame)
            yuv_count += 1
            logger.info("send yuv: count,ret=%d, %s", yuv_count, ret)
            await pacer_yuv.apace_interval(yuv_sendinterval)
        frame_buf = None


async def my_conn_life_timer(cevent, delay):
    logger.info(f"conn_life_timer: {delay}")
    await asyncio.sleep(delay)
    logger.info(f"conn_life_timer: {delay} finish")
    cevent.set()


async def push_yuv_data_from_file2(width, height, fps, video_sender: VideoFrameSender, video_file_path):
    # logger.warning(f'push_yuv_data_from_file time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}')
    timer_conn_exit = asyncio.Event()
    asyncio.create_task(my_conn_life_timer(timer_conn_exit, 5))

    with open(video_file_path, "rb") as video_file:
        yuv_sendinterval = 1.0/fps
        pacer_yuv = Pacer(yuv_sendinterval)
        yuv_count = 0
        yuv_len = int(width*height*3/2)
        frame_buf = bytearray(yuv_len)
        while not timer_conn_exit.is_set():
            success = video_file.readinto(frame_buf)
            if not success:
                video_file.seek(0)
                continue
            frame = ExternalVideoFrame()
            frame.buffer = frame_buf
            frame.type = 1
            frame.format = 1
            frame.stride = width
            frame.height = height
            frame.timestamp = 0
            frame.metadata = "hello metadata"
            ret = video_sender.send_video_frame(frame)
            yuv_count += 1
            logger.info("send yuv: count,ret=%d, %s", yuv_count, ret)
            await pacer_yuv.apace_interval(yuv_sendinterval)
        frame_buf = None

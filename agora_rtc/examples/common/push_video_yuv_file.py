#!env python

from agora.rtc.video_frame_sender import ExternalVideoFrame, VideoFrameSender
from common.pacer import Pacer
from asyncio import Event
import datetime
import logging
logger = logging.getLogger(__name__)


async def push_yuv_data_from_file(width, height, fps, video_sender: VideoFrameSender, video_file_path, _exit: Event):
    # logger.warning(f'push_yuv_data_from_file time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}')
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

#!env python

from asyncio import Event
import logging
logger = logging.getLogger(__name__)
from common.pacer import Pacer
from agora.rtc.video_encoded_image_sender import EncodedVideoFrameInfo, VideoEncodedImageSender
from agora.rtc.agora_base import AudioCodecType
import av
import itertools


async def push_encoded_video_from_file(video_sender:VideoEncodedImageSender, video_file_path, _exit:Event):
    frame_rate = 30
    pacer = Pacer(1.0/frame_rate)
    count = 0
    width = 352
    height = 288
    container = av.open(video_file_path)
    for stream in container.streams:
        if stream.type == 'video':
            width = stream.width
            height = stream.height
            codec_name = stream.codec.name
            print(f"codec name: {codec_name}")
            logger.info(f"Video stream: width = {width}, height = {height}， codec_name = {codec_name}")
            frame_rate = int(stream.average_rate)
            if frame_rate is not None:
                print(f"frame_rate: {frame_rate}")
            else:
                print("frame_rate is None")
            break
    while  True:
        for packet in itertools.cycle(container.demux()):
            if _exit.is_set():
                logger.info("exit")
                return
            if packet.stream.type == 'video':
                logger.info(f"Read packet with size {packet.size} bytes, PTS {packet.pts}")
                is_keyframe = packet.is_keyframe
                if is_keyframe:
                    logger.info(f"Keyframe packet with size {packet.size} bytes, PTS {packet.pts}")
                else:
                    logger.info(f"Non-keyframe packet with size {packet.size} bytes, PTS {packet.pts}")
                encoded_video_frame_info = EncodedVideoFrameInfo()
                encoded_video_frame_info.codec_type = 2            
                encoded_video_frame_info.width = width
                encoded_video_frame_info.height = height
                encoded_video_frame_info.frames_per_second = frame_rate                        
                if is_keyframe:
                    encoded_video_frame_info.frame_type = 3
                else:
                    encoded_video_frame_info.frame_type = 4        
                ret = video_sender.send_encoded_video_image(packet.buffer_ptr, packet.buffer_size ,encoded_video_frame_info)        
                count += 1
                logger.info(f"count,ret={count}, {ret}")
                await pacer.apace_interval(1.0/frame_rate)


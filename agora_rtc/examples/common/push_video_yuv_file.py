#!env python

from agora.rtc.video_frame_sender import ExternalVideoFrame, VideoFrameSender
from common.pacer import Pacer
from asyncio import Event
import asyncio
import datetime
import logging
import random
from PIL import Image 
import numpy as np
from pathlib import Path
import time
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
            #frame.alpha_buffer = first_frame
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

def jpeg_to_bytearray(file_path):
        start = time.time()*1000
        image = Image.open(file_path)  
        open_time = time.time()*1000
            
        # 将图像转换为RGB模式（如果需要）  
        image = image.convert('RGBA')  
        convert_time = time.time()*1000
        
        # 访问图像数据（例如，获取像素值）  
        #pixels = image.load()  
        pixels = list(image.getdata())
        width, height = image.size  
        pix_time = time.time()*1000

        
        np_array = np.array(image)  # 将图像转换为numpy数组  
        np_time = time.time()*1000
        #byte_data = np_array.tobytes()  # 直接将numpy数组转换为bytearray（实际上是bytes，但可以转换为bytearray）  
        # 注意：tobytes()方法返回的是bytes对象，如果你确实需要bytearray，可以这样做：  
        byte_data = bytearray(np_array.tobytes())  
        bytes_time = time.time()*1000
        image.close()
        print(f"open time: {open_time-start}, convert: {convert_time-open_time}, px time: {pix_time - convert_time}, np: {np_time - pix_time}, byte: {bytes_time - np_time}")
        return width, height, byte_data

async def push_jpeg_from_file(path, video_sender, fps, _exit:Event):
    #file_path = '/Users/weihognqin/Downloads/zhipusource/image_67208e95d8c26bb498989948_1730186920.788217.jpeg'
    # 指定你想要遍历的目录路径 ， format： '/path/to/your/directory'
    print("path:", path)
    directory_path = Path(path)  
    
    # 获取目录中的所有文件和子目录对象（不包括子目录中的文件）  
    items = directory_path.iterdir()  

    
    # 如果你只想获取文件而不包括目录，可以进一步过滤  
    file_names = [f for f in items if f.is_file()]  
    
    # 获取文件名列表  
    #file_names = [f.name for f in files_only]  
    rgb_count = 0
    interval = 1.0/30

    pacer = Pacer(interval)

    #simulate only 3 jpges
    bytes_data = []
    for file_name in file_names:
        post_ext = file_name.suffix
        now = time.time()*1000
        print(f"----sufix:  {post_ext}, {now}")
        if post_ext.lower() != ".jpeg":
            continue
        

    
        width, height, byte_data = jpeg_to_bytearray(file_name)
        bytes_data.append(byte_data)



    while  not  _exit.set():
        for bytes in bytes_data :
            
            rgb_len = int(width*height*4)
            frame_buf = bytes
            #while not _exit.is_set():
            
                
            frame = ExternalVideoFrame()
            frame.buffer = frame_buf
            frame.type = 1
            frame.format = 4 #RGBA
            frame.stride = width
            frame.height = height
            frame.timestamp = 0
            frame.metadata = "hello metadata"
            #frame.alpha_buffer = first_frame
            ret = video_sender.send_video_frame(frame)
            rgb_count += 1
            logger.info("send jpg: count,ret=%d, %d, %d, %d, %d", rgb_count, ret, width, height,time.time()*1000)
            await pacer.apace_interval(interval)
            #asyncio.sleep(1)
                #pacer_yuv.apace_interval(yuv_sendinterval)
            frame_buf = None
            #image.close()


#!env python

from agora.rtc.video_frame_sender import ExternalVideoFrame, VideoFrameSender

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
            frame.metadata = bytearray(b'hello metadata')
            #frame.alpha_buffer = first_frame
            ret = video_sender.send_video_frame(frame)
            yuv_count += 1
            logger.info("send yuv: count,ret=%d, %s", yuv_count, ret)
            await asyncio.sleep(yuv_sendinterval)
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
            frame.metadata = bytearray(b'hello metadata')
            ret = video_sender.send_video_frame(frame)
            yuv_count += 1
            logger.info("send yuv: count,ret=%d, %s", yuv_count, ret)
            
            await asyncio.sleep(yuv_sendinterval)
        frame_buf = None

""""
# some data for jpeg_to_bytearray:
#NOTE:1
    # Assuming `image_data` is a byte stream containing image data,
    # you can avoid writing to a file and instead operate directly in memory by using the following approach:
    
    # `BytesIO` is used to create an in-memory file-like object from the byte stream.
    from io import BytesIO
    from PIL import Image
 
    # `image_data` should be a bytes object containing the JPEG image data.
    # Create an in-memory file-like object from the byte stream.
    image_stream = BytesIO(image_data)
    image = Image.open(image_stream)
    # Now you can use the `image` object as you would with an image loaded from a file.
#NOTE2:
    # test data from file: the jpeg file is 1920*1080 
    open time: 0.8271484375, convert: 7.343017578125, px time: 0.0009765625, np: 1.93701171875, byte: 1.255859375, total: 11.364013671875
    ----sufix:  .jpeg, 1731293372695.532
    open time: 0.3173828125, convert: 7.106689453125, px time: 0.0009765625, np: 1.93994140625, byte: 1.2353515625, total: 10.600341796875
    ----sufix:  .jpeg, 1731293372706.36
    open time: 0.328125, convert: 8.114013671875, px time: 0.0009765625, np: 1.912109375, byte: 1.033935546875, total: 11.38916015625
    ----sufix:  .jpeg, 1731293372717.9739
    open time: 0.324951171875, convert: 7.613037109375, px time: 0.001953125, np: 1.737060546875, byte: 1.010009765625, total: 10.68701171875
    ----sufix:  .jpeg, 1731293372728.8909
    open time: 0.35205078125, convert: 7.2861328125, px time: 0.0009765625, np: 2.15185546875, byte: 0.88818359375, total: 10.67919921875
"""
def jpeg_to_bytearray(file_path):
        start = time.time()*1000
        image = Image.open(file_path)  
        open_time = time.time()*1000
            
        # 将图像转换为RGB模式（如果需要）  
        image = image.convert('RGBA')  #RGBA
        convert_time = time.time()*1000
        
        # 访问图像数据（例如，获取像素值）  
        width, height = image.size  
        pix_time = time.time()*1000

        #convert to bytearray
        np_array = np.array(image)  # 将图像转换为numpy数组  
        np_time = time.time()*1000
        #byte_data = np_array.tobytes()  # 直接将numpy数组转换为bytearray（实际上是bytes，但可以转换为bytearray）  
        # 注意：tobytes()方法返回的是bytes对象，如果你确实需要bytearray，可以这样做：  
        byte_data = bytearray(np_array.tobytes())  
        bytes_time = time.time()*1000
        image.close()
        print(f"open time: {open_time-start}, convert: {convert_time-open_time}, px time: {pix_time - convert_time}, np: {np_time - pix_time}, byte: {bytes_time - np_time}, total: {bytes_time - start}")
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
    interval = 1.0/fps

 

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
        print(f"width: {width}, height: {height},len: {len(byte_data)}")
    

    print("finnish: bytes_data:", len(bytes_data))


    while  not  _exit.is_set():
        for bytes in bytes_data :
            
            rgb_len = int(width*height*4)
            frame_buf = bytes
            print(f"rgb_len: {rgb_len}, len: {len(frame_buf)}")
            
            
                
            frame = ExternalVideoFrame()
            frame.buffer = frame_buf
            frame.type = 1
            frame.format = 4 #RGBA,I420
            frame.stride = width
            frame.height = height
            frame.timestamp = 0
            frame.metadata = bytearray(b'hello metadata')
            #frame.alpha_buffer = first_frame
            ret = video_sender.send_video_frame(frame)
            rgb_count += 1
            logger.info("send jpg: count,ret=%d, %d, %d, %d, %d", rgb_count, ret, width, height,time.time()*1000)

            await asyncio.sleep(interval)
           
            frame_buf = None
            #image.close()


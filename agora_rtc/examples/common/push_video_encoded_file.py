#!env python
import asyncio
import itertools
import av
import av.packet
from agora.rtc.agora_base import AudioCodecType
from agora.rtc.video_encoded_image_sender import EncodedVideoFrameInfo
from agora.rtc.rtc_connection import RTCConnection

from asyncio import Event
import logging
import ctypes
import struct
import os
logger = logging.getLogger(__name__)


def convert_intptr_to_bytes_without_copy(int_ptr:int, size:int):
    '''
    NOTE: need convert cytpe.ptr ie. c++ memory pointer to python bytes or bytearray without copy
    mv = memoryview((ctypes.c_char * buffer_size).from_address(ctypes.addressof(buffer_ptr.contents)))

    # 转换为 bytes 或 bytearray（仍无拷贝）
    bytes_data = mv.tobytes()  # 如果需要不可变数据
    byte_array = bytearray(mv)  # 如果需要可变数据
    '''
    #cast from int to void_P_ptr
    #validity check
    if int_ptr == 0:
        logger.info("**** int_ptr is 0 **********")
        return None
    # cast from int to bytes without copy!!!!but user Must care the life cycle of the pointer
    # The pointer returned by packet.buffer_ptr has the same life cycle as the packet
    # In your case, packet might be freed when you've processed all packets, so the pointer is invalid.
    buffer_ptr = ctypes.cast(int_ptr, ctypes.POINTER(ctypes.c_void_p))
    mv = memoryview((ctypes.c_char * size).from_address(ctypes.addressof(buffer_ptr.contents)))
    bytes_data = mv.tobytes()
    return bytes_data

#can work in file write: by wei on 0313
def convert_to_annex_b(packet, sps_pss):
    """将 MP4 (AVC) 格式的 H.264 Packet 转换为 Annex B 格式"""
    annex_b_data = b""
    nal_start_code = b'\x00\x00\x00\x01'  # Annex B 头
    if sps_pss is not None:
        nal_start_code = nal_start_code + sps_pss
    
    data = bytes(packet)  # 获取 Packet 原始数据
    offset = 0

    while offset < len(data):
        if offset + 4 > len(data):  # 避免超出边界
            print("❌ NAL 解析错误：数据不足")
            break

        nal_length = struct.unpack(">I", data[offset:offset+4])[0]  # 读取 NAL 长度
        offset += 4
        if offset + nal_length > len(data):
            print("❌ NAL 长度超出范围")
            break

        annex_b_data += nal_start_code + data[offset:offset+nal_length]
        offset += nal_length

    return annex_b_data
def get_sps_pps(codec_context):
    sps = b""
    pps = b""

        # 检查是否为 H.264/H.265
    if codec_context.name not in ('h264', 'hevc'):
        print("非H.264/H.265编码的视频")
        return b""
    print("codec_context.name: ", codec_context.name)
    
    # 提取 extradata
    extradata = codec_context.extradata
    if not extradata:
        print("未找到extradata信息")
        return b""
    
    # 解析 H.264 的 extradata (AVCC格式)
    if codec_context.name == 'h264':
        # 检查 AVCC 头部结构
        print("h264 extradata长度: ", len(extradata))
        if len(extradata) < 7:
            print("extradata长度异常")
            return b""
        
        # 解析 SPS
        sps_count = extradata[5] & 0x1F  # 取低5位
        offset = 6
        for _ in range(sps_count):
            if offset + 2 > len(extradata):
                break
            sps_len = struct.unpack('>H', extradata[offset:offset+2])[0]
            offset += 2
            if offset + sps_len > len(extradata):
                break
            sps = extradata[offset:offset+sps_len]
            offset += sps_len
        
        # 解析 PPS
        pps_count = extradata[offset] & 0x1F if offset < len(extradata) else 0
        offset += 1
        for _ in range(pps_count):
            if offset + 2 > len(extradata):
                break
            pps_len = struct.unpack('>H', extradata[offset:offset+2])[0]
            offset += 2
            if offset + pps_len > len(extradata):
                break
            pps = extradata[offset:offset+pps_len]
            offset += pps_len
    
    # 解析 H.265 的 extradata (HVCC格式)
    elif codec_context.name == 'hevc':
        # 更复杂的HVCC解析逻辑（此处简化解法）
        nal_units = []
        offset = 21  # 跳过HVCC头部固定部分
        while offset < len(extradata):
            if offset + 2 > len(extradata):
                break
            nal_len = struct.unpack('>H', extradata[offset:offset+2])[0]
            offset += 2
            if offset + nal_len > len(extradata):
                break
            nal_unit = extradata[offset:offset+nal_len]
            nal_type = (nal_unit[0] >> 1) & 0x3F  # HEVC NAL类型
            if nal_type == 33:  # SPS
                sps = nal_unit
            elif nal_type == 34:  # PPS
                pps = nal_unit
            offset += nal_len
    print(f"SPS: {sps.hex(), pps.hex()}")
    return sps+b"\x00\x00\x00\x01" + pps + b"\x00\x00\x00\x01"

async def push_encoded_video_from_file(connection: RTCConnection, sample_options, _exit: Event):
    frame_rate = 30
    video_file_path = sample_options.video_file
    frame_rate = sample_options.fps
    
    count = 0
    width = sample_options.width
    height = sample_options.height
    container = av.open(video_file_path)
    for stream in container.streams:
        if stream.type == 'video':
            width = stream.width
            height = stream.height
            codec_name = stream.codec.name
            logger.info(f"Video stream: width = {width}, height = {height}， codec_name = {codec_name}")
            frame_rate = int(stream.average_rate)
            if frame_rate is not None:
                print(f"frame_rate: {frame_rate}")
            else:
                print("frame_rate is None")
            break
        '''
    while True:
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
                encoded_video_frame_info = EncodedVideoFrameInfo(
                    codec_type=2,
                    width=width,
                    height=height,
                    frames_per_second=frame_rate
                )
                if is_keyframe:
                    encoded_video_frame_info.frame_type = 3
                else:
                    encoded_video_frame_info.frame_type = 4
                ret = video_sender.send_encoded_video_image(packet.buffer_ptr, packet.buffer_size, encoded_video_frame_info)
                count += 1
                logger.info(f"count,ret={count}, {ret}")
                await asyncio.sleep(1.0/frame_rate)
                '''
    # 获取文件扩展名：通过扩展名来区分是mp4还是264流;
    _, file_ext = os.path.splitext(video_file_path)
    is_h264_file = True
    if file_ext is not None and file_ext.lower() == '.mp4':
        is_h264_file = False

    # 获取视频流
    video_stream = next(s for s in container.streams if s.type == 'video')

# 获取 SPS/PPS 数据（MP4 的 H.264 视频存储在 extradata 中）
    sps_pps = get_sps_pps(video_stream.codec_context)
    string_sps_pps = sps_pps.hex()

    print(f"SPS/PPS: codec: {video_stream.codec_context.extradata},, sps_pps: {sps_pps}, sps_pps_hex: {string_sps_pps}")


    for packet in container.demux(video_stream):
        if _exit.is_set():
            logger.info("exit")
            return
        if packet.is_corrupt or packet.is_discard or packet.is_disposable:
            logger.info(f"----Corrupt packet with size {packet.size} bytes")
            continue
        if packet.stream.type != 'video':
            logger.info(f"----Non-video packet with size {packet.size} bytes")
            continue
        
        is_keyframe = packet.is_keyframe
        logger.info(f"Read packet with size {packet.size} bytes, PTS {packet.pts}, keyframe {is_keyframe}")
        
        encoded_video_frame_info = EncodedVideoFrameInfo(
            codec_type=2,
            width=width,
            height=height,
            frames_per_second=frame_rate
        )
        if is_keyframe:
            encoded_video_frame_info.frame_type = 3
        else:
            encoded_video_frame_info.frame_type = 4
        # change packet to bytes
        
        
        if is_h264_file:
            bytes_data = convert_intptr_to_bytes_without_copy(packet.buffer_ptr, packet.buffer_size)
            if bytes_data is None:
                logger.info("bytes_data is None")
                continue
            ret = connection.push_video_encoded_data(bytes_data, encoded_video_frame_info)
        else:

            if packet.is_keyframe:
                annex_b_data = convert_to_annex_b(packet, sps_pps)
            else:
                annex_b_data = convert_to_annex_b(packet, None)
    
    # 关键帧前插入 SPS/PPS，确保解码器可用
            #if packet.is_keyframe:
            #   annex_b_data = extradata + annex_b_data
            
            # 重新封装到 Packet
            new_packet = av.Packet(annex_b_data)
            new_packet.pts = packet.pts
            new_packet.dts = packet.dts
            new_packet.stream = video_stream  # 关联视频流
            
            
            #buffer_ptr = ctypes.cast(packet.buffer_ptr, ctypes.POINTER(ctypes.c_ubyte))
            # 创建新的 Packet 并替换数据
           
            #new_packet.stream = new_stream  # 关联流

            # 获取指针的内存地址（转换为 int 类型）
                #buffer_address = ctypes.addressof(buffer_ptr.contents)
            bytes_data = convert_intptr_to_bytes_without_copy(new_packet.buffer_ptr, new_packet.buffer_size)
            if bytes_data is None:
                logger.info("bytes_data is None")
                continue
            ret = connection.push_video_encoded_data(bytes_data, encoded_video_frame_info)
        count += 1
        logger.info(f"count,ret={count}, {ret}")
        await asyncio.sleep(1.0/frame_rate)

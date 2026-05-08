#!env python
import asyncio
import itertools
import av
import av.packet

import logging
import ctypes
import struct
logger = logging.getLogger(__name__)


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
    #return sps + pps


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

    annexb_data = bytes()
    # 将 packet 数据转换为字节
    data = bytes(packet)

    # 将 Length-prefixed NAL 单元转换为 Annex B 格式
    i = 0
    while i < len(data):
        # 读取 NAL 单元长度
        nal_unit_length = int.from_bytes(data[i:i+4], byteorder='big')
        i += 4

        # 添加起始码 (0x00000001)
        annexb_data += b"\x00\x00\x00\x01"

        # 添加 NAL 单元数据
        annexb_data += data[i:i+nal_unit_length]
        i += nal_unit_length

    return annexb_data

    """将 MP4 (AVC) 格式的 H.264/H.265 Packet 转换为 Annex B 格式"""
    nal_start_code = b'\x00\x00\x00\x01'  # Annex B 头
    annex_b_data = b''
    offset = 0
    data = bytes(packet)  # 获取 Packet 原始数据

    while offset < len(data):
        # 读取 NAL 单元长度（MP4 里 NAL 前是 4 字节长度）
        nal_length = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4

        # 替换为 Annex B 头
        annex_b_data += nal_start_code + data[offset:offset+nal_length]
        offset += nal_length

    return annex_b_data
async def push_encoded_video_from_file( video_file_path):
    frame_rate = 30
    
    count = 0
    width = 352
    height = 288
    container = av.open(video_file_path)
    out_file_path = './output.h264'
    out_file = open(out_file_path, 'wb')
    
    # 获取视频流 and print video stream info
    video_stream = next(s for s in container.streams if s.type == 'video')
    width = video_stream.width
    height = video_stream.height
    codec_name = video_stream.codec.name
    logger.info(f"Video stream: width = {width}, height = {height}， codec_name = {codec_name}")
    frame_rate = int(video_stream.average_rate)
    if frame_rate is not None:
        print(f"frame_rate: {frame_rate}")
    else:
        print("frame_rate is None")
    
    #case1: 
    # 输出 H.264 码流
    
    

# 获取 SPS/PPS 数据（MP4 的 H.264 视频存储在 extradata 中）

    sps_pps = get_sps_pps(video_stream.codec_context)
    string_sps_pps = sps_pps.hex()

    print(f"SPS/PPS: codec: {video_stream.codec_context.extradata}, sps_pps: {sps_pps}, sps_pps_hex: {string_sps_pps}")

    
    key_frame_count = 0
    for packet in container.demux(video_stream):
      
        if packet.is_corrupt or packet.is_discard or packet.is_disposable:
            logger.info(f"----Corrupt packet with size {packet.size} bytes")
            continue
        if packet.stream.type != 'video':
            logger.info(f"----Non-video packet with size {packet.size} bytes")
            continue
        
        is_keyframe = packet.is_keyframe
        logger.info(f"Read packet with size {packet.size} bytes, PTS {packet.pts}, keyframe {is_keyframe}")
        
       
        # change packet to bytes
        
        is_h264_file = 0
        if is_h264_file:
            ret = 1
        else:

            

        # **关键帧前再插入 SPS/PPS**
            if packet.is_keyframe:
                key_frame_count += 1
                annex_b_data = convert_to_annex_b(packet, sps_pps)
            else:
                annex_b_data = convert_to_annex_b(packet, None)
            #    annex_b_data =  annex_b_data + sps_pps
            
    #结果：case1:当有extradata+convert_to_annex_b 是错的
    # case2: 当只有convert_to_annex_b 是错的
    # case3: packet_to_nanexb 是错的！
    # case4: packet_to_nanex+extradata 是错的
    # case5: 直接bytes +每一帧前面附加\x00\x00\x00\x01 是错的
    # case6: 直接bytes +key frame 添加extradta，non-key frame 添加\x00\x00\x00\x01 是错的
    # casee7: 直接bytes +所有的都 添加extradta，是错的
            
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
            ret = 1
            out_file.write(annex_b_data)
        count += 1
        print(f"count,ret={count}, {ret}, {key_frame_count}")
        await asyncio.sleep(0.001)

if __name__ == '__main__':
    file_path = "/Users/weihognqin/Documents/work/Agora-Python-Server-SDK/test_data/111.mp4"
    asyncio.run(push_encoded_video_from_file(file_path))
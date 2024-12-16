#!env python

import os
import numpy as np
from PIL import Image
import datetime
from agora.rtc.video_frame_observer import IVideoFrameObserver, VideoFrame
import logging
logger = logging.getLogger(__name__)

source_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
filename, _ = os.path.splitext(os.path.basename(__file__))
log_folder = os.path.join(
    source_dir,
    'logs',
    filename,
    datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_folder, exist_ok=True)


def yuv_to_rgb(y: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Convert YUV to RGB using numpy operations"""
    # YUV to RGB conversion matrix
    y = y.astype(np.float32)
    u = u.astype(np.float32) - 128.0
    v = v.astype(np.float32) - 128.0

    # RGB conversion using BT.601 standard
    r = y + 1.402 * v
    g = y - 0.344136 * u - 0.714136 * v
    b = y + 1.772 * u

    # Clip values to [0, 255] and convert to uint8
    rgb = np.stack([r, g, b], axis=-1)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    return rgb


def resize_plane(plane: np.ndarray, target_shape: tuple) -> np.ndarray:
    """Resize UV plane using bilinear interpolation"""
    h, w = plane.shape
    target_h, target_w = target_shape

    # Create coordinate matrices
    x = np.linspace(0, w - 1, target_w)
    y = np.linspace(0, h - 1, target_h)
    x_coords, y_coords = np.meshgrid(x, y)

    # Get integer and fractional parts
    x0 = np.floor(x_coords).astype(int)
    x1 = np.minimum(x0 + 1, w - 1)
    y0 = np.floor(y_coords).astype(int)
    y1 = np.minimum(y0 + 1, h - 1)

    # Get weights
    wx = x_coords - x0
    wy = y_coords - y0

    # Get values at corners
    v00 = plane[y0, x0]
    v10 = plane[y1, x0]
    v01 = plane[y0, x1]
    v11 = plane[y1, x1]

    # Interpolate
    result = (v00 * (1 - wx) * (1 - wy) +
              v01 * wx * (1 - wy) +
              v10 * (1 - wx) * wy +
              v11 * wx * wy)

    return result.astype(np.uint8)


def convert_I420_to_RGB(video_frame: VideoFrame) -> Image.Image:
    # YUV420P(I420) to RGB
    # TODO:
    # 使用numba进行JIT编译
    # 实现SIMD优化
    # 使用多线程处理不同的颜色平面 (or use cuda)

    width = video_frame.width
    height = video_frame.height

    # Extract YUV planes
    y_plane = np.frombuffer(
        video_frame.y_buffer, dtype=np.uint8).reshape(height, width)
    u_plane = np.frombuffer(
        video_frame.u_buffer, dtype=np.uint8).reshape(height // 2, width // 2)
    v_plane = np.frombuffer(
        video_frame.v_buffer, dtype=np.uint8).reshape(height // 2, width // 2)

    # Resize U and V planes
    u_resized = resize_plane(u_plane, (height, width))
    v_resized = resize_plane(v_plane, (height, width))

    # Convert to RGB
    rgb = yuv_to_rgb(y_plane, u_resized, v_resized)
    image = Image.fromarray(rgb)

    return image


def convert_I420_to_RGB_with_cv(video_frame: VideoFrame) -> Image.Image:
    import cv2
    # 从YUV420P(I420)转换到RGB
    width = video_frame.width
    height = video_frame.height

    # 从YUV缓冲区提取Y、U、V平面
    y_size = width * height
    u_size = (width * height) // 4

    y_plane = np.frombuffer(
        video_frame.y_buffer, dtype=np.uint8).reshape(height, width)
    u_plane = np.frombuffer(
        video_frame.u_buffer, dtype=np.uint8).reshape(height // 2, width // 2)
    v_plane = np.frombuffer(
        video_frame.v_buffer, dtype=np.uint8).reshape(height // 2, width // 2)

    # 将U和V平面放大到与Y相同的尺寸
    u_resized = cv2.resize(u_plane, (width, height), interpolation=cv2.INTER_LINEAR)
    v_resized = cv2.resize(v_plane, (width, height), interpolation=cv2.INTER_LINEAR)

    # 将YUV转换为RGB
    yuv = cv2.merge([y_plane, u_resized, v_resized])
    # 如果出现图像质量问题,可以尝试调整插值方法(如改用cv2.INTER_CUBIC)
    rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)

    # 转换为PIL Image
    image = Image.fromarray(rgb)
    return image


def save_image(image: Image.Image, channel_id, remote_uid):
    file_path = os.path.join(log_folder, channel_id + "_" + remote_uid + '.jpeg')
    image.save(file_path)
    return file_path


def save_yuv(channel_id, remote_uid, log_folder, frame):
    file_path = os.path.join(log_folder, channel_id + "_" + remote_uid + '.yuv')
    y_size = frame.y_stride * frame.height
    uv_size = (frame.u_stride * frame.height // 2)
    # logger.info(f"on_frame, file_path={file_path}, y_size={y_size}, uv_size={uv_size}, len_y={len(frame.y_buffer)}, len_u={len(frame.u_buffer)}, len_v={len(frame.v_buffer)}")
    with open(file_path, 'ab') as f:
        f.write(frame.y_buffer[:y_size])
        f.write(frame.u_buffer[:uv_size])
        f.write(frame.v_buffer[:uv_size])


class ExampleVideoFrameObserver(IVideoFrameObserver):
    def __init__(self, save_to_disk=0):
        super(ExampleVideoFrameObserver, self).__init__()
        self._save_to_disk = save_to_disk

    def on_frame(self, channel_id, remote_uid, frame: VideoFrame):
        logger.info(
            f"on_frame, channel_id={channel_id}, remote_uid={remote_uid},type={frame.type}, width={frame.width}, height={frame.height}, y_stride={frame.y_stride}, u_stride={frame.u_stride}, v_stride={frame.v_stride}, len_y={ len(frame.y_buffer)}, len_u={ len(frame.u_buffer)}, len_v={len(frame.v_buffer)}, len_alpha_buffer={len(frame.alpha_buffer) if frame.alpha_buffer else 0}")

        # logger.info(f"on_frame, channel_id={channel_id}, remote_uid={remote_uid},len_alpha_buffer={len(frame.alpha_buffer) if frame.alpha_buffer else 0}")

        if self._save_to_disk:
            # image = convert_I420_to_RGB(frame)
            image = convert_I420_to_RGB_with_cv(frame)
            file_path = save_image(image, channel_id, remote_uid)
            print(f"save to {file_path}")
            # save_yuv(channel_id, remote_uid, log_folder, frame)
        return 1

    def on_user_video_track_subscribed(
            self,
            agora_local_user,
            user_id,
            info,
            agora_remote_video_track):
        logger.info(
            f"on_user_video_track_subscribed, agora_local_user={agora_local_user}, user_id={user_id}, info={info}, agora_remote_video_track={agora_remote_video_track}")
        return 0

    # def on_user_video_track_subscribed(self, agora_local_user, user_id, agora_remote_video_track:RemoteVideoTrack, video_track_info):
        # logger.info("ExampleVideoFrameObserver _on_user_video_track_subscribed:", agora_local_user, user_id, agora_remote_video_track, video_track_info)
        # agora_remote_video_track.register_video_encoded_image_receiver(video_encoded_image_receiver)

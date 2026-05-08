# coding=utf-8
"""
JPEG 流查看器 - 按声网文档接收设备端 JPEG（收发都需设置 codec_type=20）
文档：https://doc.shengwang.cn/doc/rtsa/c/best-practices/interoperate-rtc 视频一节

用法：
  # 保存为 JPEG 文件到当前目录（默认）
  python viewer.py --app_id=xxx --channel_id=xxx --token=xxx --uid=1234

"""
import argparse
import os
import sys
import time
import cv2
import numpy as np
import faulthandler
# 在import之后直接添加以下启用代码即可
faulthandler.enable()
# 后边正常写你的代码

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app_id', required=True, help='声网 App ID')
    parser.add_argument('--channel_id', required=True, help='频道名')
    parser.add_argument('--token', required=True, help='user_token（观众用）')
    parser.add_argument('--uid', type=int, default=5678, help='观众 UID，默认 5678')
    parser.add_argument('--save_dir', default='.', help='保存 JPEG 的目录，默认当前目录')
    parser.add_argument('--display', action='store_true', help='弹窗显示而非保存')
    parser.add_argument('--max_frames', type=int, default=10, help='最多保存帧数，默认 10')
    parser.add_argument('--raw_only', action='store_true', help='仅订阅原始帧（发送端 YUV 推流时用，勿设 codec_type=20）')
    parser.add_argument('--no_observer', action='store_true', help='测试用：不注册任何视频 observer，仅加入+订阅，用于排查对端加入时 segfault 是否与 observer 有关')
    args = parser.parse_args()

    if os.environ.get("AGORA_VIEWER_SHOW_SEGFAULT_HELP"):
        print("[viewer] Segfault 调试: ulimit -c unlimited && gdb --args $(pyenv which python) viewer.py ... => run => 崩溃后 (gdb) bt full")
    if args.no_observer:
        print("[viewer] 模式: --no_observer，不注册 observer，仅加入频道并订阅")
    else:
        print("[viewer] 模式: 接收JPEG (codec_type=20)" if not args.raw_only else "[viewer] 模式: --raw_only，接收 YUV/解码帧")

    try:
        from agora.rtc.agora_service import AgoraService
        from agora.rtc.agora_base import (
            AgoraServiceConfig, RTCConnConfig,
            ClientRoleType, ChannelProfileType, AudioProfileType, AudioScenarioType,
            VideoSubscriptionOptions, VideoStreamType,
        )
        from agora.rtc.video_encoded_frame_observer import IVideoEncodedFrameObserver
        from agora.rtc.video_frame_observer import IVideoFrameObserver
        RtcConnectionPublishConfig = getattr(
            __import__('agora.rtc.agora_base', fromlist=['RtcConnectionPublishConfig']),
            'RtcConnectionPublishConfig',
            None,
        )
    except ImportError as e:
        print(f"ImportError: {e}")
        print("请安装: pip install agora-python-server-sdk opencv-python numpy")
        print("若已安装，确认 python 与 pip 同一环境: which python && pip show agora-python-server-sdk")
        return 1

    latest_frame = {'data': None}
    frame_count = {'n': 0}
    recv_count = {'n': 0}
    raw_frame_count = {'n': 0}

    def _is_jpeg_magic(data):
        """JPEG 文件头为 FFD8，尾可选 FFD9"""
        if not data or len(data) < 2:
            return False
        return data[:2] == b'\xff\xd8'

    class JpegFrameObserver(IVideoEncodedFrameObserver):
        """仅验证推流是否到达、是否为 JPEG，不写文件以免影响稳定性或掩盖问题。"""
        def __init__(self, save_dir, max_frames):
            super().__init__()
            self.save_dir = save_dir
            self.max_frames = max_frames

        def on_encoded_video_frame(self, uid, image_buffer, length, info):
            try:
                recv_count['n'] += 1
                data = bytes(image_buffer[:length])
                latest_frame['data'] = data
                is_jpeg = _is_jpeg_magic(data)
                # 第一时间打印：推流到了 + 长度 + 是否像 JPEG
                if recv_count['n'] == 1:
                    print(f"[JPEG] 推流数据已到 uid={uid} length={length} 是否JPEG(头FFD8): {'是' if is_jpeg else '否'} info={info}")
                elif recv_count['n'] <= 5 or recv_count['n'] % 30 == 0:
                    print(f"[JPEG] 编码帧 #{recv_count['n']} uid={uid} length={length} 是否JPEG: {'是' if is_jpeg else '否'}")
                # 不保存到文件，仅做验证
                frame_count['n'] = recv_count['n']
            except Exception as e:
                print("[JPEG] 处理异常:", e)
            return 1

    class RawFrameObserver(IVideoFrameObserver):
        """接收解码后的 YUV 帧（发送端 YUV 推流时走此路径）"""
        def __init__(self, save_dir, max_frames, latest_frame_ref=None):
            super().__init__()
            self.save_dir = save_dir
            self.max_frames = max_frames
            self.latest_frame_ref = latest_frame_ref

        def on_frame(self, channel_id, remote_uid, frame):
            try:
                raw_frame_count['n'] += 1
                if raw_frame_count['n'] <= 3 or raw_frame_count['n'] % 50 == 0:
                    print(f"[raw] 收到 YUV 帧 channel={channel_id} uid={remote_uid} {frame.width}x{frame.height}")
                h, w = frame.height, frame.width
                ys, us, vs = frame.y_stride, frame.u_stride, frame.v_stride
                y_sz = ys * h
                uv_sz = (us * h) // 2
                y = np.frombuffer(bytes(frame.y_buffer[:y_sz]), dtype=np.uint8).reshape((h, ys))[:, :w]
                u = np.frombuffer(bytes(frame.u_buffer[:uv_sz]), dtype=np.uint8).reshape((h // 2, us))[:, :w // 2]
                v = np.frombuffer(bytes(frame.v_buffer[:uv_sz]), dtype=np.uint8).reshape((h // 2, vs))[:, :w // 2]
                i420 = np.zeros((h * 3 // 2, w), dtype=np.uint8)
                i420[:h, :] = y
                i420[h:h + h // 2, :] = np.repeat(np.repeat(u, 2, axis=1), 2, axis=0)
                i420[h + h // 2:, :] = np.repeat(np.repeat(v, 2, axis=1), 2, axis=0)
                bgr = cv2.cvtColor(i420, cv2.COLOR_YUV2BGR_I420)
                if self.latest_frame_ref is not None:
                    _, jpg = cv2.imencode('.jpg', bgr)
                    self.latest_frame_ref['data'] = jpg.tobytes()
                if self.save_dir and frame_count['n'] < self.max_frames:
                    path = os.path.join(self.save_dir, f"frame_{frame_count['n']:04d}.jpg")
                    cv2.imwrite(path, bgr)
                    frame_count['n'] += 1
                    print(f"[raw] 已保存 {path}")
            except Exception as e:
                print("[raw] 保存异常:", e)
            return 1

    config = AgoraServiceConfig()
    if hasattr(config, 'appid'):
        config.appid = args.app_id  # 2.2.4
    else:
        config.app_id = args.app_id  # 2.4.x
    svc = AgoraService()
    svc.initialize(config)

    # 先试只收解码后的原始帧（encoded 回调收不到时用此路径）
    sub_opt_raw = VideoSubscriptionOptions(
        type=VideoStreamType.VIDEO_STREAM_HIGH,
        encodedFrameOnly=0,
    )
    sub_opt_encoded = VideoSubscriptionOptions(
        type=VideoStreamType.VIDEO_STREAM_HIGH,
        encodedFrameOnly=1,
    )

    # 2.4.x 需要 con_config + publish_config；2.2.4 仅 con_config
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        auto_subscribe_audio=1,
        auto_subscribe_video=1,
    )
    if RtcConnectionPublishConfig is not None:
        publish_config = RtcConnectionPublishConfig(is_publish_audio=False, is_publish_video=False)
        conn = svc.create_rtc_connection(con_config, publish_config)
    else:
        conn = svc.create_rtc_connection(con_config)
    if not conn:
        print("创建连接失败")
        return 1

    save_dir = args.save_dir.strip() if not args.display else ''
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        print(f"将保存 JPEG 到: {os.path.abspath(save_dir)} (最多 {args.max_frames} 帧)")

   
    pass

    if not args.raw_only:
        try:
            conn.get_agora_parameter().set_parameters('{"engine.video.codec_type": "20"}')
            print("[viewer] 已设置接收 JPEG (engine.video.codec_type=20)，在 connect 之前")
        except Exception as e:
            print("[viewer] 设置 codec_type 失败:", e)
    else:
        print("[viewer] 已启用 --raw_only，不设 codec_type（接收 YUV/解码帧）")

    print(f"[viewer] 正在加入频道 channel_id={args.channel_id} uid={args.uid} ...")
    ret = conn.connect(args.token, args.channel_id, str(args.uid))
    if ret < 0:
        print(f"[viewer] 加入频道失败: ret={ret}")
        return 1
    print(f"[viewer] 已加入频道，等待远端用户加入与 JPEG 帧...")

    # 2.2.4 写法：按官方 demo 在 local_user 上注册（example_video_encoded_receive / example_video_yuv_receive）
    local_user = conn.get_local_user()
    if not local_user:
        print("[viewer] 无法获取 local_user")
        conn.release()
        svc.release()
        return 1

    # 2.4.x 可能用 _register_video_encoded_frame_observer，兼容两种命名
    _register_encoded = getattr(local_user, 'register_video_encoded_frame_observer', None) or getattr(local_user, '_register_video_encoded_frame_observer', None)
    _register_frame = getattr(local_user, 'register_video_frame_observer', None) or getattr(local_user, '_register_video_frame_observer', None)
    _unregister_encoded = getattr(local_user, 'unregister_video_encoded_frame_observer', None) or getattr(local_user, '_unregister_video_encoded_frame_observer', None)
    _unregister_frame = getattr(local_user, 'unregister_video_frame_observer', None) or getattr(local_user, '_unregister_video_frame_observer', None)

    # --no_observer：不注册任何 observer，用于排查对端加入时 segfault 是否与 observer 有关
    if not args.no_observer:
        jpeg_observer = JpegFrameObserver(save_dir, args.max_frames)
        raw_observer = RawFrameObserver(save_dir, args.max_frames, latest_frame)
        if args.raw_only:
            fn = _register_frame
            if fn is None:
                print("[viewer] LocalUser 无 register_video_frame_observer 方法")
            else:
                ret = fn(raw_observer)
                if ret < 0:
                    print(f"[viewer] register_video_frame_observer 失败: {ret}")
                else:
                    print("[viewer] 已在 local_user 注册 IVideoFrameObserver（原始帧）")
        else:
            fn = _register_encoded
            if fn is None:
                print("[viewer] LocalUser 无 register_video_encoded_frame_observer 方法")
            else:
                ret = fn(jpeg_observer)
                if ret < 0:
                    print(f"[viewer] register_video_encoded_frame_observer 失败: {ret}")
                else:
                    print("[viewer] 已在 local_user 注册 IVideoEncodedFrameObserver（JPEG）")
    else:
        print("[viewer] 未注册 observer，等待对端加入观察是否仍 segfault...")

    if args.raw_only:
        local_user.subscribe_all_video(sub_opt_raw)
        # 与官方 example_video_yuv_receive 一致：接收端也调用 publish_audio/publish_video
        try:
            conn.publish_audio()
            conn.publish_video()
        except Exception as e:
            print("publish_audio/publish_video 忽略:", e)
        print("[viewer] 已订阅原始帧（YUV），等待设备推流...")
    else:
        local_user.subscribe_all_video(sub_opt_encoded)
        print("[viewer] 已订阅编码帧（JPEG），等待设备推流；若一直无帧请确认设备端已设 codec_type=20 并推 JPEG")

    try:
        if save_dir:
            # 保存模式：收到足够帧后退出
            last_log = [time.monotonic()]
            while frame_count['n'] < args.max_frames:
                time.sleep(0.1)
                if frame_count['n'] == 0 and time.monotonic() - last_log[0] >= 5.0:
                    print("  [调试] 仍未收到任何帧。请确认：① 与设备同 channel_id/token ② 设备端已按文档设 engine.video.codec_type=20 并推 JPEG ③ 是否出现「远端用户加入」日志")
                    last_log[0] = time.monotonic()
            print(f"验证完成，已保存 {frame_count['n']} 张 JPEG 到 {save_dir}，可直接打开查看")
        else:
            # 显示模式
            print("(按 q 退出)")
            while True:
                data = latest_frame.get('data')
                if data:
                    try:
                        arr = np.frombuffer(data, dtype=np.uint8)
                        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        if img is not None:
                            cv2.imshow('Device Stream (JPEG)', img)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    except Exception as e:
                        print("显示异常:", e)
                time.sleep(0.03)
            cv2.destroyAllWindows()
    finally:
        # 2.4.x 可能用 _unregister_*，兼容两种命名
        if not args.no_observer:
            try:
                if args.raw_only and _unregister_frame:
                    _unregister_frame()
                elif not args.raw_only and _unregister_encoded:
                    _unregister_encoded()
            except Exception:
                pass
        conn.disconnect()
        conn.release()
        svc.release()
    return 0

if __name__ == '__main__':
    sys.exit(main())

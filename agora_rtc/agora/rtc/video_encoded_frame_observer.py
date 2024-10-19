
class EncodedVideoFrameInfo():
    def __init__(self, codec_type=0, width=0, height=0, frames_per_second=0, frame_type=0, rotation=0, track_id=0, capture_time_ms=0, decode_time_ms=0, uid=0, stream_type=0) -> None:
        self.codec_type = codec_type
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.frame_type = frame_type
        self.rotation = rotation
        self.track_id = track_id
        self.capture_time_ms = capture_time_ms
        self.decode_time_ms = decode_time_ms
        self.uid = uid
        self.stream_type = stream_type


class IVideoEncodedFrameObserver():
    def on_encoded_video_frame(self, uid, image_buffer, length, video_encoded_frame_info: EncodedVideoFrameInfo):
        pass


class EncodedVideoFrameInfo():
    def __init__(self, codec_type = 0, width = 0, height = 0, frames_per_second = 0, frame_type = 0, rotation = 0, track_id = 0, capture_time_ms = 0, decode_time_ms = 0, uid = 0, stream_type = 0) -> None:
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

class  IVideoEncodedFrameObserver():

    #   int (*on_encoded_video_frame)(AGORA_HANDLE agora_video_encoded_frame_observer, uid_t uid, const uint8_t* image_buffer, size_t length,  const encoded_video_frame_info* video_encoded_frame_info);
    def on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info:EncodedVideoFrameInfo):
        pass
    

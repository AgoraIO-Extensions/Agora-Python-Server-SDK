# MARK: TODO_CHECK

from .agora_base import VideoFrame


class IVideoFrameObserver():
    def on_frame(self, channel_id, remote_uid, frame: VideoFrame):
        pass

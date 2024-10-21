from .audio_pcm_data_sender import AudioPcmDataSender
from .audio_encoded_frame_sender import AudioEncodedFrameSender
from .video_frame_sender import VideoFrameSender
from .video_encoded_image_sender import VideoEncodedImageSender
from .agora_base import *
from ._ctypes_handle._ctypes_data import *


agora_media_node_factory_create_audio_pcm_data_sender = agora_lib.agora_media_node_factory_create_audio_pcm_data_sender
agora_media_node_factory_create_audio_pcm_data_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_pcm_data_sender.argtypes = [AGORA_HANDLE]

# agora_media_node_factory_create_audio_encoded_frame_sender
agora_media_node_factory_create_audio_encoded_frame_sender = agora_lib.agora_media_node_factory_create_audio_encoded_frame_sender
agora_media_node_factory_create_audio_encoded_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_encoded_frame_sender.argtypes = [AGORA_HANDLE]

# agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender = agora_lib.agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_frame_sender.argtypes = [AGORA_HANDLE]

# agora_media_node_factory_create_video_encoded_image_sender
agora_media_node_factory_create_video_encoded_image_sender = agora_lib.agora_media_node_factory_create_video_encoded_image_sender
agora_media_node_factory_create_video_encoded_image_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_encoded_image_sender.argtypes = [AGORA_HANDLE]

agora_media_node_factory_destroy = agora_lib.agora_media_node_factory_destroy
agora_media_node_factory_destroy.argtypes = [AGORA_HANDLE]


class MediaNodeFactory():
    def __init__(self, media_node_factory) -> None:
        self.media_node_factory = media_node_factory
        return

    # createAudioPcmDataSender	create a pcm data sender.
    def create_audio_pcm_data_sender(self):
        sender_handle = agora_media_node_factory_create_audio_pcm_data_sender(self.media_node_factory)
        if sender_handle is None:
            return None
        return AudioPcmDataSender(sender_handle)
    # createAudioEncodedFrameSender	create a audio encoded frame sender.

    def create_audio_encoded_frame_sender(self):
        handle = agora_media_node_factory_create_audio_encoded_frame_sender(self.media_node_factory)
        if handle is None:
            return None
        if not handle:
            return None
        return AudioEncodedFrameSender(handle)
    # createVideoFrameSender create a yuv frame sender.

    def create_video_frame_sender(self):
        handle = agora_media_node_factory_create_video_frame_sender(self.media_node_factory)
        if handle is None:
            return None
        return VideoFrameSender(handle)
    # createVideoEncodedImageSender: create a video encoded image sender.

    def create_video_encoded_image_sender(self):
        handle = agora_media_node_factory_create_video_encoded_image_sender(self.media_node_factory)
        if handle is None:
            return None
        return VideoEncodedImageSender(handle)

    def release(self):
        if self.media_node_factory:
            agora_media_node_factory_destroy(self.media_node_factory)
        self.media_node_factory = None

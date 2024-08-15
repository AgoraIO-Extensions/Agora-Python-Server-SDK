from .audio_pcm_data_sender import AudioPcmDataSender
from .video_sender import VideoFrameSender
from .agora_base import *

agora_media_node_factory_create_audio_pcm_data_sender = agora_lib.agora_media_node_factory_create_audio_pcm_data_sender
agora_media_node_factory_create_audio_pcm_data_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_pcm_data_sender.argtypes = [AGORA_HANDLE]

#agora_media_node_factory_create_audio_encoded_frame_sender
agora_media_node_factory_create_audio_encoded_frame_sender = agora_lib.agora_media_node_factory_create_audio_encoded_frame_sender
agora_media_node_factory_create_audio_encoded_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_encoded_frame_sender.argtypes = [AGORA_HANDLE]

#agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender = agora_lib.agora_media_node_factory_create_video_frame_sender
agora_media_node_factory_create_video_frame_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_frame_sender.argtypes = [AGORA_HANDLE]

#agora_media_node_factory_create_video_encoded_image_sender
agora_media_node_factory_create_video_encoded_image_sender = agora_lib.agora_media_node_factory_create_video_encoded_image_sender
agora_media_node_factory_create_video_encoded_image_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_video_encoded_image_sender.argtypes = [AGORA_HANDLE]

class MediaNodeFactory():
    def __init__(self, media_node_factory) -> None:
        self.media_node_factory = media_node_factory
        return
    
    #createAudioPcmDataSender	创建一个 PCM 数据发送模块。
    def create_audio_pcm_data_sender(self):
        sender_handle = agora_media_node_factory_create_audio_pcm_data_sender(self.media_node_factory)
        return AudioPcmDataSender(sender_handle)
    #createAudioEncodedFrameSender	创建一个已编码音频数据发送模块。
    def create_audio_encoded_frame_sender(self):
        encoded_sender_handle = agora_media_node_factory_create_audio_encoded_frame_sender(self.media_node_factory)
        return encoded_sender_handle
    #createVideoFrameSender 创建一个 YUV 视频帧发送模块。
    def create_video_frame_sender(self):
        video_frame_sender = agora_media_node_factory_create_video_frame_sender(self.media_node_factory)
        return VideoFrameSender(video_frame_sender)
    #createVideoEncodedImageSender: 创建一个已编码视频发送模块。
    def create_video_encoded_image_sender(self):
        video_encoded_image_sender = agora_media_node_factory_create_video_encoded_image_sender(self.media_node_factory)
        return video_encoded_image_sender
        
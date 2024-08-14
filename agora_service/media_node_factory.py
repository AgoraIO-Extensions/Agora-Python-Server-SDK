from .audio_pcm_data_sender import AudioPcmDataSender
from .agora_base import *

agora_media_node_factory_create_audio_pcm_data_sender = agora_lib.agora_media_node_factory_create_audio_pcm_data_sender
agora_media_node_factory_create_audio_pcm_data_sender.restype = AGORA_HANDLE
agora_media_node_factory_create_audio_pcm_data_sender.argtypes = [AGORA_HANDLE]

class MediaNodeFactory():
    def __init__(self, media_node_factory) -> None:
        self.media_node_factory = media_node_factory
        return
    
    def create_audio_pcm_data_sender(self):
        pcm_data_sender = agora_media_node_factory_create_audio_pcm_data_sender(self.media_node_factory)
        return AudioPcmDataSender(pcm_data_sender)
        
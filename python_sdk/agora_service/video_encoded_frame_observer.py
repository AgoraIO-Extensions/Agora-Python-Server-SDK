class  IVideoEncodedFrameObserver():

    #   int (*on_encoded_video_frame)(AGORA_HANDLE agora_video_encoded_frame_observer, uid_t uid, const uint8_t* image_buffer, size_t length,  const encoded_video_frame_info* video_encoded_frame_info);
    def on_encoded_video_frame(self, agora_video_encoded_frame_observer, uid, image_buffer, length, video_encoded_frame_info):
        pass
    

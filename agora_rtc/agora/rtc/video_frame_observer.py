class VideoFrame():
    def __init__(self,
                type = 0,
                width = 0,
                height = 0,
                y_stride = 0,
                u_stride = 0,
                v_stride = 0,
                y_buffer = None,
                u_buffer = None,
                v_buffer = None,
                rotation = 0,
                render_time_ms = 0,
                avsync_type = 0,
                metadata_buffer = None,
                metadata_size = 0,
                shared_context = None,
                texture_id = 0,
                matrix = None,
                alpha_buffer = None                
                 ) -> None:
        self.type = type
        self.width = width
        self.height = height
        self.y_stride = y_stride
        self.u_stride = u_stride
        self.v_stride = v_stride
        self.y_buffer = y_buffer
        self.u_buffer = u_buffer
        self.v_buffer = v_buffer
        self.rotation = rotation
        self.render_time_ms = render_time_ms
        self.avsync_type = avsync_type
        self.metadata_buffer = metadata_buffer
        self.metadata_size = metadata_size
        self.metadata = ""
        self.shared_context = shared_context
        self.texture_id = texture_id
        self.matrix = matrix
        self.alpha_buffer = alpha_buffer

class IVideoFrameObserver():
    def on_frame(self, agora_handle, channel_id, user_id, video_frame:VideoFrame):
        pass
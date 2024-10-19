#MARK: TODO_CHECK
class VideoFrame():
    def __init__(self,
                type:int = 0,
                width:int = 0,
                height:int = 0,
                y_stride:int = 0,
                u_stride:int = 0,
                v_stride:int = 0,
                y_buffer:bytearray = None,
                u_buffer:bytearray = None,
                v_buffer:bytearray = None,
                rotation:int = 0,
                render_time_ms:int = 0,
                avsync_type:int = 0,
                metadata_buffer:bytearray = None,
                metadata_size:int = 0,
                shared_context:str = None,
                texture_id:int = 0,
                matrix:list = [],
                alpha_buffer:bytearray = None
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
    def on_frame(self, channel_id, remote_uid, frame:VideoFrame):
        pass
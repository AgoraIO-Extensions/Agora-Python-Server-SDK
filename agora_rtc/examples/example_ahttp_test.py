# coding=utf-8


# for audiostream processing
class AudioStreamProcessor:
    def __init__(self, sample_rate, num_channels, interval=0.1):
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.interval = interval
        self.buffer_size = 65536 #64k
        self.send_size = int(sample_rate * num_channels * interval * 2)
        self.buffer = bytearray()
        self.pack_size = int(sample_rate * num_channels * 2 / 100)
        
    async def process_stream(self, response, audio_consumer, interrupt_event):
        if response.status != 200:
            return
            
        try:
            async for chunk in response.content.iter_chunked(self.buffer_size):
                if not chunk or interrupt_event.is_set():
                    break
                    
                self.buffer.extend(chunk)
                buffer_len = len(self.buffer)
                #需要拆分为10ms的整数倍
            
                pack_num = buffer_len // self.pack_size
                if pack_num > 0 and audio_consumer:
                    #push to audio consumer
                    data = self.buffer[:pack_num * self.pack_size]
                    self.buffer = self.buffer[pack_num * self.pack_size:]
                    audio_consumer.push_pcm_data(data)
                   
                
                    
        except Exception as e:
            logger.error(f"Error processing audio stream: {e}")
        finally:
            # 处理剩余数据
            if self.buffer and audio_consumer:
                # check if buffer is 10ms
                pack_num = len(self.buffer) // self.pack_size
                if pack_num > 0:
                    data = self.buffer[:pack_num * self.pack_size]
                    self.buffer = self.buffer[pack_num * self.pack_size:]
                    audio_consumer.push_pcm_data(data)




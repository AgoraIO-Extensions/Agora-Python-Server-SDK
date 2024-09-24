import argparse
import logging
logger = logging.getLogger(__name__)

class SampleOptions:
    def __init__(self):
        self.app_id = None
        self.token = None
        self.channel_id = None
        self.connection_number:int = 1
        self.user_id = 0
        self.audio_file = None
        self.low_delay = False
        self.video_file = None
        self.sample_rate:int = None
        self.num_of_channels:int = None
        self.fps = None
        self.width = None
        self.height = None
        self.bitrate = None
        self.hours = 0
        self.msg = "hello agora python sdk"


def parse_args():
    parser = argparse.ArgumentParser(description="Agora SDK Example")
    parser.add_argument("--appId", required=True, help="The token for authentication / must")
    parser.add_argument("--channelId", required=True, help="Channel Id / must")
    parser.add_argument("--connectionNumber", default=1, help="Enter the channel number")
    parser.add_argument("--userId", default="0", help="User Id / default is 0")
    parser.add_argument("--audioFile", required=False, help="The audio file in raw PCM format to be sent")
    parser.add_argument("--lowdelay", action="store_true", help="Enable the low delay")
    parser.add_argument("--videoFile", help="The video file in YUV420 format to be sent")
    parser.add_argument("--sampleRate", type=int, help="Sample rate for the PCM file to be sent")
    parser.add_argument("--numOfChannels", type=int, help="Number of channels for the PCM file to be sent")
    parser.add_argument("--fps", type=int, help="Target frame rate for sending the video stream")
    parser.add_argument("--width", type=int, help="Image width for the YUV file to be sent")
    parser.add_argument("--height", type=int, help="Image height for the YUV file to be sent")
    parser.add_argument("--bitrate", type=int, help="Target bitrate (bps) for encoding the YUV stream")
    parser.add_argument("--message", help="The message to be sent")
    parser.add_argument("--hours", default="0", help="The time to run")

    return parser.parse_args()

def parse_args_example() -> SampleOptions:
    args = parse_args()
    logger.info(f"Parsed arguments:{args}")
    sample_options = SampleOptions()
    sample_options.app_id = args.appId
    sample_options.token = args.appId    
    sample_options.channel_id = args.channelId
    sample_options.connection_number = int(args.connectionNumber)
    sample_options.audio_file = args.audioFile
    sample_options.user_id = args.userId
    sample_options.low_delay = args.lowdelay
    sample_options.video_file = args.videoFile
    sample_options.sample_rate = args.sampleRate
    sample_options.num_of_channels = args.numOfChannels
    sample_options.fps = args.fps
    sample_options.width = args.width
    sample_options.height = args.height
    sample_options.bitrate = args.bitrate
    sample_options.msg = args.message
    sample_options.hours = args.hours

    return sample_options

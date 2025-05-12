import argparse
import logging
logger = logging.getLogger(__name__)


class ExampleOptions:
    def __init__(self):
        self.app_id = None
        self.token = None
        self.channel_id = None
        self.connection_number: int = 1
        self.user_id = "0"
        self.audio_file = None
        self.low_delay = False
        self.video_file = None
        self.sample_rate: int = None
        self.num_of_channels: int = None
        self.fps = None
        self.width = None
        self.height = None
        self.bitrate = None
        self.save_to_disk = 0
        self.hours = 0
        self.mode = 1
        self.value = 0
        self.dir_path = None #directory path
        self.msg = "hello agora python sdk"
        self.role = 1  # default is broadcaster

def parse_args():
    parser = argparse.ArgumentParser(description="Agora Python SDK Example")
    parser.add_argument("--appId", required=True, help="The appid for authentication / must")
    parser.add_argument("--token", help="The token for authentication ")
    parser.add_argument("--channelId", required=True, help="Channel Id / must")
    parser.add_argument("--connectionNumber", default=1, help="Enter the channel number")
    parser.add_argument("--userId", default="0", help="User Id / default is 0")
    parser.add_argument("--audioFile", required=False, help="The audio file in raw PCM format to be sent")
    parser.add_argument("--lowdelay", action="store_true", help="Enable the low delay")
    parser.add_argument("--videoFile", help="The video file in YUV420 format to be sent")
    parser.add_argument("--sampleRate", type=int, help="Example rate for the PCM file to be sent")
    parser.add_argument("--numOfChannels", type=int, help="Number of channels for the PCM file to be sent")
    parser.add_argument("--fps", type=int, help="Target frame rate for sending the video stream")
    parser.add_argument("--width", type=int, help="Image width for the YUV file to be sent")
    parser.add_argument("--height", type=int, help="Image height for the YUV file to be sent")
    parser.add_argument("--bitrate", type=int, help="Target bitrate (bps) for encoding the YUV stream")
    parser.add_argument("--message", help="The message to be sent")
    parser.add_argument("--hours", default="0", help="The time to run")
    parser.add_argument("--saveToDisk", default=0, help="The time to run")
    # added by wei on 10/10
    parser.add_argument("--mode", type=int, help="mode value", default=1)
    parser.add_argument("--value", type=int, help="reversed value", default=0)

    parser.add_argument("--dir", help="The dir  to be sent")

    # added by wei on 2025/05/12 for role
    parser.add_argument("--role", type=int, help="role value: 1 for broadcaster; 0 for audience", default=1)

    return parser.parse_args()


def parse_args_example() -> ExampleOptions:
    args = parse_args()
    logger.info(f"Parsed arguments:{args}")
    sample_options = ExampleOptions()
    sample_options.app_id = args.appId
    if args.token:
        sample_options.token = args.token
    else:
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
    sample_options.save_to_disk = args.saveToDisk
    sample_options.mode = args.mode
    sample_options.value = args.value
    sample_options.dir_path = args.dir
    sample_options.role = args.role
    return sample_options

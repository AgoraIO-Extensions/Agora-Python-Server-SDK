#!env python

import os
import sys
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
agora_rtc = os.path.dirname(os.path.dirname(script_dir))
if agora_rtc not in sys.path:
    sys.path.insert(0, agora_rtc)


def get_log_path_with_filename(channel_id, file):
    log_folder = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"_"+channel_id
    filename, _ = os.path.splitext(os.path.basename(file))
    return os.path.join(os.path.dirname(agora_rtc), 'logs', filename, log_folder, 'agorasdk.log')

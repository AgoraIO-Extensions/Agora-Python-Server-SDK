#!env python

import os
import sys
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(os.path.dirname(script_dir))
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)




def get_log_path_with_filename(filename):
    log_folder = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename, _ = os.path.splitext(os.path.basename(__file__))
    return os.path.join(os.path.dirname(sdk_dir), 'logs', filename ,log_folder, 'agorasdk.log')
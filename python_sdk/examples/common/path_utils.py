#!env python

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sdk_dir = os.path.dirname(os.path.dirname(script_dir))
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

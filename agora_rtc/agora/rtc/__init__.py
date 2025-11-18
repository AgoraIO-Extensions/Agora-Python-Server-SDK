#!/usr/bin/env python

import hashlib
import ssl
import zipfile
import site
from urllib import request
import ctypes
import os
import sys
import platform
import logging
logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context


from .. import sdk_library_dir, sdk_rtc_dir, sdk_rtm_dir

lib_dir = sdk_library_dir

try:
    if sys.platform == 'darwin':
        lib_agora_rtc_path = os.path.join(lib_dir, 'libAgoraRtcKit.dylib')
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)
        ctypes.CDLL(os.path.join(lib_dir, 'libAgoraAiNoiseSuppressionExtension.dylib'))

    elif sys.platform == 'linux':
        lib_agora_rtc_path = os.path.join(lib_dir, 'libagora_rtc_sdk.so')
        ctypes.CDLL(os.path.join(lib_dir, 'libagora-fdkaac.so'))
        #ctypes.CDLL(os.path.join(lib_dir, 'libagora_ai_noise_suppression_extension.so'))
        ctypes.CDLL(os.path.join(lib_dir, 'libagora-ffmpeg.so'))
        ctypes.CDLL(os.path.join(lib_dir, 'libagora-soundtouch.so'))
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)
        # should load it or the ains can not work
        ctypes.CDLL(os.path.join(lib_dir, 'libagora_ai_noise_suppression_extension.so'))
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {lib_agora_rtc_path}")
    sys.exit(1)

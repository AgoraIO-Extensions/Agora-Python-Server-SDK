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

#get so path: no need to check and download rtm sdk
# we have pack the rtm sdk into rtc package
# so no need to do downlaod and md5 check
logger.error(f"lib_dir: {sdk_library_dir}")


try:
    if sys.platform == 'darwin':
        lib_agora_rtm_path = os.path.join(sdk_library_dir, 'libagora_rtm_sdk_c.dylib')
        rtm_lib = ctypes.CDLL(lib_agora_rtm_path)

    elif sys.platform == 'linux':
        lib_agora_rtm_path = os.path.join(sdk_library_dir, 'libagora_rtm_sdk_c.so')
        rtm_lib = ctypes.CDLL(lib_agora_rtm_path)
        ctypes.CDLL(os.path.join(sdk_library_dir, 'libagora_rtm_sdk.so'))
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {lib_agora_rtm_path}")
    sys.exit(1)

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


def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_sdk_path():
    agora_service_path = os.path.dirname(os.path.abspath(__file__))
    # change from dir like: /home/xxx/agora_rtc/agora/rtc/agora_sdk to
    # /home/xxx/agora/agora_sdk
    # /home/xxx/agora/rtc
    # /home/xxx/agora/rtm
    parent_dir = os.path.dirname(agora_service_path)
    sdk_dir = os.path.join(parent_dir, "agora_sdk")
    
    return sdk_dir


def _check_download_and_extract_rtm():
    # just disalbe and manual download it to sdk_dir
    arch = platform.machine()
    os_type = platform.system()
    logger.error(f"arch: {arch}, os_type: {os_type}")
    pass
    





#get so path: no need to check and download rtm sdk
# we have pack the rtm sdk into rtc package
# so no need to do downlaod and md5 check
lib_path = get_sdk_path()
logger.error(f"lib_path: {lib_path}")


try:
    if sys.platform == 'darwin':
        lib_agora_rtm_path = os.path.join(lib_path, 'libagora_rtm_sdk_c.dylib')
        rtm_lib = ctypes.CDLL(lib_agora_rtm_path)

    elif sys.platform == 'linux':
        lib_agora_rtm_path = os.path.join(lib_path, 'libagora_rtm_sdk_c.so')
        rtm_lib = ctypes.CDLL(lib_agora_rtm_path)
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {lib_agora_rtm_path}")
    sys.exit(1)

#!/usr/bin/env python

import os
import sys
import logging
logger = logging.getLogger(__name__)
import ctypes
from urllib import request
import site
import zipfile
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import hashlib

def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _check_download_and_extract_sdk():
    agora_service_path = os.path.dirname(os.path.abspath(__file__))
    sdk_dir = os.path.join(agora_service_path, "agora_sdk")
    zip_path = os.path.join(agora_service_path, "agora_rtc_sdk.zip")

    url = "https://download.agora.io/sdk/release/agora_rtc_sdk-linux-gnu-v4.4.30-20241012_114642-379681.zip"
    libagora_rtc_sdk_path = os.path.join(sdk_dir, "libagora_rtc_sdk.so")
    rtc_md5 = "cf2705347bc8c3eae4bea98eab3dbf7e"
    if sys.platform == 'darwin':
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk_mac_v4.4.30_22304_FULL_20241015_1616_384496.zip"
        libagora_rtc_sdk_path = os.path.join(sdk_dir, "libAgoraRtcKit.dylib")
        rtc_md5 = "95dd26aa8942c63ae4ed05c71256c873"

    if os.path.exists(libagora_rtc_sdk_path) and get_file_md5(libagora_rtc_sdk_path) == rtc_md5:
        return

    logger.error("missing agora sdk, now download it, please wait for a while...")
    if os.path.exists(sdk_dir):
        os.system(f"rm -rf {sdk_dir}")        
    os.makedirs(agora_service_path, exist_ok=True)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    logger.info(f"agora_service_path: {agora_service_path}")
    logger.info(f"Downloading {url}...")
    request.urlretrieve(url, zip_path)

    logger.info(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(agora_service_path)

    if os.path.exists(zip_path):
        os.remove(zip_path)
    logger.error("download done, continue...")


_check_download_and_extract_sdk()

sdk_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(sdk_dir, 'agora_sdk')

try:
    if sys.platform == 'darwin':
        lib_agora_rtc_path =os.path.join(lib_path, 'libAgoraRtcKit.dylib')
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)

    elif sys.platform == 'linux':
        lib_agora_rtc_path =os.path.join(lib_path, 'libagora_rtc_sdk.so')
        ctypes.CDLL(os.path.join(lib_path, 'libagora-fdkaac.so'))
        ctypes.CDLL(os.path.join(lib_path, 'libaosl.so'))
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)    
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {lib_agora_rtc_path}")
    sys.exit(1)
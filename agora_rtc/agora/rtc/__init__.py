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


def _check_download_and_extract_sdk():
    agora_service_path = os.path.dirname(os.path.abspath(__file__))
    sdk_dir = os.path.join(agora_service_path, "agora_sdk")
    zip_path = os.path.join(agora_service_path, "agora_rtc_sdk.zip")

    # for diff os and arch
    arch = platform.machine()
    os_type = platform.system()

    

    #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.30-20241024_101940-398537.zip"
    # version 2.2.0 for linux
    #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.31-20241223_111509-491956.zip"
    url  = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250425_144419-675648.zip"
        
           
    libagora_rtc_sdk_path = os.path.join(sdk_dir, "libagora_rtc_sdk.so")
    #rtc_md5 = "7031dd10d1681cd88fd89d68c5b54282"
    rtc_md5 = "0d6c96bbebdd9b0a84b9cdf01ba6aa7f"
    if sys.platform == 'darwin':
        #url = "https://download.agora.io/sdk/release/agora_rtc_sdk_mac_rel.v4.4.30_22472_FULL_20241024_1224_398653.zip"
        # version   2.2.0 for mac
        #url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.31_23136_FULL_20241223_1245_492039.zip"
        url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_24257_FULL_20250425_1609_675722.zip"

        libagora_rtc_sdk_path = os.path.join(sdk_dir, "libAgoraRtcKit.dylib")
        #rtc_md5 = "ca3ca14f9e2b7d97eb2594d1f32dab9f"
        rtc_md5 = "358be32c5dfc72192402cf49838ea942"
    if arch == "aarch64" and sys.platform == 'linux':
        #url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.31-20250307_175457-603878.zip"
        url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20250425_150503-675674.zip"
        rtc_md5 = "a217a8ed32c964843b120006511121cf"


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
        lib_agora_rtc_path = os.path.join(lib_path, 'libAgoraRtcKit.dylib')
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)

    elif sys.platform == 'linux':
        lib_agora_rtc_path = os.path.join(lib_path, 'libagora_rtc_sdk.so')
        ctypes.CDLL(os.path.join(lib_path, 'libagora-fdkaac.so'))
        ctypes.CDLL(os.path.join(lib_path, 'libaosl.so'))
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {lib_agora_rtc_path}")
    sys.exit(1)

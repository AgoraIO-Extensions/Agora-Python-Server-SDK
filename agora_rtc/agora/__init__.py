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

'''
# this is the global init for agora python server sdk, include rtc and rtm
# it will check the sdk version and download the latest sdk if needed
path dir structure is:
   /home/xxx/agora/
                agora_sdk
                    include
                    *.so/*.dylib
                rtc
                    __init__.py
                    rtc*.py
                rtm
                    __init__.py
                    rtm*.py
                __init__.py
                setup.py
                README.md
                LICENSE
                CHANGELOG.md
                CONTRIBUTING.md
                CODE_OF_CONDUCT.md
                SECURITY.md
                CONTRIBUTORS.md
'''
'''
# requirement for package zip file:
no root dir, only so/dylib file in the root dir
'''




def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"get_file_md5 error: {e}")
        return ""


#get agora root path, like: /home/xxx/agora
def get_sdk_root_path():
    agora_path = os.path.dirname(os.path.abspath(__file__))
    return agora_path
#get agora 's library path, like: /home/xxx/agora/agora_sdk/
def get_sdk_library_path():
    agora_path = get_sdk_root_path()
    library_path = os.path.join(agora_path, "agora_sdk")    
    
    return library_path
def get_sdk_rtc_path():
    agora_path = get_sdk_root_path()
    rtc_path = os.path.join(agora_path, "rtc")
    return rtc_path
def get_sdk_rtm_path():
    agora_path = get_sdk_root_path()
    rtm_path = os.path.join(agora_path, "rtm")
    return rtm_path


#helper function to download file from ur
def report_progress(blocknum, blocksize, totalsize):
    """
    下载进度回调函数
    """
    if totalsize > 0:
        # calculate download progress percentage
        percent = min(100, (blocknum * blocksize) / totalsize * 100)
        # use carriage return to overwrite current line, to update progress in place
        print(f"\rDownloading: ----{percent:.2f}%-----", end='', flush=True)
        # when download is complete (or calculated value exceeds 100%)
        if percent >= 100:
            print("Downloading: ----100.00%-----\n")
    else:
        # if cannot get file total size, show downloaded bytes
        downloaded = blocknum * blocksize
        print(f"\rDownloading: ----{downloaded} bytes-----", end='', flush=True)


def _check_download_and_extract_sdk():
    agora_service_path = os.path.dirname(os.path.abspath(__file__))
    # change from dir like: /home/xxx/agora_rtc/agora/rtc/agora_sdk to
    # /home/xxx/agora_rtc/agora/agora_sdk
    # /home/xxx/agora_rtc/agora/rtc
    # /home/xxx/agora_rtc/agora/rtm
    global sdk_library_dir, sdk_root_dir
    
    zip_path = os.path.join(sdk_root_dir, "agora_rtc_sdk.zip")
    logger.error(f"sdk_library_dir: {sdk_library_dir}")
    logger.error(f"zip_path: {zip_path}")

    # for diff os and arch
    arch = platform.machine()
    os_type = platform.system()

    

    #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.30-20241024_101940-398537.zip"
    # version 2.2.0 for linux
    #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.31-20241223_111509-491956.zip"
    #url  = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250715_161625-791246.zip"
    #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250829_160340-860733.zip"
    #fusion version: 20251023

    url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250829_160340-860733-aed_20251107_1642.zip"
    #20251110 Fusion version: with apm filter
    mac_sdk="https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.30_25869_FULL_20251030_1836_953684-aed.zip"
    linux_sdk = "https://download.agora.io/sdk/release/agora_rtc_sdk_x86_64-linux-gnu-v4.4.32.150_26715_SERVER_20251030_1807-aed.zip"
    
          
    linux_libfile_path = os.path.join(sdk_library_dir, "libagora_rtc_sdk.so")
    mac_libfile_path = os.path.join(sdk_library_dir, "libAgoraRtcKit.dylib")
    linux_md5 = "821cb1a388279648fcb204ca795e6476"
    mac_md5 = "5b9940d3fca033a53ac30216d5c39be6"

    #rtc_md5 = "7031dd10d1681cd88fd89d68c5b54282"
    url = linux_sdk
    rtc_md5 = linux_md5
    rtc_libfile_path = linux_libfile_path
    if sys.platform == 'darwin':
        #url = "https://download.agora.io/sdk/release/agora_rtc_sdk_mac_rel.v4.4.30_22472_FULL_20241024_1224_398653.zip"
        # version   2.2.0 for mac
        #url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.31_23136_FULL_20241223_1245_492039.zip"
        #url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_24915_FULL_20250715_1710_791284.zip"
        #url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_25418_FULL_20250829_1647_860754.zip"
        #20251023 Fusion version: one sdk package include rtc and rtm
        #url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_25418_FULL_20250829_1647_860754-aed_20251107_1639.zip"
        url = mac_sdk

        rtc_libfile_path = mac_libfile_path
        #rtc_md5 = "ca3ca14f9e2b7d97eb2594d1f32dab9f"
        rtc_md5 = mac_md5
    if arch == "aarch64" and sys.platform == 'linux':
        #url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.31-20250307_175457-603878.zip"
        #url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20250425_150503-675674.zip"
        #url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20251009_145437-921455.zip"
        url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20251009_145437-921455_20251023_1538.zip"
        rtc_md5 = "5c002f25d2b381e353082da4f835b4f2"

    is_file_exist = os.path.exists(rtc_libfile_path)
    if is_file_exist:
        md5_value = get_file_md5(rtc_libfile_path)
    else:
        md5_value = ""
    if md5_value == rtc_md5:
        return

    logger.error(f"missing agora sdk, now download it, please wait for a while...: {rtc_libfile_path} {md5_value} {rtc_md5} {is_file_exist}")
    if os.path.exists(sdk_library_dir):
        os.system(f"rm -rf {sdk_library_dir}")
    os.makedirs(sdk_library_dir, exist_ok=True)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    logger.error(f"sdk_library_dir: {sdk_library_dir}")
    logger.error(f"Downloading {url}...")
    #download_file_with_progress(url, zip_path)
    request.urlretrieve(url, zip_path,reporthook=report_progress)


    logger.error(f"Extracting {zip_path}...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(sdk_root_dir)

    if os.path.exists(zip_path):
        os.remove(zip_path)
    logger.error("download done, continue...")



sdk_root_dir = get_sdk_root_path()
sdk_rtc_dir = get_sdk_rtc_path()
sdk_rtm_dir = get_sdk_rtm_path()
sdk_library_dir = get_sdk_library_path()

_check_download_and_extract_sdk()


if sys.platform == 'darwin':
    rtc_libfile_path = os.path.join(sdk_library_dir, 'libAgoraRtcKit.dylib')
else:
    rtc_libfile_path = os.path.join(sdk_library_dir, 'libagora_rtc_sdk.so')
    ctypes.CDLL(os.path.join(sdk_library_dir, 'libaosl.so'))

#check if the library exists
if not os.path.exists(rtc_libfile_path):
    logger.error(f"library {rtc_libfile_path} not found")
    sys.exit(1)

# 显式导出这些变量，确保子模块可以导入
__all__ = ['sdk_library_dir', 'sdk_rtc_dir', 'sdk_rtm_dir', 'sdk_root_dir']
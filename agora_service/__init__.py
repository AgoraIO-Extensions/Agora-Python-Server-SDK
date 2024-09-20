#!/usr/bin/env python

import os
import sys
import ctypes

sdk_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(sdk_dir, 'agora_sdk')

print("sdk_dir:", lib_path)

try:
    if sys.platform == 'darwin':
        lib_agora_rtc_path =os.path.join(lib_path, 'libAgoraRtcKit.dylib')
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)
    elif sys.platform == 'linux':        
        lib_agora_rtc_path =os.path.join(lib_path, 'libagora_rtc_sdk.so')
        ctypes.CDLL(os.path.join(lib_path, 'libagora-fdkaac.so'))
        ctypes.CDLL(os.path.join(lib_path, 'libagora-core.so'))
        agora_lib = ctypes.CDLL(lib_agora_rtc_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    print(f"Attempted to load from: {lib_agora_rtc_path}")
    sys.exit(1)
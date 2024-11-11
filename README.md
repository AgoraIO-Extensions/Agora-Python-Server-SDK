# Note
- This is a Python SDK wrapper for the Agora RTC SDK.
- It supports Linux and Mac platforms.
- The examples are provided as very simple demonstrations and are not recommended for use in production environments.

# Very Important Notice !!!
- A process can only have one instance.
- An instance can have multiple connections.
- In all observers or callbacks, you must not call the SDK's own APIs, nor perform CPU-intensive tasks in the callbacks; data copying is allowed.

# Required Operating Systems and Python Versions
- Supported Linux versions:
  - Ubuntu 18.04 LTS and above
  - CentOS 7.0 and above
  
- Supported Mac versions:
  - MacOS 13 and above

- Python version:
  - Python 3.10 and above

# Using Agora-Python-Server-SDK
```
pip install agora_python_server_sdk
```

# Running Examples

## Preparing Test Data
- Download and unzip [test_data.zip](https://download.agora.io/demo/test/test_data_202408221437.zip) to the Agora-Python-Server-SDK directory.

## Executing Test Script
```
python agora_rtc/examples/example_audio_pcm_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
```

# Change log

## 2024.11.11 发布 2.1.3
- Added a new sample: example_jpeg_send.py which can push JPEG files or JPEG streams to a channel.
-
- Performance overhead, as noted in the example comments, can be summarized as follows:
- For a 1920x1080 JPEG file, the process from reading the file to converting it to an RGBA bytearray - takes approximately 11 milliseconds.


## 2024.11.07 release 2.1.2
- Updates `user_id` in the `AudioVolumeInfoInner and AudioVolumeInfo` structure to `str` type.
- Fixes the bug in `_on_audio_volume_indication` callback, where it could only handle one callback to speaker_number 
- Corrects the parameter type in `IRTCLocalUserObserver::on_audio_volume_indication` callback to `list` type.

## 2024.10.29 release 2.1.1

Add audio VAD interface of version 2 and corresponding example.

## 2024.10.24 release 2.1.0

Fixed some bug.

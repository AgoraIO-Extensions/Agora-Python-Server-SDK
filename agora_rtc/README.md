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
  - Python 3.8 and above

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


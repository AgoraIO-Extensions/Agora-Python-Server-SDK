# Notice
- this is a python sdk wrappered agora rtc sdk.
- can dev under mac, and release unde linux
- the examples is just a simple demo, it is not a good practice to use it in production
# Very import notice !!!!!!!
- It's crucial that a process can only have one instance.
- One instance can have multiple connections.
- In all observers or callbacks, it is not allowed to call the SDK's own APIs, nor is it permitted to perform   CPU-intensive tasks within the callbacks. However, data copying is allowed.

# Required OS and python version
- supported Linux version: 
  - Ubuntu 18.04 LTS and above
  - CentOS 7.0 and above
  
- supported Mac version:

  - MacOS 13 and above

- python version:
  - python 3.8 above

# Test Data
- download and unzip [test_data.zip](https://download.agora.io/demo/test/test_data_202408221437.zip)

# Use Agora-Python-Server-SDK
```
pip install agora_python_server_sdk
```

## run examples
```
python agora_rtc/examples/example_audio_pcm_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
```

# Some import call sequence
- about audio frame observer： 

set_playback_audio_frame_before_mixing_parameters MUST be call before register_audio_frame_observer

sample code:
```
localuser.set_playback_audio_frame_before_mixing_parameters(1, 16000)
audio_observer = BizAudioFrameObserver()
localuser.register_audio_frame_observer(audio_observer)
```
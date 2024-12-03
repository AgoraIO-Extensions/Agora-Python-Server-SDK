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

## 2024.12.03 release Version 2.1.5
- Modifications:
  - LocalUser/audioTrack:
    -- When the scenario is chorus, developers don't need to call setSendDelayInMs.
    -- When the scenario is chorus, developers don't need to set the audio scenario of the track to chorus.
    -- NOTE: This can reduce the difficulty for developers. In AI scenarios, developers only need to set the service to chorus.
- Additions:
  -- Added the VadDump class, which can assist in troubleshooting vad issues in the testing environment. However, it should not be enabled in the online env  ironment.
  -- Added the on_volume_indication callback.
  -- Added the on_remote_video_track_state_changed callback.
- Removals:
  -- Removed Vad V1 version, only retaining the V2 version. Refer to voice_detection.py and sample_audio_vad.py.
- Updates:
  -- Updated relevant samples: audioconsume, vad sample.

## 2024.11.12 release 2.1.4
- Modify the type of metadata in videoFrame from str to bytes type to be consistent with C++; thus, it can support byte streams.
- The internal encapsulation of ExteranlVideoFrame has been modified to support byte streams. Regarding the support for alpha encoding, a logical judgment has been made. If fill_alpha_buffer is 0, it will not be processed.
## 2024.11.11 release 2.1.3
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


### Common Usage Q&A
## The relationship between service and process?
- A process can only have one service, and the service can only be initialized once.
- A service can only have one media_node_factory.
- A service can have multiple connections.
- Release media_node_factory.release() and service.release() when the process exits.
## If using Docker with one user per Docker, when the user starts Docker and logs out, how should Docker be released?
- In this case, create service/media_node_factory and connection when the process starts.
- Release service/media_node_factory and connection when the process exits, ensuring that...
## If Docker is used to support multiple users and Docker runs for a long time, what should be done?
- In this case, we recommend using the concept of a connection pool.
- Create service/media_node_factory and a connection pool (only new connections, without initialization) when the process starts.
- When a user logs in, get a connection from the connection pool, initialize it, execute con.connect() and set up callbacks, and then join the channel.
- Handle business operations.
- When a user logs out, execute con.disconnect() and release the audio/video tracks and observers associated with the connection, but do not call con.release(); then put the connection back into the connection pool.
- When the process exits, release the connection pool (release each con.release()), service/media_node_factory, and the connection pool (release each con.release()) to ensure resource release and optimal performance.
## Use of VAD
# Source code: voice_detection.py
# Sample code: example_audio_vad.py
# It is recommended to use VAD V2 version, and the class is: AudioVadV2; Reference: voice_detection.py.
# Use of VAD:
  1. Call _vad_instance.init(AudioVadConfigV2) to initialize the vad instance. Reference: voice_detection.py. Assume the instance is: _vad_instance
  2. In audio_frame_observer::on_playback_audio_frame_before_mixing(audio_frame):

  3. Call the process of the vad module: state, bytes = _vad_instance.process(audio_frame)
Judge the value of state according to the returned state, and do corresponding processing.

    A. If state is _vad_instance._vad_state_startspeaking, it indicates that the user is "starting to speak", and speech recognition (STT/ASR) operations can be started. Remember: be sure to pass the returned bytes to the recognition module instead of the original audio_frame, otherwise the recognition result will be incorrect.
    B. If state is _vad_instance._vad_state_stopspeaking, it indicates that the user is "stopping speaking", and speech recognition (STT/ASR) operations can be stopped. Remember: be sure to pass the returned bytes to the recognition module instead of the original audio_frame, otherwise the recognition result will be incorrect.
    C. If state is _vad_instance._vad_state_speaking, it indicates that the user is "speaking", and speech recognition (STT/ASR) operations can be continued. Remember: be sure to pass the returned bytes to the recognition module instead of the original audio_frame, otherwise the recognition result will be incorrect.
# Note: 
  If the vad module is used and it is expected to use the vad module for speech recognition (STT/ASR) and other operations, then be sure to pass the returned bytes to the recognition module instead of the original audio_frame, otherwise the recognition result will be incorrect.
# How to better troubleshoot VAD issues: It includes two aspects, configuration and debugging.
  1. Ensure that the initialization parameters of the vad module are correct. Reference: voice_detection.py.
  2. In state, bytes = on_playback_audio_frame_before_mixing(audio_frame):

    - A . Save the data of audio_frame to a local file, reference: example_audio_pcm_send.py. This is to record the original audio data. For example, it can be named: source_{time.time()*1000}.pcm
    - B.Save the result of each vad processing:

      - a When state == start_speaking: create a new binary file, for example, named: vad_{time.time()*1000}.pcm, and write bytes to the file.
      - b When state == speaking: write bytes to the file.
      - c When state == stop_speaking: write bytes to the file and close the file.
    Note: In this way, problems can be troubleshot based on the original audio file and the audio file processed by vad. This function can be disabled in the production environment.
### How to push the audio generated by TTS into the channel?
  # Source code: audio_consumer.py
  # Sample code: example_audio_consumer.py
### How to release resources?

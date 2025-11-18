# Note
- This is a Python SDK wrapper for the Agora RTC SDK.
- It supports Linux and Mac platforms.
- The examples are provided as very simple demonstrations and are not recommended for use in production environments.
-rtc examples：https://github.com/AgoraIO-Extensions/Agora-python-Server-SDK/examples
-rtm examples: https://github.com/AgoraIO-Extensions/Agora-python-Server-SDK/examples_rtm

# Very Important Notice !!!
- A process can only have one instance,and the instance created in process startup is the global instance,and released in process shutdown.
- An instance can have multiple connections.
- In all observers or callbacks, you must not call the SDK's own APIs, nor perform CPU-intensive tasks in the callbacks; data copying is allowed.
- supported video codec:
  - H264: support both encoding and decoding
  - VP8: support both encoding and decoding
  - VP9: support both encoding and decoding
  - H265: only decoding is supported, encoding willl support in the future
  - AV1: both encoding and decoding are suported but if video image's solution is less than 360p, the codec will be changed to H264
- if you want to recive the encoded video data:
  - set: video_subscription_options.encodedFrameOnly = 1
  - and then register: set_encoded_video_frame_observer


# Required Operating Systems and Python Versions
- Supported Linux versions:
  - Ubuntu 18.04 LTS and above
  - CentOS 7.0 and above
  
- Supported Mac versions:
  - MacOS 13 and above(only for coding and testing)

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
or linux os, should set env to ：/site_packages/agora/agora_sdk/, like:
export LD_LIBRARY_PATH=/site_packages/agora/agora_sdk/
```
python agora_rtc/examples/example_audio_pcm_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
```

# Change log
## 2025.11.18 Release version 2.4.0
-- Update SDK to APM version: 4.4.32/1025
-- Add configure support for enabling/disabling APM
-- Update methods in setup.py and __init__.py, ok, including version/URL, md5, etc.
-- Overall code pipeline ok, needs testing?? ok
-- Add support to rtm, one single sdk supports both rtm and rtc, ok
-- todo:
  -[] Need to add VAD algorithm update ok
  -[] Need to add vad_dump modifications ok
  -[] Modify APM algorithm to support VAD switch, ok
  -[] Add VAD configure parameter settings, ok
  -[] Download every time, check md5 mismatch?? ok
  NOTE:
  APM features, i.e., server-side echo cancellation, noise suppression, automatic gain control, background voice removal, etc.
  Normally, AEC/AINS/AGC, etc., are already implemented on the client side, and the server side does not need to implement them again, unless there are special requirements.
  If you want to enable APM features, please contact Agora technical support.
  NOTE：
  How to use rtc,please ref to: https://github.com/AgoraIO-Extensions/Agora-Python-Server-SDK/tree/main/agora_rtc/examples
  Hot to use rtm,please ref to ://github.com/AgoraIO-Extensions/Agora-Python-Server-SDK/tree/main/agora_rtc/rtm_examples
# 2025.11.07 release 2.3.3
-- update: to support rtm
-- adjust sdk's directory structure
-- change requests to urllib
# 2025.10.23 release 2.3.2: support rtc and rtm in one package
-- update: to support rtm.can support both rtc and rtm in one package.
-- adjust sdk's directory structure
-- update rtc sdk
# 2025.10.09  release 2.3.1
-- update arm64 rtc sdk:Fixed a JNI referencing issue in the previous arm64 build. This issue only outputs logs to the console and does not affect functionality.

#2025.09.01  release 2.3.0

Overview

Agora Python SDK version 2.3.0 introduces significant enhancements for real-time audio and video communication, with particular optimizations for AI server scenarios. This release includes API improvements, automation of previously manual processes, and increased flexibility in connection configuration.

New Features

1. AudioScenarioAiServer Support

• Added support for the AudioScenarioAiServer scenario type, now set as the default AudioScenario.

• Enables configuration of different scenarios and profiles for connections within the same process.

• Important: When using AI server scenario, client-side must use AIClient scenario to avoid audio abnormalities. Please consult Agora support for SDK versions supporting AIClient scenario.

2. Enhanced Connection Configuration

• Introduced PublishConfigure parameter in connection creation for setting:

  • Scenario and profile configurations

  • Audio/Video publication settings

  • Other publication parameters

• Added multiple observer registration methods to connections:

  • RegisterLocalUserObserver

  • RegisterAudioFrameObserver

  • RegisterVideoFrameObserver

  • RegisterVideoEncodedFrameObserver

3. Stream Management Improvements

• Added publication control methods:

  • PublishAudio/UnpublishAudio

  • PublishVideo/UnpublishVideo

• Added data pushing methods:

  • PushAudioPcmData/PushAudioEncodedData

  • PushVideoFrame/PushVideoEncodedData

• Added InterruptAudio method for supporting interruption functionality

• Added IsPushToRTCCompleted method for checking push status

• Added SendAudioMetaData method for audio metadata transmission

4. Automation Enhancements

• Eliminated manual CreateDataStream calls - now handled automatically

• Automatic observer unregistration on Release() instead of manual unregistering

• Internal handling of media node factory creation:

  • No longer requires manual calls to newMediaNodeFactory

  • Automatic handling of track creation (NewCustomAudioTrackPcm, NewCustomAudioTrackEncoded, NewCustomVideoTrack)

  • Automatic management of audio data senders (NewAudioPcmDataSender)

Integration Process

The updated integration workflow is as follows:

1. Initialize Agora Service (once per process startup):
   config = AgoraServiceConfig()
   agora_service = AgoraService()
   agora_service.initialize(config)
   

2. Connection Management (can be looped for multiple connections):
   # Create connection with configuration
   con = agora_service.create_rtc_connection(con_config, publish_config)
   
   # Register observers
   con.register_observer(conHandler)
   con.register_audio_frame_observer(audioFrameObserver)
   con.register_local_user_observer(localUserObserver)
   
   # Connect and publish
   con.connect(token, channelName, userId)
   con.publish_audio()  # or con.publish_video()
   
   # Push data
   con.push_audio_pcm_data()  # or push_audio_encoded_data()
   # or con.push_video_frame()/push_video_encoded_data()
   
   # Disconnect and release
   con.disconnect()
   con.release()
   

3. Release Agora Service (once during process termination):
   agora_service.release()
   

Performance Recommendations

1. For AI Scenarios:
   • Use AudioScenarioAIServer for server-side applications

   • Provides optimized performance with lower latency (20-30ms reduction on iPhone compared to chorus)

   • Enhanced experience in weak network conditions

   • Mandatory: Client must use AIClient scenario

2. For Non-AI Scenarios:
   • Consult Agora technical support for appropriate scenario configuration

   • Ensure configuration matches specific business use cases

Bug Fixes

• Updated RTC SDK with 2 bug fixes

Important Notes

• Backward Compatibility: Review integration code for manual calls that are now automated

• Scenario Matching: Ensure client-server scenario compatibility (AIServer requires AIClient)

• Resource Management: Connection release now automatically handles observer unregistration

• Consult Support: For specific integration guidance and upgrade assistance, contact Agora SA

Summary of Core Changes

Before After 2.3.0

Manual CreateDataStream ✅ Automatic

Manual observer unregistration ✅ Automatic on Release()

Fixed per-process scenario ✅ Multi-scenario per process

Client/Server scenario mismatch ❗ AIClient mandatory for AI use

For detailed implementation guidance and version-specific support, please consult Agora technical support.


## 2025.04.28 Release 2.2.4
-- Update: update rtc sdk from 4.4.31 to 4.4.32
## 2025.04.14 Release 2.2.3
-- Fix: 
  -- Fixed a bug in the salt processing in enable_encryption
  -- Updated the logic in enable_encryption, no processing when enable is 0
2025.04.10 Release 2.2.2
-- Additions:
  - Added push_video_encoded_file.py to support pushing mp4 files and h264 encoded h.264 files. Includes conversion from mp4 file avformat to raw 264 stream in annex B format.
-- Additions:
  - Added set_log_file_filter function to set the log filter level.
-- Additions:
  - Added support for arm64 version, but currently this version does not support audio label algorithm. Therefore, it is not supported on arm64!
-- Changes:
  - Modified localuserstats, local video stats, local audio stats, remote video stats, remote audio stats.
-- Additions:
  - Added connection::agora_rtc_conn_enable_encryption.
-- Additions:
  - Added connectionObserver::on_encryption_error (but not working for now, need to fix in the next monthly version 4.4.32).

2025.02.26 Release 2.2.1
--Update：
  ​- Reduced buffer size from ​180ms​ to ​100ms​ to minimize latency.
-- Added：
  - AudioConsumer::is_push_to_rtc_completed： Add audio consumer support for playback state notifications.
-- ​Bug fix:
  - Fixed incorrect _samples_per_channel calculation in stereo mode.

2025.01.08 Release 2.2.0
-- Updates:
  - Update the SDK version from 4.4.30 to 4.4.31. Done.
-- FEAT:
  - Add serviceconfigure.
    - Add domain_limit. Done.
    - Add should_callback_when_muted. Done.
    - Add colorspacetype to ExternalVideoFrame to support the encoding of solid-color backgrounds in virtual human scenarios. Done.
-- FEAT:
  - Add the AudioMetaData interface: localuser::send_audio_meta_data. Done.
  - Add the OnAudioMetaDataReceived callback to localuserObserver::on_audio_meta_data_received. Done.
-- Sample modifications.
2024.12.17 Release 2.1.7
--Changes:

  Fixed the typeError issue in LocalUser::sub/unsub audio/video.
  Adjusted the default stopRecogCount for VAD from 30 to 50.
  Modified sample_vad.
## 2024.12.09 Release 2.1.6
- New Features:
  -- Added AudioVadManager to manage VAD (Voice Activity Detection) instances.
  -- Integrated VAD functionality into the SDK. Developers no longer need to worry about how to use VAD; they only need to focus on setting appropriate parameters. Reference: sample_audio_vad.py
- Changes:
  -- In register_audio_frame_observer, two new parameters have been added to set the VAD parameters. Reference: sample_audio_vad.py
  -- In on_playback_audio_frame_before_mixing, two new return values have been added: vad_result_state and vad_result_bytearray.
    state:
    < 0: No internal automatic VAD applied
    0: No speaking
    1: Started speaking
    2: Speaking
    3: Stopped speaking
    vad_result_bytearray: The result processed by VAD, returned when VAD is active.
    If automatic VAD is enabled:
    Developers should use vad_result_bytearray for subsequent business processing (e.g., sending to ASR/STT), rather than using the raw frame data.
    Reference: sample_audio_vad.py
- Optimizations:
  -- Replaced the use of pacer with AudioConsumer for pushing PCM audio.
- Updates:
  -- Updated the samples related to Pacer and VAD.
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

### How to release resource?
## 如何释放资源？
    localuser.unpublish_audio(audio_track)
    localuser.unpublish_video(video_track)
    audio_track.set_enabled(0)
    video_track.set_enabled(0)

    localuser.unregister_audio_frame_observer()
    localuser.unregister_video_frame_observer()
    localuser.unregister_local_user_observer()

    connection.disconnect()
    connection.unregister_observer()

    localuser.release()
    connection.release()

    
    audio_track.release()
    video_track.release()
    pcm_data_sender.release()
    video_data_sender.release()
    audio_consumer.release()

    media_node_factory.release()
    agora_service.release()
    
    #set to None
    audio_track = None
    video_track = None
    audio_observer = None
    video_observer = None
    local_observer = None
    localuser = None
    connection = None
    agora_service = None

## Interrupt Handling in AI Scenarios
# Definition of Interrupt
In human-machine dialogue, an interrupt refers to the situation where a user suddenly interrupts the robot's response, requesting the robot to stop its current response immediately and shift to answer the user's new question. This behavior is called an interrupt.

# Trigger Conditions for Interrupts
Interrupts can be defined in different ways depending on the product. There are generally two modes:

- Mode 1: Voice Activation Mode
When it detects that the user is speaking, the interrupt strategy is triggered. For example, when the system recognizes speech, it triggers the interrupt strategy to stop the robot's response.

- Mode 2: ASR Activation Mode
When the system detects that the user is speaking and receives a result from ASR (Automatic Speech Recognition) or STT (Speech-to-Text), the interrupt strategy is triggered.

# Advantages of Different Interrupt Strategies
Voice Activation Interrupt

Advantages:
Reduces the user's wait time and the likelihood of interrupts, as the robot will stop its response immediately when the user starts speaking, eliminating the need for the user to wait for the robot to finish speaking.
Disadvantages:
Since this is voice-activated, it may be triggered by meaningless audio signals, depending on the accuracy of the VAD (Voice Activity Detection). For example, if someone is typing on the keyboard while the AI is speaking, it might trigger the interrupt incorrectly.
ASR Activation Interrupt

Advantages:
Reduces the probability of unnecessary interrupts because the interrupt strategy is triggered only after ASR or STT has recognized the user’s speech.
Disadvantages:
Since this is ASR/STT-triggered, it requires converting the audio signal into text, which introduces a delay before the interrupt can be processed.
- Recommended Mode
If the VAD can filter out non-speech signals and only triggers when human speech is detected, the Voice Activation Mode is recommended. This mode is also suitable when the delay in processing the interrupt is not a major concern.

If the interrupt delay is not sensitive, the ASR Activation Mode is recommended. This mode can filter out non-speech signals more effectively and reduce the probability of an unintended interrupt.

How to Implement Interrupts? What Actions Are Required?
In a human-machine dialogue system, conversations are typically structured in "rounds," where each round consists of a question from the user, followed by a response from the robot, and so on. For each round, we can assign a roundId, incrementing it with each new round. A round consists of the following stages:

VAD (Voice Activity Detection):
This marks the start of the dialogue, where the system detects the beginning and end of the user's speech. It then passes this information to the ASR for further processing.

ASR (Automatic Speech Recognition):
This phase involves recognizing the user's speech and converting it into text, which is then passed to the LLM (Large Language Model).

LLM (Large Language Model):
This is the generation phase, where the LLM processes the recognized user input and generates a response.

TTS (Text-to-Speech):
In this phase, the LLM’s response is converted into an audio format.

RTC Streaming:
The generated audio is streamed via RTC (Real-Time Communication) to be played back to the user.

Therefore, an interrupt happens when, in the next round (roundId+1), either through Voice Activation (triggered by the VAD phase) or ASR Activation (triggered when ASR recognizes the user’s speech), the following actions must be performed:

Stop the LLM Generation in the current round (roundId).
Stop the TTS Synthesis in the current round (roundId).
Stop the RTC Streaming in the current round (roundId).
API Call References:
Call: AudioConsumer.clear()
Call: LocalAudioTrack.clear_sender_buffer()
Business Layer: Clear any remaining TTS-related data (if applicable)


## When to Pass LLM Results to TTS for Synthesis?
LLM (Large Language Model) results are returned asynchronously and in a streaming manner. When should the results from the LLM be passed to TTS (Text-to-Speech) for synthesis?

Two main factors need to be considered:

Ensure that the TTS synthesized speech is unambiguous:
The speech synthesized by TTS must be clear, complete, and continuous. For example, if the LLM returns the text: "中间的首都是北京吗？", and we pass it to TTS as:

"中",
"国首",
"是北",
"京吗？",
This would result in ambiguous synthesis because there are no spaces between certain words (e.g., between "中" and "国", "首" and "是", and "京" and "吗"). Proper segmentation must be ensured to avoid such ambiguities.
Minimize overall processing delay:
If the LLM results are passed to TTS only after the entire response is generated, the speech synthesis will be unambiguous and continuous. However, this approach introduces significant delay, which negatively affects the user experience.

Recommended Approach
To achieve a balance between clarity and minimal delay, the following steps should be followed:

Store the LLM results in a cache as they are received.
Perform a reverse scan of the cached data to find the most recent punctuation mark.
Truncate the data from the start to the most recent punctuation mark and pass it to TTS for synthesis.
Remove the truncated data from the cache. The remaining data should be moved to the beginning of the cache and continue waiting for additional data from the LLM.

##VAD Configuration Parameters
AgoraAudioVadConfigV2 Properties

Property Name	Type	Description	Default Value	Value Range
preStartRecognizeCount	int	Number of audio frames saved before detecting speech	16	[0, ]
startRecognizeCount	int	Total number of audio frames to detect speech start	30	[1, max]
stopRecognizeCount	int	Number of audio frames to detect speech stop	50	[1, max]
activePercent	float	Percentage of active frames in startRecognizeCount frames	0.7	[0.0, 1.0]
inactivePercent	float	Percentage of inactive frames in stopRecognizeCount frames	0.5	[0.0, 1.0]
startVoiceProb	int	Probability that an audio frame contains human voice	70	[0, 100]
stopVoiceProb	int	Probability that an audio frame contains human voice	70	[0, 100]
startRmsThreshold	int	Energy dB threshold for detecting speech start	-50	[-100, 0]
stopRmsThreshold	int	Energy dB threshold for detecting speech stop	-50	[-100, 0]
Notes:
startRmsThreshold and stopRmsThreshold:

The higher the value, the louder the speaker's voice needs to be compared to the surrounding background noise.
In quiet environments, it is recommended to use the default value of -50.
In noisy environments, you can increase the threshold to between -40 and -30 to reduce false positives.
Adjusting these thresholds based on the actual use case and audio characteristics can achieve optimal performance.
stopRecognizeCount:

This value reflects how long to wait after detecting non-human voice before concluding that the user has stopped speaking. It controls the gap between consecutive speech utterances. Within this gap, VAD will treat adjacent sentences as part of the same speech.
A shorter gap will increase the likelihood of adjacent sentences being recognized as separate speech segments. Typically, it is recommended to set this value between 50 and 80.
For example: "Good afternoon, [interval_between_sentences] what are some fun places to visit in Beijing?"

If the interval_between_sentences between the speaker's phrases is greater than the stopRecognizeCount, the VAD will recognize the above as two separate VADs:

VAD1: Good afternoon
VAD2: What are some fun places to visit in Beijing?
If the interval_between_sentences is less than stopRecognizeCount, the VAD will recognize the above as a single VAD:

VAD: Good afternoon, what are some fun places to visit in Beijing?



If latency is a concern, you can lower this value, or consult with the development team to determine how to manage latency while ensuring semantic continuity in speech recognition. This will help avoid the AI being interrupted too sensitively.
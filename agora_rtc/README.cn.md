
# 注意
- 这是一个 Python SDK 封装的 Agora RTC SDK。
- 支持Linux和Mac平台。
- examples只是作为非常简单的演示，不建议在生产环境中使用。

# 非常重要的通知 !!!
- 一个进程只能有一个实例
- 一个实例，可以有多个connection
- 所有的observer或者是回调中，都不能在调用sdk自身的api，也不能在回调中做cpu耗时的工作，数据拷贝是可以的。

# 所需的操作系统和 Python 版本
- 支持的 Linux 版本：
  - Ubuntu 18.04 LTS 及以上
  - CentOS 7.0 及以上
  
- 支持的 Mac 版本：
  - MacOS 13 及以上

- Python 版本：
  - Python 3.10及以上


# 使用Agora-Python-Server-SDK
```
pip install agora_python_server_sdk
```

# 运行examples

## 准备测试数据
- 下载并解压 [test_data.zip](https://download.agora.io/demo/test/test_data_202408221437.zip) 到Agora-Python-Server-SDK目录

## 执行测试脚本
```
python agora_rtc/examples/example_audio_pcm_send.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm --sampleRate=16000 --numOfChannels=1
```

# 更新日志
## 2024.12.03 发布 2.1.5
- 修改: LocalUser/audioTrack：
  - 当场景为chorus的时候，开发者不需要调用setsenddelayinms；
  - 当场景为chorus的时候，开发者不需要调用track的setaudioscnario 为chorus
  - NOTE： 可以降低开发者难度。在ai场景下，开发者只需要设置service为chorus就可以。
- 增加：VadDump 类，在测试环境下可以协助排查vad的问题。但在线上环境中，不要开启
- 移除: Vad V1版本，只保留v2 版本。参考voice_detection.py,sample_audio_vad.py
- 增加： on_volume_indication 回调
- 增加： on_remote_video_track_state_changed 回调
- 更新：更新有关的samples：audioconsume, vad sample

## 2024.11.15 发布 2.1.4
- 修改videoFrame中的metadata的类型从str修改bytes类型，和c++保持一致；从而可以支持字节流；
- 修改了内部对ExteranlVideoFrame的封装，从而支持字节流；对alpha编码的支持，做了逻辑判断，如果fill_alpha_buffer 为0 ，则不处理

## 2024.11.11 发布 2.1.3
- 增加了一个sample：example_jpeg_send.py 可以将jpeg文件或者jpeg 流 推送到频道中
- 性能耗费参考example中的注释，可以简单总结为对1920*1080对jpeg文件，从读取文件到转换为RGBA bytearry，耗费在11ms
## 2024.11.07 发布 2.1.2

- 对AudioVolumeInfoInner 以及 AudioVolumeInfo 结构中的user_id更新为str 类型
- 修复了_on_audio_volume_indication中回调的bug，原来只能回调一个；修改成可以回调speaker_number个 ():
- 修复了IRTCLocalUserObserver::on_audio_volume_indication中回调的参数类型为list类型

## 2024.10.29 发布 2.1.1

- 添加V2版本的音频 VAD 接口及相应的示例。

## 2024.10.24 发布 2.1.0

- 修复了一些 bug

#### 常见用法Q&A
## serveice和进程的关系？
- 一个进程只能有一个service，只能对service做一次初始化；
- 一个service，只能有一个media_node_factory；
- 一个service，可以有多个connection；
- 在进程退出去的时候，再释放：media_node_factory.release() 和 service.release()

## 如果对docker的使用是一个docker一个用户，用户的时候，启动docker，用户退出去的时候，就释放docker，那么应该这么来做？
- 这个时候就在进程启动的时候，创建service/media_node_factory 和 connection；
- 在进程退出的时候，释放service/media_node_factory 和 connedtion，这样就可以保证

## 如果docker的使用是一个docker支持多个用户的时候，docker会长时间运行，应该怎么做？
- 这个情况下，我们推荐用connection pool的概念
- 在进程启动的时候，创建service/media_node_factory 和 connection pool（只是new connection，并不初始化）；
- 当有用户进来的时候，就从connection pool中获取一个connection，然后初始化，执行 con.connect()并且设置好回调，然后加入频道；
- 处理业务
- 当用户退出的时候，con.disconnect()并释放跟随该conn 的audio/video track，observer等，但不调用con.release();然后将该con 放回connection pool中；
- 在进程退出的时候，释放和 connedtion pool（对每一个con.release()
释放 service/media_node_factory 和 connedtion pool（对每一个con.release()），这样就可以保证资源的释放和性能最优




## VAD的使用
# source code: voice_detection.py
# sample code: example_audio_vad.py
- 推荐用VAD V2版本，类为： AudioVadV2； 参考：voice_detection.py；

- VAD 的使用： 
  - 1. 调用 _vad_instance.init(AudioVadConfigV2) 初始化vad实例.参考：voice_detection.py。 实例假如为： _vad_instance
  - 2. 在audio_frame_observer::on_playback_audio_frame_before_mixing(audio_frame) 中:
    - 1. 调用 vad模块的process:  state, bytes = _vad_instance.process(audio_frame)
    - 2. 根据返回的state，判断state的值，并做相应的处理
       - A. 如果state为 _vad_instance._vad_state_startspeaking，则表明当前“开始说话”，可以开始进行语音识别（STT/ASR）等操作。记住：一定要将返回的bytes 交给识别模块，而不是原始的audio_frame，否则会导致识别结果不正确。
       - B. 如果state为 _vad_instance._vad_state_stopspeaking，则表明当前“停止说话”，可以停止语音识别（STT/ASR）等操作。记住：一定要将返回的bytes 交给识别模块，而不是原始的audio_frame，否则会导致识别结果不正确。
       - C. 如果state为 _vad_instance._vad_state_speaking，则表明当前“说话中”，可以继续进行语音识别（STT/ASR）等操作。记住：一定要将返回的bytes 交给识别模块，而不是原始的audio_frame，否则会导致识别结果不正确。
  备注：如果使用了vad模块，并且希望用vad模块进行语音识别（STT/ASR）等操作，那么一定要将返回的bytes 交给识别模块，而不是原始的audio_frame，否则会导致识别结果不正确。
- 如何更好的排查VAD的问题：包含2个方面，配置和调试。
  - 1. 确保vad模块的初始化参数正确，参考：voice_detection.py。
  - 2. 在state,bytes = on_playback_audio_frame_before_mixing(audio_frame) 中，
    - 1. 将audio_frame的data 的data 保存到本地文件，参考：example_audio_pcm_send.py。这个就是录制原始的音频数据。比如可以命名为：source_{time.time()*1000}.pcm
    - 2. 保存每一次vad 处理的结果：
      - A state==start_speaking的时候：新建一个二进制文件，比如命名为：vad_{time.time()*1000}.pcm，并将bytes 写入到文件中。
      - B state==speaking的时候：将bytes 写入到文件中。
      - C state==stop_speaking的时候：将bytes 写入到文件中。并关闭文件。
  备注：这样就可以根据原始音频文件和vad处理后的音频文件，进行排查问题。生产环境的时候，可以关闭这个功能

## 如何将TTS生成的音频推入到频道中？
# source code: audio_consumer.py
# sample code: example_audio_consumer.py

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

## netx one
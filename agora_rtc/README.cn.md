
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
  
- 支持的 Mac 版本:（仅支持开发测试）
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
## 2025.04.28 发布 2.2.4
-- 更新：更新rtc sdk 到版本4.4.32
## 2025.04.14 发布 2.2.3
-- Fix: 
  -- 修复了enable_encryption 在salt 处理中的一个bug
  -- 更新在enable_encryption 中的逻辑，当enable为0的时候，不做处理
## 2025.04.10 发布 2.2.2
-- Add:
  - push_video_encoded_file.py: 支持推送mp4文件；支持推送h264编码的h.264文件；其中里面有从mp4文件的avformat转换为raw 264流的annex B格式的转换。
-- Add：增加set_log_file_filter函数，可以设置日志的过滤级别
-- 增加arm64版本的支持，但目前该版本不支持audio label 算法！所以在arm64 下不支持！
-- 修改loalauidostats, local video stats, local audio stats, remote video stats, remote audio stats, 
-- 增加：connnection::agora_rtc_conn_enable_encryption 
-- 增加：connectionObserver::on_encryption_error (but not working for now, need to fix in the next monthly version 4.4.32)
## 2025.02.26 发布 2.2.1
-- sdk 更新：
  -- sdk更新到20250102版本，优化main线程参考群：？？？
-- AudioConsumer修改：==>支持业务上能感知对TTS数据的播放状态，包括：开始播放、结束播放；从而可以推送播放状态信息给app端，完成业务诉求 
  -- AudioConsumer的buffer大小修改为100ms，原来是180ms；ok
  -- AudioConsumer::_samples_per_channel 在立体声下计算错误的bu g
  -- AudioConsumer 新增加一个函数：is_push_to_rtc_completed 表示是否已经推送完成？》
  -- 验证方式：app层启动一个timer，定时的去consume，当数据为空的时候，就通过datastream发送结束的消息给app端，app端收到消息后，渲染出来；通过对app 录制视频来判断文字和语音的同步性；？？？需要测试android·端和iOS端和web 端
-- 增加：支持私有化的接口 ？？
## 2025.01.07 发布 2.2.0
-- 更新：
  -- 更新sdk 版本，从4.4.30更新到4.4.31 ok
-- 增加：serviceconfigure
  -- 增加domain_limit ok
  -- 增加should_callback_when_muted: ok
  -- ExternalVideoFrame::增加colorspacetype，支持虚拟人场景下的纯色背景的编码：ok
-- 增加：
  -- AudioMetaData接口:localuser::send_audio_meta_data ok
  -- OnAudioMetaDataReceived 回调接localuserObserver::on_audio_meta_data_received, ok
-- sample 修改
## 2024.12.17 发布 2.1.7  
--修改：
  修改了LocalUser::sub/unsub audio/video中typeError的问题
  将vad默认的stopRecogCount从30调整到50
  修改sample_vad
## 2024.12.09 发布 2.1.6
-- 增加：
  -增加了AduioVadManger，用来管理vad instance
  -将vad 功能内置在sdk内部，开发者不在需要关注如何使用vad，只需要关注设置合适的参数就可以。参考： sample_audio_vad.py
- 修改：
  -- register_audio_frame_observer中，增加了2个参数，用于设置vad的参数，参考： sample_audio_vad.py
  -- 在on_playback_audio_frame_before_mixing中，返回值增加了2个参数： vad_result_state 和 vad_result_bytearray。 state： < 0 没有设置内部自动出来vad；0: nospeaking, 1: startspeakong; 2 speaking; 3 stopspeaking. vad_result_bytearray 在vad状态下返回的vad处理后的结果。
  -- 如果启动了自动处理vad：
    . 开发者需要用vad_result_bytearray来做后续的业务处理，比如发送给ASR/STT， 而不是用frame 来做处理
  参考： sample_audio_vad.py
- 优化：
  -- 在推送pcm中，不在使用pacer，而是使用Audioconsumer 进行推送。
- 更新：
  --修改了和Pacer、vad有关的sample
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

## 在AI场景下，如何做打断？
- 打断的定义
  在人机对话中，打断是指用户在对话过程中突然打断机器人的回答，要求机器人立即停止当前回答并转而回答用户的新问题。这个行为就叫打断
- 打断触发的条件
  打断根据不同的产品定义，一般有两种方式：
  - 模式1：语音激励模式. 当检测到有用户说话，就执行打断策略，比如用户说话时，识别到用户说话，就执行打断策略。
  - 模式2：ASR激励模式. 当检测到有用户说话、并且asr/STT的识别返回有结果的时候，就执行打断策略。
- 不同打断策略的优点
  - 1. 语音激励打断：
    - 优点：
    - 1. 减少用户等待时间，减少用户打断的概率。因为用户说话时，机器人会立即停止回答，用户不需要等待机器人回答完成。
    - 缺点：
    - 1. 因为是语音激励模式，有可能会被无意义的语音信号给打断，依赖于VAD判断的准确性。比如AI在回答的时候，如果有人敲击键盘，就可能触发语音激励，将AI打断。
  -2 . ASR激励打断：
    - 优点：
    - 1. 降低用户打断的概率。因为用户说话时，asr/STT识别到用户说话，才会触发打断策略。
    - 缺点：
    - 1. 因为是asr/STT激励模式，需要将语音信号转换成文本，会增加打断的延迟。

- 推荐模式
  如果VAD能过滤掉非人声，只是在有人声的时候，才触发VAD判断，建议用语音激励模式；或者是对打断要求延迟敏感的时候，用改模式
  如果对打断延迟不敏感，建议用ASR激励模式，因为ASR激励模式，可以过滤掉非人声，降低用户打断的概率。
- 如何实现打断？打断需要做哪些操作？
  定义：人机对话，通常可以理解为对话轮的方式来进行。比如用户问一个问题，机器人回答一个问题；然后用户再问一个问题，机器人再回答一个问题。这样的模式就是对话轮。我们假设给对话轮一个roundId,每轮对话，roundId+1。 一个对话轮包含了这样的3个阶段/组成部分：vad、asr、LLM、TTS、rtc推流。
  1. vad： 是指人机对话的开始，通过vad识别出用户说话的开始和结束，然后根据用户说话的开始和结束，交给后续的ASR。
  2. asr： 是指人机对话的识别阶段，通过asr识别出用户说的话，然后交给LLM。
  3. LLM： 是指人机对话的生成阶段，LLM根据用户说的话，生成一个回答。
  4. TTS： 是指人机对话的合成阶段，LLM根据生成的回答，合成一个音频。
  5. rtc推流： 是指人机对话的推流阶段，将合成后的音频推流到rtc，然后机器人播放音频。

  因此，所谓的打断，就是在（roundid+1）轮的时候，无论是用语音激励（VAD阶段触发）还是用ASR激励（就是在ASR识别出用户说的话）打断，都需要做如下的操作：
  1. 停止当前轮roundID轮的LLM生成。
  2. 停止当前轮roundID轮的TTS合成。
  3. 停止当前轮roundID轮的RTC推流。
   API调用参考：
    a 调用:AudioConsumer.clear()；
    b 调用:LocalAudioTrack.clear_sender_buffer()；
    c 业务层：清除TTS返回来保留的数据（如果有）
## LLM的结果什么时候交给TTS做合成？
  LLM的结果是异步返回的，而且都是流式返回的。应该按照什么时机将LLM的结果交给TTS做合成呢？
  需要考虑2个因素：
  1. 确保TTS合成的语音是没有歧义：确保TTS合成的语音是没有歧义、而且是完整、连续的。比如LLM返回的文本是："中间的首都是北京吗？"如果我们给TTS的是：中  然后是：国首  然后是：是北   然后是：京吗？  这样合成会有歧义，因为"中"和"国"之间没有空格，"首"和"是"之间没有空格，"京"和"吗"之间没有空格。
  2. 确保整个流程延迟最低。LLM 生成完成后，在交给TTS，这样的处理方式，合成的语音一定是没有歧义，而且是连续的。但延迟会很大，对用户体验不友好。
  推荐的方案：
    将有LLM返回数据的时候：
    a LLM返回的结果存放在缓存中
    b 对缓存中的数据做逆序扫描，找到最近的一个标点符号
    c 将缓存中的数据，从头开始到最尾的一个标点符号截断，然后交给TTS做合成。
    d 将截断后的数据，从缓存中删除。剩余的数据，移动到缓存头位置，继续等待LLM返回数据。

## VAD配置参数的含义
AgoraAudioVadConfigV2 属性
属性名	                 类型	    描述	                         默认值	     取值范围
preStartRecognizeCount	int	    开始说话状态前保存的音频帧数	      16	       [0, ]  
startRecognizeCount	    int   	判断是否开始说话状态的音频帧总数     30	    [1, max]
stopRecognizeCount	    int	    判断停止说话状态的音频帧数	        50	    [1, max]
activePercent	          float	  在 startRecognizeCount 
                                  帧中活跃帧的百分比	            0.7	    0.0, 1.0]
inactivePercent       	float	  在 stopRecognizeCount
                                 帧中非活跃帧的百分比	             0.5     [0.0, 1.0]
startVoiceProb	        int	    音频帧是人声的概率	              70	    [0, 100]
stopVoiceProb	          int	     音频帧是人声的概率	               70	    [0, 100]
startRmsThreshold	      int	     音频帧的能量分贝阈值	            -50	     [-100, 0]
stopRmsThreshold	      int	    音频帧的能量分贝阈值            	-50	    [-100, 0]
注意事项

startRmsThreshold 和 stopRmsThreshold:
值越高，就需要说话人的声音相比周围环境的环境音的音量越大
在安静环境中推荐使用默认值 -50。
在嘈杂环境中可以调高到 -40 到 -30 之间，以减少误检。
根据实际使用场景和音频特征进行微调可获得最佳效果。

stopReecognizeCount: 反映在识别到非人声的情况下，需要等待多长时间才认为用户已经停止说话。可以用来控制说话人相邻语句的间隔，在该间隔内，VAD会将相邻的语句当作一段话。如果时间短，相邻语句就越容易被识别为2段话。通常推荐50～80
比如：下午好，[interval_between_sentences]北京有哪些好玩的地方？
如果说话人语气之间的间隔interval_between_sentences 大于stopReecognizeCount，那么VAD就会将上述识别为2个vad：
vad1: 下午好
vad2: 北京有哪些好玩的地方？
如果interval_between_sentences 小于 stopReecognizeCount，那么VAD就会将上述识别为1个vad：
vad： 下午好，北京有哪些好玩的地方？
如果对延迟敏感，可以调低该值，或者咨询研发，在降低该值的情况下，应该如何在应用层做处理，在保障延迟的情况下，还能确保语意的连续性，不会产生AI被敏感的打断的感觉。

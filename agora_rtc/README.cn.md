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
  - Python 3.8 及以上


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


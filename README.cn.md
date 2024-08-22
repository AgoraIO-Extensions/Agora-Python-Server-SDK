# 注意
- 这是一个 Python SDK 封装的 Agora RTC SDK。
- 支持Linux和Mac平台。
- examples只是作为非常简单的演示，不建议在生产环境中使用。

# 非常重要的通知 !!!!!!!
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

# 测试数据
- 下载并解压 [test_data.zip](https://download.agora.io/demo/test/test_data_202408221437.zip)
- 在与 **python_sdk** 同一目录下创建 **test_data** 目录

# Linux 调试与开发
## 准备 C 版本的 Agora RTC SDK
- 在与 **python_sdk** 同一目录下创建 **agora_sdk** 目录
- 下载并解压 [agora_sdk.zip](https://download.agora.io/sdk/release/agora_rtc_sdk_linux_20240814_320567.zip) 到**agora_sdk** 目录。
- **agora_sdk** 目录中应有 **libagora_rtc_sdk.so** 和 **include_c**

## 在 Linux 上运行示例
```
export LD_LIBRARY_PATH=/path/to/agora_sdk
cd python_sdk
python examples/example_send_pcm.py {appid} {token} {channel_id} ../test_data/demo.pcm {userid}
```


# Mac 调试与开发
## 准备 C 版本的 Agora RTC SDK
- 在与 **python_sdk** 同一目录下创建 **agora_sdk** 目录
- 下载并解压 [agora_sdk.zip](https://download.agora.io/sdk/release/agora_rtc_sdk_mac_20240814_320567.zip)，到**agora_sdk** 目录。
- **agora_sdk** 目录中应有 **libAgoraRtcKit.dylib** 和 **include_c**

## 在 Mac 上运行示例
- 将 **libagora_rtc_sdk.dylib** 添加到 **/usr/local/lib**。
- 或者 `export DYLD_LIBRARY_PATH=/path/to/agora_sdk`

```
cd python_sdk
python examples/example_send_pcm.py {appid} {token} {channel_id} ../test_data/demo.pcm {userid}
```


# Notice
- this is a python sdk wrappered agora rtc sdk, it is  only for linux purpose
- can dev under mac, and release unde linux
- the sample is a very simple demo, it is not a good practice to use it in production
# Very import notice !!!!!!!
- It's crucial that a process can only have one instance.
- One instance can have multiple connections.
- In all observers or callbacks, it is not allowed to call the SDK's own APIs, nor is it permitted to perform   CPU-intensive tasks within the callbacks. However, data copying is allowed.
- 中文说明
- 一个进程只能有一个实例
- 一个实例，可以有多个connection
- 所有的observer或者是回调中，都不能在调用sdk自身的api，也不能在回调中做cpu耗时的工作，数据拷贝是可以的

# Required OS and python version
- supported linux version: 
  - Ubuntu 18.04 LTS and above
  - CentOS 7.0 and above
  - Mac for debug & developing
- python version:
  - python 3.7 above

# Test Data
- download and unzip [test_data.zip](https://share.weiyun.com/4x3Um6b8)
- make **test_data** directory in the same directory with **python_wrapper**

# Linux debug & develop
## Prepare C version of agora rtc sdk
- download and unzip [agora_sdk.zip](https://share.weiyun.com/1tuBWw6O)
- make **agora_sdk** directory in the same directory with **python_wrapper**
- there should be **libagora_rtc_sdk.so** and **include_c** in **agora_sdk** directory

## run example on linux
```
export LD_LIBRARY_PATH=/path/to/agora_sdk
python python_wrapper/example.py
```

# Mac debug & develop
## Prepare C version of agora rtc sdk
- download and unzip [agora_sdk_mac.zip](https://share.weiyun.com/jgvFzRI0) for mac version: please contact R&D
- rename dir agora_sdk_mac to agora_sdk
- make **agora_sdk** directory in the same directory with **python_wrapper** 

## run example on mac

- add **libAgoraRtcKit.dylib** to **/usr/local/lib**
- or  `export DYLD_LIBRARY_PATH=/path/to/agora_sdk`

```
python python_wrapper/example.py {appid} {token} {channelname} {userid} {pcm sampe file path}
```

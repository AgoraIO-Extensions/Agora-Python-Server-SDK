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
- download and unzip [test_data.zip](https://share.weiyun.com/4x3Um6b8)
- make **test_data** directory in the same directory with **agora_service**

# Linux debug & develop
## Prepare C version of agora rtc sdk

- make **agora_sdk** directory in the same directory with **agora_service**
- download and unzip [agora_sdk.zip](https://download.agora.io/sdk/release/agora_rtc_sdk_linux_20240814_320567.zip) to **agora_sdk**
- there should be **libagora_rtc_sdk.so** and **include_c** in **agora_sdk** directory

## run example on linux
```
export LD_LIBRARY_PATH=/path/to/agora_sdk
python examples/example_send_pcm.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
```

# Mac debug & develop
## Prepare C version of agora rtc sdk
- make **agora_sdk** directory in the same directory with **agora_service**
- download and unzip [agora_sdk.zip](https://download.agora.io/sdk/release/agora_rtc_sdk_mac_20240814_320567.zip) to **agora_sdk**
- there should be **libagora_rtc_sdk.so** and **include_c** in **agora_sdk** directory

## run example on mac

- add **libagora_rtc_sdk.dylib** to **/usr/local/lib**
- or  `export DYLD_LIBRARY_PATH=/path/to/agora_sdk`

```
python examples/example_send_pcm.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
```

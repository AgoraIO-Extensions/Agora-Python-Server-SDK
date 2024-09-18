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
- download and unzip [test_data.zip](https://download.agora.io/demo/test/test_data_202409021506.zip)

# Use Agora-Python-Server-SDK
## Install 1.1.x version of Agora-Python-Server-SDK

```
pip install 'agora_python_server_sdk>=1.1,<1.2'
```

## run examples

```
python examples/example_send_pcm.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
```


import time
import datetime
import sys
import os
import signal





# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agora.rtm.rtm_client import RTMClient, create_rtm_client
from agora.rtm.rtm_base import RtmConfig, RtmLogConfig, RtmLogLevel, SubscribeOptions
from agora.rtm.rtm_event_handler import IRtmEventHandler, MessageEvent, LinkStateEvent

#my event handler
class MyEventHandler(IRtmEventHandler):
    def __init__(self):
        self.rtm_client = None
        super(MyEventHandler, self).__init__()
    def on_login_result(self, request_id: int, error_code: int):
        print(f"on_login_result: {request_id}, {error_code}")
    def on_logout_result(self, request_id: int, error_code: int):
        print(f"on_logout_result: {request_id}, {error_code}")
    def on_link_state_event(self, event: LinkStateEvent):
        print(f"on_link_state_event: {event}")
    def on_renew_token_result(self, request_id: int, server_type: int, channel_name: str, error_code: int):
        print(f"on_renew_token_result: {request_id}, {server_type}, {channel_name}, {error_code}")
    def on_subscribe_result(self, request_id: int, channel_name: str, error_code: int):
        print(f"on_subscribe_result: {request_id}, {channel_name}, {error_code}")
    def on_unsubscribe_result(self, request_id: int, channel_name: str, error_code: int):
        print(f"on_unsubscribe_result: {request_id}, {channel_name}, {error_code}")
    def on_publish_result(self, request_id: int, error_code: int):
        print(f"on_publish_result: {request_id}, {error_code}")
    def on_message_event(self, event: MessageEvent):
        print(f"on_message_event: {event.channel_name}, {event.message}, {event.message_type}, {event.message_length}, {event.publisher}, {event.custom_type}")
        self.rtm_client.send_channel_message(event.channel_name, event.message)
        self.rtm_client.send_user_message(event.publisher, event.message)
    def set_rtm_client(self, rtm_client: RTMClient):
        self.rtm_client = rtm_client
    

# sig handleer
def signal_handler(signal, frame):
    global g_runing
    g_runing = False
    print("prsss ctrl+c: ", g_runing)


g_runing = True
def main():
    signal.signal(signal.SIGINT, signal_handler)

    #parse cmd line
    arg_len = len (sys.argv)
    if arg_len < 4:
        print(f"usage: {__file__} <app_id> <channel_id> <user_id> <token_option>")
        return
    app_id = sys.argv[1]
    channel_id = sys.argv[2]
    user_id = sys.argv[3]
    if arg_len >= 5:
        token_option = sys.argv[4]
    else:
        token_option = app_id #use default token
   
    print(f"app_id: {app_id}, channel_id: {channel_id}, user_id: {user_id}, token_option: {token_option}")
    
    # 创建RTM客户端
    config = RtmConfig(
        app_id=app_id,
        user_id=user_id,
    )
    log_config = RtmLogConfig(
        file_path="./logs/rtm.log",
        file_size_kb=1024,
        log_level=RtmLogLevel.RTM_LOG_LEVEL_INFO
    )
    config.log_config = log_config

    rtm_client : RTMClient = None
    event_handler = MyEventHandler()
    config.event_handler = event_handler

    
   
    rtm_client = create_rtm_client(config)
    print(f"RTM客户端创建成功: {rtm_client}")

    event_handler.set_rtm_client(rtm_client)
    
    request_id = rtm_client.login(token_option)
    print(f"登录结果: {request_id}")
    time.sleep(1)

    #subscribe channel
    sub_opt = SubscribeOptions(
        with_message=True,
        with_metadata=False,
        with_presence=False,
        with_lock=False,
        be_quiet=False,
    )
    rtm_client.subscribe(channel_id, sub_opt)
    
    # 释放客户端资源
    #while True:
    time.sleep(5)
    #rtm_client.unsubscribe(channel_id)
    #time.sleep(5)

    
    while g_runing:
        time.sleep(0.05)

    rtm_client.logout()
    print(f"登出结果: {request_id}")
    time.sleep(5)

    rtm_client.release()
    print("RTM示例程序运行完成")

if __name__ == "__main__":
    main()
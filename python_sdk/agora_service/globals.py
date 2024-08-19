import time
import functools
import threading 


def agorasingleton(cls):
    """Singleton decorator."""
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@agorasingleton
class AgoraHandleInstanceMap:
    """Global class using singleton pattern."""

    def __init__(self):
        #for conmap
        self.con_map = {}
        self.con_lock = threading.RLock()

        #for local user
        self.local_user_map = {}
        self.local_user_lock = threading.RLock()
        
    # 使用示例：内部使用with方法来自动获取和释放锁
    def set_con_map(self, con_handle, con_instance):
        with self.con_lock:
            self.con_map[con_handle] = con_instance
    def get_con_map(self, con_handle):
        with self.con_lock:
            return self.con_map.get(con_handle, None)
    def del_con_map(self, con_handle):
        with self.con_lock:
            del self.con_map[con_handle]
        
    def set_local_user_map(self, local_user_handle, local_user_instance):
        with self.local_user_lock:
            self.local_user_map[local_user_handle] = local_user_instance

    def get_local_user_map(self, local_user_handle):
        with self.local_user_lock:
            return self.local_user_map.get(local_user_handle, None)
    def del_local_user_map(self, local_user_handle):
        with self.local_user_lock:
            del self.local_user_map[local_user_handle]
        


# 使用示例
if __name__ == "__main__":
    instance1 = AgoraHandleInstanceMap()
    instance2 = AgoraHandleInstanceMap()

    print(instance1 is instance2)  # 应该输出 True

    instance1.set_data('key', 'value')
    print(instance2.get_data('key'))  # 应该输出 'value'
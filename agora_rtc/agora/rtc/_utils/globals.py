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
        
    # with method to acquire & release lock
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
        


# test code
if __name__ == "__main__":
    instance1 = AgoraHandleInstanceMap()
    instance2 = AgoraHandleInstanceMap()

    print(instance1 is instance2)  # should output True

    instance1.set_con_map('key', 'value')
    print(instance2.get_con_map('key'))  # should output  'value'

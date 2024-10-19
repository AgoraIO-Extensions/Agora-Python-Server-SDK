from . import lib_path
import ctypes
import os
import sys
from enum import Enum, IntEnum
import logging
logger = logging.getLogger(__name__)


if sys.platform == 'darwin':
    agora_vad_lib_path = os.path.join(lib_path, 'libuap_aed.dylib')
elif sys.platform == 'linux':
    agora_vad_lib_path = os.path.join(lib_path, 'libagora_uap_aed.so')
try:
    agora_vad_lib = ctypes.CDLL(agora_vad_lib_path)
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {agora_vad_lib_path}")
    sys.exit(1)


class VAD_STATE(ctypes.c_int):
    VAD_STATE_NONE_SPEAKING = 0
    VAD_STATE_START_SPEAKING = 1
    VAD_STATE_SPEAKING = 2
    VAD_STATE_STOP_SPEAKING = 3


# struct def
    # def __init__(self) -> None:
    # self.data = None


agora_uap_vad_create = agora_vad_lib.Agora_UAP_VAD_Create
agora_uap_vad_create.restype = ctypes.c_int
agora_uap_vad_create.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(VadConfig)]

agora_uap_vad_destroy = agora_vad_lib.Agora_UAP_VAD_Destroy
agora_uap_vad_destroy.restype = ctypes.c_int
agora_uap_vad_destroy.argtypes = [ctypes.POINTER(ctypes.c_void_p)]

agora_uap_vad_proc = agora_vad_lib.Agora_UAP_VAD_Proc
agora_uap_vad_proc.restype = ctypes.c_int
agora_uap_vad_proc.argtypes = [ctypes.c_void_p, ctypes.POINTER(
    VadAudioData), ctypes.POINTER(VadAudioData), ctypes.POINTER(VAD_STATE)]


class AudioVad:
    def __init__(self) -> None:
        self.vadCfg = VadConfig()

        self.handler = None
        self.lastOutTs = 0
        self.initialized = False
    # return 0 if success， -1 if failed

    def Create(self, vadCfg):
        if self.initialized:
            return 0
        self.vadCfg = vadCfg
        self.initialized = True
        # creat handler
        self.handler = ctypes.c_void_p()
        ret = agora_uap_vad_create(ctypes.byref(
            self.handler), ctypes.byref(self.vadCfg))
        return ret

    # Destroy
    # return 0 if success， -1 if failed
    def Destroy(self):
        if self.initialized:
            agora_uap_vad_destroy(ctypes.byref(self.handler))
        self.initialized = False
        self.handler = None
        return 0

    # Proc
    # framein: bytearray object, include audio data
    # return ret, frameout, flag, ret: 0 if success， -1 if failed; frameout: bytearray object, include audio data; flag: 0 if non-speaking, 1 if speaking
    def Proc(self, framein):
        ret = -1
        if not self.initialized:
            return -1

        # supporse vadout is empty,vadin byte array
        inVadData = VadAudioData()
        # only a pointer to the buffer is needed, not a copy
        buffer = (ctypes.c_ubyte * len(framein)).from_buffer(framein)
        inVadData.audioData = ctypes.cast(buffer, ctypes.c_void_p)
        inVadData.size = len(framein)

        outVadData = VadAudioData(None, 0)  # c api will allocate memory
        vadflag = VAD_STATE(0)
        ret = agora_uap_vad_proc(self.handler, ctypes.byref(
            inVadData), ctypes.byref(outVadData), ctypes.byref(vadflag))

        # convert from c_char to bytearray
        bytes_from_c = ctypes.string_at(outVadData.audioData, outVadData.size)
        frameout = bytearray(bytes_from_c)
        flag = vadflag.value

        return ret, frameout, flag

import time
import ctypes

import os
import sys
from enum import Enum,IntEnum

from . import lib_path

if sys.platform == 'darwin':
    agora_vad_lib_path =os.path.join(lib_path, 'libuap_aed.dylib')
elif sys.platform == 'linux':
    agora_vad_lib_path =os.path.join(lib_path, 'libagora_uap_aed.so')    
try:
    agora_vad_lib = ctypes.CDLL(agora_vad_lib_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    print(f"Attempted to load from: {agora_vad_lib_path}")
    sys.exit(1)


class VAD_STATE(ctypes.c_int):
    VAD_STATE_NONE_SPEAKING = 0
    VAD_STATE_START_SPEAKING = 1
    VAD_STATE_SPEAKING = 2
    VAD_STATE_STOP_SPEAKING = 3

# struct def    
"""
typedef struct Vad_Config_ {
  int fftSz;  // fft-size, only support: 128, 256, 512, 1024, default value is 1024
  int hopSz;  // fft-Hop Size, will be used to check, default value is 160
  int anaWindowSz;  // fft-window Size, will be used to calc rms, default value is 768
  int frqInputAvailableFlag;  // whether Aed_InputData will contain external freq. power-sepctra, default value is 0
  int useCVersionAIModule; // whether to use the C version of AI submodules, default value is 0
  float voiceProbThr;  // voice probability threshold 0.0f ~ 1.0f, default value is 0.8
  float rmsThr; // rms threshold in dB, default value is -40.0
  float jointThr; // joint threshold in dB, default value is 0.0
  float aggressive; // aggressive factor, greater value means more aggressive, default value is 5.0
  int startRecognizeCount; // start recognize count, buffer size for 10ms 16KHz 16bit 1channel PCM, default value is 10
  int stopRecognizeCount; // max recognize count, buffer size for 10ms 16KHz 16bit 1channel PCM, default value is 6
  int preStartRecognizeCount; // pre start recognize count, buffer size for 10ms 16KHz 16bit 1channel PCM, default value is 10
  float activePercent; // active percent, if over this percent, will be recognized as speaking, default value is 0.6
  float inactivePercent; // inactive percent, if below this percent, will be recognized as non-speaking, default value is 0.2
} Vad_Config;
"""
class VadConfig(ctypes.Structure):
	_fields_ = [
		("fftSz", ctypes.c_int),
		("hopSz", ctypes.c_int),
		("anaWindowSz", ctypes.c_int),
		("frqInputAvailableFlag", ctypes.c_int),
		("useCVersionAIModule", ctypes.c_int),
		("voiceProbThr", ctypes.c_float),
		("rmsThr", ctypes.c_float),
		("jointThr", ctypes.c_float),
		("aggressive", ctypes.c_float),
		("startRecognizeCount", ctypes.c_int),
		("stopRecognizeCount", ctypes.c_int),
		("preStartRecognizeCount", ctypes.c_int),
		("activePercent", ctypes.c_float),
		("inactivePercent", ctypes.c_float)
	]
	def __init__(self)->None:
		self.fftSz = 1024
		self.hopSz = 160
		self.anaWindowSz = 768
		self.frqInputAvailableFlag = 0
		self.useCVersionAIModule = 0
		self.voiceProbThr = 0.8
		self.rmsThr = -40.0
		self.jointThr = 0.0
		self.aggressive = 5.0
		self.startRecognizeCount = 10
		self.stopRecognizeCount = 6
		self.preStartRecognizeCount = 10
		self.activePercent = 0.6
		self.inactivePercent = 0.2
		
       
	
# struct def
class VadAudioData(ctypes.Structure):
	_fields_ = [
		("audioData", ctypes.c_void_p),
		("size", ctypes.c_int)
	]   
	#def __init__(self) -> None:
		#self.data = None


"""
int Agora_UAP_VAD_Create(void** stPtr, const Vad_Config* config);
int Agora_UAP_VAD_Destroy(void** stPtr);
int Agora_UAP_VAD_Proc(void* stPtr, const Vad_AudioData* pIn, Vad_AudioData* pOut, VAD_STATE* state);
"""
agora_uap_vad_create = agora_vad_lib.Agora_UAP_VAD_Create
agora_uap_vad_create.restype = ctypes.c_int
agora_uap_vad_create.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(VadConfig)]

agora_uap_vad_destroy = agora_vad_lib.Agora_UAP_VAD_Destroy
agora_uap_vad_destroy.restype = ctypes.c_int
agora_uap_vad_destroy.argtypes = [ctypes.POINTER(ctypes.c_void_p)]

agora_uap_vad_proc = agora_vad_lib.Agora_UAP_VAD_Proc
agora_uap_vad_proc.restype = ctypes.c_int
agora_uap_vad_proc.argtypes = [ctypes.c_void_p, ctypes.POINTER(VadAudioData), ctypes.POINTER(VadAudioData), ctypes.POINTER(VAD_STATE)]

class AudioVad:
	def __init__(self) ->None:
		self.vadCfg = VadConfig()
		
		self.handler = None
		self.lastOutTs = 0
		self.initialized = False
	# Create
	# return 0 if success， -1 if failed
	def Create(self, vadCfg):
		if self.initialized:
			return 0
		self.vadCfg = vadCfg
		self.initialized = True
		# creat handler
		self.handler = ctypes.c_void_p()
		ret = agora_uap_vad_create(ctypes.byref(self.handler), ctypes.byref(self.vadCfg))
		return ret
	
    #Destroy
	#return 0 if success， -1 if failed
	def Destroy(self):
		if self.initialized:
			agora_uap_vad_destroy(ctypes.byref(self.handler))
		self.initialized = False
		self.handler = None
		return 0
	
	#Proc
	#framein: bytearray object, include audio data
	#return ret, frameout, flag, ret: 0 if success， -1 if failed; frameout: bytearray object, include audio data; flag: 0 if non-speaking, 1 if speaking
	def Proc(self, framein):
		ret = -1
		if not self.initialized:
			return -1
		
		#supporse vadout is empty,vadin byte array
		inVadData = VadAudioData()
		buffer = (ctypes.c_ubyte * len(framein)).from_buffer(framein) #only a pointer to the buffer is needed, not a copy 
		inVadData.audioData = ctypes.cast(buffer, ctypes.c_void_p) 
		inVadData.size = len(framein)
		 
		outVadData = VadAudioData(None, 0)  # 输出数据可能需要预分配，但通常C函数会处理它  
		vadflag = VAD_STATE(0)
		ret = agora_uap_vad_proc(self.handler, ctypes.byref(inVadData), ctypes.byref(outVadData), ctypes.byref(vadflag))

		#convert from c_char to bytearray
		bytes_from_c = ctypes.string_at(outVadData.audioData, outVadData.size)  
		frameout = bytearray(bytes_from_c)  
		flag = vadflag.value


		return ret, frameout, flag

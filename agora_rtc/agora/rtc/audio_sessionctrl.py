import time
import ctypes

import os
import sys
from enum import Enum,IntEnum
import logging
logger = logging.getLogger(__name__)

from . import lib_path

#dll def

if sys.platform == 'darwin':
    agora_sessionctrl_lib_path =os.path.join(lib_path, 'libagora_session_control.dylib')
elif sys.platform == 'linux':
    agora_sessionctrl_lib_path =os.path.join(lib_path, 'libagora_session_control.so')    
try:
    sessctrl_lib = ctypes.CDLL(agora_sessionctrl_lib_path)
except OSError as e:
    logger.error(f"Error loading the library: {e}")
    logger.error(f"Attempted to load from: {agora_sessionctrl_lib_path}")
    sys.exit(1)


#const & enu define
from enum import Enum

# Define constants
AGORA_UAP_SESSCTRL_VERSION = 20240626
AGORA_UAP_SESSCTRL_MAX_USERID_LEN = 128
AGORA_UAP_SESSCTRL_MAX_FRMSZ = 1000
AGORA_UAP_SESSCTRL_DEBUG_DUMP = 0
AGORA_UAP_SESSCTRL_COUNTER_ZERO_HISTOGRAM_NUM = 8
AGORA_UAP_SESSCTRL_COUNTER_LAST_WORD_DELAY_HISTOGRAM_NUM = 11
AGORA_UAP_SESSCTRL_COUNTER_FIRST_WORD_DELAY_HISTOGRAM_NUM = 11
AGORA_UAP_SESSCTRL_COUNTER_VAD_LENGTH_HISTOGRAM_NUM = 12
AGORA_UAP_SESSCTRL_COUNTER_SILENCE_LENGTH_HISTOGRAM_NUM = 18
AGORA_UAP_SESSCTRL_COUNTER_INPUT_VOLUME_HISTOGRAM_NUM = 10

# Enum for sample rate
class SessCtrlFs(ctypes.c_int):
    kFs_16000 = 16000
    kFs_32000 = 32000
    kFs_44100 = 44100
    kFs_48000 = 48000
    kFs_24000 = 24000

# Enum for session control status
class SessCtrlStatus(ctypes.c_int):
    kSCStatus_None = 0          # Not in Session
    kSCStatus_SOS = 1           # Start Of Sentence
    kSCStatus_Continue = 2      # Continue sending data during a sentence
    kSCStatus_Wait4Dec = 3      # Waiting status, It will change status to EOS if waiting for M ms
    kSCStatus_EOS = 4           # End Of Sentence
    kSCStatus_EOSRETRY = 5      # Retry of EOS event to enforce "final" from ASR
    kSCStatus_EOSRETRYSTOP = 6  # Stop EOS retry because over max iteration[eosRetryMaxIteration]
    kSCStatus_EOSDISCONNECT = 7 # Disconnect ASR server at EOS
    kSCStatus_Cnt = 8           # Number of status

# Enum for ASR events
class SessCtrlAsrEvent(ctypes.c_int):
    kSCAsrEvent_NONFINAL = 0   # "final"-waiting has been timeout
    kSCAsrEvent_FINAL = 1      # A "final" event has been received from ASR service
    kSCAsrEvent_TIME_OUT = 2   # Time out event
    kSCAsrEvent_Cnt = 3        # Number of events

# Enum for sentence finalization status
class SessCtrlSentenceFinal(ctypes.c_int):
    kSCSentence_NONFINAL = 0   # Non-final
    kSCSentence_FINAL = 1      # Final
    kSCSentence_UNKNOWN = 2    # Unknown


# Define the structures
class SessCtrl_StaticCfg(ctypes.Structure):
    _fields_ = [
        ("userID", ctypes.c_char_p),
        ("frmSz", ctypes.c_int),
        ("smplFrq", ctypes.c_int),
        ("persistentVoiceLenOfSOS", ctypes.c_int),
        ("prePaddingLenOfSessCtrlSOS", ctypes.c_int),
        ("postPaddingLenOfSessCtrlEOS", ctypes.c_int),
        ("unVoiceLenOfTriggerSessCtrlEOS", ctypes.c_int),
        ("unVoiceLenOfTriggerServerEOS", ctypes.c_int),
        ("eosWaitTime", ctypes.c_int),
        ("eosRetryWaitTime", ctypes.c_int),
        ("eosRetryPadding", ctypes.c_int),
        ("eosRetryMaxIteration", ctypes.c_int),
        ("enableMainSpeakerDet", ctypes.c_int)
    ]
    def __init__(self):
        self.userID = ctypes.c_char_p("")
        self.frmSz = 160
        self.smplFrq = 16000
        self.persistentVoiceLenOfSOS = 0
        self.prePaddingLenOfSessCtrlSOS = 0
        self.postPaddingLenOfSessCtrlEOS = 0
        self.unVoiceLenOfTriggerSessCtrlEOS = 0
        pass
    
class MSJudge_Param(ctypes.Structure):
    _fields_ =	[
        ("powScale", ctypes.c_float),
        ("powRatio", ctypes.c_float),
        ("biasDelay", ctypes.c_int),
        ("aggressive", ctypes.c_float),
        ("voiceProbThr", ctypes.c_float),
        ("suppressGain", ctypes.c_float),
        ("mainSpeakerMaintance", ctypes.c_int)
	]
    def __init__(self):
        pass


class SessCtrl_DynamCfg(ctypes.Structure):
    _fields_ = [
        ("logLv", ctypes.c_int),
        ("meterRMSThr", ctypes.c_float),
        ("vadThr", ctypes.c_float),
        ("musicGateFlag", ctypes.c_int),
        ("musicThr", ctypes.c_float),
        ("sessCtrlBSVoiceGateFlag", ctypes.c_int),
        ("sessCtrlBSVoiceAggressive", ctypes.c_float),
        ("voiceThr", ctypes.c_float),
        ("sessCtrlFinalRMSThr", ctypes.c_int),
        ("sessCtrlFinalThr", ctypes.c_int),
        ("sessCtrlFinalThrInc", ctypes.c_int),
        ("sessCtrlFinalThrMax", ctypes.c_int),
        ("vadVolumeThr", ctypes.c_float),
        ("sessCtrlTimeOutInMs", ctypes.c_int),
        ("sessCtrlStartSniffWordGapInMs", ctypes.c_int),
        ("sessCtrlWordGapLenInMs", ctypes.c_int),
        ("sessCtrlWordGapLenVolumeThr", ctypes.c_int),
        ("sessCtrlEOSDisconnectFlag", ctypes.c_int),
        ("sessCtrlAiVadBasedDenoiseFlag", ctypes.c_int),
        ("sessCtrlAiVadBasedDenoiseDelayInMs", ctypes.c_int),
        ("sessCtrlAiVadBasedVoiceDenoiseProbThr", ctypes.c_float),
        ("sessCtrlAiVadBasedMusicDenoiseProbThr", ctypes.c_float),
        ("sessCtrlEnableDumpFlag", ctypes.c_int),
        ("msJude_param", MSJudge_Param)
    ]
    def __init__(self):
        pass
    
class SessCtrl_FrmCtrl(ctypes.Structure):
    _fields_ = [
        ("trash", ctypes.c_int)
    ]
    def __init__(self):
        pass
 

class SessCtrl_InputData(ctypes.Structure):
    _fields_ = [
        ("pcm", ctypes.POINTER(ctypes.c_short)),
        ("frmIdx", ctypes.c_int),
        ("ts", ctypes.c_long)
    ]
    def __init__(self):
        self.pcm = ctypes.c_void_p(0)
        self.frmIdx = 0
        self.ts = 0
        pass

class SessCtrl_OutputData(ctypes.Structure):
    _fields_ = [
        ("userID", ctypes.c_char_p),
        ("sessID", ctypes.c_int),
        ("status", SessCtrlStatus),
        ("pcmBuf", ctypes.POINTER(ctypes.c_short)),
        ("nSamplesInPcmBuf", ctypes.c_int),
        ("eosWaitTimeInMs", ctypes.c_int),
        ("startFrmIdx", ctypes.c_int),
        ("startTs", ctypes.c_long),
        ("lastVoiceTs", ctypes.c_long),
        ("avgVadScore", ctypes.c_float),
        ("avgRMS", ctypes.c_float)
    ]
    def __init__(self):
        self.nSamplesInPcmBuf = 0
        
        pass
    

class SessCtrl_AsrResponse(ctypes.Structure):
    _fields_ = [
        ("sessionID", ctypes.c_int),
        ("event", SessCtrlAsrEvent),
        ("startDataTime", ctypes.c_long),
        ("durationTime", ctypes.c_int)
    ]
    def __init__(self):
        pass

class SessCtrl_AsrHandleResponse(ctypes.Structure):
    _fields_ = [
        ("sentenceFinal", SessCtrlSentenceFinal)
    ]
    def __init__(self):
        pass

    
class SessCtrl_GetData(ctypes.Structure):
    _fields_ = [
        ("trash", ctypes.c_int)
    ]
    def __init__(self):
        pass
    
class SessCtrl_Counter(ctypes.Structure):
    _fields_ = [
        ("rmsVadDataLenInMs", ctypes.c_int),
        ("rmsVadReportPeriodInMs", ctypes.c_int),
        ("asrDataLenInMs", ctypes.c_int),
        ("asrDataReportPeriodInMs", ctypes.c_int)  
    ]
    def __init__(self):
        pass
    
class SessCtrl_EventCounter(ctypes.Structure):
    _fields_ = [
        ("remoteUid", ctypes.c_long),
        ("sessCtrlReportNumOfFinalInSession", ctypes.c_int),
        ("sessCtrlReportNumOfFinalBetweenSession", ctypes.c_int),
        ("sessCtrlReportNumOfFinalCrossSession", ctypes.c_int),
        ("sessCtrlReportEOSNumbers", ctypes.c_int),
        ("sessCtrlReportInputLength", ctypes.c_int),
        ("sessCtrlReportOutputLength", ctypes.c_int),
        ("sessCtrlReportZeroDataLength", ctypes.c_int),
        ("sessCtrlReportSendZeroDataLenHistogram", ctypes.c_int * 8),
        ("sessCtrlReportLastWordDelayHistogram", ctypes.c_int * 8),
        ("sessCtrlReportFirstWordDelayHistogram", ctypes.c_int * 8),
        ("sessCtrlReportVadLengthHistogram", ctypes.c_int * 8),
        ("sessCtrlReportSilenceLengthHistogram", ctypes.c_int * 8),
        ("sessCtrlReportVadProbHistogram", ctypes.c_int * 8),
        ("sessCtrlReportSilenceProbHistogram", ctypes.c_int * 8),
        ("sessCtrlReportInputVolumeHistogram", ctypes.c_int * 8)
    ]
    def __init__(self):
        pass



# Function prototypes
#AGORA_API int Agora_UAP_SessCtrl_create(void** stPtr);
Agora_UAP_SessCtrl_create = sessctrl_lib.Agora_UAP_SessCtrl_create
Agora_UAP_SessCtrl_create.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
Agora_UAP_SessCtrl_create.restype = ctypes.c_int



#AGORA_API int Agora_UAP_SessCtrl_destroy(void** stPtr);
Agora_UAP_SessCtrl_destroy = sessctrl_lib.Agora_UAP_SessCtrl_destroy
Agora_UAP_SessCtrl_destroy.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
Agora_UAP_SessCtrl_destroy.restype = ctypes.c_int


#AGORA_API int Agora_UAP_SessCtrl_counterEventReport(void* stPtr,SessCtrl_EventCounter* pEventCounter);
Agora_UAP_SessCtrl_counterEventReport = sessctrl_lib.Agora_UAP_SessCtrl_counterEventReport
Agora_UAP_SessCtrl_counterEventReport.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_EventCounter)]
Agora_UAP_SessCtrl_counterEventReport.restype = ctypes.c_int


#AGORA_API int Agora_UAP_SessCtrl_memAllocate(void* stPtr, const SessCtrl_StaticCfg* pCfg);
Agora_UAP_SessCtrl_memAllocate = sessctrl_lib.Agora_UAP_SessCtrl_memAllocate
Agora_UAP_SessCtrl_memAllocate.restype = ctypes.c_int
Agora_UAP_SessCtrl_memAllocate.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_StaticCfg)]

#AGORA_API int Agora_UAP_SessCtrl_init(void* stPtr);

Agora_UAP_SessCtrl_init = sessctrl_lib.Agora_UAP_SessCtrl_init
Agora_UAP_SessCtrl_init.argtypes = [ctypes.c_void_p]
Agora_UAP_SessCtrl_init.restype = ctypes.c_int


#AGORA_API int Agora_UAP_SessCtrl_setDynamCfg(void* stPtr, const SessCtrl_DynamCfg* pCfg);
Agora_UAP_SessCtrl_setDynamCfg = sessctrl_lib.Agora_UAP_SessCtrl_setDynamCfg
Agora_UAP_SessCtrl_setDynamCfg.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_DynamCfg)]
Agora_UAP_SessCtrl_setDynamCfg.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_getStaticCfg(const void* stPtr, SessCtrl_StaticCfg* pCfg);
Agora_UAP_SessCtrl_getStaticCfg = sessctrl_lib.Agora_UAP_SessCtrl_getStaticCfg
Agora_UAP_SessCtrl_getStaticCfg.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_StaticCfg)]
Agora_UAP_SessCtrl_getStaticCfg.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_getDefaultStaticCfg(SessCtrl_StaticCfg* pCfg);
Agora_UAP_SessCtrl_getDefaultStaticCfg = sessctrl_lib.Agora_UAP_SessCtrl_getDefaultStaticCfg
Agora_UAP_SessCtrl_getDefaultStaticCfg.argtypes = [ctypes.POINTER(SessCtrl_StaticCfg)]
Agora_UAP_SessCtrl_getDefaultStaticCfg.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_getDynamCfg(const void* stPtr, SessCtrl_DynamCfg* pCfg);
Agora_UAP_SessCtrl_getDynamCfg = sessctrl_lib.Agora_UAP_SessCtrl_getDynamCfg
Agora_UAP_SessCtrl_getDynamCfg.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_DynamCfg)]
Agora_UAP_SessCtrl_getDynamCfg.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_getDefaultDynamCfg(SessCtrl_FrmCtrl* frmCtrlPtr, SessCtrl_DynamCfg* pDynamCfg);
Agora_UAP_SessCtrl_getDefaultDynamCfg = sessctrl_lib.Agora_UAP_SessCtrl_getDefaultDynamCfg
Agora_UAP_SessCtrl_getDefaultDynamCfg.argtypes = [ctypes.POINTER(SessCtrl_FrmCtrl), ctypes.POINTER(SessCtrl_DynamCfg)]
Agora_UAP_SessCtrl_getDefaultDynamCfg.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_getCounter(void* stPtr, SessCtrl_Counter* pCounter);
Agora_UAP_SessCtrl_getCounter = sessctrl_lib.Agora_UAP_SessCtrl_getCounter
Agora_UAP_SessCtrl_getCounter.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_Counter)]
Agora_UAP_SessCtrl_getCounter.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_proc(void* stPtr, const SessCtrl_FrmCtrl* pCtrl, const SessCtrl_InputData* pIn,SessCtrl_OutputData* pOut);
Agora_UAP_SessCtrl_proc = sessctrl_lib.Agora_UAP_SessCtrl_proc
Agora_UAP_SessCtrl_proc.argtypes = [ctypes.c_void_p, ctypes.POINTER(SessCtrl_FrmCtrl), ctypes.POINTER(SessCtrl_InputData), ctypes.POINTER(SessCtrl_OutputData)]
Agora_UAP_SessCtrl_proc.restype = ctypes.c_int

#AGORA_API int Agora_UAP_SessCtrl_handleAsrResponse(void* stPtr, const SessCtrl_AsrResponse* pAsrResponse, SessCtrl_OutputData* pOut,SessCtrl_AsrHandleResponseFinal* pFinal);



class SessionControl:
    def __init__(self, userid:ctypes.c_char_p):
        self._handler = ctypes.c_void_p(0)
        self._static_config = SessCtrl_StaticCfg()
        self._dynamic_config = SessCtrl_DynamCfg()
        self._initialized = False
        #pre allocated null buffer struct for proc
        self._sessctrl_in_data = SessCtrl_InputData()
        self._sessctrl_out_data = SessCtrl_OutputData()
        self._frm_ctrl = SessCtrl_FrmCtrl()
        self._frm_count = 0
        self._user_id = userid #str type
        ret = self._prepare_sessctrl_cfg()
        # for lifetime control
        self._last_access_time = time.time()*1000 #unit in ms
        pass
    def _prepare_sessctrl_cfg(self) -> int:

		#get default config and default frame config
        ret_static  = Agora_UAP_SessCtrl_getDefaultStaticCfg(ctypes.byref(self._static_config))
        ret_dynamic = Agora_UAP_SessCtrl_getDefaultDynamCfg(ctypes.byref(self._frm_ctrl), ctypes.byref(self._dynamic_config))
        

		#assign value to static config
        self._static_config.userID = ctypes.c_char_p(self._user_id.encode('utf-8'))  
        self._static_config.frmSz = 160
        self._static_config.smplFrq = SessCtrlFs.kFs_16000
        self._static_config.persistentVoiceLenOfSOS = 10
        self._static_config.prePaddingLenOfSessCtrlSOS = 0
        self._static_config.postPaddingLenOfSessCtrlEOS = 0
        self._static_config.unVoiceLenOfTriggerSessCtrlEOS = 1000000
        self._static_config.unVoiceLenOfTriggerServerEOS = 0
        self._static_config.eosWaitTime = 0
        self._static_config.eosRetryWaitTime =0
        self._static_config.eosRetryPadding = 0
        self._static_config.eosRetryMaxIteration = 0
        
		#assign value to dynamic config
        self._dynamic_config.logLv = 10
        self._dynamic_config.sessCtrlTimeOutInMs = 1000000
        self._dynamic_config.sessCtrlStartSniffWordGapInMs = 1000000
        self._dynamic_config.sessCtrlWordGapLenInMs = 10
        self._dynamic_config.sessCtrlWordGapLenVolumeThr = 0
        self._dynamic_config.sessCtrlEnableDumpFlag = 0
        self._dynamic_config.vadThr = -2
        self._dynamic_config.voiceThr = -2
        self._dynamic_config.sessCtrlFinalRMSThr = 80
        self._dynamic_config.sessCtrlFinalThr = 200
        self._dynamic_config.sessCtrlFinalThrInc = 100
        self._dynamic_config.sessCtrlFinalThrMax = 3
        self._dynamic_config.meterRMSThr = 65
        self._dynamic_config.sessCtrlBSVoiceGateFlag = 1
        self._dynamic_config.sessCtrlBSVoiceAggressive = 4
        self._dynamic_config.sessCtrlAiVadBasedDenoiseFlag = 1
        self._dynamic_config.sessCtrlAiVadBasedDenoiseDelayInMs = 50
        self._dynamic_config.sessCtrlAiVadBasedVoiceDenoiseProbThr = 0.5
        self._dynamic_config.sessCtrlAiVadBasedMusicDenoiseProbThr = 0.5

        return (ret_static and ret_dynamic)
    def _init(self) -> int:
        if self._initialized:
            return 0
        #create handler
        self._handler = ctypes.c_void_p()
        ret = Agora_UAP_SessCtrl_create(ctypes.byref(self._handler))
        if ret < 0:
            return ret
        
		#prepari static config & dynamic configure
        ret = self._prepare_sessctrl_cfg()

		#memory allocate
        ret = Agora_UAP_SessCtrl_memAllocate(self._handler, ctypes.byref(self._static_config))
        if ret < 0:
            return ret

		#init
        ret = Agora_UAP_SessCtrl_init(self._handler)
        if ret < 0:
            return ret
        
		#set dynamic configure
        ret = Agora_UAP_SessCtrl_setDynamCfg(self._handler, ctypes.byref(self._dynamic_config))
        if ret < 0:
            return ret
        self._initialized = True if ret == 0 else False
        return ret
    def process (self, c_buffer:ctypes.c_void_p, size_in_short: int) -> tuple[int, ctypes.c_void_p]: # return ret, pcm data in bytes. ret is len of uint8
       
       #update last access time
        self._last_access_time = time.time()*1000
        self._sessctrl_in_data.pcm = c_buffer
        self._sessctrl_in_data.frmIdx = self._frm_count 
        self._frm_count += 1
        #todo：
        #如果mute后，是否有必要销毁session ctrl？---暂时不考虑销毁
        #用户id：和外部对齐
        #功能点：
        #
        
        #inputData.ts = (frmCnt * frmSz) / (MT_TEST_FS / 1000);
        self._sessctrl_in_data.ts = self._frm_count * self._static_config.frmSz / (SessCtrlFs.kFs_16000 / 1000)
        self._sessctrl_out_data.status = SessCtrlStatus.kSCStatus_None
        self._sessctrl_out_data.pcmBuf = ctypes.c_void_p(0)
        self._sessctrl_out_data.nSamplesInPcmBuf = 0 #added by me ,ToDo check if needed, parameters need to be rest or not?
        
        
        ret = Agora_UAP_SessCtrl_proc(self._handler, ctypes.byref(self._frm_ctrl), ctypes.byref(self._sessctrl_in_data), ctypes.byref(self._sessctrl_out_data))
        if ret < 0:
            return ret, ctypes.c_void_p(0) #exit(1) ?? indicate error and do not continue to process next frame? ToDo
        #get output data
        if self._sessctrl_out_data.nSamplesInPcmBuf > 0: #unit: unit16
            ret = self._sessctrl_out_data.nSamplesInPcmBuf * 2 #unit: unit8
            return ret, self._sessctrl_out_data.pcmBuf
        return 0, ctypes.c_void_p(0) #no data
        pass
    def release(self):
        if self._initialized:
            ret = Agora_UAP_SessCtrl_destroy(self._handler)
            self._initialized = False
            self._handler = ctypes.c_void_p(0)
        pass
    def is_expired(self, interval: int) -> bool:
        return ( time.time()*1000 - self._last_access_time > interval )

    #manager for sessionctrol
class SessionCtrlManager:
    def __init__(self, update_interval: int = 100, expired_duration: int = 1000*10) -> None:
        self._sessions = {}
        self._last_update_time = time.time()*1000  #in ms
        self._update_interval = update_interval  # in ms, every 100ms to do check
        self._expired_duration = expired_duration  #10s expired
    pass
    def process_audio_frame(self, userid: ctypes.c_char_p, c_buffer:ctypes.c_void_p, size_in_short: int) -> tuple[int, ctypes.c_void_p]:
        #check & release the expired sessions
        ret = self._update_check()
        #get session
        #do process within session
        session = self._get_session(userid)
        ret, c_datas =  session.process(c_buffer, size_in_short)
        return ret, c_datas
        pass
    def _get_session(self, userid:ctypes.c_char_p) -> SessionControl:
        if userid not in self._sessions:
            #add new session & do init process
            session = SessionControl(userid)
            session._init()
            self._sessions[userid] = session
        return self._sessions[userid]
    def _update_check(self) -> None:
        now = time.time()*1000 #in ms
        if now - self._last_update_time < self._update_interval:
            return
        self._last_update_time = now
        for userid in self._sessions:
            session = self._sessions[userid]
            if session.is_expired(self._expired_duration):
                session.release()
                del self._sessions[userid]
    def release(self, userid: int) -> None:
        if userid in self._sessions:
            self._sessions[userid].release()
            del self._sessions[userid]
        pass
    def clear(self) -> None:
        for userid in self._sessions:
            self._sessions[userid].release()
        self._sessions.clear()
        pass
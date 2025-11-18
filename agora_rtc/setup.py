from setuptools.command.install import install
from setuptools import setup
import site
import os
import sys
import zipfile
# import urllib
from urllib import request
import ssl
import platform
ssl._create_default_https_context = ssl._create_unverified_context


class CustomInstallCommand(install):
    def run(self):
        self.download_and_extract_sdk()
        install.run(self)

    def get_sdk_path(self):
        agora_service_path = os.path.join(site.getsitepackages()[0], 'agora', 'rtc')
        parent_dir = os.path.dirname(agora_service_path)
        agora_service_path = parent_dir
        sdk_dir = os.path.join(agora_service_path, "agora_sdk")
        return sdk_dir
    def download_and_extract_rtm(self):
        sdk_dir = self.get_sdk_path()
        zip_path = os.path.join(sdk_dir, "agora_rtm_sdk.zip")
        arch = platform.machine()
        os_type = platform.system()
        
        pass

    def download_and_extract_sdk(self):
        print("download_and_extract_sdk--------------")
        agora_service_path = os.path.join(site.getsitepackages()[0], 'agora', 'rtc')
        parent_dir = os.path.dirname(agora_service_path)
        agora_service_path = parent_dir
        sdk_dir = os.path.join(agora_service_path, "agora_sdk")
        zip_path = os.path.join(agora_service_path, "agora_rtc_sdk.zip")
        arch = platform.machine()
        os_type = platform.system()

        '''# version before 2.2.0
        #url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.30-20241024_101940-398537.zip"
        #url = "https://download.agora.io/sdk/release/agora_rtc_sdk_mac_rel.v4.4.30_22472_FULL_20241024_1224_398653.zip"
        
        # verison 2.2.0
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.31-20241223_111509-491956.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.31_23136_FULL_20241223_1245_492039.zip"
        if arch == "aarch64" and sys.platform == 'linux':
            url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.31-20250307_175457-603878.zip"
         '''
        # version 2.2.4
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250425_144419-675648.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_24257_FULL_20250425_1609_675722.zip"
        if arch == "aarch64" and sys.platform == 'linux':
            url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20250425_150503-675674.zip"
        
        #verison 2.3.0: for aiqos
        url  = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250715_161625-791246.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_24915_FULL_20250715_1710_791284.zip"
        if arch == "aarch64" and sys.platform == 'linux':
          url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20250425_150503-675674.zip"
     
        #verison 2.3.0 0902 
        #date: 20250829 version:
        # fix a audio-dump thread leak bug
        # add pts field in send video frame, and send audio frame
        # add pts field in both audio and video frame callback
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250829_160340-860733.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_25418_FULL_20250829_1647_860754.zip"
        if arch == "aarch64" and sys.platform == 'linux':
            url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20250829_160340-860733.zip"

        #20251107 Fusion version: one sdk package include rtc and rtm
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.32-20250829_160340-860733-aed_20251107_1642.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.32_25418_FULL_20250829_1647_860754-aed_20251107_1639.zip"

        #20251110 Fusion version: with apm filter
        mac_sdk="https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.30_25869_FULL_20251030_1836_953684-aed.zip"
        url = "https://download.agora.io/sdk/release/agora_rtc_sdk_x86_64-linux-gnu-v4.4.32.150_26715_SERVER_20251030_1807-aed.zip"
        if sys.platform == 'darwin':
            url = mac_sdk
   
       
        if arch == "aarch64" and sys.platform == 'linux':
            url = "https://download.agora.io/sdk/release/Agora-RTC-aarch64-linux-gnu-v4.4.32-20251009_145437-921455.zip"
        
        
              
        if os.path.exists(sdk_dir):
            os.system(f"rm -rf {sdk_dir}")
        os.makedirs(agora_service_path, exist_ok=True)
        if os.path.exists(zip_path):
            os.remove(zip_path)

        print("agora_service_path:", agora_service_path)
        print(f"Downloading {url}...")
        request.urlretrieve(url, zip_path)

        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(agora_service_path)

        if os.path.exists(zip_path):
            os.remove(zip_path)


setup(
    name='agora_python_server_sdk',
    version='2.4.0',
    description='A Python SDK for Agora Server',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AgoraIO-Extensions/Agora-Python-Server-SDK',
    packages=["agora", "agora.rtc", "agora.rtc._ctypes_handle", "agora.rtc._utils","agora.rtc.utils","agora.rtm","agora.rtm._ctypes_handle"],
    classifiers=[
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.10',
    cmdclass={
        'install': CustomInstallCommand,
    },
)

if __name__ == "__main__":
    print("run setup -------------")

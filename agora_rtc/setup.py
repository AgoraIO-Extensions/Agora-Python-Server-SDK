import os
import sys
import zipfile
# import urllib
from urllib import request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import site
from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        self.download_and_extract_sdk()
        install.run(self)

    def download_and_extract_sdk(self):
        print("download_and_extract_sdk--------------")
        agora_service_path = os.path.join(site.getsitepackages()[0], 'agora', 'rtc')
        sdk_dir = os.path.join(agora_service_path, "agora_sdk")
        zip_path = os.path.join(agora_service_path, "agora_rtc_sdk.zip")

        url = "https://download.agora.io/sdk/release/agora_rtc_sdk_linux_v4.4.30-20240928_160128-358664.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_sdk_mac_v4.4.30_22119_FULL_20240928_1647_358680.zip"
        
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
    version='2.0.4',                 
    description='A Python SDK for Agora Server',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/AgoraIO-Extensions/Agora-Python-Server-SDK',  
    packages=["agora.rtc"],          
    classifiers=[                      
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",

    ],
    python_requires='>=3.8',          
    cmdclass={
    'install': CustomInstallCommand,
    },
)

if __name__ == "__main__":
    print("run setup -------------")

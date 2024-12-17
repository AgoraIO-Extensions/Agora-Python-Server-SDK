from setuptools.command.install import install
from setuptools import setup
import site
import os
import sys
import zipfile
# import urllib
from urllib import request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class CustomInstallCommand(install):
    def run(self):
        self.download_and_extract_sdk()
        install.run(self)

    def download_and_extract_sdk(self):
        print("download_and_extract_sdk--------------")
        agora_service_path = os.path.join(site.getsitepackages()[0], 'agora', 'rtc')
        sdk_dir = os.path.join(agora_service_path, "agora_sdk")
        zip_path = os.path.join(agora_service_path, "agora_rtc_sdk.zip")

        url = "https://download.agora.io/sdk/release/agora_rtc_sdk-x86_64-linux-gnu-v4.4.30-20241024_101940-398537.zip"
        if sys.platform == 'darwin':
            url = "https://download.agora.io/sdk/release/agora_rtc_sdk_mac_rel.v4.4.30_22472_FULL_20241024_1224_398653.zip"

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
    version='2.1.7',
    description='A Python SDK for Agora Server',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AgoraIO-Extensions/Agora-Python-Server-SDK',
    packages=["agora.rtc", "agora.rtc._ctypes_handle", "agora.rtc._utils","agora.rtc.utils"],
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

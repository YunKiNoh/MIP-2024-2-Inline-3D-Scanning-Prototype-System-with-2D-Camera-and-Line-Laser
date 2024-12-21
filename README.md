# MIP_2024_2_Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser

## 1. Introdution
본 Repository는 2024년 2학기에 진행된 기전융합종합 설계[Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser]에 대한 전반적인 설명 및 가이드라인 제공을 위해 제작되었습니다.

연구목적: Optical 3D Scanning 중에서 'Laser Triangulation Method'는 가장 높은 정밀도(마이크로미터 단위)를 바탕으로 'Defect Inspection for Industrial Small Parts'를 위해서 사용되고 있습니다. 이 방식은 3D 카메라를 통해서 이루어져 왔는데, 이러한 장비는 높인 비용으로 인해 산업 이외의 용도로는 쓰기 힘든 상황입니다. 하지만 'Laser Triangulation Method'를 기반으로 2D 카메라와 Line Laser의 결합을 통해 3D Scanning System 구현한다면, 더 저렴한 비용에서 해당 장비를 활용할 수 있을 것입니다. 이러한 판단 가운데, 본 프로젝트는 2D Machine Vision Camera, Line Laser, Telecentric Lens, Conveyor Belt를 활용하여 작은 산업 부품에 대한 결함 감지 달성을 목표로 두어서, 3D Scanning System 구축을 계획 및 수행하였습니다.


## 2. Build up Software Environment
이 프로젝트는 파이썬 환경에서 개발되었습니다. 이때 머신 비전 카메라를 파이썬에서 사용하기 위해서는 'Teledyne FLIR'에서 제공하는 'Spinnaker SDK' 파일을 통해 'Pyspin' 라이브러리를 다운로드 받아야 합니다. 해당 Section에서는 'Pyspin'을 설치하고 머신비전 2D 카메라('GS3-U3-41C6NIR-C')가 파이썬에서 잘 작동하는 것까지 확인할 수 있도록 환경구축 가이드를 제공하려고 합니다.

### 2.1. Make Virtual Environment for Python 3.8
Pyspin 활용을 위해 Python 3.8을 기반으로 하는 가상환경을 아나콘다에서 구축합니다.

-> conda create -n py38 python=3.8

## 2.2. Install 'Pillow==7.0.0' in the Command Prompt
명령프롬프트를 관리자 권한으로 실행하여서 Python 3.5~3.8버전을 위한 파일인 'Pillow==7.0.0'를 설치합니다.

-> -m pip install Pillow==7.0.0

## 2.3. Download Spinnaker SDK Files
Pyspin을 다운로드 받기 위해서는 'Teledyne FLIR'에서 제공하는 'Spinnaker SDK' 파일을 다운로드 받아야 합니다. 이를 위해 다음을 수행합니다.

### 2.3.1. Make ID for Download
해당 페이지에서 파일을 다운로드 받으려면 아이디를 만들어서 접속하여야 합니다. 해당 링크에서 아이디를 만든 후 다시 접속합니다. 
Link: https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK

### 2.3.2. Download 'Spinnaker-2.6.160-Windows' file
해당 페이지 맨 밑의 'Previous Version'에서 'Version 2.6.0.160'을 다운로드 받습니다. (해당 프로젝트에서는 'Spinnaker-2.6.0.160-Windows').

### 2.3.3. Install SDK file
zip파일을 unzip한 후에 노트북 사양에 맞게 'SpinnakerSDK_FULL_2.6.0.160_x.exe' 파일을 골라 설치해줍니다.

## 2.4. Install Pyspin Library
이제부터는 이전에 만든 Python 3.8 버전의 가상환경에서 설치를 진행합니다. 이를 위해 py38 가상환경을 켜줍니다.

-> conda activate py38

### 2.4.1. Unzip 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64' file
Pyspin 다운로드를 위해 Pyspin 폴더에 들어가 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.zip' 파일을 압축풀기 합니다. 해당 폴더에 들어가면, 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl' 설치 파일이 있음을 확인할 수 있습니다.

### 2.4.2. Change the path of anaconda into the path of the place where 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl' is located.
아나콘다 프롬프트에서 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl'을 다운로드 하기 위해 해당 파일이 있는 경로로 이동합니다.

-> cd "spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl가 있는 경로"

### 2.4.3. Download 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl' in the virtual environment.
해당 파일을 python 3.8 버전에서 다운로드 합니다.

-> python -m pip install spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl

### 2.4.4. Check the download state of 'spinnaker-python 2.6.0.160'
가상환경 안에서 'spinnaker-python 2.6.0.160'가 잘 설치되었는지 확인합니다. 리스트 안에 'spinnaker-python 2.6.0.160'가 있으면 성공.

-> pip list

## 2.5. Execute example code to check working of machine vision camera in the python.
'Examples' 폴더를 지나 'Python3'에 있는 'AcquireAndDisplay.py'를 실행해서 카메라를 통해 이미지를 얻어봅니다.


## 3. 


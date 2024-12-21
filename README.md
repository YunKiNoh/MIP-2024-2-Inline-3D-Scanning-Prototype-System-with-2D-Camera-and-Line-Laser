# MIP_2024_2_Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser

## 1. Introdution
본 Repository는 2024년 2학기에 진행된 기전융합종합 설계[Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser]에 대한 전반적인 설명 및 가이드라인 제공을 위해 제작되었습니다.

연구목적: Optical 3D Scanning 중에서 'Laser Triangulation Method'는 가장 높은 정밀도(마이크로미터 단위)를 바탕으로 'Defect Inspection for Industrial Small Parts'를 위해서 사용되고 있습니다. 이 방식은 3D 카메라를 통해서 이루어져 왔는데, 이러한 장비는 높인 비용으로 인해 산업 이외의 용도로는 쓰기 힘든 상황입니다. 하지만 'Laser Triangulation Method'를 기반으로 2D 카메라와 Line Laser의 결합을 통해 3D Scanning System 구현한다면, 더 저렴한 비용에서 해당 장비를 활용할 수 있을 것입니다. 이러한 판단 가운데, 본 프로젝트는 2D Machine Vision Camera, Line Laser, Telecentric Lens, Conveyor Belt를 활용하여 작은 산업 부품에 대한 결함 감지 달성을 목표로 두어서, 3D Scanning System 구축을 계획 및 수행하였습니다.


## 2. Build up Software Environment
이 프로젝트는 파이썬 환경에서 개발되었습니다. 이때 머신 비전 카메라를 파이썬에서 사용하기 위해서는 'Teledyne FLIR'에서 제공하는 'Spinnaker SDK' 파일을 통해 'Pyspin' 라이브러리를 다운로드 받아야 합니다. 해당 Section에서는 'Pyspin'을 설치하고 머신비전 2D 카메라('GS3-U3-41C6NIR-C')가 파이썬에서 잘 작동하는 것까지 확인할 수 있도록 환경구축 가이드를 제공하려고 합니다.

### 2.1. Make Virtual Environment for Python 3.8
Pyspin 활용을 위해 Python 3.8을 기반으로 하는 가상환경을 아나콘다에서 구축합니다.
```Anadonda
conda create -n py38 python=3.8
```
### 2.2. Install 'Pillow==7.0.0' in the Command Prompt
명령프롬프트를 관리자 권한으로 실행하여서 Python 3.5~3.8버전을 위한 파일인 'Pillow==7.0.0'를 설치합니다.
```
-m pip install Pillow==7.0.0
```
### 2.3. Download Spinnaker SDK Files
Pyspin을 다운로드 받기 위해서는 'Teledyne FLIR'에서 제공하는 'Spinnaker SDK' 파일을 다운로드 받아야 합니다. 이를 위해 다음을 수행합니다.

#### 2.3.1. 아이디 만들기
[Link: https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK]

#### 2.3.2. Download 'Version 2.6.0.160'
해당 페이지 맨 밑의 'Previous Version'에서 'Version 2.6.0.160'을 다운로드 받습니다. (해당 프로젝트에서는 'Spinnaker-2.6.0.160-Windows').

#### 2.3.3. Install 'SpinnakerSDK_FULL_2.6.0.160_x.exe'
zip파일을 unzip한 후에 노트북 사양에 맞게 'SpinnakerSDK_FULL_2.6.0.160_x.exe' 파일을 골라 설치해줍니다. (본 노트북에서는 'SpinnakerSDK_FULL_2.6.0.160_64.exe')

### 2.4. Install Pyspin Library
이제부터는 이전에 만든 Python 3.8 버전의 가상환경에서 파일 설치를 진행합니다. 이를 위해 py38 가상환경을 켜줍니다.
```Anadonda
conda activate py38
```
Pyspin 다운로드를 위해 Pyspin 폴더에 들어가 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.zip' 파일을 압축풀기 합니다. 해당 폴더에 들어가면, 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl' 설치 파일이 있음을 확인할 수 있습니다. 그러고 나서 아나콘다 프롬프트에서 'spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl'을 다운로드 하기 위해 해당 파일이 있는 경로로 이동합니다.
```
cd "spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl가 있는 경로"
```
이후에 해당 파일을 python 3.8 가상환경에서 다운로드 합니다.
```
python -m pip install spinnaker_python-2.6.0.160-cp38-cp38-win_amd64.whl
  ```
가상환경 안에서 'spinnaker-python 2.6.0.160'가 잘 설치되었는지 확인합니다. 리스트 안에 'spinnaker-python / 2.6.0.160'가 있으면 성공.
```
pip list
```

### 2.5. Execute example code to check working of machine vision camera in the python.
'Examples' 폴더를 지나 'Python3'에 있는 'AcquireAndDisplay.py'를 실행해서 카메라를 통해 이미지를 얻어봅니다.
```
cd "AcquireAndDisplay.py이 있는 경로"
```
```
python AcquireAndDisplay.py
```

## 3. Specifications of Hardware
본 프로젝트에서는 크게 세가지 하드웨어가 사용되었습니다. [2D Camera, Telecentric Lens, Line Laser].

![image](https://github.com/user-attachments/assets/389dbdfe-5697-4ba5-ab6d-753c8598f11a)

### 3.1. 2D Machine Vision Camera[GS3-U3-41C6NIR-C]
- Sensor: CMOSIS CMV4000, 1" format, progressive scan CMOS sensor.
- Resolution: 4.2 megapixels (2048 x 2048).
- Pixel Size: 5.5 µm x 5.5 µm.
- Sensing Area: 11.26 mm x 11.26 mm.
- Frame Rate: Up to 90 frames per second (fps).
- Shutter Type: Global shutter, ideal for capturing fast-moving objects without distortion.
- Pixel Depth: Supports 8, 12, and 16-bit output formats.
- Interface: USB 3.0 for high-speed data transfer.
- Exposure Time: Adjustable from 16 µs to 7.03 seconds, offering flexibility for various lighting conditions.
- Buffer Memory: 128 MB image buffer to help manage image transfer efficiently.
### 3.2. Telecentric Lens [TCL0.3X-130I-HR]
- Mag: 0.3X
- W.D(mm): 130
- Resolution(um): 17.7
- N.A: 0.019	
- F/#: 7.9
- D.O.F(mm): 7
- Telecentricity(Degree): 0.04
- Optical Distortion(%): 0.08
- Sensor Size(mm)(Diagonal Length): 2/3"(11mm)	
- Mount: C
### 3.3. Line Laser [Laser ZX20 450nm 60mW 30degree]
- Wavelength: 450nm
- Line width: Aapproximately "0.03[mm]~0.2[mm]" at the distance of "100[mm] ~ 700[mm]"
- DOF: Approximately "0[mm] ~ 80[mm]" at the distance of "100[mm] ~ 700[mm]"
- Input Line: VCC[Brown], GND[Blue], DIG[White], ANA[Black]
- Output Line: FAIL[Gray]

## 4. Description of Each Code
3D Scanning Prototype System을 위해 총 두가지의 코드가 사용됩니다. 첫번째는 라인 레이저의 초기 위치를 맞추기 위한 코드, 두번째는 Automatic 3D Scanning을 위한 코드입니다.
### 4.1. InitialLine_Fitting_375x375.py
해당 코드는 기초 세팅을 위해 잠시 활용하는 것으로써, '카메라 접속', '카메라를 통해 원본 이미지 받기', 그리고' 라인 레이저를 이미지 프로세싱한 뒤에 Initial Line에 맞추기'를 수행합니다.
특히, Line Laser의 물리적 각도는 해당 Initial Line과 Fine line이 곂쳐져서 최대한 Height Value'가 0.00에 근접할 수 있도록 조정합니다.

![image](https://github.com/user-attachments/assets/47c5d285-7b68-4c7c-8d5c-94b92ccde0fc)

### 4.2. 3D_Scanning.py
본 코드에서 3D 스캐닝을 진행합니다. 카메라의 최대 해상도는 2048x2048이나 메모리 부족 문제로 인하여 375x375 해상도로 낮춰, 0.1mm 단위의 3D Scanning을 수행하였습니다. 
또한 높이 값을 바탕으로 어떤 점이라도 3D Scanning Result에 반영이 가능하지만, 해당 시스템의 전체적인 파악을 위해, threshold 값을 걸어 바닥으로 인식하는 capture image의 경우 plot에 반영하지 않았습니다.
그렇기 때문에 해당 코드는 바닥만 인식하는 경우 3D 스캐닝을 진행하지 않으며, 물체를 인식하는 동안 3D 스캐닝을 진행한 후, 다시 바닥만 인식하면 3D 스캐닝을 멈춥니다.
다만, 이 코드는 시연을 위한 코드로써, 모든 데이터를 스캐닝 결과에 반영하기 위해서는 해당 코드를 바탕으로 추가적인 코드 작성 및 메모리 부족 문제를 다루어야 할 것입니다.

![image](https://github.com/user-attachments/assets/9ecf8e40-f2cc-4458-afad-83f7c58e243e)

## 5. Result
해당 프로젝트의 목표는 물체의 결함 탐지인데, 기어와 프레임을 대상으로 해당 과업의 수행 가능성을 검토하였고, 이 시스템에 대한 몇가지 문제를 개선한다면 충분히 달성 가능한 목표임을 확인하였습니다. 

![image](https://github.com/user-attachments/assets/8e596bf0-e64b-447a-90ca-262669f0c03b)

## 6. Limitations and Suggestions
그러나 이 프로젝트에서는 몇가지 문제점이 있습니다. 두 문제 모두 3D Scanning Result의 거리 왜곡을 발생시킵니다. 첫번째는 컨베이어 벨트의 불안정한 속도로 인해 발생하는 문제이며, 두번째는 레이저의 기울어진 각도로 인해 발생하는 문제입니다.

### 6.1. Unstable Velocity of The Conveyor Belt
![image](https://github.com/user-attachments/assets/2d1acdcb-81a5-49c0-852c-a93518d05cdf)

본 프로젝트에서는 3D 이미지의 (x,y,z) 값, 즉 (길이,너비,높이)의 단위 거리를 모두 0.1[mm]로 통일하였습니다. 특히 3D 이미지에서 길이의 단위 거리를 설정하기 위해서는 컨베이어 벨트와 카메라의 fps가 고려되어야 하는데, 이때 컨베이어 벨트의 속도는 대략 7.5[mm/s]로 측정됩니다. 그리고 이 속도에 대하여 매 프레임마다 캡쳐되는 2D Image 사이의 거리를 0.1[mm]로 맞추기 위해서 fps 값을 75로 설정하였습니다. 다만, 이 컨베이어 벨트는 그 속도가 조금씩 변동하고, 이에 따라 매 프레임마다 캡쳐되는 2D Image 사이의 실제 거리는 0.1[mm]로부터 멀어지고 있는 상황입니다. 이로 인해 매번 2D Image가 쌓일 때 마다 0.1[mm]의 단위 거리에 대하여 오차가 발생하고 있는데, 이러한 오차가 누적되면서 3D 스캐닝의 길이 전체에 왜곡이 발생하고 있습니다. 이러한 문제를 해결하기 위해서는 속도가 안정적으로 유지되며 추가적으로 미세하게 조절할 수 있는 컨베이어 벨트가 필요한 상황입니다. 그렇기 때문에, 이후의 연구에서는 안정적인 속도와 정밀한 속도 제어가 가능한 컨베이어 벨트를 사용해야 길이 왜곡 문제가 1차적으로 해결될 것입니다.

### 6.2. Slope Distortion
![image](https://github.com/user-attachments/assets/ac937641-01c3-4307-bd97-74e308bf4843)

본 프로젝트는 Line Triangulation의 방법 중에 한 방식인, '카메라를 지상에 수직으로 고정시키고 레이저를 일정 각도로 기울여서 3D 스캐닝을 수행'하는 방식을 채택하였습니다. 다만, 이 방식의 근본적인 문제점은 스캐닝 되는 물체 표면의 각도가 변할 때마다 일정한 시간단위로 조사되고 있는 레이저 사이의 단위 거리가 변한다는 사실입니다. [왼쪽 그림 참고]. 다만 이러한 오차는 물체의 높이가 낮으면 낮을 수록 줄어들기 때문에 작은 물체를 3D 스캐닝하는 해당 프로젝트에서는 어느정도 감수될 수 있겠으나, 이 방식은 결국 이론적으로 길이 오차가 발생할 수 밖에 없기 때문에 이러한 문제를 해결할 필요가 있습니다. 이를 해결하기 위해서는, 레이저를 지상에 수직으로 고정하고 카메라는 일정 각도로 기울여서 물체의 높이에 따른 레이저의 변위를 측정하는 방식을 채택해야 합니다. [오른쪽 그림 참고]. 이러한 방식 또한 Line Triangulation을 통한 3D 스캐닝 방식 중에 하나로써, 이 방식을 추후에 적용한다면 본 프로젝트의 길이 왜곡에 대한 근본적인 문제점을 해결할 수 있을 것입니다.



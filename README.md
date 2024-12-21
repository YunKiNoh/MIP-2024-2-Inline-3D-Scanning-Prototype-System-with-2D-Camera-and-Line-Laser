# MIP_2024_2_Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser

## 1. Introdution
본 Repository는 2024년 2학기에 진행된 기전융합종합 설계[Inline 3D Scanning Prototype System for Industrial Part Inspection with 2D Camera and Line Laser]에 대한 전반적인 설명 및 가이드라인 제공을 위해 제작되었습니다.

연구목적: Optical 3D Scanning 중에서 'Laser Triangulation Method'는 가장 높은 정밀도(마이크로미터 단위)를 바탕으로 'Defect Inspection for Industrial Small Parts'를 위해서 사용되고 있습니다. 이 방식은 3D 카메라를 통해서 이루어져 왔는데, 이러한 장비는 높인 비용으로 인해 산업 이외의 용도로는 쓰기 힘든 상황입니다. 하지만 'Laser Triangulation Method'를 기반으로 2D 카메라와 Line Laser의 결합을 통해 3D Scanning System 구현한다면, 더 저렴한 비용에서 해당 장비를 활용할 수 있을 것입니다. 이러한 판단 가운데, 본 프로젝트는 2D Machine Vision Camera, Line Laser, Telecentric Lens, Conveyor Belt를 활용하여 작은 산업 부품에 대한 결함 감지 달성을 목표로 두어서, 3D Scanning System 구축을 계획 및 수행하였습니다.

## 2. Build up Software Environment
이 프로젝트는 파이썬 환경에서 개발되었습니다. 이때 머신 비전 카메라를 파이썬에서 사용하기 위해서는 'Teledyne FLIR'에서 제공하는 'Spinnaker SDK' 파일을 통해 'Pyspin' 라이브러리를 다운로드 받아야 합니다. 해당 Section에서는 'Pyspin'을 설치하고 머신비전 2D 카메라('GS3-U3-41C6NIR-C')가 파이썬에서 잘 작동하는 것까지 확인할 수 있도록 환경구축 가이드를 제공하려고 합니다.

### 2.1. Make Virtual Environment for Python 3.8
Pyspin 활용을 위해 Python 3.8을 기반으로 하는 가상환경을 아나콘다에서 구축합니다.
-> conda create -n py38 python=3.8

### 2.2. Install "Pillow==7.0.0" in the Command Prompt

## 3. 

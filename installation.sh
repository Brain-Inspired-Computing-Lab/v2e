#!/bin/bash

echo 'Update Conda'
conda update -n base -c defaults conda -y

echo "Installing CUDA 11.3 and CuDNN"
conda install conda-forge::cudatoolkit=11.3 -y
conda install conda-forge::cudnn -y

echo "Installing CUDA Enabled PyTorch"
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch -y

echo "Install V2E dependencies"
python -m pip install -e .

echo "Installing other dependencies"
python -m pip install dv-processing
python -m pip install 'pillow<10'

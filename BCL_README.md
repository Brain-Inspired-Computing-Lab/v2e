# BCL V2E Installation Process

## Requirements
- anaconda/miniconda
- CUDA Capable GPU

# Installation Steps
1. Download SuperSloMo model from [Google Drive](https://drive.google.com/file/d/1ETID_4xqLpRBrRo1aOT7Yphs3QqWR_fx/view)

2. Make a folder called 'input' and place model inside the folder


3. Create Conda Environment

    `conda create -n v2e python=3.10 -y`

4. Activate Conda Environment

    `conda activate v2e`

5. Run Installation Shell Script

    `chmod +x installation.sh`

    `./installation.sh`


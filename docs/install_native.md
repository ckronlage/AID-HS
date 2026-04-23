# Native installation

Notes:
- The current installation has been tested on Ubuntu 18.04
- The native installation is not supported 

## Prerequisites

### Anaconda

We use **Anaconda** to manage the environment and dependencies. Please follow instructions to [install Anaconda](https://docs.anaconda.com/anaconda/install).

### HippUnfold

AID-HS extracts volume- and surface-based features of the hippocampus using **HippUnfold**. Please follow instructions to [install HippUnfold v1.1.0](https://github.com/khanlab/hippunfold/releases/tag/v1.1.0).

### Workbench Connectom
AID-HS uses **Workbench Connectom** to create additional surface-based features. Please follow instructions to [install Workbench Connectom](https://www.humanconnectome.org/software/get-connectome-workbench).

## AID-HS license
In order to run AID-HS you need to have a `aidhs_license.txt` in the aidhs folder. To get this file, please fill out the [AID-HS registration form](https://docs.google.com/forms/d/e/1FAIpQLSdPbtraBZ2s0HD1W8qtF11wr_fYVTWZjraED03Rtl2ZjxeRMA/viewform?usp=header). Once submitted, your application will be automatically reviewed and the aidhs_license.txt file will be send to your email.

## Installation & configuration
In order to run the pipeline, you'll need to configure a couple of files

1. Download `aidhs.zip` from the [latest github release](https://github.com/MELDProject/AID-HS/releases/latest) and extract it.
2. Copy the `aidhs_license.txt` into the extracted folder (see above how to get the AID-HS license)
3. Create the aidhs_data folder, if it doesn't exist already. This folder is where you would like to store MRI data to run the classifier
4. Open the file`'config.ini` and replace the line:
```
data_path = /data
```
by 
```
data_path = <the path to where your aidhs_data_folder is stored>
```

### Create the environment

Run the commands below in your terminal to create the conda environment

``` bash
# enter the aid_hs directory
cd aidhs
# create the aidhs_env environment with all the dependencies 
conda env create -f environment.yml
# activate the environment
conda activate aidhs
# install aid_hs package with pip (with `-e`, the development mode, to allow changes in the code to be immediately visible in the installation)
pip install -e .
```

## Set up paths and download model

First, you will need to copy the AID_HS `aidhs_license.txt` into the aidhs folder (see above how to get the AID-HS license)

Before being able to use AID-HS on your data, some paths need to be set up and the pretrained model needs to be downloaded. For this, run:
```bash
python prepare_aidhs.py
```

This script will ask you if you want to change the path to the data folder, answer **'y'** for yes. \
Then, it will ask for the the location of your **AID-HS data folder**, where you would like to store MRI data to run the classifier. Create the **AID-HS data folder**, if it doesn't exist, and provide the path. It will download the pretrained model and test data to a folder inside your AID-HS data folder

## Verify installation
To verify that you have installed all packages, set up paths correctly, and downloaded all data, this verification script will run the pipeline to predict the HS side on a test patient which already has the hippocampal segmentation done. It takes approximately 1 minutes to run.

```bash
# enter the aid_hs directory
cd aidhs
# run the test
pytest
```

### Errors
If you run into errors at this stage and need help, you can re-run by changing the last line of the command by the command below to save the terminal outputs in a txt file. Please send `pytest_errors.log` to us so we can work with you to solve any problems. [How best to reach us.](#contact)

```bash
# run the test
pytest -s | tee 
```

You will find `pytest_errors.log` in the folder where you launched the command. 

## FAQs
Please see our [FAQs](https://aid-hs.readthedocs.io/en/latest/FAQs.html) for common installation problems.

## Contact

If have any question please contact `m.ripart@ucl.ac.uk` for support
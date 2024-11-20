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

## Installation & configuration
In order to run the pipeline, you'll need to configure a couple of files

1. Download `aidhs.zip` from the [latest github release](https://github.com/MELDProject/aidhs/releases/latest) and extract it.
2. Download the aidhs_data_folder at https://figshare.com/s/16011ee4d6b5723b14b6
3. Unzip the folder where you want to store the aidhs_data_folder
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
Please see our [FAQs](/docs/FAQ.md) for common installation problems.

## Contact

If have any question please contact `m.ripart@ucl.ac.uk` for support
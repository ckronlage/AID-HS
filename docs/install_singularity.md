# Singularity container

The Singularity container has been created to be used on HPC supporting Linux as they do not work with Docker container. If you are not working on a HPC, we recommend to install the docker version of container. 

Notes: 
- The Singularity image is built from the Docker container. 
- You will need **~20GB of space** to install the container
- The image contains Miniconda 3, HippUnfold v1.1.0, and AID-HS. The whole image is ~18GB. .  

Here is the video tutorial demonstrating how to do the singularity installation - [Docker and Singularity Installation of AID-HS Tutorial](https://www.youtube.com/watch?v=RRAET7r05ys&t=11s&ab_channel=MELDproject). Note that some part of the installation video are outdated for AID-HS > v1.1.0. Please follow the github guidelines for up to date instructions.

## Prerequisites

### Install Singularity
You will need to have Singularity installed. Most of the HPC will already have Singularity installed or Apptainer. You can check if Singularity/Apptainer is installed on your computer by running:
```bash
singularity --version
```
If this command displays the singularity or apptainer version already installed. If not, please follow the [guidelines](https://docs.sylabs.io/guides/3.0/user-guide/installation.html) to install singularity on your machine.

## Configuration
In order to run the singularity image, you'll need to build the singularity image from the aidhs docker image. This will create a singularity image called aidh.sif where you ran the command. 

Make sure you have 20GB of storage space available for the container

```bash
singularity build aidhs.sif docker://meldproject/aidhs:latest 
```

## AID-HS license
In order to run AID-HS you need to have a `aidhs_license.txt` in the aidhs folder. To get this file, please fill out the [AID-HS registration form](https://docs.google.com/forms/d/e/1FAIpQLSdPbtraBZ2s0HD1W8qtF11wr_fYVTWZjraED03Rtl2ZjxeRMA/viewform?usp=header). Once submitted, your application will be automatically reviewed and the aidhs_license.txt file will be send to your email.

## Installation & configuration

Before being able to use AID-HS on your data, data paths need to be set up and the pretrained model needs to be downloaded. 

1. Make sure you have 20GB of storage space available for the docker, and 1GB available for the aidhs data.
2. Create the **aidhs_data** folder, if it doesn't exist already. This folder is where where you would like to store MRI data to run the tool.
3. Run this command to set the paths needed:
-  <path_to_aidhs_data_folder> : Add the path to aidhs_data folder
-  <path_to_AIDHS_license>: path where the `aidhs_license.txt` has been saved

```bash
export SINGULARITY_BINDPATH=/<path_to_aidhs_data_folder>:/data,<path_to_AIDHS_license>/aidhs_license.txt:/aidhs_license.txt:ro
export SINGULARITYENV_AIDHS_LICENSE=/aidhs_license.txt
```
OR with Apptainer
```bash
export APPTAINER_BINDPATH=/<path_to_aidhs_data_folder>:/data,<path_to_AIDHS_license>/aidhs_license.txt:/aidhs_license.txt:ro
export APPTAINERENV_AIDHS_LICENSE=/aidhs_license.txt
```

:::{admonition} Singularity
:class: tip
You can add those paths to your `~/.bashrc` file to ensure they are always activated when opening a new terminal. 
:::
4. Run this command to download the data folder 
```bash
singularity exec aidhs.sif /bin/bash -c "cd /app && python scripts/new_patient_pipeline/prepare_aidhs.py "
```
It will download the data in the aidhs_data folder you set up in step 2. 

### Errors

If you have an issue "Not enough space when with creating the SIF" please look at the solution in our [FAQ](/docs/FAQ.md)

If you run into errors during the downloading of the AID-HS docker, contact us by email with information about the package you are trying to install, your OS system and a screenshot of the error you encountered. [How best to reach us.](#contact)

If the installation seems to have worked but you are running into errors during the test you can re-run the test above by changing the last line of the command by the command below to save the terminal outputs in a txt file. Please send `pytest_errors.log` to us so we can work with you to solve any problems. [How best to reach us.](#contact)

```bash
singularity exec aidhs.sif /bin/bash -c "cd /app && pytest -s | tee pytest_errors.log" 
```

You will find `pytest_errors.log` in the folder where you launched the command. 

## FAQs
Please see our [FAQ page](https://aid-hs.readthedocs.io/en/latest/FAQs.html) for common installation problems and questions

## Contact
If you encounter any errors, please contact `meld.stydy@gmail.com` for support

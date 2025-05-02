# Common errors

# FAQs

## **Issues & questions with installation**

### **Issue with Singularity - Not enough space when with creating the SIF**
```bash
INFO:    Creating SIF file... 
FATAL:   While performing build: while creating squashfs: create command failed: exit status 1:  
Write failed because No space left on device 
```
It means there is not enough space where the default singularity/apptainer cache and temporary directories are located. Usually the default cache is located in `$HOME/.singularity/cache` and the default temporary directory `$HOME/.tmp`\
Solution:
- You can make space in the default `$HOME` directory
- You can change the singularity/apptainer cache and temporary directories for a folder where there is space:
    ```bash
    export SINGULARITY_CACHEDIR=<path_folder_with_space> 
    export SINGULARITY_TMPDIR=<path_folder_with_space>
    ```
    Or with apptainer
    ```bash
    export APPTAINER_CACHEDIR=<path_folder_with_space> 
    export APPTAINER_TMPDIR=<path_folder_with_space>
    ```
---

## **Issues & questions with pipeline use**

### **Issue with HippUnfold - HippUnfold segmentation runs until step 37 of 193 steps (19%) and then is killed**

```bash
/bin/bash: line 1:   210 Killed                  nnUNet_predict -i tempimg -o templbl -t Task101_hcp1200_T1w -chk model_best --disable_tta &> logs/sub-0001/sub-0001_hemi-R_space-corobl_nnunet.txt
Shutting down, this might take some time.
Exiting because a job execution failed. Look above for error message

```

The error is likely due to a memory issue when HippUnfold is calling nnUNet to predict.\
If you are using Docker Desktop, it could be because the memory limit is set very low by default. 
To remedy, you will need to:
1) Increase the memory in the Docker Desktop settings (more help in this [post](https://forums.docker.com/t/how-to-increase-memory-size-that-is-available-for-a-docker-container/78483))
2) Delete the hippunfold subject folders below:
    - `output/hippunfold_outputs/hippunfold/<subjectID>`
    - `output/hippunfold_outputs/work/<subjectID>`
3) Run the AID-HS command again. 

### **Warning with Orphans containers**

```bash
WARN[0000] Found orphan containers ([aid-hs-101-aidhs-run-5818580c067f aid-hs-101-aidhs-run-bd51a3643bcb aid-hs-101-aidhs-run-e7a644059fdb aid-hs-101-aidhs-run-90b9a6b2d7e7 aid-hs-101-aidhs-run-109ef780e484 aid-hs-101-aidhs-run-483c2e531ac9 aid-hs-101-aidhs-run-acacca2b2930]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
```

This is just a warning and will not impact the use of the pipeline. But to clean up the orphans containers please use the command below: 
```bash
docker-compose down --remove-orphans
```

---

## **Updating AID-HS to V1.0.1**

The instructions below are for users that already have used AID-HS v1.0.0 on patients and would like to update to AID-HS v1.0.1 while keeping the same aidhs_data_folder folder.


### 📥 **Get the updated code**

Depending on wether you previously downloaded `V1.0.0` as a zip/tar folder or used Git to download the code, you will need to follow the same route to get the update `v1.0.1` code.

::::{tab-set}

:::{tab-item} Download
1. Go to the [github releases page](https://github.com/MELDProject/AID-HS/releases) and download the latest source zip or tar of version `V1.0.1`.
2. Extract the folder `AID-HS-1.0.1`
3. Copy the files below from your old `AID-HS-1.0.0` directory to your new `AID-HS-1.0.1` directory:
    - the `compose.yml`
    - the `config.ini`
:::

:::{tab-item} Git
1) Open a terminal in your `aidhs` folder
2) Pull the latest code from GitHub (it will pull the latest data while keeping your changes made to the code)
```bash
git stash
git pull 
git stash pop
```
:::
::::

Then depending on if you have a Native, Docker or Singularity installation of AID-HS `v1.0.0` you will need to follow the same type of installation to update to `v1.0.1`: 

::::{tab-set}

:::{tab-item} Native
:sync: Native
**💻 Native Installation Users:** Your will need to update your environment with the new code. 

1. Activate your conda environment
```
conda activate aidhs
```
2. Update the code package in the environment. Make sure you are in the new `AID-HS-1.0.1` directory and run:
```
pip install -e . 
```

:::

:::{tab-item} Docker
:sync: Docker

**🐳 Docker Users:** You will need to pull the latest docker image
```bash
docker pull meldproject/aidhs:latest
```

:::

:::{tab-item} Singularity
:sync: Singularity

**🚀 Singularity Users:** You will need to pull the latest image
```bash
singularity pull docker://meldproject/aidhs:latest
```
:::
::::

### ✔️ **Run pytest again**
Follow the guidelines **"Verify installation"** to run the test again.
- 💻[Native Installation Users](https://aid-hs.readthedocs.io/en/latest/install_native.html#verify-installation)
- 🐳[Docker Users](https://aid-hs.readthedocs.io/en/latest/install_docker.html#verify-installation)
- 🚀[Singularity Users](https://aid-hs.readthedocs.io/en/latest/install_singularity.html#verify-installation)

### 🧠 **Update your predictions with the registration fix**
If you want to update the predictions with the new registration for patients you have already ran through AID-HS, please follow the instructions bellow:

1) Create a list of ids of patients you want to rerun: e.g. `list_subjects_rerun_v1.0.1.txt`

2) Then run one of the commands below. It will recreate the PDF report for your patient. 

**WARNING** This will overwrite the files and the patient report in `output/predictions_reports`

::::{tab-set}

:::{tab-item} Native
:sync: Native

**💻 Native Installation Users:** 
```bash
python scripts/new_patient_pipeline/run_pipeline_prediction.py -ids list_subjects_rerun_v1.0.1.txt
```
:::

:::{tab-item} Docker
:sync: Docker

**🐳 Docker Users:** 
```bash
DOCKER_USER="$(id -u):$(id -g)" docker compose run aidhs python scripts/new_patient_pipeline/run_pipeline_prediction.py -ids list_subjects_rerun_v1.0.1.txt
```
:::

:::{tab-item} Singularity
:sync: Singularity

**🚀 Singularity Users:**
```bash
singularity exec aidhs.sif /bin/bash -c "cd /app && python scripts/new_patient_pipeline/run_pipeline_prediction.py -ids list_subjects_rerun_v1.0.1.txt"
```
:::
::::

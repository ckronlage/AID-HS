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

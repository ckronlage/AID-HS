# Docker container


**WARNING: Installation and use not yet tested on Windows. Please do let us know if you are succeeding / failing to use the docker container on Windows**

The Docker container has all the prerequisites embedded on it which makes it easier to install and compatible with most of the OS systems. 

Notes: 
- Currently only tested on **Linux** (HPC Singularity coming soon)
- You will need **~20GB of space** to install the container
- The docker image contains Miniconda 3, HippUnfold v1.1.0, and AID-HS. The whole image is ~18GB.  

## Prerequisites

### Install Docker
You will need to have docker installed. You can check if docker is installed on your computer by running:

```bash
docker --version
```

If this command displays the docker version then it is already installed. If not, please follow the [guidelines](https://docs.docker.com/engine/install/) to install docker on your machine.

## Enable GPUs

Enabling your computer's GPUs for running the pipeline accelerates the brain segmentation when using Fastsurfer and the predictions. Follow instructions for your operating system to install.

Install the [*nvidia container toolkit*](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

## Installation & configuration
In order to run the docker, you'll need to configure a couple of files

1. Download `aidhs.zip` from the [latest github release](https://github.com/MELDProject/aidhs/releases/latest) and extract it.
2. Download the aidhs_data_folder at https://figshare.com/s/16011ee4d6b5723b14b6
3. Unzip the folder where you want to store the aidhs_data_folder
4. Edit the compose.yml `volumes` line before the `:` to point to the aidhs_data_folder. For example, if you wanted the folder to be on a mounted drive in Linux it might be:
```
    volumes:
      - /mnt/datadrive/aidhs-data:/data
```

## Verify installation
To verify that you have installed all packages, set up paths correctly, and downloaded all data, this verification script will run the pipeline to predict the HS side on a test patient which already has the hippocampal segmentation done. It takes approximately 1 minutes to run.

```bash
DOCKER_USER="$(id -u):$(id -g)" docker compose run aidhs pytest
```

### Errors
If you run into errors at this stage and need help, you can re-run by changing the last line of the command by the command below to save the terminal outputs in a txt file. Please send `pytest_errors.log` to us so we can work with you to solve any problems. [How best to reach us.](#contact)

```bash
DOCKER_USER="$(id -u):$(id -g)" docker compose run aidhs pytest -s | tee pytest_errors.log
```

You will find `pytest_errors.log` in the folder where you launched the command. 

## Test GPU

You can test that the pipeline is working well with your GPU by changing `count` to `all` in the `compose.yml` file. The `deploy` section should look like this to enable gpus:

```
deploy:
  resources:
    reservations:
      devices:
        - capabilities: [gpu]
          count: all
```

To disable gpus, change it back to `0`.

## FAQs
Please see our [FAQs](/docs/FAQ.md) for common installation problems.

## Contact

If you encounter any errors, please contact `m.ripart@ucl.ac.uk` for support
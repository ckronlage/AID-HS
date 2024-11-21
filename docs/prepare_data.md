# Prepare the data

The pipeline relies on the MRI data to be organised in the BIDS format. 

If you are preparing the data for the harmonisation step, you will also need to prepare the demographic information. 

You will need to prepare your data following a specific architecture:
If not already done, please :
- 1. Download the <aidhs_data_folder> at https://figshare.com/s/16011ee4d6b5723b14b6
- 2. Unzip the folder where you want to store the <aidhs_data_folder?
- 3. Follow the guidelines below to prepare your MRI data and demographic information

#### MRI data

Note: AID-HS has been developped on 3D T1w scans acquired at 3T. We cannot guarantee robustness and accuracy of the results on 2D scans nor scans acquired at lower (1.5T) or higher (7T) magnetic strenghts.

## Prepare the MRI data in BIDS format (Mandatory)

The AID-HS pipeline relies on the BIDS format as input data. For more information about BIDS format, please refers to their [instructions](https://bids.neuroimaging.io/)

The main key ingredients are : 
- each subject has a folder following the structure : `<sub-subject_id>`
- (optional) in each subject folder you can have a session folder, e.g. `ses-preop`. 
- in each session folder / subject folder you will need to have a datatype folder called `anat` folder. 
- in the anat folder your T1 and FLAIR nifti images should follow the structure : `<sub-subject_id>_<modality_suffix>.nii.gz` or `<sub-subject_id>_ses-<session>_<modality_suffix>.nii.gz` if you have a session.

A simple example of the BIDS structure for patient sub-test001 is given below:\
![example](/docs/images/input_structure_bids_format.png)

Additionally, you will need to have two json files in the `input` folder:
- `bids_config.json` containing the key words for session, datatype and modality suffix \
    Example: 
    ```json
    {"T1": {"session": null, 
           "datatype": "anat",
           "suffix": "T1w"},
    "FLAIR": {"session": null, 
              "datatype": "anat",
              "suffix": "FLAIR"}}
    ```
If your dataset follows another BIDS structure than the one provided in the example, you will need to adapt the bids_config.json file with the appropriate key words. Please refer to the BIDS [instructions](https://bids.neuroimaging.io/) to adapt the file to your BIDS dataset.

- `dataset_description.json` containing a description of the dataset \
    Example:
    ```json
    {"Name": "Example dataset", 
    "BIDSVersion": "1.0.2"}
    ```

## Prepare the demographic information to run the harmonisation

To compute the harmonisation parameters, you will need to provide a couple of information about the subjects into a csv file. You can find an example of this file in the aidh_data_folder. 

- `ID` : subject ID (this should be the same ID than the one used to create the MRI folder)
- `Harmo code`: the harmonisation code associated with this subject scan (if you are running the harmonisation, it should be the same for all the subjects used for the harmonisation) 
- `Group`: 'patient' if the subject is a patient or 'control' if the subject is a control 
- `Age at preoperative`: The age of the subject at the time of the preoperative T1 scan (in years)
- `Sex`: "male" if male, "female" if female
- `Scanner`: the scanner strenght associated with the MRI data ('3T' for 3 Tesla or '15T' for 1.5 Tesla)

![example](/docs/images/example_demographic_csv.png)

Notes: 
- please ensure the column names are unchanged and completed with the appropriate values, otherwise the pipeline will fail.
- note that AID-HS has not been thoroughly evaluated for data from 1.5T scanners

WARNING: for harmonisation 
- please make sure you add the appropriate age and sex of the patients. Adding dummy information can lead to suboptimal harmonisation. 
- please ensure that there is non-zero variance in the age of your subjects. Similar age for all subjects will lead to harmonisation failure. If your patients have the same age, please add randomly +- 0.01 to all age to introduce variance.   

## Prepare the demographic information to predict on a new subject

AID-HS provide individualised results, which are adapted for the age and sex of the patients. Thus, you will need to fill the demographics_file.csv file with:

- `ID` : subject ID (this should be the same ID than the one used to create the MRI folder)
- `Harmo code`: the harmonisation code associated with this subject scan or "noHarmo" if you do not want to use the harmonisation
- `Group`: patient, as you want to predict all subjects will be considered as patients
- `Age at preoperative`: The age of the subject at the time of the preoperative T1 scan (in years)
- `Sex`: 1 if male, 0 if female
- `Scanner`: the scanner strenght associated with the MRI data ('3T' for 3 Tesla or '15T' for 1.5 Tesla)

Notes: 
- please ensure the column names are unchanged and completed with the appropriate values, otherwise the pipeline will fail.
- note that AID-HS has not been thoroughly evaluated for data from 1.5T scanners

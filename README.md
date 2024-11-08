# AID-HS

**Automated and Interpretable Detection of Hippocampal Sclerosis**

AID-HS extracts hippocampal volume- and surface-based features from T1w scans using [HippUnfold](https://hippunfold.readthedocs.io/en/latest/), to provide an in-depth characterisation of hippocampal abnormality and provide an automated detection and lateralisation of hippocampal sclerosis (HS). 
For more details please read our [preprint](https://www.medrxiv.org/content/10.1101/2023.10.13.23296991v1)

Note: 
- AID-HS has been developped on T1w scans acauired at 3T. It is not yet thoroughly evaluated on 1.5T and 7T data
- You will need demographic information (age at scan, sex) to run AID-HS on your patients. 

Pipeline overview:\
<img src="images/overview_pipeline.jpg " height="500" />

## Disclaimer

The AID-HS software is intended for research purposes only and has not been reviewed or approved by the Medicines and Healthcare products Regulatory Agency (MHRA), European Medicine Agency (EMA) or by any other agency. Any clinical application of the software is at the sole risk of the party engaged in such application. There is no warranty of any kind that the software will produce useful results in any way. Use of the software is at the recipient's own risk.

## Installation & Use of the AID-HS pipeline

### Installations available 
You can install and use the AID-HS pipeline with :
- [**docker container**](/docs/install_docker.md) (STILL IN PROGRESS) recommended for easy installation of the pipeline as all the prerequisite packages are already embeded into the container. Note: Dockers are not working on High Performance Computing (HCP) systems.
- **singularity container (COMING SOON)** enables to run a container on High Performance Computing (HCP) systems. 
- [**native installation**](/docs/install_native.md): Not supported 

### Running the pipeline 
Once installed you will be able to use the AID-HS pipeline on your data following the steps:
1. Prepare your data : [guidelines](/docs/prepare_data.md)
2. (OPTIONAL) Compute the harmonisation parameters : [guidelines](/docs/harmonisation.md)
3. Run the prediction pipeline: [guidelines](/docs/run_prediction_pipeline.md)
4. Interpret the results: [guidelines]()(COMING SOON)


**What is the harmonisation process ?**

Scanners can induce a bias in the MRI data. To use the full potential of the AID-HS tool, we recommend adjusting for these scanners differences by running a preliminary harmonisation step to compute the harmonisation parameters for that specific scanner. Note: this step needs to be run only once, and requires data from at least 20 subjects acquired on the same scanner and demographic information (e.g age and sex). See [harmonisation instructions](/docs/harmonisation.md) for more details. 

Note: The AID-HS pipeline can also be run without harmonisation with no drop in performances. However, the characterisation of the hippocampal features compared to the normative growth curves will not be interpretable.


## Manuscript
Please check out our [manuscript](IN PRESS) to learn more.

An overview of the notebooks that we used to create the figures can be found [here](figure_notebooks.md).

## Contacts

Mathilde Ripart, PhD student, UCL  \
`m.ripart@ucl.ac.uk` 









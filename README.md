# AID-HS

Automated and Interpretable Detection of Hippocampal Sclerosis

AID-HS extracts hippocampal volume- and surface-based features from T1w scans using [HippUnfold](https://hippunfold.readthedocs.io/en/latest/), to provide an in-depth characterisation of hippocampal abnormality and provide an automated detection and lateralisation of hippocampal sclerosis (HS). 
For more details please read our [preprint](https://www.medrxiv.org/content/10.1101/2023.10.13.23296991v1)

Note: 
- AID-HS only works on T1w scans at 3T
- You will need demographic information (age at scan, sex) to run AID-HS on your patients. 

Pipeline overview:\
<img src="images/overview_pipeline.jpg " height="500" />

## Disclaimer

The AID-HS software is intended for research purposes only and has not been reviewed or approved by the Medicines and Healthcare products Regulatory Agency (MHRA), European Medicine Agency (EMA) or by any other agency. Any clinical application of the software is at the sole risk of the party engaged in such application. There is no warranty of any kind that the software will produce useful results in any way. Use of the software is at the recipient's own risk.

## Installation & Use of the MELD FCD prediction pipeline

### Installations available 
You can install and use the AID-HS pipeline with :
- [**docker container**](/docs/install_docker.md) (STILL IN PROGRESS) recommended for easy installation of the pipeline as all the prerequisite packages are already embeded into the container. Note: Dockers are not working on High Performance Computing (HCP) systems.
- **singularity container (COMING SOON)** enables to run a container on High Performance Computing (HCP) systems. 
- [**native installation**](/docs/install_native.md): Not supported 

### Running the pipeline 
Once installed you will be able to use the AID-HS pipeline on your data following the steps:
1. Prepare your data : [guidelines]()
2. (OPTIONAL) Compute the harmonisation parameters : [guidelines]()
3. Run the prediction pipeline: [guidelines]()
4. Interpret the results: [guidelines]()


**What is the harmonisation process ?**

Scanners can induce a bias in the MRI data. To use the full potential of the AID-HS tool, we recommend adjusting for these scanners differences by running a preliminary harmonisation step to compute the harmonisation parameters for that specific scanner. Note: this step needs to be run only once, and requires data from at least 20 subjects acquired on the same scanner and demographic information (e.g age and sex). See [harmonisation instructions]() for more details. 

Note: The MELD pipeline can also be run without harmonisation, with a small drop in performance.

## Additional information
With the native installation of the MELD classifier you can reproduce the figures from our paper and train/evaluate your own models.
For more details, check out the guides linked below:
- [Notebooks to reproduce figures](https://meld-graph.readthedocs.io/en/latest/figure_notebooks.html)


## Manuscript
Please check out our [manuscript](TBC) to learn more.

An overview of the notebooks that we used to create the figures can be found [here](figure_notebooks.md).

## Contacts

Mathilde Ripart, PhD student, UCL  \
`m.ripart@ucl.ac.uk` 









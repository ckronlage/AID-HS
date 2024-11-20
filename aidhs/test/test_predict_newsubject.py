#### tests for scripts/new_patient_pipeline.py ####
# this test used the patient MELD_TEST_3T_FCD_0011
# it test  : 
# - the prediction on new subject 
# - the creation of the AID-HS pdf reports
# It checks outputs exists and compare the prediction with the expected one.

import subprocess
import os
import pytest
import numpy as np
import nibabel as nb
import pandas as pd
from aidhs.paths import DATA_PATH


def get_data_parameters():
    data_parameters = {
        "subject": "test001",
        "harmo code" :"noHarmo", 
        "expected_prediction_csv" : "predictions_expected.csv",
        "prediction_csv" : "predictions.csv",
    }
    return data_parameters


@pytest.mark.slow
def test_predict_newsubject():
    
    # initiate parameter
    data_parameters = get_data_parameters()
    subject = data_parameters['subject']
    # call script run_script_prediction.py
    print("calling")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.abspath(os.path.join(dir_path, "../../scripts/new_patient_pipeline/run_pipeline_prediction.py"))
    print(script_path)
    subprocess.run(
                [
                    "python",
                    script_path,
                    "-id",
                    data_parameters['subject'],
                    "-harmo_code",
                    data_parameters['harmo code'],
                    "--debug_mode",
                    
                ]
            )
    
    # check if the expected file exist
    path_prediction = os.path.join(DATA_PATH, 'output', 'predictions_reports', subject, data_parameters['prediction_csv'])
    assert os.path.isfile(path_prediction)
    
    # compare results prediction with expected one
    path_prediction_expected = os.path.join(DATA_PATH, 'output', 'predictions_reports', subject, data_parameters['expected_prediction_csv'])
    prediction = pd.read_csv(path_prediction)
    expected_prediction = pd.read_csv(path_prediction_expected)
    for key in ['score left HS', 'score no asymmetry', 'score right HS']:
        diff = np.round(prediction[key].values[0] - expected_prediction[key].values[0], 3)
        print(f'Test csv results: difference in {key} with expected value: {diff}')
        assert diff <= 0.01
    prediction_class = prediction['prediction'].values[0]
    prediction_class_expected = expected_prediction['prediction'].values[0]
    print(f'Test csv results: prediction is {prediction_class} and expected class is {prediction_class_expected}')
    assert prediction_class==prediction_class_expected

import os
import sys
import re
from pathlib import Path

def test_license():

    # Get the meld license variable
    aidhs_license_file = os.getenv("AIDHS_LICENSE", None)

    if aidhs_license_file is None: 
        print('ERROR: Could not find a AIDHS_LICENSE environment variable. Please ensure you have exported the AIDHS_LICENSE environment following the AID-HS installation guidelines')
        sys.exit()
    if not os.path.isfile(aidhs_license_file): 
        print(f'ERROR: The file {aidhs_license_file} does not exist.\nPlease ensure you got the meld license file by filling the registration form provided in the AID-HS installation guidelines and provided the right path to the file')
        sys.exit()

    # check that the license is correct
    text = Path(aidhs_license_file).read_text()
    m = re.search(r"License\s*ID[:\s]*([0-9]+)", text, re.IGNORECASE)
    if m:
        license_id = m.group(1)
        if not len(license_id) == 6:
            print("ERROR: The license ID provided does not seem correct.\nPlease ensure you got the correct meld license file by filling the registration form provided in the AID-HS installation guidelines and provided the right path to the file")
            sys.exit()
    else:
        print(f"ERROR: The license file {aidhs_license_file} does not seem correct.\nPlease ensure you got the correct meld license file by filling the registration form provided in the AID-HS installation guidelines and provided the right path to the file")
        sys.exit()

# call the test
test_license()  
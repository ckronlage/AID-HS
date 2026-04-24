import urllib.request
import os
import numpy as np
from aidhs.paths import DATA_PATH
import sys
import shutil
import tempfile

def _fetch_url(url, fname):
    def dlProgress(count, blockSize, totalSize):
        percent = int(count*blockSize*100/totalSize)
        if not "SILENT" in os.environ:
            sys.stdout.write("\r" + url + "...%d%%" % percent)
            sys.stdout.flush()
    return urllib.request.urlretrieve(url, fname, reporthook=dlProgress)


def download_aidhs_data(aidhs_data_path=DATA_PATH):
    """
    download AID-HS data from GitHub release: model, parameters and test data 
    """
    url = "https://github.com/MELDProject/AID-HS/releases/download/aidhs_data/aidhs_data.zip"
    with tempfile.TemporaryDirectory() as tmpdirname:
        # download to tmpdir
        _fetch_url(url, os.path.join(tmpdirname, "aidhs_data_folder.zip"))
        # unpack
        shutil.unpack_archive(os.path.join(tmpdirname, "aidhs_data_folder.zip"), aidhs_data_path)
    print(f"\ndownloaded AID-HS data to {aidhs_data_path}")

def check_data(force_download=False):
    for folder in ['input','output','models','params']:
        exit = False
        if os.path.exists(os.path.join(DATA_PATH, folder)):
            print(f'The folder {folder} already exists at {DATA_PATH}.')
            exit = True
    if force_download:
        print('Data to download already (partially) exists. \nData will be overwritten.') 
    if exit and (force_download==False):
        print('Data to download already (partially) exists. \nDownload aborted. Please delete folders or provide a new path.')
        sys.exit()
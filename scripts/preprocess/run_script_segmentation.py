import os
import shutil
from glob import glob
from os.path import join as opj
import subprocess
from subprocess import Popen, DEVNULL, STDOUT, check_call
from aidhs.tools_pipeline import get_m

def init(lock):
    global starting
    starting = lock

def check_FS_outputs(folder):
    fname = opj(folder,'stats',f'aparc.DKTatlas+aseg.deep.volume.stats')
    if not os.path.isfile(fname):
        return False
    else:
        return True

def run_hippunfold_parallel(subjects, bids_dir=None, hippo_dir=None, num_procs=10, delete_intermediate=False, verbose=False):
    # parallel version of Hippunfold

    #make a directory for the outputs
    os.makedirs(hippo_dir, exist_ok=True)

    subjects_to_run = []
    for subject in subjects:
        hippo_s = subject.hippo_dir
        subject_bids_id = subject.bids_id

        if subject_bids_id != None:
            subject_id = subject_bids_id
        else:
            subject_id = subject.convert_bids_id()

        #check if outputs already exists
        files_surf = glob(f'{hippo_s}/surf/*_den-0p5mm_label-hipp_*.surf.gii')

        if files_surf==[]:
            subjects_to_run.append(subject_id)
        else:
            print(get_m(f'Hippunfold outputs already exists. Hippunfold will be skipped', subject_id, 'INFO'))
    
    if subjects_to_run!=[]:
        print(get_m(f'Start Hippunfold segmentation in parallel for {subjects_to_run}', None, 'INFO'))
        subjects_to_run_shortformat = [subject_id.split('sub-')[-1] for subject_id in subjects_to_run]
        command =  format(f"hippunfold {bids_dir} {hippo_dir} participant --participant-label {' '.join(subjects_to_run_shortformat)} --core {num_procs} --modality T1w")
        if verbose:
            print(command)
        proc = Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr= proc.communicate()
        if verbose:
            print(stdout)
        if proc.returncode==0:
            print(get_m(f'Finished hippunfold segmentation for {subjects_to_run}', None, 'INFO'))
            if delete_intermediate:
                print(get_m(f'Delete intermediate files that takes lot of space: hippunfold_outputs/hippunfold/<subject_id>/warps and hippunfold_outputs/work folders', subjects_to_run, 'INFO'))
                for subject in subjects_to_run:
                    shutil.rmtree(os.path.join(hippo_dir, 'hippunfold', subject, 'warps'))
                    shutil.rmtree(os.path.join(hippo_dir, 'work'))
            return True
        else:
            print(get_m(f'Hippunfold segmentation failed for 1 of the subject. Please check the logs at {hippo_dir}/logs/<subject_id>', None, 'ERROR'))
            print(get_m(f'COMMAND failing : {command} with error {stderr}', None, 'ERROR'))
            return False

def run_hippunfold(subject, bids_dir=None, hippo_dir=None, delete_intermediate=False,verbose=False):

    hippo_s = subject.hippo_dir
    subject_bids_id = subject.bids_id

    if subject_bids_id != None:
        subject_id = subject_bids_id
    else:
        subject_id = subject.convert_bids_id()

    #make a directory for the outputs
    os.makedirs(hippo_dir, exist_ok=True)

    #check if outputs already exists
    files_surf = glob(f'{hippo_s}/surf/*_den-0p5mm_label-hipp_*.surf.gii')
    files_surf=[]
    if files_surf==[]:
        print(get_m(f'Start Hippunfold segmentation', subject_id, 'INFO'))
        command =  format(f"hippunfold {bids_dir} {hippo_dir} participant --participant-label {subject_id.split('sub-')[-1]} --core 3 --modality T1w")
        if verbose:
            print(command)
        proc = Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr= proc.communicate()
        if verbose:
            print(stdout)
        if proc.returncode==0:
            print(get_m(f'Finished hippunfold segmentation', subject_id, 'INFO'))
            if delete_intermediate:
                print(get_m(f'Delete intermediate files that takes lot of space: hippunfold_outputs/hippunfold/<subject_id>/warps and hippunfold_outputs/work folders', subject_id, 'INFO'))
                if os.path.exists(os.path.join(hippo_s, 'warps')):
                        shutil.rmtree(os.path.join(hippo_s, 'warps'))
                if os.path.isfile(os.path.join(hippo_dir, 'work', f'{subject_bids_id}_work.tar.gz')):
                    os.remove(os.path.join(hippo_dir, 'work', f'{subject_bids_id}_work.tar.gz'))
            return True
        else:
            print(get_m(f'Hippunfold segmentation failed. Please check the log at {hippo_dir}/logs/{subject_id}', subject_id, 'ERROR'))
            print(get_m(f'COMMAND failing : {command} with error {stderr}', subject_id, 'ERROR'))
            return False
    else:
        print(get_m(f'Hippunfold outputs already exists. Hippunfold will be skipped', subject_id, 'INFO'))
    

    

    

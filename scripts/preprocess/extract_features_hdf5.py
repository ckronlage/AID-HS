import nibabel as nb
import os, sys
import numpy as np
import h5py
import pandas as pd
import argparse

from aidhs.paths import DATA_PATH, BASE_PATH, DEMOGRAPHIC_FEATURES_FILE

def load_gii_shape(filename):
    """ import gii file using nibabel. returns flattened data array"""
    gii_file=nb.load(filename)
    mmap_data=gii_file.darrays[0].data
    array_data=np.ndarray.flatten(mmap_data)
    return array_data

def get_group_site(fs_id, csv_path):
        """
        Read demographic features from csv file and extract group, sex and scanner 
        """
        features_name=["Harmo code", "Group", "Scanner"]
        df = pd.read_csv(csv_path, header=0, encoding="latin")
        # get index column
        id_col = None
        for col in df.keys():
            if "ID" in col:
                id_col = col
        # ensure that found an index column
        if id_col is None:
            print("No ID column found in file, please check the csv file")
            return None
        df = df.set_index(id_col)
        # find desired demographic features
        features = []
        for desired_name in features_name:
            matched_name = None
            for col in df.keys():
                if desired_name in col:
                    if matched_name is not None:
                        # already found another matching col
                        print(
                            f"Multiple columns matching {desired_name} found ({matched_name}, {col}), please make search more specific"
                        )
                        return None
                    matched_name = col
            # ensure that found necessary data
            if matched_name is None:
                    print(f"Unable to find column matching {desired_name}, please double check for typos")
                    return None

            # read feature
            # if subject does not exists, add None
            if fs_id in df.index:
                feature = df.loc[fs_id][matched_name]
            else:
                print(f"Unable to find subject matching {fs_id}, please double check this subject exists in {csv_path}")
                return None
            features.append(feature)
        return features

def save_subject(subj_id, hemi, f_name, feature, base_path, demographic_file, hdf5_file_root='{}_{}_featurematrix.hdf5', label='label-hipp'):
    if label=='label-hipp':
        n_vert = 7262  
    elif label=='label-dentate':
        n_vert = 1788
    else:
        print('label unknowns')
        return
    #get subject info from id
    print(subj_id)
    print(demographic_file)
    site_code, c_p, scanner = get_group_site(subj_id, demographic_file)
    if scanner in ("15T" , "1.5T" , "15t" , "1.5t" ):
        scanner="15T"
    elif scanner in ("3T" , "3t" ):
        scanner="3T"
    else:
        print('scanner for subject '+ subj_id + ' cannot be identified as either 1.5T or 3T...')
        scanner='false'
    #skip subject if info not available
    if 'false' in (c_p, scanner, site_code):
        print("Skipping subject " + subj_id)
    os.makedirs(os.path.join(base_path,'AIDHS_'+site_code), exist_ok=True)        
    if os.path.isfile(os.path.join(base_path,'AIDHS_'+site_code,hdf5_file_root.format(site_code,c_p))):
        mode='r+'
    else :
        mode='a'
    f=h5py.File(os.path.join(base_path,'AIDHS_'+site_code,hdf5_file_root.format(site_code,c_p)),mode)
    name=f.require_group(os.path.join(site_code,scanner,c_p,subj_id,hemi))
    dset=name.require_dataset(f_name,shape=(n_vert,), dtype='float32',compression="gzip", compression_opts=9)
    dset[:]=feature
    f.close()
    return 

def get_demographic_features(subject_id, feature_names, base_path, csv_file='demographics.csv'):
    """
    Read demographic features from csv file. Features are given as (partial) column titles
    Args:
        subject_id: id of the subject
        feature_names: list of partial column titles of features that should be returned,
        csv_path: path to the csv file containing demographics information.
                can be raw participants file or qc-ed values.
                "{site_code}" is replaced with current site_code.
    Returns:
        list of features, matching structure of feature_names
    """
    csv_path= os.path.join(base_path, csv_file)
    return_single = False
    if isinstance(feature_names, str):
        return_single = True
        feature_names = [feature_names]
    df = pd.read_csv(csv_path, header=0, encoding="latin")
    # get index column
    id_col = None
    for col in df.keys():
        if "ID" in col:
            id_col = col
    # ensure that found an index column
    if id_col is None:
        self.log.warning("No ID column found in file, please check the csv file")
        return None
    df = df.set_index(id_col)
    # find desired demographic features
    features = []
    for desired_name in feature_names:
        matched_name = None
        for col in df.keys():
            if desired_name in col:
                if matched_name is not None:
                    # already found another matching col
                    self.log.warning(
                        f"Multiple columns matching {desired_name} found ({matched_name}, {col}), please make search more specific"
                    )
                    return None
                matched_name = col
        # ensure that found necessary data
        if matched_name is None:
            self.log.warning(f"Unable to find column matching {desired_name}, please double check for typos")
            return None
        # read feature
        # if subject does not exists, add None
        if subject_id in df.index:
            feature = df.loc[subject_id][matched_name]
        else:
            feature = None
        features.append(feature)
    if return_single:
        return features[0]
    return features


def get_feature_values(subj_id, hemi, f_name, base_path, hdf5_file_root='{}_{}_featurematrix.hdf5'):
    """Outputs the values of a particular feature from a participant for one hemisphere"""
    _,site_code,scanner,c_p,ID=subj_id.split('_')
    if c_p =='C':
        c_p ='control'
    else:
        c_p='patient'
    f=h5py.File(os.path.join(base_path,"AIDHS_"+site_code,hdf5_file_root.format(site_code,c_p)),'r')
    surf_dir=f[os.path.join(site_code,scanner,c_p,subj_id,hemi)]
    overlay = surf_dir[f_name][:]
    return overlay

def convert_bids_id(bids_id=None):
        #clean id
        list_exclude = ['{','}','_']
        for l in list_exclude:
            if l in bids_id:
                bids_id = bids_id.replace(l, '')
        #add 'sub' if needed  
        if not 'sub-' in bids_id:
            bids_id = 'sub-'+bids_id
        return bids_id
    
def extract_features_hdf5(list_ids=None, sub_id=None, data_dir=None, output_dir=None):
    subject_id=None
    subject_ids=None
    if list_ids != None:
        list_ids=os.path.join(DATA_PATH, list_ids)
        try:
            sub_list_df=pd.read_csv(list_ids)
            subject_ids=np.array(sub_list_df.ID.values)
            try: 
                subject_bids_ids=np.array(sub_list_df.bids_ID.values)
                print(subject_bids_ids)
            except:
                subject_bids_ids=np.full(len(subject_ids), None)
        except:
            subject_ids=np.array(np.loadtxt(list_ids, dtype='str', ndmin=1)) 
            subject_bids_ids=np.full(len(subject_ids), None)            
    elif sub_id != None:
        subject_id=sub_id
        subject_ids=np.array([sub_id])
        subject_bids_ids=np.full(len(subject_ids), None) 
    else:
        print('ERROR: No ids were provided')
        print("ERROR: Please specify subject(s) ...")
        sys.exit(-1) 
    
    #initialise
    hemis=['lh', 'rh']
    features =[ 'label-dentate.gyrification',
                'label-dentate.curvature',
                'label-hipp.thickness',
                'label-hipp.gyrification',
                'label-hipp.curvature',
                'label-hipp.gauss-curv_filtered_sm1']

    # load subjects
    for subject_id in subject_ids:
        # print(subject_id)
        bids_id = convert_bids_id(subject_id)
        subject_dir = os.path.join(data_dir, 'hippunfold', bids_id, 'surf_aidhs')
        print(subject_dir)
        print('INFO: Extract features for subject {}'.format(subject_id))
        for feature_name in features:
            for hemi in hemis:
                #load overlay
                overlay_file=os.path.join(subject_dir,f'{hemi}.{feature_name}.shape.gii')
                if os.path.isfile(overlay_file):
                    overlay = load_gii_shape(overlay_file)
                    #save in hdf5
                    label = feature_name.split('.')[0]
                    save_subject(subject_id, 
                                 hemi = hemi, 
                                 f_name='.'+feature_name, 
                                 feature = overlay, 
                                 base_path= output_dir, 
                                 demographic_file= DEMOGRAPHIC_FEATURES_FILE,
                                 hdf5_file_root='{}_{}_featurematrix.hdf5', 
                                label = label)
                else:
                    print(f'feature {hemi}.{feature_name} not available for subject {subject_id}')

if __name__ == "__main__":
    # parse commandline arguments
    parser = argparse.ArgumentParser(description="extract features in hdf5 file")
    parser.add_argument("-id","--id",
                        help="Subject ID.",
                        default=None,
                        required=False,
                        )
    parser.add_argument("-ids","--list_ids",
                        default=None,
                        help="File containing list of ids. Can be txt or csv with 'ID' column",
                        required=False,
                        )
    args = parser.parse_args()
    print(args)

    extract_features_hdf5(list_ids=args.list_ids, 
                            sub_id=args.id, 
                            data_dir=DATA_PATH, 
                            output_dir=BASE_PATH)


    
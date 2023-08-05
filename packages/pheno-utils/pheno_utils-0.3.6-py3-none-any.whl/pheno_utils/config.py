# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_config.ipynb.

# %% auto 0
__all__ = ['REF_COLOR', 'FEMALE_COLOR', 'MALE_COLOR', 'ALL_COLOR', 'GLUC_COLOR', 'FOOD_COLOR', 'DATASETS_PATH', 'COHORT',
           'EVENTS_DATASET', 'ERROR_ACTION', 'CONFIG_FILES', 'BULK_DATA_PATH', 'generate_synthetic_data',
           'generate_synthetic_data_like']

# %% ../nbs/00_config.ipynb 3
import os
import json
import numpy as np
import pandas as pd

# %% ../nbs/00_config.ipynb 4
REF_COLOR = "k"
FEMALE_COLOR = "C1"
MALE_COLOR = "C0"
ALL_COLOR = "C5"

GLUC_COLOR = "C0"
FOOD_COLOR = "C1"

DATASETS_PATH = '/home/ec2-user/studies/hpp/'
COHORT = None
EVENTS_DATASET = 'events'
ERROR_ACTION = 'raise'
CONFIG_FILES = ['.pheno/config.json', '~/.pheno/config.json', '/efs/.pheno/config.json']
BULK_DATA_PATH = {}


for cf in CONFIG_FILES:
    cf = os.path.expanduser(cf)
    if not os.path.isfile(cf):
        continue

    f = open(cf)
    config = json.load(f)
    
    if 'DATASETS_PATH' in config:
        DATASETS_PATH = config['DATASETS_PATH']
    if 'BULK_DATA_PATH' in config:
        BULK_DATA_PATH = config['BULK_DATA_PATH']
    if 'EVENTS_DATASET' in config:
        EVENTS_DATASET = config['EVENTS_DATASET']
    if 'COHORT' in config:
        if config['COHORT'] == 0 or config['COHORT']=='None' or config['COHORT']==None :
            COHORT = None
    if 'ERROR_ACTION' in config:
        ERROR_ACTION = config['ERROR_ACTION']
    break


# %% ../nbs/00_config.ipynb 5
def generate_synthetic_data(n: int = 1000) -> pd.DataFrame:
    """
    Generates a sample DataFrame containing age, gender, and value data.

    Args:
        n: The number of rows in the generated DataFrame.

    Returns:
        A pandas DataFrame with columns 'age', 'gender', and 'val'.
    """
    pids = np.arange(n)
    # Set start and end dates
    start_date = pd.Timestamp('2020-01-01')
    end_date = pd.Timestamp('now')
    dates = pd.to_datetime(pd.to_datetime(np.random.uniform(start_date.value, end_date.value, n).astype(np.int64)).date)  
    ages = np.random.uniform(35, 73, size=n)
    genders = np.random.choice([0, 1], size=n)
    vals = np.random.normal(30 + 1 * ages + 40 * genders, 20, size=n)
    
    data = pd.DataFrame(data={"participant_id":pids,"date_of_research_stage": dates,"age_at_research_stage": ages, "sex": genders, "val1": vals}).set_index("participant_id")
    data["val2"] = data["val1"]*0.3 + 0.5*np.random.normal(0,50) + 0.2*10*data["sex"]
    return data

# %% ../nbs/00_config.ipynb 6
def generate_synthetic_data_like(df: pd.DataFrame, n: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate a sample DataFrame containing the same columns as `df`, but with random data.

    Args:
    
        df: The DataFrame whose columns should be used.
        n: The number of rows in the generated DataFrame.

    Returns:
        A pandas DataFrame with the same columns as `df`.
    """
    np.random.seed(random_seed)
    pids = np.arange(n)
    if n > len(df):
        replace = True
    else:
        replace = False

    null = df.reset_index().apply(lambda x: x.sample(frac=1).values)\
        .sample(n=n, replace=replace).assign(participant_id=pids)\
        .set_index(df.index.names)

    def is_path_string(x):
        return isinstance(x, str) and (x.count('/') > 1)

    # handle specific columns
    null.loc[:, null.applymap(is_path_string).mean() > 0.5] = '/path/to/file'
    if ('collection_timestamp' in null.columns) and ('collection_date' in null.columns):
        null['collection_date'] = null['collection_timestamp'].dt.date

    return null

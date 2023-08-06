# Last update: -08-2021

import os
import _pickle as pickle
import gc
import pandas as pd
from .my_easy_logger import my_logger, logger_cleaner
from .config_template import NN
from .pickle_fldr_2_feather_fldr import get_df_dtypes

script_name = os.path.split(__file__)[1][:-3]


# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
@logger_cleaner
def sample_save_fldrs(_src_fldr, _dst_fldr, sample_number, *args, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'
    logger_.setLevel('DEBUG')

    source_files = os.listdir(_src_fldr)
    for file in source_files:
        src_file_addr = os.path.join(_src_fldr, file)
        # only the pickle files
        # if file.split('.')[-1] != 'pickle' or 'unsw' not in file.lower():
        #     logger.info(f'file {file} ignored')
        #     continue
        gc.disable()
        if 'file_type' in kwargs:
            file_type_ = kwargs['file_type']
        else:
            file_type_ = 'pickle'

        logger_.info(f'Reading {src_file_addr} of filetype: {file_type_} ...')
        if file_type_ == 'pickle':
            with open(src_file_addr, 'rb') as f:
                df = pickle.load(f)
        else:
            df = pd.read_feather(src_file_addr)
            dt_map = get_df_dtypes(df, full_resolution_float=True)
            df = df.astype(dt_map)

        logger_.info(f"File {file} has: {df.shape[0]} rows")
        if 'without_attack' not in args:
            logger_.debug(f"File {file} attack types: {df['Attack'].unique()}")
            logger_.debug(f"\n{df['Attack'].value_counts(normalize=False)}")
            logger_.debug(f"\n{df['Attack'].value_counts(normalize=True)}")

        logger_.info("Removing NaN values from df")
        df = df[~df.isna().any(1)]
        sample_frac = sample_number / df.shape[0]

        if 'without_attack' in args:
            logger_.info(f"Sampling the df with frac: {sample_frac:.4f}")
            try:
                df = df.sample(frac=sample_frac, random_state=NN.seeds)
            except ValueError:
                logger_.info(f"{file} is not sampled because it has less row than {sample_number}")
        else:
            try:
                logger_.info(f"Stratified sampling the df with frac: {sample_frac:.4f}")
                logger_.debug(f"Number of classes before sampling:\n {df['Attack'].value_counts()}")
                df = df.groupby(by='Attack').sample(frac=sample_frac, random_state=NN.seeds)
                logger_.debug(f"Number of classes after sampling:\n {df['Attack'].value_counts()}")
            except ValueError:
                logger_.info(f"{file} is not sampled because it has less row than {sample_number}")

        df.reset_index(drop=True, inplace=True)
        if 'N' in kwargs:
            N_ = kwargs['N']
        else:
            N_ = 1

        if 'without_attack' not in args:
            dst_file_addr = os.path.join(_dst_fldr, file[:-7] + f'-{N_}m.{file_type_}')
        else:
            dst_file_addr = os.path.join(_dst_fldr, file + f'-{N_}m.{file_type_}')

        if file_type_ == 'pickle':
            with open(dst_file_addr, 'wb') as f:
                pickle.dump(df, f, protocol=-1)
        else:
            df.to_feather(dst_file_addr)

        logger_.info(f'{dst_file_addr} is done')
        logger_.info('\n' + '*--' * 30 + '\n\n\n\n')

    logger_.info('All files are done')



# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
if __name__ == '__main__':
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold,black',
        reporter_func_name=__name__,
        log_level='debug',
    )


    N = 1
    samp_num = 1_000_000 * N
    # extensions = [['', '_3class'][0]]
    file_type_dict = {
        'pickle': 2,
    }
    # for ext in extensions:
    for file_type, number in file_type_dict.items():
        for num in range(1, number):
            # src_fldr = f'/storage/datasets/{file_type}/{num}pickle{ext}'
            src_fldr = r'D:\Python_Project\siamak\datasets\NetFlow\1pickle'
            # src_fldr = f'/storage/datasets/Comscentre2017/{file_type}'
            dst_fldr = f'{src_fldr}-1m_/'
            os.makedirs(dst_fldr, exist_ok=True)
            # if num == 1 and ext == '':
            #     continue
            logger.info(f'\nsrc_fldr:{src_fldr}\ndst_fldr:{dst_fldr}')
            sample_save_fldrs(src_fldr, dst_fldr, samp_num, N=N, file_type=file_type)

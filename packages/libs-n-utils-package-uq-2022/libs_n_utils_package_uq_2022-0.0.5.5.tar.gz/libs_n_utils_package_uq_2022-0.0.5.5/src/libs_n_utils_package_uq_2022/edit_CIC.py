import _pickle as pickle
import datetime

import pandas as pd
import numpy as np
from config_template import FlowMeter
import gc
import os

from lib_pandas_extensions import rapid_csv_read
from my_easy_logger import my_logger

cols = FlowMeter.columns
cols.remove('Attack')
script_name = os.path.split(__file__)[1][:-3]
ds_names = ['BoT_IoT', 'IDS_2018', 'ToN_IoT']
ds_names = ['ToN_IoT']

if __name__ == '__main__':
    log_file = f'../../outputs/logs/{script_name[:-3]}-' \
               f'{datetime.datetime.now().strftime("%h_%m_%s")}.log'
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold_red,bg_green',
        reporter_func_name=__name__,
        log_file_address=log_file,
        log_level='debug'
    )

    for ds_name in ds_names:
        srcfile_addr = f'/storage/datasets/FlowMeter/originals/CIC_{ds_name}.csv'
        csv_dstfile_addr = f'/storage/datasets/FlowMeter/csv/FWM_{ds_name}.csv'
        pickle_dstfile_addr = f'/storage/datasets/FlowMeter/1pickle/FWM_{ds_name}.pickle'
        logger.info(f'reading file {srcfile_addr}')
        # with open(srcfile_addr, 'rb') as f:
        #       gc.disable()
        #       df = pickle.load(f)
        gc.disable()
        df = rapid_csv_read(srcfile_addr,
                            sep=',',
                            sample_rows=100_000,
                            blank_is_na=True,
                            contains_na=True,
                            verbose=False,
                            full_resolution_float=True
                            )
        # df = df.sample(frac=0.0001)
        logger.info(f"File {srcfile_addr} is read now")
        # becuase the original split csv files from CIC_IDS_2018 have 80 and 84 columns, combined file includes rw_ls lot of NaNs
        # so we remove those 4 different columns before looking for NaNs
        drop_list = ['Dst IP', 'Src Port', 'Src IP', 'Flow ID', 'Dst Port']
        logger.info(f'Number of columns before dropping columns: {df.shape[1]}')
        df.drop(columns=drop_list, errors='ignore', inplace=True)
        logger.info(f'Number of columns AFTER dropping columns: {df.shape[1]}')
        rows_0 = df.shape[0]
        logger.info(f'Row0 = {rows_0}')
        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
        rows_1 = df.shape[0]
        logger.info(f'Row1 = {rows_1}')
        logger.info(f'Rows dropped: {rows_0 - rows_1} '
                    f'rows, i.e. {100 * (rows_0 - rows_1) / rows_0:.2f}%')

        # the original CIC does not have rw_ls label field it only has attack field
        if ds_name == 'IDS_2018':
            df.rename(columns={'Label': 'Attack'}, inplace=True)
            df['Label'] = '1'
            df.loc[df['Attack'].str.contains("Benign"), 'Label'] = '0'

        logger.info(f'df.columns:\n {df.columns}')
        logger.info(f'df.loc[1,:]:\n {df.loc[1, :]}')
        logger.info(f'Writing Dataframe to {csv_dstfile_addr} ...')
        df.to_csv(csv_dstfile_addr, index=False)
        logger.info(f'{csv_dstfile_addr}: is written')

        with open(pickle_dstfile_addr, 'wb') as f:
            pickle.dump(df, f, protocol=-1)
            logger.info(f'{pickle_dstfile_addr} is written' + 50*'***' + '\n\n\n')
        gc.enable()

    logger.info('done !')

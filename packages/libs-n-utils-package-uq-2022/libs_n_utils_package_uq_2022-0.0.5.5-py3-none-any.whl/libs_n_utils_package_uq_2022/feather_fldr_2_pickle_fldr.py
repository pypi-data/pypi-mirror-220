import os
import gc
import pandas as pd
import _pickle as pickle
from .my_easy_logger import my_logger
from .pickle_fldr_2_feather_fldr import get_df_dtypes

filename = os.path.split(__file__)[1]



if __name__ == '__main__':

    base_fldr = '/storage/Documents/AQIRF/project/IDS_EXPLORE_PAPER/datasets/Comscentre2017'
    feather_fldr = f'{base_fldr}/feather/'
    pickle_fldr = f'{base_fldr}/pickle/'

    logger = my_logger(
        reporter_file_name=filename,
        reporter_func_name=__name__,
        info_c='fg_bold_blue'
    )

    feather_list = os.listdir(feather_fldr)

    for fthr in feather_list:
        feather_address = os.path.join(feather_fldr, fthr)
        logger.info(f'Reading file {feather_address} ...')
        pickle_address = os.path.join(pickle_fldr, f'{fthr}.pickle')

        gc.disable()
        df = pd.read_feather(feather_address)
        dt_map = get_df_dtypes(df, full_resolution_float=True)
        df = df.astype(dt_map)
        with open(pickle_address, 'wb') as f:
            logger.info(f'Writing to file {pickle_address}')
            pickle.dump(df, f, protocol=-1)
        gc.enable()
        logger.info(f'file {fthr} is now written to pickle in {pickle_address}')

    logger.info(f'All files in {feather_fldr} are converted to pickle now, done!')

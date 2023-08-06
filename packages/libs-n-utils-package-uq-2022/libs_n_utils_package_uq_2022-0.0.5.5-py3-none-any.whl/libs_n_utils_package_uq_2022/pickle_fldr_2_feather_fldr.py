import os
import gc
from typing import Dict, Any

import pandas as pd
import numpy as np
from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]


def get_df_dtypes(df, full_resolution_float: bool = False):
    dtype_map: Dict[Any, str] = {}
    for col in df.columns:
        v = df[col]
        if str(df[col].dtype) == "float64":
            dtype_map[col] = "float64" if full_resolution_float else "float32"
        elif str(df[col].dtype) == "object":
            dtype_map[col] = "str"
            """
            Safe assumption that all objects can be represented as strings, we can convert this to categorical
            later for extra saving
            """
        elif str(df[col].dtype) == "int64":
            max_val = np.max(v)
            dtype_map[col] = "int32" if max_val < 1_000_000 else "int64"
            """
            We use 1,000,000 here as rw_ls heuristic,if all of them are <1M, then this is probably safe for int32, but
            say we have some values in 2M, this will mean there are likely also values >2M eg 3M in the rest of the 
            dataset which is out of range for int32.

            The int16 conversion is not worth it and takes longer.
            """
        else:
            dtype_map[col] = str(df[col].dtype)
            """
            Don't change the datatype otherwise (dates for example)
            """

    return dtype_map


if __name__ == '__main__':

    pickle_folder = '/storage/datasets/FlowMeter/1pickle/'
    feather_folder = '/storage/datasets/FlowMeter/feather/'

    logger = my_logger(
        reporter_file_name=filename,
        reporter_func_name=__name__,
        info_c='fg_bold_blue'
    )

    pickle_list = os.listdir(pickle_folder)

    for pic in pickle_list:
        pickle_address = os.path.join(pickle_folder, pic)
        logger.info(f'Reading file {pickle_address} ...')
        feather_address = os.path.join(feather_folder, pic[:-7] + '.feather')
        logger.info(f'Writing to file Reading file {feather_address}')

        gc.disable()
        df = pd.read_pickle(pickle_address)
        dt_map = get_df_dtypes(df, full_resolution_float=True)
        df = df.astype(dt_map)
        df.to_feather(feather_address)
        gc.enable()
        logger.info(f'file {pic} is written to feather in {feather_address}')

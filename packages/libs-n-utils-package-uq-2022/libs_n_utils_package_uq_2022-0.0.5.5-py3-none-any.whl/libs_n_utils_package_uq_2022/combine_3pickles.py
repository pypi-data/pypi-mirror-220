import inspect
import os
import pandas as pd
import pickle
import gc
import itertools
from datetime import datetime
from functools import lru_cache
from .my_easy_logger import my_logger, logger_cleaner

scriptname = os.path.split(__file__)[1]


# ~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X
@logger_cleaner
@lru_cache()
def combine_3pickle(pickle_file1, pickle_file2, pickle_file3, **kwargs):
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_cyan,bold'

    logger_.setLevel('DEBUG')


    logger_.info('Reading the df1')
    with open(pickle_file1, 'rb') as f1:
        gc.disable()
        df1 = pickle.load(f1)
    logger_.info('Reading the df2')
    with open(pickle_file2, 'rb') as f2:
        df2 = pickle.load(f2)
    logger_.info('Reading the df3')
    with open(pickle_file3, 'rb') as f3:
        df3 = pickle.load(f3)
        gc.enable()
    df_list = [df1, df2, df3]
    logger_.info('Combining the 3 dfs')
    dfs = pd.concat(df_list)
    logger_.info('shuffling the combined dfs')
    dfs = dfs.sample(frac=1).reset_index(drop=True)

    return dfs



# ~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X
@logger_cleaner
def combine_3p_boiler(_src_fldr, _dst_fldr, **kwargs):
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_cyan,bold'

    logger_.setLevel('DEBUG')

    file_list = os.listdir(_src_fldr)
    file_list = [x for x in file_list if x.split('.')[-1] == 'pickle']
    file_list.sort()
    file_combinations = itertools.combinations(file_list, 3)
    for combination in file_combinations:
        f0 = combination[0]
        f1 = combination[1]
        f2 = combination[2]
        logger_.info(f'df1={f0},  df2={f1}, df3={f2}')
        file0 = os.path.join(_src_fldr, f0)
        file1 = os.path.join(_src_fldr, f1)
        file2 = os.path.join(_src_fldr, f2)

        df_combined = combine_3pickle(file0, file1, file2)
        # combined_name = f'{f0[:-7]}-{f1[5:-7]}-{f2[5:]}'   # without -1m
        combined_name = f'{f0[:-10]}-{f1[5:-10]}-{f2[5:]}'
        pickle_address = os.path.join(_dst_fldr, combined_name)
        logger_.info('Writing the combined dfs into the pickle file')
        gc.disable()
        df_combined.to_pickle(pickle_address)
        gc.enable()
        logger_.info(f'The combine file {combined_name} is written to {pickle_address}.')




# ~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X~~~X
if __name__ == '__main__':
    src_fldr = f'/storage/datasets/NetFlow/1pickle-1m/'
    dst_fldr = f'/storage/datasets/NetFlow/3pickle-1m/'
    log_file_addr = os.path.join(dst_fldr, scriptname[:-3]
                                 + f'_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log')
    logger = my_logger(reporter_file_name=scriptname,
                       reporter_func_name=__name__,
                       log_file_address=log_file_addr,
                       info_c='blue,bg_yellow')
    combine_3p_boiler(src_fldr, dst_fldr, logger=logger)









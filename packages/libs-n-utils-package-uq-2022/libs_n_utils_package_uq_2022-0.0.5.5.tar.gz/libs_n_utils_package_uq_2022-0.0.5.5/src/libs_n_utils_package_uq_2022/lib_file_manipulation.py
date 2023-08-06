import datetime
import inspect
import os
import re
import time
import feather
import _pickle as pickle
import gc
import pandas as pd

from .lib_pandas_extensions import rapid_csv_read
from .my_easy_logger import my_logger, logger_cleaner

filename = os.path.split(__file__)[1]
info_log_color = 'fg_bold_black,bg_white'


# ######################################################################################################################
@logger_cleaner
def rename_folder_files(folder_address, match_pattern=None, **kwargs):
    os.chdir(folder_address)
    logger_ = kwargs['logger']
    file_list = os.listdir(folder_address)
    for old_name in file_list:
        if match_pattern is not None:
            new_name = re.search(match_pattern, old_name)[1]
        elif 'add_to_old' in kwargs:
            new_name = old_name+kwargs['add_to_old']
        else:
            new_name = old_name
        os.rename(old_name, new_name)
    logger_.info(f'renaming folder {folder_address} is done.')




# ######################################################################################################################
@logger_cleaner
def create_ReadMe(folder=None, filename_=None, **kwargs):
    if filename_ is None:
        filename_ = filename
    logger_ = kwargs['logger']
    # logger_ = my_logger(reporter_file_name=filename,
    #                     reporter_func_name='create_ReadMe',
    #                     info_c=info_log_color)

    if folder is None:
        folder = os.getcwd()

    with open(folder+'/ReadMe.txt', 'w') as f:
        f.write('Author: Siamak Layeghy\n')
        f.write(f'Date, Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write('Generator Code:\n' + f'{filename_}\n')

    logger_.info(f'ReadMe.txt file is created in {folder}\n for {filename_}')




# ######################################################################################################################
@logger_cleaner
def read_CSVs_concat_write_feather(source=None, destination=None, selected_cols=None, **kwargs):
    logger_ = kwargs['logger']

    csv_list = os.listdir(source)
    csv_list.sort(key=int)
    logger_.info(f'entering folder {source} ...')
    os.chdir(source)
    logger_.info('Reading CSVs to list of DataFrames ...')
    t0 = time.perf_counter()
    if selected_cols is not None:
        csv_dfs = (pd.read_csv(csv, usecols= selected_cols) for csv in csv_list)
    else:
        csv_dfs = (pd.read_csv(csv) for csv in csv_list)
    t1 = time.perf_counter()
    logger_.info(f'reading CSVs to list of DFs took {t1 - t0:.2f} sec')

    logger_.info('writing to total DataFrame ...')
    t0 = time.perf_counter()
    total_df = pd.concat(csv_dfs)
    t1 = time.perf_counter()
    logger_.info(f'Concatenating  DFs to rw_ls single DataFrame took {t1 - t0:.2f} sec')
    del csv_dfs, csv_list

    logger_.info('Writing to feather file ...')
    t0 = time.perf_counter()
    feather_filename = source.split('/')[-1]
    feather_file_address = destination + '/' + feather_filename
    feather.write_dataframe(total_df, feather_file_address)
    t1 = time.perf_counter()
    logger_.info(f'Writing {feather_filename} to feather format took {t1 - t0:.2f} sec')




# ######################################################################################################################
@logger_cleaner
def combine_CSVs_write_csv_feather(base_folder_, dest_folder_, combined_name_, change_l7_name=False,
                                   write_feather_=False, int_sort=True, delimiter_=',', fields=None, **kwargs):

    os.makedirs(dest_folder_, exist_ok=True)
    logger_ = kwargs['logger']

    file_list = os.listdir(base_folder_)
    file_list = [f for f in file_list if
                 os.path.isfile(os.path.join(base_folder_, f))]
    if int_sort:
        if len(file_list) > 1:
            file_list.sort(key=lambda x: int(re.findall('\d+', x)[0]))

    create_ReadMe(os.path.dirname(dest_folder_), filename_=__file__)

    df_combined = pd.DataFrame()
    for file_name in file_list:
        logger_.info(f'{file_name} is being processed ...')
        file_address = os.path.join(base_folder_, file_name)
        logger_.info(f'Reading {file_name}')
        if fields is not None:
            df = pd.read_csv(file_address, usecols=fields, delimiter=delimiter_)
            df = feather.read_dataframe(df)
        else:
            df = pd.read_csv(file_address, delimiter=delimiter_)
            df = feather.read_dataframe(df)

        logger_.info(f'New DataFrame has {df.shape[0]} '
                    f'rows and {df.shape[1]} columns.')
        logger_.info(f'combining ...')
        df_combined = pd.concat([df_combined, df], axis=0)
        logger_.info(f'Combined DataFrame has {df_combined.shape[0]} '
                    f'rows and {df_combined.shape[1]} columns now.')

    df_combined.to_csv(os.path.join(dest_folder_, combined_name_ + '.csv'))
    if change_l7_name is True:
        col = 'L7_PROTO_NAME'
        df_combined[col] = df_combined[col].str.split(".").apply(lambda x: x[0])

    logger_.info(f'{os.path.join(dest_folder_, combined_name_)}: finished')
    if write_feather_:
        df_combined = df_combined.reset_index(drop=True)
        feather_folder = dest_folder_[:-3] + 'feather'
        os.makedirs(feather_folder, exist_ok=True)
        df_combined.to_feather(os.path.join(feather_folder, combined_name_))
        logger_.info(f'The feather file '
                    f'{os.path.join(feather_folder, combined_name_)}'
                    f': finished')





# ######################################################################################################################
@logger_cleaner
def swap_csv_cols(in_csv_, out_csv_, src_col_, dst_col_, **kwargs):
    logger_ = kwargs['logger']

    with open(in_csv_, 'r') as in_file:
        with open(out_csv_, 'w') as out_file:
            for line in in_file:
                line = line.strip('\n').split(',')
                line[src_col_], line[dst_col_] = line[dst_col_], line[src_col_]
                out_file.write(','.join(line)+'\n')

    logger_.info(f'{in_csv_} columns are swapped and is written to {out_csv_} ')




# ######################################################################################################################
@logger_cleaner
def modify_CSVs_write_csv_feather(source_folder_, columns_list, dest_folder_=None,
                                  file_type='csv', write_feather_=False, write_csv_=False,
                                  csv_delimiter_=',', **kwargs):

    if dest_folder_ is None:
        dest_folder_ = source_folder_
    else:
        os.makedirs(dest_folder_, exist_ok=True)

    logger_ = kwargs['logger']

    file_list = os.listdir(source_folder_)
    file_list = [f for f in file_list if
                 os.path.isfile(os.path.join(source_folder_, f))]

    for file_name in file_list:
        logger_.info(f'{file_name} is being processed ...')
        file_address = os.path.join(source_folder_, file_name)

        logger_.info(f'Reading {file_name}')
        if file_type == 'csv':
            df = pd.read_csv(file_address, delimiter=csv_delimiter_)
        else:
            df = feather.read_dataframe(file_address)

        for col in columns_list:
            df[col] = df[col].str.split(".").apply(lambda x: x[0])

        if write_csv_ is True:
            df.to_csv(file_address, sep=csv_delimiter_, index=False)

        if write_feather_ is True:
            feather_address = os.path.join(dest_folder_, file_name)
            df.to_feather(feather_address)
            logger_.info(f'The feather file {feather_address}: finished')




################################################################################
@logger_cleaner
def csvfile_2_featherfile(csv_address, feather_address, cols=None, extra_injected_cols=None,
                          sample_rows: int = 10_000, verbose: bool = True, max_rows=None,
                          skip_rows=0, full_resolution_float: bool = False, contains_na: bool = True,
                          blank_is_na: bool = False, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_bold_blue'

    logger_.info(f'Reading file {csv_address}')
    df = rapid_csv_read(csv_address, usecols=cols, sample_rows=sample_rows, verbose=verbose,
                        max_rows=max_rows, skip_rows=skip_rows, full_resolution_float=full_resolution_float,
                        contains_na=contains_na, blank_is_na=blank_is_na)

    logger_.info(f'Columns: {df.columns}')
    if extra_injected_cols is not None:
        df.drop(extra_injected_cols, axis=1, inplace=True)

    logger_.info(f'Columns after removing: {df.columns}')
    if 'index' in df.columns:
        df.drop(['index'], inplace=True, axis=1)
        df.reset_index(inplace=True)

    logger_.info(f'Writing to file {feather_address}')
    # disable garbage collector
    gc.disable()
    df.to_feather(feather_address)
    # enable garbage collector again
    gc.enable()
    logger_.info(f'Feather file written to {feather_address}')





################################################################################
@logger_cleaner
def csvfile_2_picklefile(csv_address, pickle_address, sample_rows: int = 10_000, verbose: bool = True, max_rows=None,
                         skip_rows=0, full_resolution_float: bool = False, contains_na: bool = True,
                         blank_is_na: bool = False, cols=None, extra_injected_cols=None, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_bold_blue'

    logger_.info(f'Reading file {csv_address}')
    df = rapid_csv_read(csv_address, usecols=cols, sample_rows=sample_rows, verbose=verbose,
                        max_rows=max_rows, skip_rows=skip_rows, full_resolution_float=full_resolution_float,
                        contains_na=contains_na, blank_is_na=blank_is_na)

    logger_.info(f'Columns: {df.columns}')
    if extra_injected_cols is not None:
        df.drop(extra_injected_cols, axis=1, inplace=True)

    logger_.info(f'Columns after removing: {df.columns}')
    if 'index' in df.columns:
        df.drop(['index'], inplace=True, axis=1)
        df.reset_index(inplace=True)


    logger_.info(f'Writing to file {pickle_address}')
    with open(pickle_address, 'wb') as f:
        # disable garbage collector
        gc.disable()
        pickle.dump(df, f, protocol=-1)
        # enable garbage collector again
        gc.enable()

    logger_.info(f'Pickle file written to {pickle_address}')

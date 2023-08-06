import os
import pandas as pd
import gc
import _pickle as pickle
import datetime

from .my_easy_logger import my_logger
from .lib_pandas_extensions import rapid_csv_read

filename = os.path.split(__file__)[1]



if __name__ == '__main__':
    log_file = f'../../outputs/logs/{filename[:-3]}-' \
               f'{datetime.datetime.now().strftime("%h_%m_%s")}.log'
    logger = my_logger(reporter_file_name=filename,
                       reporter_func_name=__name__,
                       info_c='yellow,bg_black',
                       log_file_address=log_file)

    drop_list = ['Dst IP', 'Src Port', 'Src IP', 'Flow ID', 'Dst Port']
    combined_name = 'CIC_IDS_2018'
    sort_folder = False
    file_ext = 'csv'
    # df_type = 'feather'
    df_type = 'pickle'
    # base_folder = '/storage/datasets/FlowMeter/09_03_2021/'
    # split_csv_direct is directly downloaded from AWS
    base_folder = '/storage/datasets/FlowMeter/split_csv/'
    # source_folder = os.path.join(base_folder, 'CSV')
    csv_dest_folder = '/storage/datasets/FlowMeter/csv'

    # feather_dest_folder = '/storage/datasets/FlowMeter/feather/'
    pickle_dest_folder = '/storage/datasets/FlowMeter/1pickle/'

    write_feather = False
    write_csv = True
    write_pickle = True

    file_list = os.listdir(base_folder)
    file_list = [f for f in file_list if
                 os.path.isfile(os.path.join(base_folder, f))]
    if len(file_list) > 1 and sort_folder:
        file_list.sort(key=lambda x: int(x[:-4]))
    # create_ReadMe(os.path.dirname(feather_dest_folder), filename_=__file__)

    selected_cols = None
    N = 84
    # n_columns = [i for i in range(n_top) if i not in [0, 1, 3, 6, 83]]
    df_combined = pd.DataFrame()
    for file_name in file_list:
        csv_address = os.path.join(base_folder, file_name)
        logger.info(f'Reading {file_name}')
        # if selected_cols is not None:
        #     df = pd.read_csv(file_address, columns=selected_cols, dtype='str')
        # else:
        #     df = pd.read_csv(file_address, dtype='str')
        df = rapid_csv_read(csv_address,
                            sep=',',
                            sample_rows=1_000_000,
                            blank_is_na=True,
                            contains_na=True,
                            verbose=False,
                            full_resolution_float=True
                            )

        logger.info(f'New DataFrame has {df.shape[0]} '
                    f'rows and {df.shape[1]} columns.')
        # logger.info(f'converting to numeric file {_file_name} ...')
        # df.iloc[:, n_columns] = df.iloc[:, n_columns].apply(pd.to_numeric, _errors='coerce')
        logger.info(f'combining ...')
        df.drop(columns=drop_list, errors='ignore', inplace=True)
        df_combined = pd.concat([df_combined, df], axis=0)
        df_combined = df_combined.reset_index(drop=True)
        logger.info(f'Combined DataFrame has {df_combined.shape[0]} '
                    f'rows and {df_combined.shape[1]} columns now.')

    if write_csv:
        csv_address = os.path.join(csv_dest_folder, combined_name+'.csv')
        gc.disable()
        df_combined.to_csv(csv_address)
        gc.enable()
        logger.info(f'{csv_address}: is written')

    # if write_feather:
    #     feather_address = os.path.join(feather_dest_folder, combined_name+'.feather')
    #     gc.disable()
    #     df_combined.to_feather(feather_address)
    #     gc.enable()
    #     logger.info(f'{feather_address} is written')

    if write_pickle:
        pickle_address = os.path.join(pickle_dest_folder, combined_name+'.pickle')
        gc.disable()
        with open(pickle_address, 'wb') as f:
            gc.disable()
            pickle.dump(df_combined, f, protocol=-1)
            gc.enable()
        logger.info(f'{pickle_address} is written')






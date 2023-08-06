

import os
import pickle
import gc
import inspect
from .my_easy_logger import my_logger
import time

filename = os.path.split(__file__)[1]


def select_dos_rows(_src_fldr, _dst_fldr, new_name_ext='3class_'):
    func_name = inspect.stack()[0][3]
    logger = my_logger(reporter_file_name=filename,
                       reporter_func_name=func_name,
                       info_c='blue,bg_white')
    try:
        os.makedirs(_dst_fldr, exist_ok=False)
        logger.info(f'folder {_dst_fldr} is now created.')
    except:
        print(f'folder {_dst_fldr} is already created.')

    file_list = os.listdir(_src_fldr)
    for file in file_list:
        if str.upper(file).__contains__('CIC_2018.'):
            continue

        pickle_file2L = os.path.join(_src_fldr, file)
        with open(pickle_file2L, 'rb') as pf:
            gc.disable()
            logger.info(f'Reading the file {pickle_file2L}')
            df = pickle.load(pf)
            # df = df.sample(frac=1)
            row0 = df.shape[0]
            logger.info(f'The dataset has originally {row0:,} rows')
            time.sleep(0.5)

        # print(pickle_file2L+":\n", df.columns, 50*"**"+"\n\n")
        # time.sleep(0.5)
        # continue
        # selecting rows only of DoS combinations and benign traffic
        logger.info(f'Selecting the rows only containing DoS combinations in Attack column')
        df = df.loc[(df['Attack'].str.contains('DOS', case=False)) |
                    (df['Attack'].str.contains('Benign', case=False))]
        row1 = df.shape[0]
        logger.info(f'number of rows selected: {row1:,}, i.e. {100*row1/row0:0.2f}% of total rows')
        logger.info('Shuffling the dataframe to make it random.')
        df = df.sample(frac=1)
        logger.info(f'Resetting the index of selected dataframe')
        df.reset_index(inplace=True, drop=True)
        new_pickle_address = os.path.join(_dst_fldr, new_name_ext + file)
        logger.info(f'writing the selected dataframe to {new_pickle_address} ')
        # print(pickle_file2L + ":\n", df.columns, 50 * "**" + "\n\n")
        with open(new_pickle_address, 'wb') as f:
            pickle.dump(df, f, protocol=-1)
            logger.info(f'{new_pickle_address} is now written')
            time.sleep(0.5)
            print(50*'**'+'\n\n\n')
        gc.enable()
    logger.info(f'Done for all files in {_src_fldr}')




if __name__ == '__main__':
    ds_formats = {'NetFlow': 4, 'FlowMeter': 3}
    ds_formats = {'FlowMeter': 3}
    for ds_format, n_ds in ds_formats.items():
        print(f'Processing {n_ds-1} folders in {ds_format} format')
        for n in range(1, n_ds):
            src_fldr = f'/storage/datasets/{ds_format}/{n}pickle/'
            dst_fldr = f'/storage/datasets/{ds_format}/{n}pickle_3class/'
            print(f'Now Processing src_fldr: {src_fldr}, dst_fldr:{dst_fldr}')
            select_dos_rows(src_fldr, dst_fldr)

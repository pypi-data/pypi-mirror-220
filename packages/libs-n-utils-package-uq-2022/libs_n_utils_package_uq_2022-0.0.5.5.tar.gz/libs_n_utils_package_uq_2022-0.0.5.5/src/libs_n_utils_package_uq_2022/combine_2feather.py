import os
import pandas as pd
import feather
from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]


def combine_2feather(feather_file1, feather_file2):
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=__name__,
                        info_c='black,bg_yellow')
    logger_.info('Reading the df1')
    df1 = feather.read_dataframe(feather_file1)
    logger_.info('Reading the df2')
    df2 = feather.read_dataframe(feather_file2)
    df_list = [df1, df2]
    logger_.info('Combining the 2 dfs')
    dfs = pd.concat(df_list)
    logger_.info('shuffling the combined dfs')
    dfs = dfs.sample(frac=1).reset_index(drop=True)

    return dfs





if __name__ == '__main__':
    logger = my_logger(reporter_file_name=filename,
                       reporter_func_name=__name__,
                       info_c='blue,bg_white')


    # src_fldr = '/storage/datasets/NetFlow/feather/'
    src_fldr = '/storage/datasets/FlowMeter/feather/'
    # dst_fldr = '/storage/datasets/NetFlow/2feather/'
    dst_fldr = '/storage/datasets/FlowMeter/2feather/'
    file_list = os.listdir(src_fldr)

    while len(file_list) > 0:
        file_name = file_list[0]
        file_list.remove(file_name)
        for other_file in file_list:
            logger.info(f'df1={file_name},  df2={other_file}')
            file1 = os.path.join(src_fldr, file_name)
            file2 = os.path.join(src_fldr, other_file)

            df_combined = combine_2feather(file1, file2)
            combined_name = f'NF-{file_name[3:-3]}-{other_file[3:]}'
            feather_address = os.path.join(dst_fldr, combined_name)
            logger.info('Writing the combined dfs into the feather file')
            df_combined.to_feather(feather_address)
            logger.info(f'The combine file {combined_name} is written to {feather_address}.')







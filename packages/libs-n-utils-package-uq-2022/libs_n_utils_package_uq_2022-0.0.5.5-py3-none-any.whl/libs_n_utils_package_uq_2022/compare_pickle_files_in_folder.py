import _pickle as pickle
from .config_template import FlowMeter
import gc
import os

from my_easy_logger import my_logger

cols = FlowMeter.columns
cols.remove('Attack')
script_name = os.path.split(__file__)[1][:-3]


if __name__ == '__main__':
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold_blue,bg_white',
        reporter_func_name=__name__,
        log_level='debug'
    )

    src_fldr = f'/storage/datasets/FlowMeter/2pickle_3class'
    file_list = os.listdir(src_fldr)

    for file_name in file_list:
        file_addr = os.path.join(src_fldr, file_name)
        logger.info(f'reading file {file_addr}')
        with open(file_addr, 'rb') as f:
            gc.disable()
            df = pickle.load(f)

        df = df.sample(frac=0.0001)
        logger.info(f"columns of {file_name}:\n {df.columns}")
        logger.info(f"Number of columns of {file_name}: {len(list(df.columns))}")
        logger.info(f"first row :\n {df.iloc[0, :]}\n\n\n"+50*"**")
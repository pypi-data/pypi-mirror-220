import os
import pandas as pd
from .config_template import FlowMeter as FM
from .my_easy_logger import my_logger
import _pickle as pickle


cols = FM.columns
to_replace = FM.replace_these
script_name = os.path.split(__file__)[1][:-3]


if __name__ == "__main__":
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='fg_blue,bg_black',
        reporter_func_name=__name__,
        log_level='debug'
    )

    inputFileName = "/storage/datasets/FlowMeter/csv/FWM_ToN_IoT.csv"
    outputFileName = "/storage/datasets/FlowMeter/csv/CIC_ToN_IoT.csv"
    logger.info(f"Reading {inputFileName} ...")
    df = pd.read_csv(inputFileName, dtype='str')
    df_cols = list(df.columns)
    # tmp.py = df_cols[-2]
    # df_cols[-2] = df_cols[-1]
    # df_cols[-1] = tmp.py
    # df = df.reindex(columns=df_cols)
    logger.info("renaming the columns")
    df = df.rename(columns={x: y for x, y in zip(to_replace, cols)})

    logger.info(f" Writing to csv file: {outputFileName}")
    df.to_csv(outputFileName, index=False)

    # feather_address = outputFileName[:-4]+'.feather'
    # logger.info(f" Writing to feather file: {feather_address}")
    # df.to_feather(feather_address)

    pickle_address = outputFileName[:-4] + '.pickle'
    logger.info(f'Writing to pickle file: {pickle_address}')
    with open(pickle_address, 'wb') as fp:
        pickle.dump(df, fp, protocol=-1)

    logger.info("All formats are written now.")

import gc
import os
import _pickle as pickle
import feather
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from .lib_binary_classification import netflow_identifiers, seed_, netflow_columns
from .my_easy_logger import logger_cleaner





# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def get_dataset_prepared(_file_addr, *args, _n_rows=None, _do_scale=True, drop_label=True, **kwargs):
    if 'seed' in kwargs:
        seed = kwargs['seed']
    else:
        seed = 0

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,bg_cyan,fg_black'
    logger_.setLevel('DEBUG')

    logger_.info(f'reading {_file_addr}')
    if 'pickle_file' in args:
        with open(_file_addr, 'rb') as f:
            df = pickle.load(f)
    else:
        df = pd.read_csv(_file_addr)

    df.reset_index(drop=True, inplace=True)
    if 'columns_2_drop' in kwargs:
        columns_2_drop_ = kwargs['columns_2_drop']
    else:
        columns_2_drop_ = ['L4_DST_PORT', 'IPV4_DST_ADDR', 'L4_SRC_PORT', 'IPV4_SRC_ADDR']

    if 'Attack' in columns_2_drop_:
        columns_2_drop_.remove('Attack')
        drop_attack = True
    else:
        drop_attack = False

    for col in columns_2_drop_:
        try:
            df.drop(col, axis=1, inplace=True)
        except KeyError:
            logger_.info(f'column {col} was not dropped, or not in dataframe')

    if 'fill_na' in args:
        df.fillna(0, inplace=True)
        logger_.info(f'NaN entries were filled with 0')

    logger_.info(f'number of rows BEFORE removing NaN: {df.shape[0]}')
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]         # df.isna().sum()
    logger_.info(f'number of rows AFTER removing NaN: {df.shape[0]}')
    df.reset_index(drop=True, inplace=True)
    if _n_rows is not None:
        sample_frac = _n_rows / df.shape[0]
        logger_.info(f"Stratified sampling the df with frac: {sample_frac:.4f}")
        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
        df = df.groupby(by='Attack').sample(frac=sample_frac, random_state=seed)
        df.reset_index(drop=True, inplace=True)

    logger_.info("df Loaded")


    if drop_label:
        df.drop('Label', axis=1, inplace=True)

    if 'drop_attack_classes' in kwargs:
        drop_attack_classes = kwargs['drop_attack_classes']
        for drop_class in drop_attack_classes:
            df = df.loc[df['Attack'] != drop_class, :]
            df.reset_index(drop=True, inplace=True)
            logger_.info(f'attack class {drop_class} is removed')


    attack = df['Attack']
    if _do_scale:
        df.drop('Attack', axis=1, inplace=True)
        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
        x = df.fillna(0).values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled, columns=df.columns)

    if not drop_attack:
        df['Attack'] = attack
    features_list = df.columns.tolist()

    return df, features_list






# *--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# noinspection PyTypeChecker
@logger_cleaner
def get_binary_prepared(_source_fldr, _file_name, _file_type='pickle', scale_data=True, stratify_field='None',
                        _split=1, _seed=None, _flow_columns=None, _remove_label=True,
                        _train_size=0.75, _frac=1, _columns2drop=None, apply_numeric=True,
                        _selected_columns=None, _flow_identifiers=None, remove_attack=False, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'

    file_address = os.path.join(_source_fldr, _file_name)
    if _flow_identifiers is None:
        _flow_identifiers = netflow_identifiers
    if _seed is None:
        _seed = seed_
    if _flow_columns is None:
        _flow_columns = netflow_columns
    if _columns2drop is None:
        # Attack used to be here to be deleted 22-11-2021         x_scaled = min_max_scaler.fit_transform(df)
        # _columns2drop = _flow_identifiers + ['Attack']
        _columns2drop = _flow_identifiers
    if _selected_columns is None:
        _selected_columns = [
            x for x in _flow_columns
            if x not in _columns2drop
        ]

    logger_.info(f'Reading file {file_address} ...')
    gc.disable()
    if _file_type.lower() == 'pickle':
        with open(file_address, 'rb') as fp:
            df = pickle.load(fp)
            logger_.debug(df.columns)
        if _selected_columns is not None:
            df = df[_selected_columns]
            logger_.debug(df.columns)

    elif _file_type.lower() == 'csv':
        df = pd.read_csv(file_address)

    else:
        if _selected_columns is not None:
            df = feather.read_dataframe(
                file_address,
                columns=_selected_columns
            )
        else:
            df = feather.read_dataframe(
                file_address
            )

    df.reset_index(inplace=True, drop=True)
    gc.enable()

    logger_.info(f'Sampling the loaded Dataframe, fraction= {_frac:_}')
    if _frac > 1:
        if _frac <= df.shape[0]:
            df = df.sample(n=_frac, random_state=_seed)
        else:
            _frac = 1
            df = df.sample(frac=_frac, random_state=_seed)
    elif _frac < 1:
        df = df.sample(frac=_frac, random_state=_seed)

    # if frac was not 1, then we need to reset the index
    if _frac != 1:
        df.reset_index(drop=True, inplace=True)

    logger_.info(f'File {file_address} is read, now processing ...')
    rows_0 = df.shape[0]
    df_columns = df.columns
    if apply_numeric:
        if 'Attack' in df_columns:
            if remove_attack:
                if stratify_field != 'Attack':
                    df.drop('Attack', axis=1, inplace=True)
                else:
                    attack_col = df.pop('Attack')
            else:
                attack_col = df.pop('Attack')
        elif stratify_field == 'Attack':
            exit('Attack is listed as stratified column, but it is not in the columns')


        df = df.apply(pd.to_numeric, errors='coerce')
        #df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
        df = df[np.isfinite(df).all(1)]
        rows_1 = df.shape[0]
        logger_.info(f'Rows dropped due to NaN etc: {rows_0 - rows_1} '
                 f'rows, i.e. {100*(rows_0 - rows_1)/rows_0:.2f}%')

    if 'Label' in df.columns:
        if _remove_label:
            y = df.pop('Label')
        else:
            y = df['Label']
    else:
        y = None

    if scale_data:
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(df)
        x = pd.DataFrame(
            x_scaled,
            columns=df.columns
        )
    else:
        x = df

    if _split:
        if stratify_field is not None:
            if stratify_field == 'Attack':
                stratify = attack_col[x.index]
            else:
                stratify = df[stratify_field]
        else:
            stratify = None
        x_train_, x_test_, y_train_, y_test_ = train_test_split(
            x, y,
            train_size=_train_size,
            shuffle=True,
            stratify=stratify,
            random_state=_seed
        )
        return x_train_, x_test_, y_train_, y_test_
    else:
        return x, y
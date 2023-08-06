import os
import pickle as pickle
import sys

import numpy as np
from scipy.stats import wasserstein_distance
from .config_template import NN
from .lib_data_preprocessing import get_binary_prepared
from .lib_plotters import plot_hist_list
from .my_easy_logger import logger_cleaner

seed_ = NN.seeds


# ----------------------------------------------------------------------------------------------------------------------
@logger_cleaner
def compute_CDF(_values_df, column=0, **kwargs):
    """
    Computes the CDF of a single column of _values_df dataframe, if column is not given, selects the first column
    :param _values_df: dataframe from which the column to be selected
    :param column:  the column whose CDF to be calculated
    :param kwargs:
    :return:
    """
    logger_ = kwargs['logger']
    logger_.info(f"computing CDF of values column {column}")

    if str(column).isnumeric():
        listed_col = _values_df.iloc[:, column].to_list()
    else:
        listed_col = _values_df.loc[:, column].to_list()

    listed_col.sort()
    sorted_values_ = listed_col
    N = len(sorted_values_)
    Freq_ = np.array(range(N)) / float(N - 1)

    return [sorted_values_, Freq_]


# ----------------------------------------------------------------------------------------------------------------------
@logger_cleaner
def wasserstein_table_df_list(df_list, colors, *args, **kwargs):
    if 'datasets_list' in kwargs:
        datasets_list = kwargs['datasets_list']
    logger_ = kwargs['logger']
    logger_.info("computing Wasserstein distances for the list of Dataframes ...")

    num_ds = len(df_list)
    wasserstein_table = np.zeros((num_ds, num_ds))
    for n1, df1 in enumerate(df_list):
        df1_values = df1.iloc[:, 0].values
        for n2, df2 in enumerate(df_list):
            if n1 != n2:
                df2_values = df2.iloc[:, 0].values
                x = df1_values
                x = x[~np.isnan(x)]
                y = df2_values
                y = y[~np.isnan(y)]
                wasserstein_table[n1, n2] = wasserstein_distance(x, y)
                if 'datasets_list' in kwargs:
                    title = f'sample size {x.shape[0]} - WD: {wasserstein_table[n1, n2]:0.2f}'
                    if 'plot_distributions' in args:
                        if 'save_fldr' in kwargs:
                            plot_hist_list([x, y], [datasets_list[n1], datasets_list[n2]], [colors[n1], colors[n2]],
                                           title=title, save_fldr=kwargs['save_fldr'])
                        else:
                            plot_hist_list([x, y], [datasets_list[n1], datasets_list[n2]], [colors[n1], colors[n2]],
                                           title=title)
                logger_.info(f'wasserstein distance({n1},{n2}) equals to: {wasserstein_table[n1, n2]}')

    return wasserstein_table


# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def intra_dataset_wasserstein_table(df, _features, _groups, _pickle_fdlr=None, df_file_name=None, **kwargs):
    """
    Computes the Wasserstein Distances for all the columns/features of dataframe by grouping by attack columns values
    :param df:
    :param _features:
    :param _groups:
    :param _pickle_fdlr:
    :param df_file_name:
    :param kwargs:
    :return:
    """

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'
    logger_.setLevel('DEBUG')

    _features.sort()
    overall_dict = dict.fromkeys(_features)
    for feature in _features:
        ws_array = np.zeros((len(_groups), len(_groups)))
        # overall_dict[feature] = ws_array
        for in1, attack1 in enumerate(_groups):
            for in2, attack2 in enumerate(_groups):
                if attack1 != attack2:
                    x = df.loc[df['Attack'] == attack1, feature]
                    y = df.loc[df['Attack'] == attack2, feature]
                    ws_array[in1, in2] = wasserstein_distance(x, y)
        overall_dict[feature] = ws_array
        logger_.info(f'Calculating feature {feature} done.')

    overall_dict['groups'] = _groups
    if _pickle_fdlr is not None:
        pickle_addr = os.path.join(_pickle_fdlr,
                                   f'Wasserstein_{df_file_name[:-4]}_'
                                   f'whole_rows_{len(_features)}_features.pickle')
        with open(pickle_addr, 'wb') as f:
            pickle.dump(overall_dict, f)
            logger_.info(f'the overall dict for {len(_features)} '
                         f'features is saved into {pickle_addr}')

    return overall_dict







# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def inter_dataset_wasserstein_table(features_list, _flow_columns=None, _flow_identifiers=None, dataset_dict=None,
                                    _src_fldr=None, _src_files=None, _pickle_fdlr=None, **kwargs):
    """
    Computes the Wasserstein Distance for columns of all datasets/dataframes saved in the _src_fldr
    :param _src_fldr:
    :param _src_files:
    :param features_list:
    :param _flow_columns:
    :param _flow_identifiers:
    :param dataset_dict: a dictionary of dataframe of datasets "ALL DATASETS MUST HAVE Exactly THE SAME SIZE"
    :param _save_fldr:
    :param _pickle_fdlr:
    :param kwargs:
    :return:
    """
    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'

    if dataset_dict is None:
        mode = 'file_load_mode'
        min_size = sys.maxsize
        frac = 1
    else:
        mode = 'dict_of_df_mode'
        all_ds_size = 0

    if mode == 'file_load_mode':
        if _src_files is None or _src_fldr is None or _flow_columns is None or _flow_identifiers is None:
            exit('Either dataset dict or src files and folder must be given')

        dataset_dict = dict()
        for n0, base_file in enumerate(_src_files):
            x_preprocessed, _ = get_binary_prepared(
                _src_fldr,
                base_file,
                _remove_label=True,
                remove_attack=True,
                _selected_columns=features_list,
                _split=0,
                _frac=frac,
                scale_data=False,
                _flow_columns=_flow_columns,
                _flow_identifiers=_flow_identifiers,
                _seed=seed_
            )
            logger_.info(f'{base_file} loaded.')
            logger_.info(f'adding {base_file[:-7]} to total Dataframe')
            dataset_dict[base_file[:-7]] = x_preprocessed
            if x_preprocessed.shape[0] < min_size:
                min_size = x_preprocessed.shape[0]

    dataset_name_list = list(dataset_dict.keys())
    dataset_name_list.sort()


    logger_.info("sampling the datasets using the minimum size of datasets to make all the same")
    for n, ds in enumerate(dataset_name_list):
        if mode == 'file_load_mode':
            tmp = dataset_dict[ds].sample(n=min_size, random_state=seed_)
            tmp.reset_index(drop=True, inplace=True)
            dataset_dict[ds] = tmp
        else:
            if n == 0:
                all_ds_size = dataset_dict[ds].shape
            elif all_ds_size != dataset_dict[ds].shape:
                exit('Datasets in Dict are not of the same size')

    features_list.sort()
    overall_dict = dict.fromkeys(features_list)
    for feature in features_list:
        logger_.info(f'Calculating Wasserstein Distance for {feature} '+'-*-'*20)
        ws_array = np.zeros((len(dataset_name_list), len(dataset_name_list)))
        for n1, ds1 in enumerate(dataset_name_list):
            for n2, ds2 in enumerate(dataset_name_list):
                if n2 > n1:
                    x = dataset_dict[ds1][feature]
                    y = dataset_dict[ds2][feature]
                    ws_array[n1, n2] = wasserstein_distance(x, y)
                    ws_array[n2, n1] = ws_array[n1, n2]
                    logger_.info(f'WS of {ds1} and {ds2} over feature {feature} is: {ws_array[n1, n2]}')

        # overall_dict[feature] = ws_array / ws_array.max()
        overall_dict[feature] = ws_array
        logger_.info(f'Calculating for feature {feature} done.')

    if _pickle_fdlr is not None:
        if 'save_name' in kwargs:
            save_name = kwargs['save_name']
        else:
            save_name = "-".join(dataset_name_list)
        pickle_addr = os.path.join(_pickle_fdlr,
                                   f'Wasserstein_{save_name}_'
                                   f'all_raw_features.pickle')
        with open(pickle_addr, 'wb') as f:
            pickle.dump(overall_dict, f)
            logger_.info(f'the overall dict for WS of {len(features_list)} '
                         f'over {len(dataset_name_list)} datasets'
                         f'features is saved into {pickle_addr}')

    return overall_dict

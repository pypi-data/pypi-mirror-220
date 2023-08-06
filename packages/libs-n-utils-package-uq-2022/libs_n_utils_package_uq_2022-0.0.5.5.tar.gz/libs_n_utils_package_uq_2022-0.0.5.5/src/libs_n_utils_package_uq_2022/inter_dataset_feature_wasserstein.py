
import os
import pickle
import re

import numpy as np

from .config_template import NetFlow_v2, FlowMeter
from .lib_plotters import plot_wasserstein_table
from .lib_stat_distribution import inter_dataset_wasserstein_table
from .my_easy_logger import my_logger, logger_cleaner

script_name = os.path.split(__file__)[1][:-3]




@logger_cleaner
def main(weighted, model_number, algorithm_number, **kwargs):
    logger_ = kwargs['logger']
    flow_columns_ = NetFlow_v2.columns
    flow_identifiers_ = NetFlow_v2.flow_identifiers
    cols_to_load_ = NetFlow_v2.columns[4:-2]
    plot_individual_feature_ws_ = False
    file_type = 'pickle'
    algorithm = ['Supervised', 'Unsupervised'][algorithm_number]
    param_dict = {'Supervised': [0, 0, [0, 1, 2], [5, -10]],
                  'Unsupervised': [1, 1, [3, 4, 5], [5, -14]],
                  }

    extension_ = ["-1m", "-balanced"][param_dict[algorithm][0]]
    src_fldr_ = f'/storage/datasets/NetFlow/1pickle{extension_}'
    save_fig_fldr = '/home/nids1/PycharmProjects/IDS_Generalization/' \
                    'outputs/figures/shap_weighted_wasserstein'
    saved_ws_name_ = ['Wasserstein_NFv2-BoT_IoT-1m-NFv2-'
                      'CIC_2018-1m-NFv2-ToN_IoT-1m-NFv2-UNSW_NB15-1m_all_raw_features.pickle',
                      "Wasserstein_NFv2-BoT_IoT-balanced-NFv2-CIC_2018-balanced-NFv2-ToN_IoT-"
                      "balanced-NFv2-UNSW_NB15-balanced_all_raw_features.pickle"][param_dict[algorithm][1]]
    model_name_ = ['Extra Tree',  'Feed Forward', 'Random Forest',
                   'Isolation Forest', 'SGD-oSVM', 'oSVM'][param_dict[algorithm][2][model_number]]
    y_shift = [25 / 72., 35 / 72., 35 / 72., 50 / 72., 30 / 72.]
    tick_label_chops_ = param_dict[algorithm][3]

    logger_.info(f'Algorithm: {algorithm} and Model: {model_name_}')
    pickle_fldr_ = '/home/nids1/PycharmProjects/IDS_Generalization/outputs/wasserstein'
    shap_values_fldr = '/home/nids1/PycharmProjects/IDS_Generalization/outputs/scores/SHAP_values/'
    shap_values_files = os.listdir(shap_values_fldr)
    shap_values_files.sort()
    shap_values_file = shap_values_files[param_dict[algorithm][2][model_number]]
    logger_.info(f'Selected SHAP file: {shap_values_file}')
    shap_values_filepath = os.path.join(shap_values_fldr, shap_values_file)


    logger_.info(f'Computing the weighted WS for {shap_values_file}')
    SHAP_df = [pickle.load(open(shap_values_filepath, 'rb')), None][0]


    ws_pipeline(
        pickle_fldr_,
        src_fldr_,
        file_type_=file_type,
        flow_columns=flow_columns_,
        flow_identifiers=flow_identifiers_,
        cols_to_load=cols_to_load_,
        saved_ws_name=saved_ws_name_,
        save_fig_fldr=save_fig_fldr,
        y_shift=y_shift,
        plot_individual_feature_ws=plot_individual_feature_ws_,
        all_features_weight_df=SHAP_df if weighted else None,
        average_plot_name=f'Weighted Avg. by {model_name_} SHAP values' if weighted else 'Averaged',
        tick_label_chops=tick_label_chops_,
        logger=logger_
    )





# ---------------------------------------------------------------------------------------------------------------------
@logger_cleaner
def ws_pipeline(pickle_fldr, src_fldr, file_type='pickle', saved_ws_name=None, save_fig_fldr=None,
                all_features_weight_df=None, plot_individual_feature_ws=False, cols_to_load=None,
                flow_columns=None, flow_identifiers=None, average_plot_name='Average', save_fig_name=None,
                tick_label_chops=None, mode='file_load', plot_average_ws=True, save_avg_table_fldr=None,
                save_avg_table_name=None, normalize_average_ws=True, **kwargs):
    """
    computes the wasserstein distance between features of different datasets and averages, if a weight is provided
    applies it for averaging, then plots wasserstein tables and the averaged wasserstein table
    :param normalize_average_ws: if true, average ws table will be normalized
    :param save_avg_table_name: name for the average table to be saved
    :param save_fig_name: name for the figures to be saved
    :param save_avg_table_fldr: folder to save the average table, if we want to save
    :param plot_average_ws: If True, plots the average WS table
    :param mode: compute by WS by using files of dfs or df_dict
    :param pickle_fldr: folder to save ws tables or load saved ws tables
    :param src_fldr: dataset folder
    :param file_type: pickle by default
    :param saved_ws_name: if wasserstein is supplied it just averages and plots the table
    :param save_fig_fldr: if provided, figures will be saved to this fldr
    :param plot_individual_feature_ws: if True ws tables of each feature will be plotted
    :param all_features_weight_df: if provided, will be applied for averaging
    :param cols_to_load: list of features/columns
    :param flow_columns: flow columns
    :param flow_identifiers: flow identifier features that should be removed/dropped
    :param average_plot_name: name to be assigned to the average plot
    :param tick_label_chops: e.g. [5, -7] the section of ds names to be used for tick labels
    :param kwargs:
    :return: saves wasserstein distances and plots tables
    """
    logger_ = kwargs['logger']
    if not os.path.isdir(pickle_fldr):
        os.mkdir(pickle_fldr)

    src_files = os.listdir(src_fldr)
    src_files = [f for f in src_files if f.split('.')[-1] == file_type]
    src_files.sort()
    logger_.info(f' files to be loaded: {src_files} from folder\n{src_fldr}')

    if saved_ws_name is None:
        if mode == 'file_load':
            overall_ws_dict = inter_dataset_wasserstein_table(
                cols_to_load,
                _src_fldr=src_fldr,
                _src_files=src_files,
                _flow_columns=flow_columns,
                _flow_identifiers=flow_identifiers,
                _pickle_fdlr=pickle_fldr,
                **kwargs
            )
        else:
            all_features_dict = kwargs['all_features_dict']
            overall_ws_dict = inter_dataset_wasserstein_table(
                cols_to_load,
                dataset_dict=all_features_dict,
                _pickle_fdlr=pickle_fldr,
                **kwargs
            )
    else:
        pickle_name = saved_ws_name
        pickle_path = os.path.join(pickle_fldr, pickle_name)
        overall_ws_dict = pickle.load(open(pickle_path, 'rb'))

    if tick_label_chops is None:
        tick_label_chops = [5, -7]

    if 'label_pattern' not in kwargs:
        tick_labels = [file[tick_label_chops[0]:tick_label_chops[1]] for file in src_files]
    else:
        label_pattern = kwargs['label_pattern']
        tick_labels = [make_label(file, label_pattern, tick_label_chops) for file in src_files]

    features_list = list(overall_ws_dict.keys())
    average_ws_table = np.zeros((len(tick_labels), len(tick_labels)))

    for feature in features_list:
        print(feature)
        if save_fig_fldr is not None:
            if save_fig_name is None:
                save_fig_name = "-".join(tick_labels)
            save_address = os.path.join(save_fig_fldr, f'{feature}_wasserstein_{save_fig_name}.pdf')
        else:
            save_address = None
        feature_ws_table = overall_ws_dict[feature]
        feature_ws_table[np.isnan(feature_ws_table)] = 0

        if all_features_weight_df is not None:
            feature_weight_df = all_features_weight_df.loc[:, feature]
            weighted_feature_ws_table = apply_weights_to_ws_table(feature_ws_table, feature_weight_df, src_files)
        else:
            weighted_feature_ws_table = feature_ws_table

        n_nan_feature = np.isnan(feature_ws_table).sum()
        if n_nan_feature > 0:
            logger_.info(f'Feature {feature} has {n_nan_feature} NaN values')

        if plot_individual_feature_ws:
            plot_wasserstein_table(
                weighted_feature_ws_table,
                tick_labels,
                'bold_xticklabels',
                'bold_yticklabels',
                _figsize=(10, 8),
                _cbar_label_fontsize=16,
                _cbar_ticklabel_fontsize=15,
                _annot_fontsize=15,
                _xticklabel_size=15,
                _yticklabel_size=15,
                _save_address=save_address,
                _feature_name=feature,
                **kwargs
            )

        average_ws_table += weighted_feature_ws_table

    # average_ws_table = average_ws_table / len(features_list)
    if normalize_average_ws:
        average_ws_table = average_ws_table / average_ws_table.max()
    if save_avg_table_fldr is not None:
        if save_avg_table_name is None:
            save_avg_table_name = "-".join(tick_labels)
        save_avg_table_address = os.path.join(save_fig_fldr,
                                              f'Average_wasserstein_table_{save_avg_table_name}.pickle')
        pickle.dump(average_ws_table, open(save_avg_table_address, 'wb'))
        logger_.info(f'average_ws_table is saved to {save_avg_table_address}')


    if save_fig_fldr is not None:
        if average_plot_name is None:
            average_plot_name = "-".join(tick_labels)
        save_address = os.path.join(save_fig_fldr,  f'{average_plot_name}_wasserstein.pdf')
    else:
        save_address = None

    if plot_average_ws:
        plot_wasserstein_table(
            average_ws_table,
            tick_labels,
            'bold_xticklabels',
            'bold_yticklabels',
            'bold_cbarlabels',
            _xlabel='Target Dataset',
            _ylabel='Source Dataset',
            _xlabel_fontsize=16,
            _ylabel_fontsize=16,
            _xlabel_fontweight='bold',
            _ylabel_fontweight='bold',
            cmap='Reds',
            cbar_label=f'Wasserstein Distance ({average_plot_name})',
            _figsize=(20, 15),
            _cbar_label_fontsize=14,
            _cbar_ticklabel_fontsize=15,
            _annot_fontsize=15,
            _xticklabel_size=10,
            _yticklabel_size=10,
            _save_address=save_address,
            _feature_name=average_plot_name,
            **kwargs
        )

    logger_.info('All done.')





# ---------------------------------------------------------------------------------------------------------------------
def make_label(label_string, pattern, chops=(None, None)):
    matched = re.search(pattern, label_string)
    l1 = matched.groups()[0][chops[0]:chops[1]]
    l2 = matched.groups()[1][chops[0]:chops[1]]
    return f'{l1}-{l2}'





# ---------------------------------------------------------------------------------------------------------------------
def apply_weights_to_ws_table(feature_ws_table, feature_weight_df, src_files):
    # normalizing the weights (SHAP values)
    feature_weight_df[feature_weight_df.isna()] = 1
    if (feature_weight_df == 0).sum() == feature_weight_df.shape[0]:
        # if all weights are zero do not do anything
        return feature_ws_table

    feature_weight_df = feature_weight_df / feature_weight_df.max()
    ds_names = [sf[:-7] for sf in src_files]
    ds_names.sort()
    # order of datasets are the same in both the features ws and feature weights (both sorted list of src files)
    for n_src, src_ds in enumerate(ds_names):
        for n_trgt, trgt_ds in enumerate(ds_names):
            feature_ws_table[n_src, n_trgt] = feature_weight_df.loc[(src_ds, trgt_ds)] * \
                                              feature_ws_table[n_src, n_trgt]

    return feature_ws_table






# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='fg_blue',
        reporter_func_name=__name__,
        log_level='debug'
    )

    for weighted_ in [True, False]:
        for algorithm_number_ in range(2):
            for model_number_ in range(3):
                if not weighted_ and model_number_ > 0:
                    continue

                logger.info(f'plotting WS for weighted={weighted_}, '
                            f'model_number: {model_number_}, '
                            f'algorithm_number: {algorithm_number_}')
                main(weighted_, model_number_, algorithm_number_, logger=logger)

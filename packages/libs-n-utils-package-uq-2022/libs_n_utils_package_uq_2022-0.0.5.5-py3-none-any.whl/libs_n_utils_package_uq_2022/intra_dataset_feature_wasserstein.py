"""
This scripts computes the wasserstein distances between attack classes
and plots them using heat-maps
"""

import os

from .lib_data_preprocessing import get_dataset_prepared
from .lib_plotters import plot_wasserstein_table
from .lib_stat_distribution import intra_dataset_wasserstein_table
from .my_easy_logger import my_logger, logger_cleaner

script_name = os.path.split(__file__)[1][:-3]




# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def fw_boiler_plate(_src_fldr, _file_name, *args, _n_rows=None, _do_scale=True,
                    _n_features=-1, _pickle_fdlr=None, **kwargs):

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'
    logger_.setLevel('DEBUG')

    file_addr = os.path.join(_src_fldr, _file_name)
    df, features = get_dataset_prepared(file_addr, *args, _n_rows=_n_rows, _do_scale=True, **kwargs)
    features.remove('Attack')
    if _n_features != -1:
        features = features[:_n_features]
    features.sort()

    attacks = df['Attack'].unique().tolist()
    attacks.sort()
    if 'Benign' in attacks:
        attacks.remove('Benign')

    overall_dict = intra_dataset_wasserstein_table(
        df,
        features,
        attacks,
        _pickle_fdlr=_pickle_fdlr,
        df_file_name=_file_name,
        **kwargs
    )

    # Plotting results
    tick_labels = attacks
    for feature in features:
        plot_array = overall_dict[feature]
        plot_wasserstein_table(
            plot_array,
            tick_labels,
            _feature_name=feature,
            **kwargs
        )

    logger_.info('All done.')




# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
if __name__ == '__main__':
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold_cyan',
        reporter_func_name=__name__,
        log_level='debug'
    )
    # src_fldr = '/storage/datasets/NetFlow/csv'
    src_fldr = '/storage/datasets/originals'
    save_fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds'
    pickle_fdlr = save_fldr
    file_name = 'UNSW-NB15.csv'
    dataset_dict = {
        'UNSW-NB15.csv': {
            'columns_2_drop':
                ['srcip', 'dstip', 'sport', 'dsport']
        },
        'NF-UNSW-NB15-v2.csv': {
            'columns_2_drop':
                ['L4_DST_PORT', 'IPV4_DST_ADDR', 'L4_SRC_PORT', 'IPV4_SRC_ADDR']
        }
    }
    columns_2_drop = dataset_dict[file_name]['columns_2_drop']
    n_rows = [100_000, None][0]
    logger.info(f'{n_rows if n_rows is not None else "whole"} rows are loading from {file_name}')
    do_scale = True
    n_features = -1
    fw_boiler_plate(src_fldr,
                    file_name,
                    'fill_na',
                    _n_rows=n_rows,
                    _do_scale=do_scale,
                    _n_features=n_features,
                    _pickle_fdlr=pickle_fdlr,
                    _save_fldr=save_fldr,
                    # drop_attack_classes=['Benign', 'Shellcode', 'Worms'],
                    columns_2_drop=columns_2_drop,
                    )

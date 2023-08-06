import inspect
import os
import _pickle as pickle
import warnings
import pandas as pd
from .intra_dataset_feature_wasserstein import get_dataset_prepared
import numpy as np
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from .my_easy_logger import my_logger, logger_cleaner

script_name = os.path.split(__file__)[1][:-3]




# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def fs_boiler_plate(_src_fldr, _file_name, *args, _n_rows=None, _do_scale=True,
                    _n_features=-1, _pickle_fdlr=None, **kwargs):

    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'

    logger_.setLevel('DEBUG')

    file_addr = os.path.join(_src_fldr, _file_name)
    df, features = get_dataset_prepared(file_addr, *args, _n_rows=_n_rows, _do_scale=True, **kwargs)
    features.remove('Attack')
    if _n_features != -1:
        features = features[:_n_features]

    _n_features = len(features)
    logger_.info(features)

    attacks = df['Attack'].unique().tolist()
    if 'Benign' in attacks:
        attacks.remove('Benign')

    fi_dict = dict.fromkeys(attacks)
    fi_dict['features'] = features
    for attack in attacks:
        logger_.info(f'computing mutual information of features for {attack}')
        the_one = df.loc[df['Attack'] == attack, :]
        the_one.loc[:, 'Attack'] = 1
        the_all = df.loc[df['Attack'] != attack, :]
        the_all.loc[:, 'Attack'] = 0
        X = pd.concat([the_one.loc[:, features], the_all.loc[:, features]], axis=0)
        Y = pd.concat([the_one.loc[:, 'Attack'], the_all.loc[:, 'Attack']], axis=0)
        # mi = mutual_info_regression(X, Y)
        mi = mutual_info_classif(X, Y)
        mi /= np.max(mi)
        fi_dict[attack] = mi
        logger_.info(f'the mutual information for {attack} is done now')

    logger_.info('All done.')
    if '_save_fldr' in kwargs:
        _save_fldr = kwargs['_save_fldr']
        if _n_rows == None:
            _n_rows = 'whole'
        _save_addr = os.path.join(_save_fldr,
                                  f'feature_importance_using_mi[mutual_info_classif]_'
                                  f'{_n_features}_'
                                  f'features_{_file_name[:-4]}_{_n_rows}_rows.pickle')
        logger_.info(f'saving mi to {_save_addr}')
        with open(_save_addr, 'wb') as f:
            pickle.dump(fi_dict, f, protocol=-1)





# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold_cyan',
        reporter_func_name=__name__,
        log_level='debug'
    )
    # src_fldr = '/storage/datasets/NetFlow/csv'
    # save_fldr = '/home/nids1/Desktop/ZSL_visualizations/'
    src_fldr = '/storage/datasets/originals'
    save_fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds'
    pickle_fdlr = save_fldr
    # file_name = 'NF-UNSW-NB15-v2.csv'
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
    n_rows = [1_000_000, None][1]
    logger.info(f'{n_rows if n_rows is not None else "whole"} rows are loading from {file_name}')
    do_scale = True
    n_features = -1
    logger.info(f'number of selected features: {n_features if n_features != -1 else "all features"}')
    fs_boiler_plate(
        src_fldr,
        file_name,
        _n_rows=n_rows,
        _do_scale=do_scale,
        _n_features=n_features,
        _pickle_fdlr=pickle_fdlr,
        # drop_attack_classes=['Benign', 'Shellcode', 'Worms'],
        # _save_fldr=save_fldr,
        columns_2_drop=columns_2_drop
    )

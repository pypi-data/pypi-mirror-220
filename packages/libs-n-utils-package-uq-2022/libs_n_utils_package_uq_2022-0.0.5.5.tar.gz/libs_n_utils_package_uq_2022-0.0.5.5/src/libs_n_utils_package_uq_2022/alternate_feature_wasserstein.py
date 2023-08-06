"""
This scripts computes the wasserstein distances in the alternative way, i.e.
the difference between z-attack training sets and the test set.
It also plots them using bar-charts
"""


import inspect
import os
import _pickle as pickle
import pandas as pd
from scipy.stats import wasserstein_distance

from .intra_dataset_feature_wasserstein import get_dataset_prepared
from .lib_plotters import draw_bar_chart
from .my_easy_logger import my_logger, logger_cleaner

script_name = os.path.split(__file__)[1][:-3]
logger = my_logger(
    reporter_file_name=script_name,
    info_c='bold_blue',
    reporter_func_name=__name__,
    log_level='debug'
)





# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def afw_boiler_plate(_src_fldr, _file_name, *args, _n_rows=None, _do_scale=True,
                    _n_features=-1, _pickle_fdlr=None, **kwargs):
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'fg_blue,bold'

    logger_.setLevel('DEBUG')

    file_addr = os.path.join(_src_fldr, _file_name)
    df, features = get_dataset_prepared(
        file_addr,
        *args,
        _n_rows=_n_rows,
        _do_scale=_do_scale,
        drop_label=True,
        **kwargs
    )

    if 'tst_ratio' in kwargs:
        tst_ratio_ = kwargs['tst_ratio']
    else:
        tst_ratio_ = 0.3

    if 'seed' in kwargs:
        seed_ = kwargs['seed']
    else:
        seed_ = 0

    tst_df = df.groupby(by='Attack').sample(frac=tst_ratio_, random_state=seed_)
    tst_df.drop('Attack', axis=1, inplace=True)
    tr_df = df[~df.index.isin(tst_df.index)]
    tst_df.reset_index(drop=True, inplace=True)
    tr_df.reset_index(drop=True, inplace=True)

    features.remove('Attack')
    if _n_features != -1:
        features = features[:_n_features]
    features.sort()

    attacks = df['Attack'].unique().tolist()
    attacks.sort()
    if 'Benign' in attacks:
        attacks.remove('Benign')

#######################################
    ws_distance_df = pd.DataFrame(0, columns=features, index=attacks, dtype=float)
    for feature in features:
        for attack in attacks:
            logger_.info(f'Calculating ws for feature [{feature}] '
                         f'when ---> {attack} <--- is missing vs when it is present.')
            x = tr_df.loc[tr_df['Attack'] != attack, feature]
            y = tst_df[feature]
            ws_distance_df.loc[attack, feature] = wasserstein_distance(x, y)

    if _pickle_fdlr is not None:
        pickle_addr = os.path.join(_pickle_fdlr,
                                   f'Alternate_Wasserstein_{file_name[:-4]}_'
                                   f'whole_rows_{len(features)}_features.pickle')
        with open(pickle_addr, 'wb') as f:
            pickle.dump(ws_distance_df, f)
            logger_.info(f'the overall dict for {len(features)} '
                         f'features is saved into {pickle_addr}')
############################################

    # Plotting results
    if 'ylog_scale_' in kwargs:
        ylog_scale_ = kwargs['ylog_scale']
    else:
        ylog_scale_ = False
    tick_labels = attacks
    x_values = range(ws_distance_df.shape[0])
    xticks_rotation_dic = {
        'rotation_mode': "anchor",
        'ha': "center"
    }
    if 'save_fldr' in kwargs:
        save_fldr_ = kwargs['save_fldr']
    else:
        save_fldr_ = src_fldr
    ymin = ws_distance_df.min().min()
    ymax = ws_distance_df.max().max()
    for feature in features:
        save_addr = os.path.join(save_fldr_, f'alternate_feature_WS_{feature}.pdf')
        # for feature in features:
        draw_bar_chart(x_values, ws_distance_df[feature],
                       _title_text=f'WS of {feature} [attacks absent and present]', _xlabel='Attacks',
                       _ylabel=f'Wasserstein Distance', _xticks=x_values, _xticks_rotation=10, _xticklabel_size=12,
                       _ylims=[ymin, ymax], _title_fontweight='bold', _ylog_scale=ylog_scale_, _save_address=save_addr,
                       _xticks_rotation_dic=xticks_rotation_dic, _yticklabel_size=12, _title_fontsize=18,
                       _xlabel_fontsize=18, _ylabel_fontsize=18, _figsize=(12, 8), _xticklabel_weight='bold',
                       _ylabel_fontweight='bold', _xlabel_fontweight='bold', _xtick_labels=tick_labels)




    logger_.info('All done.')


# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
if __name__ == '__main__':
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
    n_rows = [100_000, None][1]
    logger.info(f'{n_rows if n_rows is not None else "whole"} '
                f'rows are loading from {file_name}')
    do_scale = True
    n_features = -1
    logger.info(f'number of selected features: '
                f'{n_features if n_features != -1 else "all features"}')

    afw_boiler_plate(
        src_fldr,
        file_name,
        # 'fill_na',
        _n_rows=n_rows,
        _do_scale=do_scale,
        _n_features=n_features,
        _pickle_fdlr=pickle_fdlr,
        save_fldr=save_fldr,
        # drop_attack_classes=['Benign', 'Shellcode', 'Worms'],
        columns_2_drop=columns_2_drop,
        ylog_scale=False
    )



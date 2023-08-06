import inspect
import os
import warnings
import pandas as pd
import _pickle as pickle
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy
from .my_easy_logger import my_logger, logger_cleaner
from .intra_dataset_feature_wasserstein import get_dataset_prepared

script_name = os.path.split(__file__)[1][:-3]
logger = my_logger(
    reporter_file_name=script_name,
    info_c='bold_blue',
    reporter_func_name=__name__,
    log_level='debug'
)




# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def BorutaPy_feature_select(*args, _n_rows=None, _do_scale=True, drop_label=True, **kwargs):
    """
    Computes the Boruta feature selection
    :param df: the dataframe input
    :param _src_fldr: if df is not given _src_fldr and _file_name will be used
    :param _file_name: if df is not given _src_fldr and _file_name will be used
    :param _n_rows: if df is not given _src_fldr and _file_name will be used
    :param _do_scale: if df is not given _src_fldr and _file_name will be used
    :param drop_label: if df is not given _src_fldr and _file_name will be used
    :param kwargs:
    :return:
    """
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,fg_blue,bg_white'


    if args[0].__class__ != pd.DataFrame:
        assert len(args) >= 2, 'If df is not given, _src_fldr and file_name should be provided'
        _src_fldr = args[0]
        _file_name = args[1]
        file_addr = os.path.join(_src_fldr, _file_name)
        df, features = get_dataset_prepared(
            file_addr,
            _n_rows=_n_rows,
            _do_scale=_do_scale,
            drop_label=drop_label,
            **kwargs
        )
        logger_.info('Dataframe is loaded, now converting to np array')
    else:
        df = args[0]

    # BorutaPy accepts numpy arrays only
    y = df['Attack'].values
    y = y.ravel()
    df.drop('Attack', axis=1, inplace=True)
    feat = list(df.columns)
    X = df.values

    logger_.info('Running Borutapy for feature selection')
    rf = RandomForestClassifier(
        n_jobs=-1,
        class_weight='balanced',
        max_depth=5
    )
    if 'max_iter' in kwargs:
        max_iter = kwargs['max_iter']
    else:
        max_iter = 100
    feat_selector = BorutaPy(
        rf,
        n_estimators='auto',
        verbose=2,
        random_state=1,
        max_iter=max_iter
    )
    feat_selector.fit(X, y)
    # feat_selector.support_ is the mask
    rankings = feat_selector.ranking_
    logger_.info(f'feat_selector.ranking_: {rankings}')
    selected_feat = [f for f, fr in zip(feat, rankings) if fr == 1]

    logger_.info(f'Selected features: {selected_feat}')

    return feat, selected_feat, rankings






# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def bufs_boiler_plate(_src_fldr, _file_name, *args, _n_rows=None, _do_scale=True, _n_features=-1, **kwargs):
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,fg_blue,bg_yellow'


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
    tr_df = df[~df.index.isin(tst_df.index)]
    tst_df.reset_index(drop=True, inplace=True)
    tr_df.reset_index(drop=True, inplace=True)

    attacks = list(df['Attack'].unique())
    if 'Benign' in attacks:
        attacks.remove('Benign')
    attacks.sort()
    # select_feat_dict = dict.fromkeys(attacks)
    if 'Attack' in features:
        features.remove('Attack')
    feature_ranks_df = pd.DataFrame(0, columns=features, index=attacks, dtype=int)
    for attack in attacks:
        logger_.info(f'Selecting features for TRAINING SETS, attack class {attack}')
        tr_df_attack = tr_df.loc[tr_df['Attack'] != attack, :]
        tr_df_attack.reset_index(drop=True, inplace=True)
        logger_.info(f'attack class {attack} is removed')

        all_features, _ , ranks = BorutaPy_feature_select(tr_df_attack, **kwargs)
        assert list(feature_ranks_df.columns) == all_features, 'Features are not equal in and out'
        feature_ranks_df.loc[attack, :] = ranks
        logger_.info(f'Selected features for attack class {attack} are now computed')

        if 'save_fldr' in kwargs:
            if _n_rows is None:
                rows_num = 'whole'
            else:
                rows_num = _n_rows
            _save_fldr = kwargs['save_fldr']
            save_addr = os.path.join(_save_fldr,
                                     f'selected_features_per_attack_dict_{rows_num}_rows.pickle')
            with open(save_addr, 'wb') as f:
                pickle.dump(feature_ranks_df, f, protocol=-1)
                logger_.info(f'Features selected for all attacks are saved to {save_addr}')

    # for test set, i.e. all classes together
    logger_.info(f'Selecting features for TEST SET, including all classes together')
    all_features, _, ranks = BorutaPy_feature_select(tst_df, **kwargs)
    assert list(feature_ranks_df.columns) == all_features, 'Features are not equal in and out'
    feature_ranks_df.loc['all_classes',:] = ranks

    if 'save_fldr' in kwargs:
        if _n_rows is None:
            rows_num = 'whole'
        else:
            rows_num = _n_rows
        _save_fldr = kwargs['save_fldr']
        save_addr = os.path.join(_save_fldr,
                                 f'selected_features_per_attack_dict_{rows_num}_rows.pickle')
        with open(save_addr, 'wb') as f:
            pickle.dump(feature_ranks_df, f, protocol=-1)
            logger_.info(f'Features selected for all attacks are saved to {save_addr}')





# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
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
    do_scale = False
    n_features = -1
    logger.info(f'number of selected features: '
                f'{n_features if n_features != -1 else "all features"}')

    bufs_boiler_plate(
        src_fldr,
        file_name,
        _n_rows=n_rows,
        _do_scale=do_scale,
        _n_features=n_features,
        logger=logger,
        max_iter=50,
        # drop_attack_classes=['Benign'],
        columns_2_drop=columns_2_drop,
        save_fldr=save_fldr
    )

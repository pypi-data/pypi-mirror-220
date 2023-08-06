import inspect
import os
import warnings
import pandas as pd
import _pickle as pickle
from sklearn.ensemble import RandomForestClassifier
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
def randomforest_feature_importance(*args, _n_rows=None, _do_scale=True, drop_label=True, **kwargs):
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

    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,fg_blue,bg_black'


    if 'seed' in kwargs:
        seed_ = kwargs['seed']
    else:
        seed_ = 0

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
    y = df['Label'].values
    # y = df['Attack'].values
    y = y.ravel()
    df.drop('Label', axis=1, inplace=True)
    # df.drop('Attack', axis=1, inplace=True)
    X = df.values

    logger_.info('Running Random Forest for feature importance')
    rf_classifier = RandomForestClassifier(
        n_jobs=-1,
        class_weight='balanced',
        max_depth=5,
        random_state=seed_
    )

    rf_classifier.fit(X, y)
    feature_importances = rf_classifier.feature_importances_
    # feat_selector.support_ is the mask
    logger_.info(f'feature importances: {feature_importances}')

    return feature_importances






# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
@logger_cleaner
def bufs_boiler_plate(_src_fldr, _file_name, _n_rows=None, _do_scale=True, _n_features=-1, **kwargs):
    func_name = inspect.stack()[0][3]
    logger_ = kwargs['logger']

    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,fg_blue,bg_yellow'


    file_addr = os.path.join(_src_fldr, _file_name)
    df, features = get_dataset_prepared(
        file_addr,
        _n_rows=_n_rows,
        _do_scale=_do_scale,
        drop_label=False,
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
    # tst_df.drop('Label', axis=1, inplace=True)
    tr_df = df[~df.index.isin(tst_df.index)]
    tst_df.reset_index(drop=True, inplace=True)
    tr_df.reset_index(drop=True, inplace=True)

    attacks = list(df['Attack'].unique())
    if 'Benign' in attacks:
        attacks.remove('Benign')
    attacks.sort()
    features.remove('Attack')
    features.remove('Label')
    feature_importance_df = pd.DataFrame(columns=features, dtype=float)

    for attack in attacks:
        logger_.info(f'Selecting features for TRAINING SETS, attack class {attack}')
        tr_df_attack = tr_df.loc[tr_df['Attack'] != attack, :]
        tr_df_attack.drop('Attack', axis=1, inplace=True)
        # tr_df_attack.drop('Label', axis=1, inplace=True)
        tr_df_attack.reset_index(drop=True, inplace=True)
        logger_.info(f'attack class {attack} is removed')
        tr_df_attack_columns = list(tr_df_attack.columns)
        tr_df_attack_columns.remove('Label')
        # tr_df_attack_columns.remove('Attack')
        assert list(tr_df_attack_columns) == features, 'features and tr_df_attack_columns does not match'

        feature_importances = randomforest_feature_importance(tr_df_attack, seed=seed_, **kwargs)
        feature_importance_df.loc[attack, :] = feature_importances
        logger_.info(f'Selected features for attack class {attack} are now computed')

        if 'save_fldr' in kwargs:
            if _n_rows is None:
                rows_num = 'all'
            else:
                rows_num = _n_rows
            _save_fldr = kwargs['save_fldr']
            save_addr = os.path.join(_save_fldr,
                                     f'features_importances_per_attack_df_{rows_num}_rows.pickle')
            with open(save_addr, 'wb') as f:
                pickle.dump(feature_importance_df, f, protocol=-1)
                logger_.info(f'Features importances for attack {attack} are now saved to {save_addr}')

    # for test set, i.e. all classes together
    logger_.info(f'Selecting features for TEST SET, including all classes together')
    tst_df_columns = list(tst_df.columns)
    tst_df_columns.remove('Label')
    # tst_df_columns.remove('Attack')
    assert list(tst_df_columns) == features, 'features and tr_df_attack_columns does not match'
    feature_importances = randomforest_feature_importance(tst_df, seed=seed_, **kwargs)
    feature_importance_df.loc['all_classes', :] = feature_importances

    if 'save_fldr' in kwargs:
        if _n_rows is None:
            rows_num = 'all'
        else:
            rows_num = _n_rows
        _save_fldr = kwargs['save_fldr']
        save_addr = os.path.join(_save_fldr,
                                 f'features_importances_per_attack_df_{rows_num}_rows.pickle')
        with open(save_addr, 'wb') as f:
            pickle.dump(feature_importance_df, f, protocol=-1)
            logger_.info(f'Features selected for all attacks are saved to {save_addr}')





# ---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**---**
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    src_fldr = '/storage/datasets/NetFlow/csv'
    save_fldr = '/home/nids1/Desktop/ZSL_visualizations/'
    pickle_fdlr = save_fldr
    file_name = 'NF-UNSW-NB15-v2.csv'
    n_rows = [1_000_000, None][1]
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
        # drop_attack_classes=['Benign'],
        save_fldr=save_fldr
    )

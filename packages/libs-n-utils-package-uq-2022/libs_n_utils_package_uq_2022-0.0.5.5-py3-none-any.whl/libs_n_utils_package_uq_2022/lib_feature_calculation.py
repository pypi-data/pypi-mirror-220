
import _pickle as pickle
import feather
import pandas as pd
import config_template
import os
from datetime import datetime
from .my_easy_logger import logger_cleaner
from .config_template import NetFlow_fields
from .lib_file_manipulation import create_ReadMe

param_dic = config_template.plot_parameters.CDFplot_params_dic
groupby_features = config_template.features.groupby_features
features_class = config_template.features()



#     fields = 0-FIRST_SWITCHED, 1-IN_BYTES, 2-IN_PKTS, 3-IPV4_DST_ADDR, 4-IPV4_SRC_ADDR,
#              5-L4_DST_PORT, 6-L4_SRC_PORT, 7-L7_PROTO_NAME, 8-LAST_SWITCHED, 9-OUT_BYTES,
#              10-OUT_PKTS, 11-ROTOCOL


@logger_cleaner
def features_calculation(_df, _feature_list, *args, _unidirect_flow=True, **kwargs):
    """
    :param _df: The dataframe including netflow or other formats of nids datasets
    :param _feature_list: list of feature to be calculated
    :param _unidirect_flow: are flows included in this dataset unidirectional?
    :param kwargs:
    :return: _df that includes the calculated features
    """

    logger_ = kwargs['logger']
    logger_.handlers[0].formatter.log_colors['INFO'] = 'bold,fg_yellow,bg_black'
    logger_.setLevel('DEBUG')

    fields = NetFlow_fields.fields[:]
    netflow = NetFlow_fields()
    nob, nop, nib, nip, nfs, nls, nl7, nsi, ndi, nsp, ndp, npo = netflow.field_numbers()

    # removing entries with out_bytes=0
    if _unidirect_flow is True:
        if fields[nob] in _df.columns or fields[nop] in _df.columns:
            rows = _df.loc[(_df[fields[nob]] == 0) | (_df[fields[nop]] == 0)]
            n_rows_before = _df.shape[0]
            _df.drop(rows.index, inplace=True)
            # after dropping rows, re-indexing is needed
            _df.reset_index(drop=True, inplace=True)
            n_rows_after = _df.shape[0]
            n_removed_rows = n_rows_before - n_rows_after
            removed_rows_percentage = (n_removed_rows / n_rows_before) * 100
            logger_.debug(f"Number of removed zero OUT_BYTES or OUT_PKTS rows "
                         f"{n_removed_rows} -> "
                         f"({removed_rows_percentage:.2f}%)")

        # removing entries with in_bytes=0
        if fields[nib] in _df.columns or fields[nip] in _df.columns:
            rows = _df.loc[(_df[fields[nib]] == 0) | (_df[fields[nip]] == 0)]
            n_rows_before = _df.shape[0]
            _df.drop(rows.index, inplace=True)
            # after dropping rows, re-indexing is needed
            _df.reset_index(drop=True, inplace=True)
            n_rows_after = _df.shape[0]
            n_removed_rows = n_rows_before - n_rows_after
            removed_rows_percentage = (n_removed_rows / n_rows_before) * 100
            logger_.debug(f"Number of removed zero IN_BYTES or IN_PKTS rows "
                         f"{n_removed_rows} -> "
                         f"({removed_rows_percentage:.2f}%)")

    for feature in _feature_list:
        if feature == 'flow_duration':
            logger_.info(f' Computing {feature} using ({fields[nls]} - {fields[nfs]})')
            _df.eval(f'{feature} = {fields[nls]}-{fields[nfs]}', inplace=True)

        elif feature == 'Total_packet':
            logger_.info(f' Computing {feature} using ({fields[nip]} + {fields[nop]})')
            _df.eval(f'{feature} = ({fields[nip]}+{fields[nop]})', inplace=True)

        elif feature == 'IN_packet_size':
            logger_.info(f' Computing {feature} using ({fields[nib]} / {fields[nip]})')
            _df.eval(f'{feature} = {fields[nib]} / {fields[nip]}', inplace=True)

        elif feature == 'OUT_packet_size':
            logger_.info(f' Computing {feature} using ({fields[nob]} / {fields[nop]})')
            _df.eval(f'{feature} = {fields[nob]} / {fields[nop]}', inplace=True)

        elif feature == 'Total_packet_size':
            logger_.info(f' Computing {feature} using ({fields[nib]}+{fields[nob]}) / ({fields[nip]}+{fields[nop]})')
            _df.eval(f'{feature} = ({fields[nib]}+{fields[nob]}) / ({fields[nip]}+{fields[nop]})', inplace=True)

        elif feature == 'avg_Total_packet_duration':
            logger_.info(f' Computing {feature} using ({fields[nls]}-{fields[nfs]}) / ({fields[nip]}+{fields[nop]})')
            _df.eval(f'{feature} = ({fields[nls]}-{fields[nfs]}) / ({fields[nip]}+{fields[nop]})', inplace=True)

        elif feature == 'Total_flow_size':
            logger_.info(f' Computing {feature} using ({fields[nib]} + {fields[nob]})')
            _df.eval(f'{feature} = {fields[nib]} + {fields[nob]}', inplace=True)

        elif feature == 'packet_symmetry':
            logger_.info(f' Computing {feature} using abs(log(({fields[nip]}+1 )/ ({fields[nop]}+1)))')
            _df.eval(f'{feature} = abs(log(({fields[nip]}+1 )/ ({fields[nop]}+1)))', inplace=True)

        elif feature in groupby_features:
            f0, f1 = features_class.feature_fields(feature)
            logger_.info(f' Computing {feature} using df_.groupby({fields[f0]})[{fields[f1]}].nunique()')
            series = _df.groupby(fields[f0])[fields[f1]].nunique()
            series = series.reset_index()
            _df[[fields[f0], fields[f1]]] = series

    return _df




# --~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--^^--~~----~~--
@logger_cleaner
def compute_netflow_features(_src_fldr, _dst_fldr, _feature, _file_type, ds_name=None, **kwargs):
    """
    :param _src_fldr:
    :param _dst_fldr:
    :param _feature:
    :param _file_type:
    :param ds_name:
    :param kwargs:
    :return:
    """
    logger_ = kwargs['logger']
    netflow = NetFlow_fields()
    fields = netflow.fields[:]

    os.makedirs(_dst_fldr, exist_ok=True)
    date_str = datetime.now().strftime("%Y%h%d_%H%M%S")
    create_ReadMe(_dst_fldr, filename_=f'{__file__}_{date_str}.txt')

    file_list = os.listdir(_src_fldr)
    file_list = [x for x in file_list if x.split('.')[-1] == _file_type]
    file_list.sort()

    vc = pd.Series()
    per_file_dict = dict()
    per_file_stat_df = pd.DataFrame()
    mass_distribution_dict = dict()

    f0, f1 = features_class.feature_fields(_feature)
    selected_cols = [*f0, *f1] if f0.__class__ == list else [f0, f1]
    selected_fields = [fields[x] for x in selected_cols]

    if _feature in groupby_features:
        number = 0
        for file_name in file_list:
            file_address = os.path.join(_src_fldr, file_name)
            if ds_name == 'Comscentre2017' and file_name.split('.')[-2] != '26':
                logger_.debug(f'dataset {ds_name} is ignored')
                continue
            logger_.info(f'Reading file {file_name}')
            df = feather.read_dataframe(file_address, columns=selected_fields)
            logger_.info(f'Calculating feature {_feature}')

            if number == 0:
                vc = df.groupby(fields[f0])[fields[f1]].value_counts()
                per_file_dict[file_name] = vc
                idx = vc.index
                summarized_columns = pd.DataFrame([*idx], columns=idx.names)
                mass_distribution = summarized_columns.groupby(idx.names[0]).nunique()
                stats = mass_distribution.describe()
                per_file_stat_df.loc[:, file_name] = stats.iloc[:, 0]
            else:
                tmp = df.groupby(fields[f0])[fields[f1]].value_counts()
                per_file_dict[file_name] = tmp
                idx = tmp.index
                summarized_columns = pd.DataFrame([*idx], columns=idx.names)
                mass_distribution = summarized_columns.groupby(idx.names[0]).nunique()
                stats = mass_distribution.describe()
                per_file_stat_df.loc[:, file_name] = stats.iloc[:, 0]
                vc = vc.add(tmp, fill_value=0)

            number += 1
            mass_distribution_dict[file_name] = mass_distribution

        per_file_dict['all_files'] = vc
        idx = vc.index
        summarized_columns = pd.DataFrame([*idx], columns=idx.names)
        mass_distribution = summarized_columns.groupby(idx.names[0]).nunique()
        mass_distribution_dict['all_files_mass_distribution'] = mass_distribution
        stats = mass_distribution.describe()
        per_file_stat_df.loc[:, 'all_files'] = stats.iloc[:, 0]
    else:
        number = 0
        for file_name in file_list:
            file_address = os.path.join(_src_fldr, file_name)
            if ds_name == 'Comscentre2017' and file_name.split('.')[-2] != '26':
                logger_.debug(f'dataset {ds_name} is ignored')
                continue
            logger_.info(f'Reading file {file_name}')
            df = feather.read_dataframe(file_address, columns=selected_fields)
            logger_.info(f'Calculating feature {_feature}')

            if _feature == 'flow_duration':
                logger_.info(f' Computing {_feature} using ({fields[f1]} - {fields[f0]})')
                df.eval(f'{_feature} = {fields[f1]}-{fields[f0]}', inplace=True)

            elif _feature == 'Total_packet':
                logger_.info(f' Computing {_feature} using ({fields[f1]} + {fields[f0]})')
                df.eval(f'{_feature} = ({fields[f1]}+{fields[f0]})', inplace=True)

            elif _feature == 'IN_packet_size':
                logger_.info(f' Computing {_feature} using ({fields[f1]} / {fields[f0]})')
                df.eval(f'{_feature} = {fields[f1]} / {fields[f0]}', inplace=True)

            elif _feature == 'OUT_packet_size':
                logger_.info(f' Computing {_feature} using ({fields[f1]} / {fields[f0]})')
                df.eval(f'{_feature} = {fields[f1]} / {fields[f0]}', inplace=True)

            elif _feature == 'Total_packet_size':
                logger_.info(f' Computing {_feature} using ({fields[f1[1]]}+{fields[f1[0]]}) / ({fields[f0[0]]}+{fields[f0[1]]})')
                df.eval(f'{_feature} = ({fields[f1[0]]}+{fields[f1[1]]}) / ({fields[f0[0]]}+{fields[f0[1]]})', inplace=True)

            elif _feature == 'avg_Total_packet_duration':
                logger_.info(f' Computing {_feature} using ({fields[f1[1]]}-{fields[f1[0]]}) / ({fields[f0[1]]}+{fields[f0[0]]})')
                df.eval(f'{_feature} = ({fields[f1[1]]}-{fields[f1[0]]}) / ({fields[f0[1]]}+{fields[f0[0]]})', inplace=True)

            elif _feature == 'Total_flow_size':
                logger_.info(f' Computing {_feature} using ({fields[f1]} + {fields[f0]})')
                df.eval(f'{_feature} = {fields[f1]} + {fields[f0]}', inplace=True)

            elif _feature == 'packet_symmetry':
                logger_.info(f' Computing {_feature} using abs(log(({fields[f1]}+1 )/ ({fields[f0]}+1)))')
                df.eval(f'{_feature} = abs(log(({fields[f1]}+1 )/ ({fields[f0]}+1)))', inplace=True)

            if number == 0:
                mass_distribution = df[_feature]
                per_file_stat_df.loc[:, file_name] = mass_distribution.describe()
                mass_distribution = pd.DataFrame(mass_distribution)
                mass_distribution_dict[file_name] = mass_distribution
            else:
                tmp = df[_feature]
                per_file_stat_df.loc[:, file_name] = tmp.describe()
                tmp = pd.DataFrame(tmp)
                per_file_dict[file_name] = tmp
                mass_distribution_dict[file_name] = tmp
                mass_distribution = pd.concat([mass_distribution, tmp], axis=0)

            number += 1


        per_file_dict['all_files'] = None
        mass_distribution_dict['all_files_mass_distribution'] = mass_distribution
        stats = mass_distribution.describe()
        per_file_stat_df.loc[:, 'all_files'] = stats.iloc[:, 0]


    prefix = '' if 'n_rows' not in kwargs else kwargs['n_rows'] +\
             _src_fldr.split('/')[-1] if 'save_name' not in kwargs else kwargs['save_name']


    save_name_ds_summary = f"{_feature}{prefix}.pickle"
    save_addr0 = os.path.join(_dst_fldr, save_name_ds_summary)
    with open(save_addr0, 'wb') as f:
        pickle.dump(per_file_dict, f, protocol=-1)
        logger_.info(f'per_file_dict saved to {save_addr0}')

    save_name_mass = f"mass_distribution_{_feature}{prefix}.pickle"
    save_addr2 = os.path.join(_dst_fldr, save_name_mass)
    with open(save_addr2, 'wb') as f:
        pickle.dump(mass_distribution_dict, f, protocol=-1)
        logger_.info(f'mass_distribution_dict saved to {save_addr2}')

    save_name_stats = f"stat_{_feature}{prefix}.pickle"
    save_addr1 = os.path.join(_dst_fldr, save_name_stats)
    with open(save_addr1, 'wb') as f:
        pickle.dump(per_file_stat_df, f, protocol=-1)
        logger_.info(f'stat_df saved to {save_addr1}')

    return per_file_dict, mass_distribution_dict, per_file_stat_df






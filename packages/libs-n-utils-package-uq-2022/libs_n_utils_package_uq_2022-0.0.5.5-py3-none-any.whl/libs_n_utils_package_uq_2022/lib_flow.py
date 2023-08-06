import inspect
import pandas as pd
import os

from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]
info_log_color = 'blue,bg_white'




# ######################################################################################################################
def flows_period(dataframe=None):
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)
    logger_.info('choosing the columns from dataframe ...')
    fields = ['SRC_VLAN', 'FIRST_SWITCHED', 'LAST_SWITCHED']
    df = dataframe.loc[:, fields]
    del dataframe
    df.loc[:, 'FLOW_PERIOD'] = df[fields[2]] - df[fields[1]]
    total_flow_periods = df['FLOW_PERIOD'].values
    Vlan_df = pd.Series(df.groupby('SRC_VLAN')['FLOW_PERIOD'])
    Vlan_Ids = []
    Vlan_flow_periods = []
    logger_.info('computing flow periods for vlans ...')
    for v_id, flow_p in Vlan_df:
        Vlan_Ids.append(v_id)
        Vlan_flow_periods.append(list(flow_p))

    Vlan_flow_periods.append([total_flow_periods])
    Vlan_Ids.append('Comscentre')
    return Vlan_Ids, Vlan_flow_periods




# ######################################################################################################################
def flow_size_distribution(dataframe=None):
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)
    logger_.info('Starting the process of IN_BYTES for vlans ...')
    df = dataframe.loc[:, ['SRC_VLAN', 'IN_BYTES']]
    del dataframe
    total_inBYTES = df['IN_BYTES'].values
    Vlan_df = pd.Series(df.groupby('SRC_VLAN')['IN_BYTES'])
    Vlan_Ids = []
    Vlan_inBYTES = []
    logger_.info('appending vlans ...')
    for v_id, IN_BYTES in Vlan_df:
        Vlan_Ids.append(v_id)
        Vlan_inBYTES.append(list(IN_BYTES))

    Vlan_inBYTES.append([total_inBYTES])
    Vlan_Ids.append('Comscentre')
    return Vlan_Ids, Vlan_inBYTES




# ######################################################################################################################
def packet_sizes_per_group(dataframe_=None, fields_=None, total_group_name=None):
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)
    logger_.info('choosing the columns from dataframe ...')
    if fields_ is None:
        fields_ = ['SRC_VLAN', 'IN_BYTES', 'IN_PKTS']
    df = dataframe_.loc[:, fields_]
    del dataframe_
    df.loc[:, 'IN_PKT_SIZE'] = df[fields_[-2]] / df[fields_[-1]]

    grouped_df = pd.Series(df.groupby(fields_[:-2])['IN_PKT_SIZE'])
    Grouped_Ids = []
    Grouped_Packet_Sizes = []
    logger_.info('computing packet sizes for grouped fields ...')
    for g_id, pkt_sizes in grouped_df:
        Grouped_Ids.append(g_id)
        Grouped_Packet_Sizes.append(list(pkt_sizes))
    if total_group_name is not None:
        total_inPKT_Sizes = df['IN_PKT_SIZE'].values
        Grouped_Packet_Sizes.append([total_inPKT_Sizes])
        Grouped_Ids.append(total_group_name)
    return Grouped_Ids, Grouped_Packet_Sizes

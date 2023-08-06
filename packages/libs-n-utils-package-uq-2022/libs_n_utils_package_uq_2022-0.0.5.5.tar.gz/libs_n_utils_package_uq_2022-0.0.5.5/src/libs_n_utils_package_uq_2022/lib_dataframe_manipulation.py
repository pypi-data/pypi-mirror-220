import inspect
import numpy as np
import os

from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]
info_log_color = 'fg_bold_purple,bg_white'


# ######################################################################################################################
def nunique_groups(dataframe, field_list, value_field=None, log_msg=None):
    if log_msg is None:
        log_msg = 'nunique_groups function started ...'
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)
    logger_.info(log_msg)
    if value_field is None:
        value_field = field_list[-1]
    agg_field_list = [x for x in field_list if x != value_field]
    df = dataframe.loc[:, field_list]
    del dataframe
    unique_count = df.groupby(agg_field_list)[value_field].nunique()

    return unique_count



# ######################################################################################################################
def dataframe_column_combiner(dataframe_tobe_combined=None, new_column=None,
                              new_rows=None, new_column_name=None):
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)

    total_rows = dataframe_tobe_combined.index
    dataframe_tobe_combined[new_column_name] = [[]] * len(dataframe_tobe_combined.index)
    fresh_rows = set(new_rows) - set(total_rows)
    total_rows = set(total_rows).union(set(fresh_rows))
    if len(fresh_rows) is not 0:
        for row in fresh_rows:
            dataframe_tobe_combined.loc[row] = [[]] * len(dataframe_tobe_combined.columns)

    logger_.info('parsing rows ...')
    for row in total_rows:
        if row in new_rows:
            list_index = new_rows.index(row)
            dataframe_tobe_combined.loc[row, new_column_name] = new_column[list_index]

    return dataframe_tobe_combined





# ######################################################################################################################
def dataframe_column_unifier(dataframe_tobe_combined=None, new_column=None, new_rows=None):
    k0 = dataframe_tobe_combined.keys()[0]
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)

    total_rows = dataframe_tobe_combined.index
    # dataframe_tobe_combined['Total'] = [[]] * len(dataframe_tobe_combined.index)
    fresh_rows = set(new_rows) - set(total_rows)
    total_rows = set(total_rows).union(set(fresh_rows))
    if len(fresh_rows) is not 0:
        for row in fresh_rows:
            dataframe_tobe_combined.loc[row] = [[]] * len(dataframe_tobe_combined.columns)

    logger_.info('parsing rows ...')
    for row in total_rows:
        if row in new_rows:
            list_index = new_rows.index(row)
            dataframe_tobe_combined.loc[row, k0] += new_column[list_index]

    return dataframe_tobe_combined





# ######################################################################################################################
def dataframe_row_sampler(original_dataframe, sampling_percentage, seed_=0):
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)


    np.random.seed(seed_)
    n_rows = original_dataframe.shape[0]
    n_new_rows = int(n_rows*sampling_percentage)
    # random_rows = np.random.randint(0, n_rows, n_new_rows) #it had repetition
    random_rows = np.random.choice(range(1, n_rows-1), size=n_new_rows, replace=False)
    random_rows = list(random_rows)
    random_rows.sort()
    sampled_dataframe = original_dataframe.loc[random_rows]
    return sampled_dataframe



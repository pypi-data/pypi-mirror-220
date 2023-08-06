import os
import inspect

from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]
info_log_color = 'black,bg_white'



# ######################################################################################################################
def get_figures_params(filename_, n_day_, base_save_folder_, df_type_, title_msg_):
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=inspect.stack()[0][3],
                        info_c=info_log_color)
    logger_.info(f'Creating parameters of figure of file {filename_}')
    index_name_ = f'nprobe-2017.07.{n_day_:02}'
    title_text_ = f'{title_msg_} on {index_name_}' +\
                  (f'[during first 10000 flows of each day]'
                   if df_type_ is 'csv' else '')
    save_folder_ = f'{base_save_folder_}' +\
                   ('/first10000flows' if df_type_ is 'csv'
                    else '/daily_counts')
    os.makedirs(save_folder_, exist_ok=True)
    figure_save_address_ = save_folder_ + \
                           f'/{filename_}-2017-07-{n_day_}' + \
                           (f'[10K-flows]' if df_type_ is 'csv'
                            else '') + '.png'

    return index_name_, title_text_, save_folder_, figure_save_address_








import os
import numpy as np
import _pickle as pickle
from .intra_dataset_feature_wasserstein import plot_wasserstein_table
from .lib_plotters import draw_bar_chart
from .my_easy_logger import my_logger

script_name = os.path.split(__file__)[1]






# Main -----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    logger = my_logger(
        reporter_file_name=script_name,
        info_c='bold_cyan',
        reporter_func_name=__name__,
        log_level='debug'
    )

    src_fldr = '/home/nids1/Desktop/ZSL_visualizations/'
    file_name = 'Wasserstein_NF-UNSW-NB15-v2_whole_rows_39_features.pickle'

    file_addr = os.path.join(src_fldr, file_name)

    with open(file_addr, 'rb') as f:
        overall_dict = pickle.load(f)

    features = list(overall_dict.keys())
    features.remove('groups')
    tick_labels = overall_dict['groups']
    average_array = np.zeros(overall_dict[features[0]].shape)
    for feature in features:
        feature_array = overall_dict[feature]
        normalized_feature_array = feature_array / np.max(feature_array)
        average_array += normalized_feature_array

    average_array = average_array / len(features)
    plot_wasserstein_table(
        average_array,
        tick_labels,
        logger=logger,
        _save_fldr=src_fldr,
        save_name='average_WS_whole_dataset.pdf'
    )

    average_ws = np.mean(average_array, axis=0)
    x_values = list(range(len(average_ws)))
    xticks_rotation_dic = {
        'rotation_mode': "anchor",
        'ha': "center"
    }

    save_addr = os.path.join(src_fldr, 'averaged_average_WS_whole_dataset.pdf')
    draw_bar_chart(x_values, average_ws, _save_address=save_addr, _xlabel='Attacks',
                   _ylabel='Average Wasserstein Distance', _xticks=x_values, _xticks_rotation_dic=xticks_rotation_dic,
                   _xtick_labels=tick_labels)











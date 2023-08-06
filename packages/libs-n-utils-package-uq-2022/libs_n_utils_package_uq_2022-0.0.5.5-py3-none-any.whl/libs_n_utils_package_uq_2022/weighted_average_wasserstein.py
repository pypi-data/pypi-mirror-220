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

    n_rows = 'whole'
    extra = '_without_Benign_Shellcode_Worms'
    n_feature = 39
    src_fldr = '/home/nids1/Desktop/ZSL_visualizations/'
    # ws_file_name = f'Wasserstein_NF-UNSW-NB15-v2_{n_rows}_rows_{n_feature}_features{extra}.pickle'
    ws_file_name = 'Wasserstein_NF-UNSW-NB15-v2_whole_rows_39_features_.pickle'
    # fi_file_name = f'feature_importance_using_mi_{n_feature}_features_NF-UNSW-NB15-v2_{n_rows}_rows{extra}.pickle'
    fi_file_name = 'feature_importance_using_mi_39_features_NF-UNSW-NB15-v2_whole_rows.pickle'


    ws_file_addr = os.path.join(src_fldr, ws_file_name)
    with open(ws_file_addr, 'rb') as f:
        overall_ws_dict = pickle.load(f)

    fi_file_addr = os.path.join(src_fldr, fi_file_name)
    with open(fi_file_addr, 'rb') as f:
        fi_dict = pickle.load(f)

    features = list(overall_ws_dict.keys())
    features.remove('groups')
    features.sort()
    tick_labels = overall_ws_dict['groups']
    tick_labels.sort()
    attacks = list(fi_dict.keys())
    attacks.remove('features')
    attacks.sort()
    assert attacks == tick_labels, "The attack in WS dict and FI dict are not similar"
    features_ = fi_dict['features']
    features_.sort()
    assert features_ == features, "The features in WS dict and FI dict are not similar"

    average_array = np.zeros(overall_ws_dict[features[0]].shape)
    for attack in attacks:
        weights = fi_dict[attack]
        for k, feature in enumerate(features):
            weight = weights[k]
            feature_array = overall_ws_dict[feature] * weight
            average_array += feature_array

        average_array = average_array / len(features)
        average_array = average_array / np.max(average_array)
        save_name = f'MI_Weighted_average_WS_{attack}_vs_all.pdf'
        plot_wasserstein_table(average_array, tick_labels,
                               logger=logger,
                               cbar_label=f'Averaged Wasserstein Distance ({attack})',
                               _save_fldr=src_fldr,
                               save_name=save_name
                               )

        average_ws = np.mean(average_array, axis=0)
        x_values = list(range(len(average_ws)))
        xticks_rotation_dic = {
            'rotation_mode': "anchor",
            'ha': "center"
        }

        save_addr = os.path.join(src_fldr, f'averaged_MI_weighted_average_WS_{attack}_vs_all.pdf')
        draw_bar_chart(x_values, average_ws, _save_address=save_addr, _xlabel='Attacks',
                       _ylabel=f'Averaged Wasserstein Distance ({attack} vs all)', _xticks=x_values,
                       _xticks_rotation_dic=xticks_rotation_dic, _ylabel_fontweight='bold', _xlabel_fontweight='bold',
                       _xtick_labels=tick_labels)

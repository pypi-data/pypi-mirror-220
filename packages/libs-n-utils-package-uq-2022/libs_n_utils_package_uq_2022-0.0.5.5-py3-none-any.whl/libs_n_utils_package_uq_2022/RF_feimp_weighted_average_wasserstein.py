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
    ws_file_name = 'Wasserstein_NF-UNSW-NB15-v2_whole_rows_39_features.pickle'
    fi_file_name = 'features_importances_per_attack_df_all_rows.pickle'

    ws_file_addr = os.path.join(src_fldr, ws_file_name)
    with open(ws_file_addr, 'rb') as f:
        overall_ws_dict = pickle.load(f)

    fi_file_addr = os.path.join(src_fldr, fi_file_name)
    with open(fi_file_addr, 'rb') as f:
        feat_impo_df = pickle.load(f)

    features = list(overall_ws_dict.keys())
    features.remove('groups')
    features.sort()
    tick_labels = overall_ws_dict['groups']
    tick_labels.sort()
    attacks = list(feat_impo_df.index)
    attacks.remove('all_classes')
    attacks.sort()
    assert attacks == tick_labels, "The attack in WS dict and FI dict are not similar"

    feat_impo_df = feat_impo_df.reindex(sorted(feat_impo_df.columns), axis=1)
    features_ = list(feat_impo_df.columns)
    assert features_ == features, "The features in WS dict and FI dict are not similar"

    average_array = np.zeros(overall_ws_dict[features[0]].shape)
    average_array_dict = dict.fromkeys(attacks)
    for attack in attacks:
        for feature in features:
            feature_array = overall_ws_dict[feature]
            feature_array = feature_array / np.max(feature_array)
            weight = feat_impo_df.loc[attack, feature]
            logger.info(f'weight for feature {feature} equals to: {weight}')
            weighted_feature_array = feature_array * weight
            average_array += weighted_feature_array

        average_array_dict[attack] = average_array / np.max(average_array)
        save_name = f'RF_Weighted_average_WS_{attack}_vs_all.pdf'
        plot_wasserstein_table(average_array_dict[attack], tick_labels,
                               logger=logger,
                               cbar_label=f'Averaged Wasserstein Distance ({attack})',
                               _save_fldr=src_fldr,
                               # save_name=save_name
                               )

        average_ws = np.mean(average_array, axis=0)
        x_values = list(range(len(average_ws)))
        xticks_rotation_dic = {
            'rotation_mode': "anchor",
            'ha': "center"
        }

        save_addr = os.path.join(src_fldr, f'averaged_RF_weighted_average_WS_{attack}_vs_all.pdf')
        draw_bar_chart(x_values, average_ws, _xlabel='Attacks', #_save_address=save_addr,
                       _ylabel=f'Averaged Wasserstein Distance ({attack} vs all)', _xticks=x_values,
                       _xticks_rotation_dic=xticks_rotation_dic, _ylabel_fontweight='bold',
                       _xlabel_fontweight='bold', _xtick_labels=tick_labels)

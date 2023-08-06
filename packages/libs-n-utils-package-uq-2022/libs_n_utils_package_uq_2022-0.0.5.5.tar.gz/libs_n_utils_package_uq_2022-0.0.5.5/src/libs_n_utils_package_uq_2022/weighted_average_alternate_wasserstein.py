"""
This script takes two files
atws_file_name: the wasserstein distances computed in the alternative way, i.e.
the difference between z-attack training sets and the test set.

fi_file_name: the featue importance values, that can be either of MI-based or RF-based

If we need the raw/pure (not-weighted) average, then we can comment lines related to feature importance
and use
# multiplied_atws_df = overall_atws_df * feat_impo_df
multiplied_atws_df = overall_atws_df

to go without weights
"""


import os
import pickle
from .lib_plotters import draw_bar_chart
import pandas as pd


# src_fldr = '/home/nids1/Desktop/ZSL_visualizations/NetFlow/'
# save_fldr = '/home/nids1/Desktop/ZSL_visualizations/alternate_feature_wasserstein/'
src_fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds/src/'
save_fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds'

# atws_file_name = 'Alternate_Wasserstein_NF-UNSW-NB15-v2_whole_rows_39_features.pickle'
atws_file_name = 'Alternate_Wasserstein_UNSW-NB15_whole_rows_43_features.pickle'
# atws_file_name = 'Alternate_Wasserstein_UNSW-NB15_whole_rows_41_features.pickle'
# fi_file_name = 'features_importances_per_attack_df_all_rows.pickle'
# fi_file_name = 'feature_importance_using_mi[mutual_info_classif]_39_features_NF-UNSW-NB15-v2_whole_rows.pickle'
# fi_file_name = 'feature_importance_using_mi_39_features_NF-UNSW-NB15-v2_whole_rows.pickle'
# fi_file_name = 'UNSW_NB15_unity_feature_importance_weight.pickle'
fi_file_name = 'feature_importance_using_mi_[mutual_info_classif]_43_features_UNSW-NB15_whole_rows.pickle'
from_mi = True

ws_file_addr = os.path.join(src_fldr, atws_file_name)
with open(ws_file_addr, 'rb') as f:
    overall_atws_df = pickle.load(f)

fi_file_addr = os.path.join(src_fldr, fi_file_name)
with open(fi_file_addr, 'rb') as f:
    feat_impo_df = pickle.load(f)

if from_mi:
    features = feat_impo_df.pop('features')
    feat_impo_df = pd.DataFrame.from_dict(
        feat_impo_df,
        orient='index',
        columns=features
    )


tick_labels = list(overall_atws_df.index)
tick_labels.sort()
features = list(overall_atws_df.columns)
features.sort()
attacks = list(feat_impo_df.index)
if not from_mi:
    attacks.remove('all_classes')
attacks.sort()
assert attacks == tick_labels, "The attack in WS dict and FI dict are not similar"

feat_impo_df = feat_impo_df.reindex(sorted(feat_impo_df.columns), axis=1)
features_ = list(feat_impo_df.columns)
# assert features_ == features, "The features in WS dict and FI dict are not similar"

if not from_mi:
    feat_impo_df.drop('all_classes', inplace=True, axis=0)

multiplied_atws_df = overall_atws_df * feat_impo_df
# multiplied_atws_df = overall_atws_df


ymin = multiplied_atws_df.min().min()
ymax = multiplied_atws_df.max().max()

x_values = range(multiplied_atws_df.shape[0])
xticks_rotation_dic = {
    'rotation_mode': "anchor",
    'ha': "center"
}

_ylog_scale = False

# to plot individual feature Wasserstein Differences
# for feature in features:
#     save_addr = os.path.join(save_fldr, f'{"log_" if _ylog_scale else ""}alternate_feature_WS_{feature}.pdf')
#     draw_bar_chart(x_values, multiplied_atws_df[feature],
#                    _title_text=f'WS of {feature} [attacks absent and present]', _xlabel='Attacks',
#                    _ylabel=f'{"(log) " if _ylog_scale else ""}Wasserstein Distance', _xticks=x_values,
#                    _xticks_rotation=10, _xticklabel_size=12, _ylims=[ymin, ymax], _title_fontweight='bold',
#                    _ylog_scale=_ylog_scale, _xticks_rotation_dic=xticks_rotation_dic, _yticklabel_size=12,
#                    _title_fontsize=18, _xlabel_fontsize=18, _ylabel_fontsize=18, _figsize=(12, 8),
#                    _xticklabel_weight='bold', _ylabel_fontweight='bold', # _save_address=save_addr,
#                    _xlabel_fontweight='bold', _xtick_labels=tick_labels)


mean_fe = multiplied_atws_df.mean(axis=1)
mean_fe = mean_fe / mean_fe.max()

save_addr = os.path.join(save_fldr,
                         f'{"log_" if _ylog_scale else ""}'
                         f'UNSW_NB15_MI_weighted_average_alternate_feature_WS_all_features.pdf')
# to plot [weighted] averaged feature Wasserstein Differences
draw_bar_chart(x_values, mean_fe,
               _title_text=f'MI weighted averaged WS of all features [attacks absent and present]', _xlabel='Attacks',
               _ylabel=f'{"(log) " if _ylog_scale else ""}Wasserstein Distance', _xticks=x_values, _xticks_rotation=10,
               _xticklabel_size=12, _title_fontweight='bold', _ylog_scale=_ylog_scale,  _save_address=save_addr,
               _xticks_rotation_dic=xticks_rotation_dic, _yticklabel_size=12, _title_fontsize=18,
               _xlabel_fontsize=18, _ylabel_fontsize=18, _figsize=(12, 8), _xticklabel_weight='bold',
               _ylabel_fontweight='bold', _xlabel_fontweight='bold', _xtick_labels=tick_labels)
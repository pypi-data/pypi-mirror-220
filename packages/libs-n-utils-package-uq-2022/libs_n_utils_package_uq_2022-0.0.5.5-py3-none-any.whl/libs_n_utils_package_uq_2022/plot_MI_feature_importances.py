import _pickle as pickle
import os
import matplotlib.pyplot as plt
from .lib_plotters import draw_bar_chart

fn = 'feature_importance_using_mi_39_features_NF-UNSW-NB15-v2_whole_rows.pickle'
fldr = '/home/nids1/Desktop/ZSL_visualizations'
addr = os.path.join(fldr, fn)
mi_dict = pickle.load(open(addr, 'rb'))
keys = list(mi_dict.keys())
attacks = keys[:-1]
features = mi_dict[keys[-1]]

x_values = list(range(len(features)))
tick_labels = features
plt.figure(figsize=(40, 20))
xticks_rotation_dic = {
    'rotation_mode': "default",
    'ha': "right"
}
save_addr = os.path.join(fldr, 'MI_feature_importance_whole_dataset_all_classes.pdf')
for i, attack in enumerate(attacks):
    plt.subplot(3, 3, i + 1)
    draw_bar_chart(x_values, mi_dict[attack], 'not_show', _xlabel='Features',
                   _ylabel=f'MI (Feature Importances)', _xticks=x_values, _xticks_rotation=45,
                   _xticks_rotation_dic=xticks_rotation_dic, plt_handle=plt, _xticklabel_size=12,
                   _xtick_labels=tick_labels, _title_text=rf'Mutual Information [$\bf{attack}$ vs all other classes]',
                   _yticklabel_size=12, _title_fontsize=20, # _title_fontweight='bold',
                   _xlabel_fontsize=18, _ylabel_fontsize=18, _xticklabel_weight = 'bold',
                   _ylabel_fontweight='bold', _xlabel_fontweight='bold')
    plt.tight_layout()

plt.savefig(save_addr)
plt.show()

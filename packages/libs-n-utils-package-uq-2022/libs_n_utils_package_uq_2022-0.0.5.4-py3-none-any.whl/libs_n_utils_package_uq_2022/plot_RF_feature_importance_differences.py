import _pickle as pickle
import os
import matplotlib.pyplot as plt
import numpy as np



fn = 'features_importances_per_attack_df_all_rows.pickle'
fldr = '/home/nids1/Desktop/ZSL_visualizations'
addr = os.path.join(fldr, fn)
df = pickle.load(open(addr, 'rb'))


attacks = list(df.index)

for i in range(df.shape[0] - 1):
    df.iloc[i, :] -= df.iloc[-1, :]

# removing the base of difference row: all_class
df.drop(attacks[-1], inplace=True)


attacks.pop()

ax_minlim = min(df.min())
ax_maxlim = max(df.max())

plt.figure(figsize=(40, 20))
for i in range(df.shape[0]):
    plt.subplot(4, 3, i + 1)
    df.iloc[i, :].plot.bar()
    t_sum = np.sum(np.abs(df.iloc[i, :]))
    plt.ylim(ax_minlim, ax_maxlim)
    plt.title(f'{attacks[i]} -> Total abs difference {t_sum:0.3f}', fontsize=28, fontweight='bold')
    plt.tight_layout()

save_addr = os.path.join(fldr, 'feature_importance_difference_with_all_classes.pdf')
# plt.savefig(save_addr)
plt.show()
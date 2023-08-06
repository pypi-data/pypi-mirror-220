import math
import matplotlib.pyplot as plt
from scipy.stats import binom


p = 0.5
trials = 43
pmf = [binom.pmf(x, trials, p) for x in range(trials + 1)]
mean, var = binom.stats(trials, p)

std = math.sqrt(var)
lim = 3 * std
low_lim = mean - lim
high_lim = mean + lim


x_values = range(len(pmf))

plt.plot(x_values, pmf, 'ro', markersize=6, markerfacecolor='none')
plt.plot(x_values, pmf, 'b--')
ymin = 0
ymax = max(pmf)
plt.vlines(low_lim, ymin, ymax, linestyles='--', colors='#CCCCCC')
plt.vlines(high_lim, ymin, ymax, linestyles='--', colors='#CCCCCC')
plt.ylim([ymin, ymax])

plt.xticks(x_values)
plt.show()
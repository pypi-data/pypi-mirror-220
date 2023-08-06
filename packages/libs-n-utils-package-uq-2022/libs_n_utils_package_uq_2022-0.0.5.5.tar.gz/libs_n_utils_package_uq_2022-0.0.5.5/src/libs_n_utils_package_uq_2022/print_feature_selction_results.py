
import os
import _pickle as pickle
import math
from scipy.stats import binom
from datetime import datetime
from .my_easy_logger import my_logger


filename = os.path.split(__file__)[1]


def boruta_result_interpret(n_trial, rank_value_list, probability=0.5):
    # pmf = [binom.pmf(x, n_trial, probability) for x in range(n_trial + 1)]
    mean, var = binom.stats(n_trial, probability)
    std = math.sqrt(var)

    criterion = 3 * std
    low_lim = mean - criterion
    high_lim = mean + criterion

    boruta_output = []
    for rank in rank_value_list:
        rank_value = n_trial - rank + 1
        if rank_value < low_lim:
            boruta_output.append('Rejected')
        elif low_lim <= rank_value <= high_lim:
            boruta_output.append('Tentative')
        else:
            boruta_output.append('Accepted')

    return boruta_output












if __name__ == '__main__':

    fn = 'selected_features_per_attack_dict_100000_rows.pickle'
    # fn = 'UNSW_selected_features_per_attack_dict_whole_rows_with_ranks.pickle'
    fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds/'
    addr = os.path.join(fldr, fn)

    log_file = os.path.join(
        fldr,
        f'{fn}_'
        f'{datetime.now().strftime("[%h_%m_%d-%H_%M_%S]")}.txt'
    )

    logger = my_logger(
        reporter_func_name=__name__,
        info_c='bold,fg_green',
        log_file_address=log_file
    )


    with open(addr, 'rb') as f:
        df = pickle.load(f)

    ks = list(df.index)
    for k in ks:
        ranks = df.loc[k].to_list()
        results = boruta_result_interpret(len(ranks), ranks)

        logger.info(
            f'\nClass {k}:\n'
            f'Accepted={results.count("Accepted")}\n'
            f'Tentative={results.count("Tentative")}\n'
            f'Rejected={results.count("Rejected")}\n'
        )

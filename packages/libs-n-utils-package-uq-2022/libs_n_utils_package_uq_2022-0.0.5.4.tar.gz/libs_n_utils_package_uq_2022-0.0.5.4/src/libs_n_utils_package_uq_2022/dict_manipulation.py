import os
import _pickle as pickle
from termcolor import cprint, colored

fldr = '../../outputs/scores/NFv2B'
files = os.listdir(fldr)

for file in files:
    cprint(f'loading {file} ...', 'green', attrs=['bold'])
    add = os.path.join(fldr, file)
    with open(add, 'rb') as f:
        dic = pickle.load(f)

    keys = list(dic.keys())
    write_flag = 0
    for k in keys:
        cprint(f'\nReading dictionary of the base key {colored(k, "blue", attrs=["bold"])}: ', 'blue')
        low_keys = list(dic[k][1].keys())
        for lk in low_keys:
            if any([x in k.split('.')[0] for x in lk.split('.')[0].split('-')[1:]]):
                write_flag = 1
                del dic[k][1][lk]
                cprint(f'{colored(lk, attrs=["bold"])} was part of {colored(k, "red")}, and is removed.', 'red')
            else:
                print(f'{colored(lk, attrs=["bold"])} is NOT part of the base key so, it should not be removed')

    # input(colored('Press <ENTER> to continue\n', 'red', 'on_cyan', attrs=['bold']))
    if write_flag:
        with open(add, 'wb') as f:
            pickle.dump(dic, f, protocol=-1)
        cprint(f'The new file is saved to {colored(add, attrs=["bold"])}.', 'red')
    else:
        continue

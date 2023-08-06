import pandas as pd
import _pickle as pickle
import os

file = 'WISDM_ar_v1.1_raw.txt'
fldr = r'/storage/Documents/AQIRF/project/IDS_EXPLORE_PAPER/datasets/WISDM_ar_v1.1'

file_addr = os.path.join(fldr, file)
f = open(file_addr, 'r')

dict_tmp = {
    'user': [],
    'activity': [],
    'timestamp': [],
    'x-acceleration': [],
    'y-acceleration': [],
    'z-acceleration': []
}
keys = list(dict_tmp.keys())

m = 0
flag = 0
for n, row in enumerate(f):
    row_ls = row.split(',')
    if len(row_ls) == 6:
        for k, val in enumerate(row_ls):
            dict_tmp[keys[k]] += [val.replace(';\n', '')]
    else:
        flag = 1
        row = row.split(';')
        for rw in row:
            rw_ls = rw.split(',')
            if len(rw_ls) == 6:
                flag = 0
                for k, val in enumerate(rw_ls):
                    dict_tmp[keys[k]] += [val.replace(';\n', '')]
            elif len(rw_ls) == 7 and rw_ls[6] == '':
                flag = 0
                for k in range(6):
                    dict_tmp[keys[k]] += [rw_ls[k].replace(';\n', '')]

f.close()

df = pd.DataFrame.from_dict(dict_tmp)
pickle_file_addr = f'{file_addr[:-4]}.pickle'
with open(pickle_file_addr, 'wb') as f:
    pickle.dump(df, f, protocol=-1)

print(f'df is saved to {pickle_file_addr}')
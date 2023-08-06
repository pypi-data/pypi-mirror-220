import os
import pandas as pd
import gc


n_select_rows = 2_000_000
base_fldr = '/storage/datasets/Comscentre2017'
src_fldr = f'{base_fldr}/feather/'
dst_fldr = f'{base_fldr}/feather_2m_sel_cols/'
select_cols = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'L4_DST_PORT', 'L4_SRC_PORT',
               'FIRST_SWITCHED', 'LAST_SWITCHED', 'PROTOCOL', 'IN_BYTES',
               'OUT_BYTES', 'IN_PKTS', 'OUT_PKTS', 'L7_PROTO']


file_list = os.listdir(src_fldr)
file_list.sort()

for file_name in file_list:
    file_addr = os.path.join(src_fldr, file_name)

    gc.disable()
    print(f'Reading 12 cols from file {file_addr}')
    df = pd.read_feather(file_addr, columns=select_cols)
    n_rows = df.shape[0]
    if n_rows > n_select_rows:
        print(f'sampling rows of{file_addr}')
        df = df.sample(n=n_select_rows)
        df.reset_index(drop=True, inplace=True)

    dst_addr = os.path.join(dst_fldr, f'2mRows_12Cols_{file_name}')
    print(f'Writing select rows and cols to {dst_addr}')
    df.to_feather(dst_addr)
    gc.enable()
    print(f'File {dst_addr} is now done')

print('Exiting all files are done !')

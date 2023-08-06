import os
import pandas as pd
from pathlib import Path

fldr = '/storage/datasets/originals/UNSW-NB15_CSV_Files/'
info_file_addr = os.path.join(fldr, 'NUSW-NB15_features.csv')
info_data = pd.read_csv(info_file_addr, encoding='unicode_escape')
df_header = info_data['Name'].tolist()

print("Loading files...")
df = pd.DataFrame()
for n in range(1, 5):
    addr = os.path.join(fldr, f'UNSW-NB15_{n}.csv')
    df_ = pd.read_csv(addr, names=df_header)
    df = pd.concat([df, df_])

print("Ready!")

# try:
#     df.drop('id', axis=1, inplace=True)
# except KeyError:
#     pass
#
# try:
#     df.drop('srcip', axis=1, inplace=True)
# except KeyError:
#     pass
#
# try:
#     df.drop('dstip', axis=1, inplace=True)
# except KeyError:
#     pass
#
# try:
#     df.drop('sport', axis=1, inplace=True)
# except KeyError:
#     pass
#
# try:
#     df.drop('dsport', axis=1, inplace=True)
# except KeyError:
#     pass

##fix attack names
df['attack_cat'] = df['attack_cat'].str.strip()
df['attack_cat'] = df['attack_cat'].replace('Backdoors', 'Backdoor')
df['attack_cat'] = df['attack_cat'].fillna('Benign')
df.rename(columns={"attack_cat": "Attack"}, inplace=True)

# attack_cat_val = df['attack_cat'].reset_index()
# attack_cat_val.drop('index', axis=1, inplace=True)
# df.drop('attack_cat', axis=1, inplace=True)
df['c_proto'] = pd.Categorical(df['proto']).codes
df.drop('proto', axis=1, inplace=True)
df['c_service'] = pd.Categorical(df['service']).codes
df.drop('service', axis=1, inplace=True)
df['c_state'] = pd.Categorical(df['state']).codes
df.drop('state', axis=1, inplace=True)
df.replace(' ', 0, inplace=True)
df.replace('-', 0, inplace=True)

# x = df.fillna(0).values  # returns a numpy array
# min_max_scaler = MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# df = pd.DataFrame(x_scaled, columns=df.columns)
# df = pd.concat([df, attack_cat_val], axis=1)

p_fldr = Path(fldr).parent
filename = 'UNSW-NB15.csv'
addr = os.path.join(p_fldr, filename)

df.to_csv(addr, sep=',', index=False)
print(f'df is written to {addr}')
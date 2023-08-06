import os
from .lib_file_manipulation import csvfile_2_featherfile
from .config_template import FlowMeter

cols = FlowMeter.columns

csv_folder = '/storage/datasets/Comscentre2017/Elasticsearch_CSV_full_headers/'
feather_folder = '/storage/datasets/Comscentre2017/feather/'

if not os.path.isdir(feather_folder):
    os.makedirs(feather_folder)

csv_list = os.listdir(csv_folder)

for csv in csv_list:
    csv_address = os.path.join(csv_folder, csv)
    print(f'Reading file {csv_address} ...')
    feather_address = os.path.join(feather_folder, csv[:-4]+'.feather')
    print(f'Writing to file Reading file {feather_address}')
    csvfile_2_featherfile(csv_address, feather_address=feather_address)
    print(f'file {csv} is written to feather in {feather_address}')


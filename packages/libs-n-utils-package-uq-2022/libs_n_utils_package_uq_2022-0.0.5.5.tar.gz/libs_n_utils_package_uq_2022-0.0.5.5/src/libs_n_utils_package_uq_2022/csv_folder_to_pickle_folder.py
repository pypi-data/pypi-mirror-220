import os
from .lib_file_manipulation import csvfile_2_picklefile
from .config_template import FlowMeter


cols = FlowMeter.columns

csv_folder = '/storage/datasets/FlowMeter/csv/'
pickle_folder = '/storage/datasets/FlowMeter/1pickle/'

csv_list = os.listdir(csv_folder)

for csv in csv_list:
    csv_address = os.path.join(csv_folder, csv)
    print(f'Reading file {csv_address} ...')
    pickle_address = os.path.join(pickle_folder, csv[:-4]+'.pickle')
    # print(f'Writing to file {pickle_address} ...')
    csvfile_2_picklefile(csv_address, pickle_address,
                         sample_rows=1_000_000,
                         blank_is_na=True,
                         contains_na=True,
                         full_resolution_float=True,
                         verbose=False
                         )

    print(f'file {csv} is written to pickle in {pickle_address}')


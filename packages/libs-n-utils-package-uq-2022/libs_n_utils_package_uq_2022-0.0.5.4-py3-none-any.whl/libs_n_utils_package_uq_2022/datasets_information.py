import os
import _pickle as pickle


def print_df_infor(file_path):
    print(f'Reading file {file_path} ...')
    df = pickle.load(open(file_path, 'rb'))
    print(f'{file_path} has {df.shape[1]} columns and {df.shape[0]} rows')





if __name__ == "__main__":
    fldr = "/storage/datasets/NetFlow/1pickle/"
    file_list = os.listdir(fldr)
    file_list.sort()

    for file_ in file_list:
        file_path_ = os.path.join(fldr, file_)
        print_df_infor(file_path_)

    print('done')

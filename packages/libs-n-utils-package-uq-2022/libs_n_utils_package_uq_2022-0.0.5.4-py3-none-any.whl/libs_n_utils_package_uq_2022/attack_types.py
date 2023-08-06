import os
import feather

source_fldr = '/storage/datasets/NetFlow/feather/'
source_files = os.listdir(source_fldr)

for file in source_files:
    file_address = os.path.join(source_fldr, file)
    df = feather.read_dataframe(
        file_address
    )
    df = df.sample(frac=0.1)
    print(f"File {file} attack types: {df['Attack'].unique()}")
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline


def random_sample_visualize(data_array, labels_array, _random_seed=0):
    print(f'(data_array.shape[0], data_array.shape[1], data_array.shape[2]): '
          f'{(data_array.shape[0], data_array.shape[1], data_array.shape[2])}')
    rng = np.random.default_rng(_random_seed)
    numbers = rng.choice(data_array.shape[0], size=4, replace=False)
    plt.figure(figsize=(12, 8))
    for k, randN in enumerate(numbers):
        print(f'Random sample no. {k} is: {randN}: (Label = {labels_array[randN]})')
        data_sample = np.reshape(data_array[randN, :, :],
                                 (data_array.shape[1],
                                  data_array.shape[2]))
        label_sample = labels_array[randN]
        plt.subplot(1, 4, k + 1)
        plt.imshow(data_sample)
        plt.title(f'Sample {randN}, Label {label_sample}')
    plt.tight_layout()
    plt.show()


def smote_balance(imbal_x, imbal_y):
    """
    First over samples classes smaller than rw_ls border (class average)
    Then, under samples classes larger than rw_ls border (class average)
    :param imbal_x: data without labels
    :param imbal_y: labels
    :return:
    bal_x: balanced data
    bal_y: labels of balanced data
    """
    _counter = Counter(imbal_y)
    counts = list(_counter.values())
    border = int(np.mean(counts))
    # define pipeline
    over_strategy = {key: val if val > border else border
                     for key, val in _counter.items()}
    under_strategy = {key: val if val < border else border
                      for key, val in over_strategy.items()}
    over = SMOTE(sampling_strategy=over_strategy)
    under = RandomUnderSampler(sampling_strategy=under_strategy)
    steps = [('o', over), ('u', under)]
    pipeline = Pipeline(steps=steps)
    # transform the dataset
    bal_x, bal_y = pipeline.fit_resample(imbal_x, imbal_y)
    return bal_x, bal_y


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    working_fldr = '/home/edge-lab/myPy/lite2'
    data_file_addr = f'{working_fldr}/TFDout_AllClsAccxyzMagnGyroxyzS2TW10XS5Fc2.0.npy'
    label_file_addr = f'{working_fldr}/LabelTFDout_AllClsAccxyzMagnGyroxyzS2TW10XS5Fc2.0.npy'
    data = np.load(data_file_addr)
    labels = np.load(label_file_addr)
    counter = Counter(labels)
    print(f'Imbalanced Class counts:\n {sorted(counter.items())}')
    random_sample_visualize(data, labels, _random_seed=100)

    # Since resampling works only for 2D-data, we have to reshape it
    reshaped_data = np.reshape(data, (data.shape[0], data.shape[1] * data.shape[2]))
    bal_data, bal_labels = smote_balance(reshaped_data, labels)
    print(f'bal_data.shape:{bal_data.shape}, bal_labels.shape:{bal_labels.shape}')
    bal_counter = Counter(bal_labels)
    print(f'Balanced class counts:\n {sorted(bal_counter.items())}')
    reshaped_bal_data = np.reshape(bal_data, (data.shape[0], data.shape[1], data.shape[2]))
    random_sample_visualize(reshaped_bal_data, bal_labels, _random_seed=100)

import inspect
import os
import tensorflow as tf
from .my_easy_logger import my_logger

filename = os.path.split(__file__)[1]
info_log_color = 'fg_bold_purple,bg_white'
# TODO: BatchNormalization 

# metrics for evaluation (not loss function) --------
METRICS = [
    tf.keras.metrics.TruePositives(name='tp'),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'),
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall'),
    tf.keras.metrics.AUC(name='auc_synth'),
]



# early stopping function -------------------------
def early_stopping(monitor='loss',
                   min_delta=0.0001, patience=3):
    return tf.keras.callbacks.EarlyStopping(
        monitor=monitor,
        min_delta=min_delta,
        patience=patience
    )


# -------------------------------------------   MLP model  ------------------------------------------------
class MLP:
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)

    def __init__(self, metrics=None, dropout_value=0.2, n_nodes=10,
                 seed_=None, learning_rate=0.0001, n_layers=4, optimiser='adam'):
        if metrics is None:
            metrics = METRICS
        if seed_ is not None:
            tf.random.set_seed(seed_)

        self.model = tf.keras.models.Sequential()
        # adding layers except the last two layers
        for n in range(n_layers):
            self.model.add(
                tf.keras.layers.Dense(
                    n_nodes,
                    activation='relu',
                    kernel_initializer='random_normal',
                    bias_initializer='zeros'
                )
            )
            self.model.add(tf.keras.layers.Dropout(dropout_value))

        self.model.add(
            tf.keras.layers.Dense(1, activation='sigmoid')
            )
        # self.model.add(tf.keras.layers.Dense(n_nodes, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(dropout_value))
        # self.model.add(tf.keras.layers.Dense(n_nodes, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(dropout_value))
        # self.model.add(tf.keras.layers.Dense(n_nodes, activation='relu'))
        # self.model.add(tf.keras.layers.Dense(1, activation='sigmoid'))



        # TODO:
        #  1. Weight Initialization
        # Compiling the model
        if optimiser == 'adam':
            opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        else:
            lr = tf.Variable(1, trainable=False, dtype=tf.float32)
            opt = tf.keras.optimizers.SGD(lr, momentum=1.0, decay=0.0, nesterov=False)

        self.model.compile(
            optimizer=opt,
            loss='binary_crossentropy',
            metrics=metrics,
        )

    # -------------------------------  train  --------------------------------------------------------------------
    def train(self, train_data_x, train_data_y, class_weights=None,
              batch_size=5000, epochs=25, validation_split=0.3,
              callbacks=None, verbose=0):
        self.logger_.info(f'Fitting the TF model to the '
                          f'train data of size {train_data_x.shape}')
        self.model.fit(
            x=train_data_x,
            y=train_data_y,
            batch_size=batch_size,
            epochs=epochs,
            callbacks=callbacks,
            shuffle=True,
            validation_split=validation_split,
            class_weight=class_weights,
            verbose=verbose
        )
        return self.model

    # -------------------------------  train on batch  -----------------------------------------------------------
    def train_on_batch(self, x_batch, y_batch,
                       sample_weight=None,
                       reset_metrics=True,
                       class_weight=None,
                       return_dict=True):
        self.logger_.info(f'Training the data'
                          f' of batch size {x_batch.shape}')
        return self.model.train_on_batch(
            x_batch, y_batch,
            sample_weight=sample_weight,
            reset_metrics=reset_metrics,
            class_weight=class_weight,
            return_dict=return_dict
        )

    # ------------------------------  test on batch  -------------------------------------------------------------
    def test_on_batch(self, x_batch, y_batch,
                      sample_weight=None,
                      reset_metrics=True,
                      return_dict=True):
        self.logger_.info(f'Testing the data'
                          f' of batch size {x_batch.shape}')
        return self.model.test_on_batch(
            x_batch, y_batch,
            sample_weight=sample_weight,
            reset_metrics=reset_metrics,
            return_dict=return_dict
        )


"""
def generate_arrays_from_file(path):
    while 1:
        f = open(path)
        for line in f:
            # create numpy arrays of input data
            # and labels, from each line in the file
            x, y = process_line(line)
            img = load_images(x)
            yield (img, y)
        f.close()
"""



# -------------------------------------------   LSTM model  ------------------------------------------------
class LSTM(MLP):
    def __init__(self, metrics=None, dropout_value=0.2, n_nodes=10,
                 seed_=None, learning_rate=0.0001, n_layers=4, optimiser='adam'):
        super().__init__(metrics, dropout_value, n_nodes, seed_,
                         learning_rate, n_layers, optimiser)
        if metrics is None:
            metrics = METRICS
        if seed_ is not None:
            tf.random.set_seed(seed_)

        self.model = tf.keras.models.Sequential()
        # LSTM expects inputs a 3D tensor, with shape [batch, timesteps, feature]
        self.model.add(tf.keras.layers.InputLayer(input_shape=(100, 1, 39)))
        for _ in range(n_layers-1):
            self.model.add(tf.keras.layers.LSTM(n_nodes, activation='relu', return_sequences=True))
            self.model.add(tf.keras.layers.Dropout(dropout_value))

        self.model.add(tf.keras.layers.LSTM(n_nodes, activation='relu', return_sequences=False))
        self.model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        # TODO:
        #  1. Weight Initialization
        # Compiling the model
        if optimiser == 'adam':
            opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        else:
            lr = tf.Variable(1, trainable=False, dtype=tf.float32)
            opt = tf.keras.optimizers.SGD(lr, momentum=1.0, decay=0.0, nesterov=False)

        self.model.compile(
            optimizer=opt,
            loss='binary_crossentropy',
            metrics=metrics,
        )
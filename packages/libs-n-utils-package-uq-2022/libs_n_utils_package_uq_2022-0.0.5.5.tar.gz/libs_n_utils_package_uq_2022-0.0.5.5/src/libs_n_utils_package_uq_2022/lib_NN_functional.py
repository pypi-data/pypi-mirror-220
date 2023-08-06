import inspect
import tensorflow as tf
from .my_easy_logger import my_logger
import os

filename = os.path.split(__file__)[1]
info_log_color = 'fg_bold_purple,bg_white'

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



# MLP model -----------------------------------------------------------------------------------------------------------
def deep_learning_model(train_data_x, train_data_y, class_weights,
                        metrics=None, batch_size=None, epochs=None,
                        validation_split=None, dropout=None):
    if dropout is None:
        dropout = 0.2
    if validation_split is None:
        validation_split = 0.1
    if epochs is None:
        epochs = 25
    if batch_size is None:
        batch_size = 5000
    if metrics is None:
        metrics = METRICS
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(reporter_file_name=filename,
                        reporter_func_name=func_name,
                        info_c=info_log_color)

    # tf.random.set_seed(1)
    # earlystop_binary = tf.keras.callbacks.EarlyStopping(
    #     monitor='val_accuracy',
    #     min_delta=0.00001,
    #     patience=3
    # )

    logger_.info('Defining the TF model')
    # n_nodes = train_data_x.shape[1]
    n_nodes = 10
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(n_nodes, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(n_nodes, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(n_nodes, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(n_nodes, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    logger_.info('Compiling the TF model')
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=metrics,
    )

    logger_.info(f'Fiting the TF model to the train data of size {train_data_x.shape}')
    model.fit(x=train_data_x,
              y=train_data_y,
              batch_size=batch_size,
              epochs=epochs,
              # callbacks=[earlystop_binary],
              shuffle=True,
              validation_split=validation_split,
              class_weight=class_weights,
              )

    logger_.info(f'Created TF model summary: {model.summary()}')
    return model





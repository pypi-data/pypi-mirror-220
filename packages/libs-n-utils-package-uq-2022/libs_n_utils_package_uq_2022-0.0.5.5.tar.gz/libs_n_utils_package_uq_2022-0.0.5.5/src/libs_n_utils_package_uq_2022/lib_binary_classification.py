import os
from .my_easy_logger import my_logger
from .config_template import NetFlow_v2, NN
import inspect

seed_ = NN.seeds
script_name = os.path.split(__file__)[1][:-3]
logger = my_logger(
    reporter_file_name=script_name,
    info_c='fg_blue,bg_black',
    reporter_func_name=__name__,
    log_level='debug'
)


"""
9 Metrics:
 0- loss, 1- tp, 2- fp, 3- tn, 4- fn
 5- accuracy, 6- precision, 7- recall, 8- auc_synth
"""


script_name = os.path.split(__file__)[1][:-3]
netflow_columns = NetFlow_v2.columns
netflow_identifiers = NetFlow_v2.flow_identifiers




# *--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
def get_AK_model(x_train_, y_train_, x_test_, y_test_, dataset_name, dest_fldr=None, epochs_=None):
    import tensorflow as tf
    import autokeras as ak
    from lib_NN_models import METRICS
    tf.random.set_seed(seed_)
    func_name = inspect.stack()[0][3]
    logger_ = my_logger(
        reporter_file_name=script_name,
        info_c='fg_blue,bg_black',
        reporter_func_name=func_name,
        log_level='debug'
    )
    clf = ak.StructuredDataClassifier(
        overwrite=True,
        max_trials=3,
        metrics=METRICS
    )
    logger_.info('fitting to model')
    # logger_.info(psutil.virtual_memory())
    if epochs_ is not None:
        clf.fit(x_train_, y_train_, epochs=epochs_)
    else:
        clf.fit(x_train_, y_train_)

    logger_.info('Exporting the model')
    # logger_.info(psutil.virtual_memory())
    model = clf.export_model()
    if dest_fldr is not None:
        address = os.path.join(dest_fldr, f'{dataset_name}_model')
        model.save(address, save_format="tf")
        logger_.info(f'model {dataset_name}_model is now saved to {address}')
        # logger_.info(psutil.virtual_memory())


    logger_.info(f'evaluating for {dataset_name}')
    # logger_.info(psutil.virtual_memory())
    scores = clf.evaluate(x_test_, y_test_)

    return model, scores


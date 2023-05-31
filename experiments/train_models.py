import numpy as np
from ampligraph.datasets import load_fb15k, load_fb15k_237, load_wn18, load_wn18rr
from ampligraph.latent_features import ScoringBasedEmbeddingModel
from ampligraph.latent_features.loss_functions import get as get_loss
from ampligraph.latent_features.regularizers import get as get_regularizer
from ampligraph.utils import save_model
import tensorflow as tf
import configparser
import os

config = configparser.ConfigParser()
config.read(os.getcwd() + "/experiments/data/hyperparameters.ini")
for dataset in config.keys():
    print(dataset)
    if dataset == "FB15k":
        X = load_fb15k()
    elif dataset == "FB15k-237":
         X = load_fb15k_237()
    elif dataset == "WN18":
         X = load_wn18()
    elif dataset == "WN18RR":
         X = load_wn18rr()
    else:
         continue
    current_config = config[dataset]
    print("Training model for {}".format(dataset))
    model = ScoringBasedEmbeddingModel(k=current_config.getint("dimensions"),
                                    eta=current_config.getint("eta"),
                                    scoring_type='TransE')

    # Optimizer, loss and regularizer definition
    optim = tf.keras.optimizers.Adam(learning_rate=current_config.getfloat("lr"))
    loss = get_loss(current_config.get("loss"))
    regularizer = get_regularizer(current_config.get("regularizer"), 
                                  {'p': current_config.getint("p"), 
                                   'lambda': current_config.getfloat("lambda")})

    # Compilation of the model
    model.compile(optimizer=optim, loss=loss, entity_relation_regularizer=regularizer)

    # For evaluation, we can use a filter which would be used to filter out
    # positives statements created by the corruption procedure.
    # Here we define the filter set by concatenating all the positives
    filter = {'test' : np.concatenate((X['train'], X['valid'], X['test']))}

    # Early Stopping callback
    checkpoint = tf.keras.callbacks.EarlyStopping(
        monitor='val_{}'.format('hits10'),
        min_delta=0,
        patience=5,
        verbose=1,
        mode='max',
        restore_best_weights=True
    )

    # Fit the model on training and validation set
    batch_count = current_config.getint("batches_count")
    model.fit(X['train'],
            batch_size=int(X['train'].shape[0] / batch_count),
            epochs=current_config.getint("epochs"),                    # Number of training epochs
            validation_freq=20,           # Epochs between successive validation
            validation_burn_in=100,       # Epoch to start validation
            validation_data=X['valid'],   # Validation data
            validation_filter=filter,     # Filter positives from validation corruptions
            callbacks=[checkpoint],       # Early stopping callback (more from tf.keras.callbacks are supported)
            verbose=True                  # Enable stdout messages
            )

    # Save the model
    storage_path = os.getcwd() + "/experiments/data/trainedModels/{}".format(dataset)
    save_model(model, model_name_path=storage_path)
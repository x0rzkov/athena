"""

@author: Ying Meng (y(dot)meng201011(at)gmail(dot)com)
"""

import copy
import os

import models
from utils.config import *
from data import load_data
from transformation import transform


def train_model(data, transformation_type):
    X, Y = data

    print('Transforming training data set [{}]...'.format(transformation_type))
    X = transform(X, transformation_type)

    model_name = 'model-{}-cnn-{}'.format(DATA.CUR_DATASET_NAME, transformation_type)
    model = models.create_model(DATA.CUR_DATASET_NAME)
    print('Training model [{}]...'.format(model_name))
    model = models.train(model, X, Y, model_name)
    print('Saving model...')
    models.save_model(model, model_name)
    print('Done.')

    return model

def test_model(model, test_data, transformation_type):
    X, Y = test_data

    print('Transforming test data set...')
    X = transform(X, transformation_type)

    print('Testing model [{}]...'.format(transformation_type))
    models.evaluate_model(model, X, Y)

    del X, Y

def main():
    DATA.set_current_dataset_name(DATA.mnist)

    # trans_types = TRANSFORMATION.supported_types()
    trans_types = [TRANSFORMATION.clean]

    adversary_types = ATTACK.get_AETypes()

    _, (X, Y) = load_data(DATA.CUR_DATASET_NAME)

    for transformation_type in trans_types:
        TRANSFORMATION.set_cur_transformation_type(transformation_type)
        try:
            # model = train_model(training_data, transformation_type)
            model = models.load_model('model-{}-cnn-{}'.format(DATA.CUR_DATASET_NAME,
                                                               transformation_type))
            for adversary in adversary_types:
                X_adv_file = 'test_AE-{}-cnn-clean-{}.npy'.format(DATA.CUR_DATASET_NAME, adversary)
                print('Evaluating weak defenses on dataset [{}]'.format(X_adv_file))
                X_adv_file = os.path.join(PATH.ADVERSARIAL_FILE, X_adv_file)
                X_adv = np.load(X_adv_file)

                test_model(model, copy.deepcopy((X_adv, Y)), transformation_type)
                del X_adv, X_adv_file

            print('')
        except (FileNotFoundError, OSError) as e:
            print(e)
            print('')
            continue

        del model

if __name__ == '__main__':
    main()


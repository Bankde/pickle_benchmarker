#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# keras model
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import tensorflow as tf
import numpy as np

class Test(helper.PickleTest):
    mock_weight = [np.array([[ 0.8, 0.3, -0.9],[0.3,0.8,-0.3]]), np.array([0,0,0]), np.array([[-0.3,0.8],[0.7,-0.1],[0.3,0.5]]), np.array([0,0])]
    mock_model = ['Model: "test_model"', '_________________________________________________________________', 'Layer (type)                 Output Shape              Param #   ', '=================================================================', 'input_layer (InputLayer)     [(None, 2)]               0         ', '_________________________________________________________________', 'dense_layer (Dense)          (None, 3)                 9         ', '_________________________________________________________________', 'softmax_layer (Dense)        (None, 2)                 8         ', '=================================================================', 'Total params: 17', 'Trainable params: 17', 'Non-trainable params: 0', '_________________________________________________________________']

    def test_model(self):
        model_summary_arr = []
        def writeToArr(txt):
            model_summary_arr.append(txt)

        inputs = tf.keras.Input(shape=(2,), name="input_layer")
        x = tf.keras.layers.Dense(3, activation=tf.nn.relu, name="dense_layer")(inputs)
        outputs = tf.keras.layers.Dense(2, activation=tf.nn.softmax, name="softmax_layer")(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs, name="test_model")
        model.compile(optimizer='adam', loss='binary_crossentropy')
        model.set_weights(self.mock_weight)
        self.obj["model"] = self.dumps(model)

        self.assertListEqual(model.get_weights(), self.mock_weight)
        pred = model.predict([[1,2]])[0]
        self.assertTrue(np.allclose(pred, np.array([0.49500012, 0.5049999])))
        model.summary(print_fn=writeToArr)
        self.assertListEqual(model_summary_arr, self.mock_model)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()
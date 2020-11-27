
# Copyright (c) 2020, Ahmed M. Alaa
# Licensed under the BSD 3-clause license (see LICENSE.txt)

from __future__ import absolute_import, division, print_function

import pickle
from sklearn.preprocessing import StandardScaler
import numpy as np
from copy import deepcopy
import time
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def process_MIMIC_data(max_seq_len=20):

    feature_names  = ['temphigh', 'heartratehigh', 'sysbplow', 'diasbplow', 'meanbplow', 'spo2high',
                      'fio2high', 'respratelow', 'glucoselow', 'bicarbonatehigh',
                      'bicarbonatelow', 'creatininehigh', 'creatininelow', 'hematocrithigh',
                      'hematocritlow', 'hemoglobinhigh', 'hemoglobinlow', 'platelethigh',
                      'plateletlow', 'potassiumlow', 'potassiumhigh', 'bunhigh', 'bunlow',
                      'wbchigh', 'wbclow', 'antibiotics', 'norepinephrine', 'mechanical_ventilator'
                      'age', 'weight']  


    with open('data/mimic/mimic.p', 'rb') as f:
        MIMIC_data = pickle.load(f)
    
    XX     = MIMIC_data["longitudinal"][:, :, :]
    static = np.repeat(MIMIC_data['static'].reshape((-1, 1, 2)), XX.shape[1], axis=1)

    X = np.concatenate((XX, static), axis=2) #MIMIC_data["longitudinal"][:, :, :] #list(set(list(range(28))) - set([23, 24, 25]))]
    Y = MIMIC_data["longitudinal"][:, :, 23]
    T = MIMIC_data["longitudinal"][:, :, 25]
    L = MIMIC_data['trajectory_lengths'] 
    
    scaler      = StandardScaler()
    X_unrolled  = X.reshape((X.shape[0] * X.shape[1], X.shape[2]))
    X_unrolled  = scaler.fit_transform(X_unrolled)
    X_rerolled  = X_unrolled.reshape((X.shape[0], X.shape[1], X.shape[2]))
    X_          = [X_rerolled[k, :L[k]-1, :] for k in range(X_rerolled.shape[0])]
    Y_          = [Y[k, 1:L[k]] for k in range(Y.shape[0])]
    T_          = [T[k,  :L[k]] for k in range(T.shape[0])]
    
    max_len = 0
    for x in X_:
        len_x = x.shape[0]
        if len_x > max_len:
            max_len = len_x

    max_len = np.min([max_len,max_seq_len])

    ori_data = np.zeros([5833,max_len,30])

    for i,x in enumerate(X_):
        ori_data[i,:]

        curr_no = len(x)
        if curr_no >= max_len:
            ori_data[i, :, :] = x[:max_len,:]
        else:
            ori_data[i, :curr_no, :] = x

    return ori_data, Y_, T_, L, feature_names





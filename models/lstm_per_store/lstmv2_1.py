import os
import sys

import caffe

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
import pickle
from scipy.stats import ortho_group
import time

sys.path.append('C:\\Users\\Peter\\Documents\\GitHub\\CZ4041')
from src import util

# Some constants
batch_size = 500

# Load train & test data
data_dir = '../data'

with open('dsetv3.pickle', 'rb') as f:
    dset = pickle.load(f)
    stores = dset['stores']
    zeroes = dset['zeroes']
    del dset

def train(store_id, num_epoch=100, solver_prototxt='solverv2_1.prototxt'):
    net_fname = os.path.join('temp', '_%d.caffemodel' % store_id)

    print '+=============================================================================+'
    print '| Traininig store % 4d                                                        |' % store_id
    print '+=============================================================================+'

    start_time = time.time()

    solver = caffe.get_solver(solver_prototxt)
    net = solver.net
    # losses = []

    x = stores[store_id]['x']
    y = stores[store_id]['y']
    cont = stores[store_id]['cont']
    mean = stores[store_id]['mean']
    std = stores[store_id]['std']
    num_ts = len(x)

    prev_loss = float('inf')
    for epoch in range(1,num_epoch+1):
        for t in range(0, num_ts, batch_size):
            net.blobs['data'].data[:] = x[t:t+batch_size]
            net.blobs['cont'].data[:, 0] = cont[t:t+batch_size]
            net.blobs['target'].data[:, 0] = y[t:t+batch_size]
            solver.step(1)

            # losses.append(net.blobs['loss'].data.item(0))
            curr_loss = net.blobs['loss'].data.item(0)
            if epoch * 2 >= num_epoch and curr_loss < prev_loss:
                prev_loss = curr_loss
                solver.net.save(net_fname)

    print '+=============================================================================+'
    print '| Testing store % 4d, time taken: %.9f' % (store_id, time.time() - start_time)
    print '+=============================================================================+'

    test_net = caffe.Net('lstmv2_1.prototxt', net_fname, caffe.TEST)

    # Peek again after training
    preds = np.zeros(num_ts)
    for t in range(0, num_ts, batch_size):
        test_net.blobs['data'].data[:] = x[t:t+batch_size]
        test_net.blobs['cont'].data[:, 0] = cont[t:t+batch_size]
        preds[t:t+batch_size] = test_net.forward()['output'][:, 0]

    # Reconstruct
    y_de = mean + y * std
    preds = mean + preds * std

    # Avoid division by small number
    mask = y_de >= 1.

    RMSE  = np.sqrt( np.sum((y_de-preds)**2)/num_ts )
    RMSPE = np.sqrt( np.sum(((y_de[mask]-preds[mask])/y_de[mask])**2)/mask.sum() )
    print 'RMSE  : %.9f' % RMSE
    print 'RMSPE : %.9f' % RMSPE

    # Plot losses
    # plt.subplots()
    # plt.subplots_adjust(left=0.025, bottom=0.025, right=1.0, top=1.0, wspace=0., hspace=0.)
    # plt.xlim(0, len(losses))
    # plt.ylim(0, max(losses))
    # plt.plot(np.arange(len(losses)), losses)

    # Plot prediction vs. actual
    # plt.subplots()
    # plt.subplots_adjust(left=0.025, bottom=0.025, right=1.0, top=1.0, wspace=0., hspace=0.)
    # plt.xlim(0, num_ts)
    # y_min=min(preds.min(), y_de.min())
    # y_max=max(preds.max(), y_de.max())
    # plt.ylim(y_min, y_max)
    # plt.plot(np.arange(num_ts), y_de, '-b')
    # plt.plot(np.arange(num_ts), preds, '-r')
    # plt.show()

    return solver

def predict(store_id, net):
    xtest = stores[store_id]['xtest']
    cont_test = stores[store_id]['cont_test']
    mean = stores[store_id]['mean']
    std = stores[store_id]['std']
    submid = stores[store_id]['submid']
    num_ts = len(xtest)

    preds = np.zeros(num_ts)
    for t in range(0, num_ts, batch_size):
        net.blobs['data'].data[:] = xtest[t:t+batch_size]
        net.blobs['cont'].data[:, 0] = cont_test[t:t+batch_size]
        preds[t:t+batch_size] = net.forward()['output'][:, 0]

    preds = mean + preds * std

    with open('submission.csv', 'a') as f:
        for i in range(len(submid)):
            f.write('%d,%.15f\n' % (submid[i], preds[i]))

with open('submission.csv', 'w') as f:
    for store_id in zeroes:
        f.write('%d,%.15f\n' % (store_id, 0.))

for store_id in stores:
    net_fname = os.path.join('temp', '_%d.caffemodel' % store_id)
    solver = train(store_id, 300)
    predict(store_id, caffe.Net('lstmv2_1.prototxt', net_fname, caffe.TEST))
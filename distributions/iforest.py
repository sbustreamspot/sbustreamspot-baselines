#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-baselines

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from params import *
from distribution import *
from utils import split_train_test, pr_curve
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import LeaveOneOut
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.ensemble import IsolationForest
import sys
import random

random.seed(SEED)
np.random.seed(SEED)
rng = np.random.RandomState(SEED)

# arguments
train_frac = float(sys.argv[1])
ntrees = int(sys.argv[2])
sample_frac = float(sys.argv[3])
feat_frac = float(sys.argv[4])

# train-test split
train_gids, test_gids = split_train_test(BENIGN_SCENARIOS, MALICIOUS_SCENARIOS,
                                         train_frac)
train_gids = set(train_gids)
test_gids = set(test_gids)

# features
features = ['avg-degree', 'avg-distinct-degree', 'avg-eccentricity',
            'avg-path-length', 'density', 'diameter', 'effective-diameter',
            'max-degree', 'max-distinct-degree', 'nedges', 'nverts']

Xtrain = []
idx_train = [] # idx_train[i] = gid of features in row i of Xtrain
Xtest = []
idx_test = [] # idx_test[i] = gid of features in row i of Xtest
for i, feat_name in enumerate(features):
    feat_file = 'metrics/' + feat_name + '.txt'
    column_train = []
    column_test = []
    with open(feat_file, 'r') as f:
        # skip 3 header lines
        next(f)
        next(f)
        next(f)
        for line in f:
            fields = line.strip().split('\t')
            gid = int(fields[0])
            feat_value = float(fields[1])
            scenario = gid/100

            if gid in train_gids:
                column_train.append(feat_value)
                idx_train.append(gid)
            elif gid in test_gids:
                column_test.append(feat_value)
                idx_test.append(gid)
            else:
                print "ERROR"
                sys.exit(-1)

    Xtrain.append(column_train)
    Xtest.append(column_test)

Xtrain = np.transpose(np.array(Xtrain))
Xtest = np.transpose(np.array(Xtest))
idx_train = idx_train[:Xtrain.shape[0]]
idx_test = idx_test[:Xtest.shape[0]]

# fit an iforest
iforest =  IsolationForest(n_estimators=ntrees,
                           max_samples=sample_frac, max_features=feat_frac,
                           n_jobs=-1, random_state=rng, verbose=1)
iforest.fit(Xtrain)

# anomaly scores
y_pred_train = iforest.predict(Xtrain)
y_pred_test = iforest.predict(Xtest)

y_pred_all = np.concatenate((y_pred_train, y_pred_test))
idx_all = idx_train + idx_test
y_true = [1 if gid/100 in MALICIOUS_SCENARIOS else 0
          for gid in idx_all]
benign_pred = [y_pred_all[i] for i in range(len(y_pred_all)) if y_true[i] == 0]
malicious_pred = [y_pred_all[i] for i in range(len(y_pred_all)) if y_true[i] == 1]

# compute histograms
binwidth = 0.01
minval = min(y_pred_all)
maxval = max(y_pred_all)
nbins = (maxval - minval)/binwidth;
bins = np.arange(minval, maxval+binwidth+binwidth, binwidth)
a = np.arange(len(bins))

benign_hist, _ = np.histogram(benign_pred, bins=bins)
malicious_hist, _ = np.histogram(malicious_pred, bins=bins)

# plot histogram
colours = ["#348ABD", "#A60628"]
plt.figure(figsize=(16,4))
plt.hold(True)
plt.bar(left=bins[:-1], width=binwidth, height=benign_hist, color=colours[0],
        label='Benign', alpha=0.6, edgecolor=colours[0], lw="3")
plt.bar(left=bins[:-1], width=binwidth, height=malicious_hist, color=colours[1],
        label='Malicious', alpha=0.6, edgecolor=colours[1], lw="3")

"""
# plot rug data points
ymin, ymax = plt.ylim()
ycenter = (ymax - ymin) * 0.8
plt.plot(train_values, [ycenter]*len(train_values), '|', color='k',
         label='Training feature values')

test_values = np.array([feat_val
                        for gid, feat_val in test_feature_values]).reshape(-1,1)
test_malicious_values = [feat_val for gid, feat_val in test_feature_values
                         if gid/100 in MALICIOUS_SCENARIOS]
test_benign_values = [feat_val for gid, feat_val in test_feature_values
                         if gid/100 in BENIGN_SCENARIOS]
plt.plot(test_benign_values, [ycenter]*len(test_benign_values), '|',
         color=colours[0], label='Test feature values (benign)')
plt.plot(test_malicious_values, [ycenter]*len(test_malicious_values), '|',
         color='red', label='Test feature values (malicious)')
"""

plt.legend(loc='best')
plt.xlim(bins[0]-binwidth, bins[-1]+binwidth)
plt.xticks(bins, ["{:0.03f}".format(x) for x in bins.flatten()], rotation=45)
plt.savefig('iforest-scores.pdf', bbox_inches='tight')
plt.clf()
plt.close()

"""
# plot PR curve
precision, recall, _ = precision_recall_curve(y_true=y_true,
                                              probas_pred=y_pred_all)
ap = average_precision_score(y_true, anomaly_scores)
print precision
print recall
print ap

plt.figure()
plt.plot(recall, precision, label='AUC={0:0.2f}'.format(ap))
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.legend()
plt.savefig('pr-' + feat_name + '.pdf', bbox_inches='tight')
plt.clf()
plt.close()
"""

# plot my own PR curve
precision, recall, ap = pr_curve(y_true, y_pred_all)
print ap
plt.figure()
plt.plot(recall, precision, label='AUC={0:0.3f}'.format(ap))
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.legend()
plt.savefig('iforest-pr.pdf', bbox_inches='tight')
plt.clf()
plt.close()

#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-baselines

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from params import *
from distribution import *
from utils import split_train_test
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import LeaveOneOut
import sys
import random

random.seed(SEED)
np.random.seed(SEED)

# arguments
feat_file = sys.argv[1]
feat_name = sys.argv[2]
binwidth = float(sys.argv[3])
train_frac = float(sys.argv[4])
bandwidth = -1.0
if len(sys.argv) > 5:
    bandwidth = float(sys.argv[5])

# train-test split
train_gids, test_gids = split_train_test(BENIGN_SCENARIOS, MALICIOUS_SCENARIOS,
                                         train_frac)
train_gids = set(train_gids)
test_gids = set(test_gids)

# collect feature values from file
train_feature_values = []
test_feature_values = []
with open(feat_file, 'r') as f:
    # skip 3 header lines
    next(f)
    next(f)
    next(f)
    for line in f:
        fields = line.strip().split('\t')
        gid = int(fields[0])
        if feat_name == "density":
            feat_value = float(fields[1]) * 10000
        else:
            feat_value = float(fields[1])
        scenario = gid/100

        if gid in train_gids:
            train_feature_values.append((gid, feat_value))
        elif gid in test_gids:
            test_feature_values.append((gid, feat_value))
        else:
            print "ERROR"
            sys.exit(-1)

# compute kde and bandwidth using likelihood CV on training data
if bandwidth < 0:
    train_values = np.array(sorted([fval
                                    for gid, fval
                                    in train_feature_values])).reshape(-1,1)
    params = {'bandwidth': np.arange(1, 10, 0.05)}
    print params
    grid = GridSearchCV(KernelDensity(), params, cv=LeaveOneOut(len(train_values)),
                        n_jobs=4, verbose=1)
    grid.fit(train_values)
    print "Best bandwidth:", grid.best_params_, grid.best_score_

# compute histogram
minval = min(train_values)
maxval = max(train_values)
nbins = (maxval - minval)/binwidth;
bins = np.arange(minval, maxval+binwidth+binwidth, binwidth)
a = np.arange(len(bins))
hist, _ = np.histogram(train_values, bins=bins, density=True)
#print hist
#print bins

# plot histogram
colours = ["#348ABD", "#A60628"]
plt.figure(figsize=(16,4))
plt.hold(True)
plt.bar(left=bins[:-1], width=binwidth, height=hist, color=colours[0],
        label='Normalized Histogram', alpha=0.6, edgecolor=colours[0], lw="3")

# plot kde
kdex = np.arange(bins[0]-binwidth, bins[-1]+binwidth, step=binwidth/100.0)
kde = grid.best_estimator_
pdf = np.exp(kde.score_samples(kdex.reshape(-1,1)))
plt.plot(kdex, pdf, lw="2", alpha=0.6, color='black', label='PDF')

# plot rug data points
ymin, ymax = plt.ylim()
ycenter = (ymax - ymin) * 0.8
plt.plot(train_values, [ycenter]*len(train_values), '|', color='k',
         label='Feature Values')

plt.legend(loc='best')
plt.xlim(bins[0]-binwidth, bins[-1]+binwidth)
plt.xticks(bins, bins.flatten(), rotation=45)
plt.savefig('kde-' + feat_name + '.pdf', bbox_inches='tight')

# for each training point, anomaly score = 1 - p(x) where p(x) is from KDE 
# compute anomaly scores

# plot PR curve

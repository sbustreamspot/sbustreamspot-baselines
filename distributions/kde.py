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

print 'Computing KDE for', feat_name

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
train_values = np.array(sorted([fval
                                for gid, fval
                                in train_feature_values])).reshape(-1,1)
if bandwidth < 0:
    params = {'bandwidth': np.arange(1, 10, 0.05)}
    print params
    grid = GridSearchCV(KernelDensity(), params, cv=LeaveOneOut(len(train_values)),
                        n_jobs=4, verbose=1)
    grid.fit(train_values)
    kde = grid.best_estimator_
    print "Best bandwidth:", grid.best_params_, grid.best_score_
else:
    kde = KernelDensity(bandwidth=bandwidth).fit(train_values)

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
colours = ["#348ABD", "#A60628", "#f04b09"]
plt.figure(figsize=(16,4))
plt.hold(True)
plt.bar(left=bins[:-1], width=binwidth, height=hist, color=colours[0],
        label='Normalized histogram', alpha=0.6, edgecolor=colours[0], lw="3")

# plot kde
kdex = np.arange(bins[0]-binwidth, bins[-1]+binwidth, step=binwidth/100.0)
pdf = np.exp(kde.score_samples(kdex.reshape(-1,1)))
plt.plot(kdex, pdf, lw="2", alpha=0.6, color='black', label='Estimated PDF')

# plot rug data points
ymin, ymax = plt.ylim()
ycenter = (ymax - ymin) * 0.8
plt.plot(train_values, [ycenter]*len(train_values), '|', color='k',
         label='Training feature values')

test_values = np.array([feat_val
                        for gid, feat_val in test_feature_values]).reshape(-1,1)
test_malicious_values = {}
for scenario in MALICIOUS_SCENARIOS:
    test_malicious_values[scenario] = [feat_val
                                       for gid, feat_val in test_feature_values
                                       if gid/100 == scenario]
test_benign_values = [feat_val for gid, feat_val in test_feature_values
                         if gid/100 in BENIGN_SCENARIOS]
plt.plot(test_benign_values, [ycenter]*len(test_benign_values), '|',
         color=colours[0], label='Test feature values (benign)')
for i, scenario in enumerate(MALICIOUS_SCENARIOS):
    values = test_malicious_values[scenario]
    plt.plot(values, [ycenter]*len(values), '|',
             color=colours[i+1],
             label='Test feature values (malicious ' + str(scenario) + ')')

plt.legend(loc='best')
plt.xlim(bins[0]-binwidth, bins[-1]+binwidth)
plt.xticks(bins, bins.flatten(), rotation=45)
plt.savefig('kde-' + feat_name + '.pdf', bbox_inches='tight')
plt.clf()
plt.close()
# finished kde plot

# scores for all points
for i, scenario in enumerate(MALICIOUS_SCENARIOS):
    all_feature_values = train_feature_values + \
                         [(gid, feat_value)
                          for gid, feat_value in test_feature_values
                          if gid/100 in BENIGN_SCENARIOS or
                             gid/100 == scenario]
    all_values = np.array([feat_value
                           for gid, feat_value in all_feature_values]).reshape(-1,1)
    y_true = [1 if gid/100 in MALICIOUS_SCENARIOS else 0
              for gid, feat_value in all_feature_values]
    anomaly_scores = [-p for p in np.exp(kde.score_samples(all_values)).flatten()]
    
    # plot my own PR curve
    precision, recall, ap = pr_curve(y_true, anomaly_scores)
    print 'Scenario: ', scenario, ap
    plt.figure()
    plt.plot(recall, precision, label='AUC (Scenario ' + str(scenario) + \
                                      ')={0:0.3f}'.format(ap), color=colours[i+1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.legend()
    plt.savefig('pr-' + feat_name + str(scenario) + '.pdf', bbox_inches='tight')
    plt.clf()
    plt.close()

"""
# visualise anomaly scores
for i in range(len(test_feature_values)):
    gid, feat_value = test_feature_values[i]
    p = inv_anomaly_scores[i]
    if gid/100 in BENIGN_SCENARIOS:
        color = colours[0]
    else:
        color = colours[1]
    plt.plot((feat_value, feat_value), (ycenter, ycenter + p),
              '-', color=color)
"""

"""
# plot PR curve
precision, recall, _ = precision_recall_curve(y_true=y_true,
                                              probas_pred=anomaly_scores)
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


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

train_values = np.array(sorted([fval
                                for gid, fval
                                in train_feature_values])).reshape(-1,1)
# compute histogram
minval = min(train_values)
maxval = max(train_values)
nbins = (maxval - minval)/binwidth;
bins = np.arange(minval, maxval+binwidth+binwidth, binwidth)
a = np.arange(len(bins))
hist, _ = np.histogram(train_values, bins=bins)
nevents = len(bins) - 1
total = np.sum(hist)
pmf = {bins[i]: (float(hist[i]) + 1.0) / (total + nevents) for i in range(len(hist))}
#print hist
#print pmf
#print bins

"""
# plot histogram
colours = ["#348ABD", "#A60628"]
plt.figure(figsize=(16,4))
plt.hold(True)
plt.bar(left=bins[:-1], width=binwidth, height=pmf, color=colours[0],
        label='PMF', alpha=0.6, edgecolor=colours[0], lw="3")

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

plt.legend(loc='best')
plt.xlim(bins[0]-binwidth, bins[-1]+binwidth)
plt.xticks(bins, bins.flatten(), rotation=45)
plt.savefig('pmf-' + feat_name + '.pdf', bbox_inches='tight')
plt.clf()
plt.close()
"""

# scores for all points
all_feature_values = train_feature_values + test_feature_values
all_values = np.array([feat_value
                       for gid, feat_value in all_feature_values]).reshape(-1,1)
y_true = [1 if gid/100 in MALICIOUS_SCENARIOS else 0
          for gid, feat_value in all_feature_values]
anomaly_scores = []
for value in all_values.flatten():
    if value in pmf:
        anomaly_scores.append(-pmf[value])
    else:
        prob = (0.0 + 1.0) / (total + nevents)
        anomaly_scores.append(-prob)

#print all_values.flatten()[300:400]
#print anomaly_scores[300:400]

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

# plot my own PR curve
precision, recall, ap = pr_curve(y_true, anomaly_scores)
print ap
plt.figure()
plt.plot(recall, precision, label='AUC={0:0.3f}'.format(ap))
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.legend()
plt.savefig('pr-' + feat_name + '.pdf', bbox_inches='tight')
plt.clf()
plt.close()

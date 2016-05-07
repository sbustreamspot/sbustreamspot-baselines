#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-baselines

from params import *
from distribution import *
import sys

feat_file = sys.argv[1]
feat_name = sys.argv[2]
binwidth = float(sys.argv[3])

benign_values = []
malicious_values = []
graphs = {}
with open(feat_file, 'r') as f:
    # skip 3 header lines
    next(f)
    next(f)
    next(f)
    for line in f:
        fields = line.strip().split('\t')
        gid = int(fields[0])
        scenario = gid/100

        if scenario in BENIGN_SCENARIOS:
            for feat_value in fields[1:]:
                benign_values.append(float(feat_value))
        elif scenario in MALICIOUS_SCENARIOS:
            for feat_value in fields[1:]:
                malicious_values.append(float(feat_value))
        else:
            print "ERROR:", gid
            sys.exit(-1)

        graphs[gid] = [float(i) for i in fields[1:]]

# set bins
all_values = benign_values + malicious_values
minval = min(all_values)
maxval = max(all_values)
nbins = (maxval - minval)/binwidth;
bins = np.arange(minval, maxval+binwidth+binwidth, binwidth)
a = np.arange(len(bins))

benign_hists = []
malicious_hists = [] 
for i in range(600):
    scenario = i/100
    values = graphs[i]
    hist, _ = np.histogram(values, bins=bins)
    if scenario in BENIGN_SCENARIOS:
        benign_hists.append(hist)
    elif scenario in MALICIOUS_SCENARIOS:
        malicious_hists.append(hist)
    else:
        print "ERROR"
        sys.exit(-1)

benign_hists = np.array(benign_hists)
malicious_hists = np.array(malicious_hists)

bmean = np.mean(benign_hists, axis=0)
bstd = np.std(benign_hists, axis=0)
mmean = np.mean(malicious_hists, axis=0)
mstd = np.std(malicious_hists, axis=0)

print bmean
print mmean
print bins

colours = ["#348ABD", "#A60628"]
plt.figure(figsize=(16,4))
plt.bar(left=a[:-1], width=1.0, height=bmean, color=colours[0],
        label='Benign', yerr=bstd, alpha=0.6, edgecolor=colours[0], lw="3")
plt.bar(left=a[:-1], width=1.0, height=mmean, color=colours[1],
        label='Malicious', yerr=mstd, alpha=0.6, edgecolor=colours[1], lw="3")
plt.xticks(a, bins, rotation=45)
plt.legend()
plt.ylabel("avg. number")
plt.xlabel(feat_name)
plt.savefig(feat_name + ".pdf", bbox_inches="tight")

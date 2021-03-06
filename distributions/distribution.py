#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-baselines

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

colours = ["#348ABD", "#A60628", "#f04b09"]

def plot_distribution(benign_values, malicious_values, feat_name, binwidth=20,
                      malicious_scenario=0):
    malicious_scenarios = list(malicious_values.keys())
    all_values = [i for i in benign_values]
    for l in malicious_values.values():
        all_values.extend(l)
    minval = min(all_values)
    maxval = max(all_values)
    print 'Min, max, bw:', minval, maxval, binwidth
    nbins = (maxval - minval)/binwidth;
    bins = np.arange(minval, maxval+binwidth+binwidth, binwidth)
    a = np.arange(len(bins))
    benign_hist, _ = np.histogram(benign_values, bins=bins)
    malicious_hists = []
    for scenario in malicious_scenarios:
        malicious_hist, _ = np.histogram(malicious_values[scenario], bins=bins)
        malicious_hists.append(malicious_hist)
    print 'Benign:', benign_hist
    print 'Malicious:', malicious_hists
    print 'Bins:', bins

    plt.figure(figsize=(16,4))
    plt.bar(left=a[:-1], width=1.0, height=benign_hist, color=colours[0],
            label='Benign', alpha=0.6, edgecolor=colours[0], lw="3")
    plt.bar(left=a[:-1], width=1.0, height=malicious_hists[malicious_scenario],
            color=colours[malicious_scenario+1],
            label='Malicious (Scenario ' + \
                   str(malicious_scenarios[malicious_scenario]) + ')',
            alpha=0.6, edgecolor=colours[malicious_scenario+1], lw="3")
    plt.xticks(a, bins, rotation=45) 
    plt.legend()
    """
    if feat_name == "density":
        plt.xlabel(feat_name + " x 10000")
    else:
        plt.xlabel(feat_name)
    plt.ylabel("number of graphs")
    """
    plt.savefig(feat_name + str(malicious_scenario) + ".pdf", bbox_inches="tight")

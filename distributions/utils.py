#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-analyze

import numpy as np
from params import *
from collections import defaultdict

def split_train_test(benign_scenarios, attack_scenarios, train_frac):
    """
        - Samples train_frac of the benign graphs in given scenarios for training.
        - Uses the attack graphs and 1 - train_frac of the benign graphs in the
          given scenarios for testing.
    """

    num_graphs_train = int(train_frac * NUM_SCENARIO_GRAPHS)
    train_ids = []
    test_ids = []
    for i in benign_scenarios:
        scenario_gids = range(100*i, 100*i + NUM_SCENARIO_GRAPHS)

        np.random.shuffle(scenario_gids)
        train_gids = scenario_gids[:num_graphs_train]
        test_gids = scenario_gids[num_graphs_train:]

        train_ids.extend(train_gids)
        test_ids.extend(test_gids)

    for attack_scenario in attack_scenarios:
        test_ids.extend(range(100*attack_scenario,
                              100*attack_scenario + NUM_SCENARIO_GRAPHS))

    return train_ids, test_ids

def pr_curve(labels, scores):
    labels_and_scores = zip(labels, scores)
    labels_and_scores = sorted(labels_and_scores, key=lambda x: x[1],
                               reverse=True)
    prev_r = 0.0
    ap = 0.0
    anomaly_idx = 0.0
    precisions = []
    recalls = []
    for threshold_idx in range(len(labels_and_scores)-1):
        label = labels_and_scores[threshold_idx][0]
        score = labels_and_scores[threshold_idx][1]
        if label == 0: # not an anomaly
            continue
        anomaly_idx += 1.0

        pred_true = [t[0] for t in labels_and_scores[:threshold_idx+1]]
        pred_false = [t[0] for t in labels_and_scores[threshold_idx+1:]]

        tp = sum([1 for i in pred_true if i == 1])
        fp = sum([1 for i in pred_true if i == 0])
        tn = sum([1 for i in pred_false if i == 0])
        fn = sum([1 for i in pred_false if i == 1])

        p = float(tp) / (tp + fp)
        r = float(tp) / (tp + fn)
        tpr = float(tp) / (tp + fn)
        fpr = float(fp) / (fp + tn)

        assert r == anomaly_idx/100.0

        ap += p * (r - prev_r)
        prev_r = r

        precisions.append(p)
        recalls.append(r)

    return precisions, recalls, ap

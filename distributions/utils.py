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

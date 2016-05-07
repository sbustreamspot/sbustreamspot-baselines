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

        if scenario in BENIGN_SCENARIOS:
            benign_values.append(feat_value)
        elif scenario in MALICIOUS_SCENARIOS:
            malicious_values.append(feat_value)
        else:
            print "ERROR:", gid
            sys.exit(-1)

plot_distribution(benign_values, malicious_values, feat_name=feat_name,
                  binwidth=binwidth)

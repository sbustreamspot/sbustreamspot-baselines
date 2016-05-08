#!/usr/bin/env bash
python kde.py metrics/density.txt "density" 2 0.75 2.33
python kde.py metrics/avg-path-length.txt "avg-path-length" 0.05 0.75 0.004
python kde.py metrics/avg-eccentricity.txt "avg-eccentricity" 0.02 0.75 0.011
python kde.py metrics/avg-degree.txt "avg-degree" 150 0.75 115.0
python kde.py metrics/avg-distinct-degree.txt "avg-distinct-degree" 5 0.75 9.0

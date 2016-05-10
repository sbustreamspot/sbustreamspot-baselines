#!/usr/bin/env bash
python graph_distributions.py metrics/nverts.txt "nverts" 150 0
python graph_distributions.py metrics/nverts.txt "nverts" 150 1
python graph_distributions.py metrics/nedges.txt "nedges" 15000 0
python graph_distributions.py metrics/nedges.txt "nedges" 15000 1
python graph_distributions.py metrics/density.txt "density" 2 0
python graph_distributions.py metrics/density.txt "density" 2 1
python graph_distributions.py metrics/diameter.txt "diameter" 1 0
python graph_distributions.py metrics/diameter.txt "diameter" 1 1
python graph_distributions.py metrics/effective-diameter.txt "effective-diameter" 1 0
python graph_distributions.py metrics/effective-diameter.txt "effective-diameter" 1 1
python graph_distributions.py metrics/avg-path-length.txt "avg-path-length" 0.1 0
python graph_distributions.py metrics/avg-path-length.txt "avg-path-length" 0.1 1
python graph_distributions.py metrics/avg-eccentricity.txt "avg-eccentricity" 0.02 0
python graph_distributions.py metrics/avg-eccentricity.txt "avg-eccentricity" 0.02 1
python graph_distributions.py metrics/radius.txt "radius" 1 0
python graph_distributions.py metrics/radius.txt "radius" 1 1
python graph_distributions.py metrics/max-degree.txt "max-degree" 10000 0
python graph_distributions.py metrics/max-degree.txt "max-degree" 10000 1
python graph_distributions.py metrics/avg-degree.txt "avg-degree" 150 0
python graph_distributions.py metrics/avg-degree.txt "avg-degree" 150 1
python graph_distributions.py metrics/max-distinct-degree.txt "max-distinct-degree" 25 0
python graph_distributions.py metrics/max-distinct-degree.txt "max-distinct-degree" 25 1
python graph_distributions.py metrics/avg-distinct-degree.txt "avg-distinct-degree" 5 0
python graph_distributions.py metrics/avg-distinct-degree.txt "avg-distinct-degree" 5 1
#python feature_distribution.py path-length-distribution.txt "path-length-distribution" 1
#python feature_distribution.py degree-distribution.txt "degree-distribution" 10000
#python feature_distribution.py distinct-degree-distribution.txt "distinct-degree-distribution" 100

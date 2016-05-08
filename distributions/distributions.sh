#!/usr/bin/env bash
python graph_distribution.py metrics/nverts.txt "# nodes" 150
python graph_distribution.py metrics/nedges.txt "# edges" 15000
python graph_distribution.py metrics/density.txt "density" 2
python graph_distribution.py metrics/diameter.txt "diameter" 1
python graph_distribution.py metrics/effective-diameter.txt "effective-diameter" 1
python graph_distribution.py metrics/avg-path-length.txt "avg-path-length" 0.1
python graph_distribution.py metrics/avg-eccentricity.txt "avg-eccentricity" 0.02
python graph_distribution.py metrics/radius.txt "radius" 1
python graph_distribution.py metrics/max-degree.txt "max-degree" 10000
python graph_distribution.py metrics/avg-degree.txt "avg-degree" 150
python graph_distribution.py metrics/max-distinct-degree.txt "max-distinct-degree" 25
python graph_distribution.py metrics/avg-distinct-degree.txt "avg-distinct-degree" 5
python feature_distribution.py path-length-distribution.txt "path-length-distribution" 1
python feature_distribution.py degree-distribution.txt "degree-distribution" 10000
python feature_distribution.py distinct-degree-distribution.txt "distinct-degree-distribution" 100

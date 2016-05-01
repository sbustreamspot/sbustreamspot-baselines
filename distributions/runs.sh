#!/usr/bin/env bash
python main.py nverts.txt "# nodes" 150
python main.py nedges.txt "# edges" 15000
python main.py density.txt "density" 2
python main.py diameter.txt "diameter" 1
python main.py effective-diameter.txt "effective-diameter" 1
python main.py avg-path-length.txt "avg-path-length" 0.1
python main.py avg-eccentricity.txt "avg-eccentricity" 0.02
python main.py radius.txt "radius" 1
python main.py density.txt "density" 2
python main.py max-degree.txt "max-degree" 10000
python main.py avg-degree.txt "avg-degree" 150
python main.py max-distinct-degree.txt "max-distinct-degree" 25
python main.py avg-distinct-degree.txt "avg-distinct-degree" 5

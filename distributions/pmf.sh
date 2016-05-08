#!/usr/bin/env bash
python pmf.py metrics/diameter.txt "diameter" 1 0.75
python pmf.py metrics/max-degree.txt "max-degree" 1 0.75
python pmf.py metrics/max-distinct-degree.txt "max-distinct-degree" 1 0.75
python pmf.py metrics/nedges.txt "# edges" 1 0.75
python pmf.py metrics/nverts.txt "# nodes" 1 0.75

#!/usr/bin/env bash
for feature in nverts nedges density diameter effective-diameter avg-path-length avg-degree max-degree avg-distinct-degree max-distinct-degree avg-eccentricity
do
  echo "Computing $feature..."
  ./streamspot --edges=../../sbustreamspot-data/all.tsv --feature $feature > $feature.txt
  echo "Done."
done

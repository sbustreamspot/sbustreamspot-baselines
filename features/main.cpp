/* 
 * Copyright 2016 Emaad Ahmed Manzoor
 * License: Apache License, Version 2.0
 * http://www3.cs.stonybrook.edu/~emanzoor/streamspot/
 */

#include <algorithm>
#include <bitset>
#include <cassert>
#include <chrono>
#include <deque>
#include <iostream>
#include <queue>
#include <random>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "cluster.h"
#include "docopt.h"
#include "graph.h"
#include "hash.h"
#include "io.h"
#include "param.h"
#include "simhash.h"
#include "streamhash.h"

using namespace std;

static const char USAGE[] =
R"(StreamSpot.

    Usage:
      streamspot --edges=<edge file>
                 --feature=<feature>

      streamspot (-h | --help)

    Options:
      -h, --help                              Show this screen.
      --edges=<edge file>                     Incoming stream of edges.
      --feature=<feature>                     Feature to compute for each graph.
)";

int main(int argc, char *argv[]) {
  map<string, docopt::value> args = docopt::docopt(USAGE, { argv + 1, argv + argc });

  string edge_file(args["--edges"].asString());
  string feature(args["--feature"].asString());

  cout << "StreamSpot (";
  cout << "Edges=" << edge_file << " ";
  cout << "Feature=" << feature << "";
  cout << ")" << endl;

  unordered_set<uint32_t> train_gids;
  for (uint32_t i = 0; i < 600; i++) {
    train_gids.insert(i);
  }

  unordered_set<uint32_t> scenarios;
  for (uint32_t i = 0; i < 6; i++) {
    scenarios.insert(i);
  }

  uint32_t num_graphs;
  uint32_t num_test_edges;
  vector<edge> train_edges;
  unordered_map<uint32_t,vector<edge>> test_edges;
  tie(num_graphs, train_edges, test_edges, num_test_edges) =
    read_edges(edge_file, train_gids, scenarios);

  if (num_graphs == 0) {
    cout << "0 graphs in file" << endl;
    exit(-1);
  }

  vector<graph> graphs(num_graphs);
  cout << "Constructing " << num_graphs << " graphs..." << endl;
  for (auto& e : train_edges) {
    update_graphs(e, graphs);
  }

  // feature computation
  if (feature.compare("nverts") == 0) {
    // # nodes
    unordered_map<uint32_t,uint32_t> number_of_nodes;
    for (uint32_t i = 0; i < num_graphs; i++) {
      number_of_nodes[i] = get_number_of_nodes(graphs[i]);
    }
    for (uint32_t i = 0; i < num_graphs; i++) {
      cout << i << "\t" << number_of_nodes[i] << endl;
    }
  } else if (feature.compare("nedges") == 0) {
    // # edges
    unordered_map<uint32_t,uint32_t> number_of_edges;
    for (uint32_t i = 0; i < num_graphs; i++) {
      number_of_edges[i] = get_number_of_edges(graphs[i]);
    }
    for (uint32_t i = 0; i < num_graphs; i++) {
      cout << i << "\t" << number_of_edges[i] << endl;
    }
  } else if (feature.compare("diameter") == 0) {
    unordered_map<uint32_t,uint32_t> diameter;
    for (uint32_t i = 0; i < num_graphs; i++) {
      diameter[i] = get_diameter(graphs[i]);
    }
    for (uint32_t i = 0; i < num_graphs; i++) {
      cout << i << "\t" << diameter[i] << endl;
    }
  } else {
    cout << "Unknown feature: " << feature << ". Available features:" << endl;
    cout << "\tnverts\t\t# nodes" << endl;
    cout << "\tnedges\t\t# nodes" << endl;
    exit(-1);
  }

  return 0;
}

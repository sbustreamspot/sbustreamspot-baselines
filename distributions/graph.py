#!/usr/bin/env python

# Copyright 2016 Emaad Ahmed Manzoor
# License: Apache License, Version 2.0
# https://github.com/sbustreamspot/sbustreamspot-baselines

from params import *
from graph_tool.all import *

def construct_graphs(edge_file):
    """
        Reads in one edge per line from the UIC data
        and constructs graph-tool graphs.
    """
    graphs = []
    for i in xrange(NUM_GRAPHS):
        g = Graph(directed=True)

        # properties
        gid = g.new_graph_property('int')
        vid = g.new_vertex_property('int')
        vtype = g.new_vertex_property('string')
        etype = g.new_edge_property('string')
        g.gp.id = gid
        g.vp.id = vid
        g.vp.type = vtype
        g.ep.type = etype

        graphs.append(g)

    lno = 0
    with open(edge_file, 'r') as f:
        for line in f:
            if lno > 10000:
                break
            lno += 1
            fields = line.split('\t')
            s = int(fields[0]) # src
            stype = fields[1]
            t = int(fields[2]) # dest
            ttype = fields[3]
            etype = fields[4]
            gid = int(fields[5])

            g = graphs[gid]
            g.gp.id = gid

            # check if source vertex exists
            matches = find_vertex(g, g.vp.id, s)
            if len(matches) == 0:
                u = g.add_vertex()
            else:
                u = matches[0]
            
            matches = find_vertex(g, g.vp.id, t)
            if len(matches) == 0:
                v = g.add_vertex()
            else:
                v = matches[0]
            
            g.vp.id[u] = s
            g.vp.type[u] = stype
            g.vp.id[v] = t
            g.vp.type[v] = ttype
            e = g.add_edge(u,v)
            g.ep.type[e] = etype

    return graphs

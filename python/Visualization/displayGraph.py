#! /usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np
import networkx as nx

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("graph_file", help="The file containing the graph")
    parser.add_argument("graph_format", help="Format of the graph")

    return parser.parse_args()

def read_graph(graph_file, graph_format):
    G = nx.Graph()
    if graph_format == 'mst':
        with open(graph_file) as input_file:
            for line in input_file:
                if line[0] == 'n':
                    _, key, x, y = line.strip('\n').split()
                    G.add_node(int(key), pos=(int(x),int(y)))
                elif line[0] == 'e':
                    _, u, v, weight = line.strip('\n').split()
                    G.add_edge(int(u),int(v))
    else:
        print("Graph format '{}' is not currently supported".format(graph_format))
    return G

if __name__ == '__main__':
    args = parse_arguments()
    G = read_graph(args.graph_file, args.graph_format)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, node_size=5, with_labels=True)
    plt.show()

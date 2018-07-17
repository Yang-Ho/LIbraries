#! /usr/bin/env python3

import argparse
import operator
import numpy as np
import sys
import networkx as nx

global _trace
_trace = False

from collections import deque

# May need to change this if the graph is too large
sys.setrecursionlimit(10000) 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file of graph")
    parser.add_argument("-l", help="Flag indicating input_file is a list of graphs", action='store_true', dest="list_flag")
    parser.add_argument("-d", help="directory containing files in list", dest="list_dir")
    parser.add_argument("-p", help="Flag indicating input_file is a list of permutations", action='store_true', dest="permutation_flag")
    parser.add_argument("-gl", help="Flag indicating input_file is a list of groups", action='store_true', dest="group_flag")
    parser.add_argument("-gd", help="directory containing group lists", dest="group_dir")
    parser.add_argument("--trace", help="trace dfs", action='store_true', dest="trace")
    return parser.parse_args()

# Read in graph
def read_graph(filename):
    G = nx.Graph()
    E = 0
    with open(filename) as in_file:
        for line in in_file:
            if '#' not in line and len(line) > 1:
                edge = [int(v) for v in line.strip('\n').split()]
                G.add_edge(*edge)
                E += 1
    return G, len(G), E

def get_k_core_number(G):
    return max(nx.core_number(G).values())

def get_key(graph_name):
    graph_name = graph_name.strip('\n')
    _, v, e, layer_var, degree_var, seed, added = graph_name.strip('.txt').split('-')
    v, e, layer_var, degree_var, added = int(v), int(e), float(layer_var), float(degree_var), int(added)
    key = (v, e, added, layer_var, degree_var)
    return key

def compute_stats(distribution):
    return np.mean(distribution), np.std(distribution, ddof=1), np.median(distribution)

if __name__ == "__main__":
    args = parse_arguments()
    _trace = args.trace
    if args.list_flag:
        list_dir = args.list_dir
        print("Instance, V, E, degen")
        with open(args.input_file) as input_list:
            for line in input_list:
                line = line.strip('\n')
                graph, V, E = read_graph(list_dir + line)
                k_core_number = get_k_core_number(graph)
                print("{},{},{},{}".format(line.strip('.txt'), V, E, k_core_number))
    elif args.permutation_flag:
        list_dir = args.list_dir
        print("Instance, mean degen, std degen, median, max, min")
        results = {}
        with open(args.input_file) as input_list:
            for line in input_list:
                line = line.strip('\n')
                graph, V, E = read_graph(list_dir + line)
                k_core_number = get_k_core_number(graph)
                base = line.strip('.txt')[:-3]
                if base not in results:
                    results[base] = []
                results[base].append(k_core_number)
        for instance in results:
            print("{},{},{},{},{},{}".format(instance,
                    np.mean(results[instance]),
                    np.std(results[instance], ddof=1),
                    np.median(results[instance]),
                    max(results[instance]),
                    min(results[instance])))
    elif args.group_flag:
        group_dir = args.group_dir
        list_dir = args.list_dir
        k_core_numbers = {}
        with open(args.input_file) as group_list:
            for group in group_list:
                group = group.strip("\n")
                with open(group_dir + group) as graph_list:
                    for graph in graph_list:
                        graph = graph.strip('\n')
                        G, _, _ = read_graph(list_dir + graph)
                        key = get_key(graph)
                        if key not in k_core_numbers:
                            k_core_numbers[key] = []
                        k_core_number = get_k_core_number(G)
                        k_core_numbers[key].append(k_core_number)
        header = ",".join(["V", "B", "A", "L", "D", "Mean degen", "Std degen", "Median degen"])
        print(header)
        for key in k_core_numbers:
            key_string = ",".join([str(k) for k in key])
            k_core_stats= compute_stats(k_core_numbers[key])
            k_core_string = ",".join([str(s) for s in k_core_stats])
            print(",".join([key_string, k_core_string]))
    else:
        graph, V, E = read_graph(args.input_file)
        print(graph)
        print(V)
        print(E)
        print("Data for {}".format(args.input_file))
        k_core_number = get_k_core_number(graph)
        print("Degeneracy {}".format(k_core_number))

#  [Last modified: 2018 02 27 at 01:26:10 GMT]

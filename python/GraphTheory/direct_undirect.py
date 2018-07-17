#! /usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file of graph")
    return parser.parse_args()

# Read in graph
def read_graph(filename):
    adj = {}
    E = 0
    lines = []
    with open(filename) as in_file:
        for line in in_file:
            line = line.strip('\n')
            if '#' not in line and len(line) > 1:
                edge = [int(v) for v in line.split()]
                if edge[0] not in adj:
                    adj[edge[0]] = []
                if edge[1] not in adj:
                    adj[edge[1]] = []
                if edge[0] != edge[1]:
                    if edge[1] not in adj[edge[0]]:
                        adj[edge[0]].append(edge[1])
                        adj[edge[1]].append(edge[0])
                        E += 1
                        lines.append(line)
            if len(line) > 1:
                lines.append(line)
    return lines, len(adj), E

if __name__ == "__main__":
    args = parse_arguments()
    lines, V, E = read_graph(args.input_file)
    print("# directed version of {}\n".format(args.input_file))
    print("# undirected stats:\nn = {}, m = {}\n".format(V, E))
    for line in lines:
        print(line)
#  [Last modified: 2018 02 27 at 01:26:10 GMT]

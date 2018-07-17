#! /usr/bin/env python
import argparse
import networkx as nx
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 20, 'lines.linewidth':2})
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math

def parse_arguments():
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("list", help="List of groups")
    parser.add_argument("direct", help="directory")
    parser.add_argument("xlims", help="xlims")
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")

    return parser.parse_args()

def get_degree_dist(graph_file_name):
    degrees = {}
    with open(graph_file_name, 'r') as graph_file:
        for line in graph_file:
            if '#' not in line:
                line = line.strip('\n')
                if len(line) > 0:
                    u, v = [int(x) for x in line.split()]
                    if u not in degrees:
                        degrees[u] = 0
                    if v not in degrees:
                        degrees[v] = 0
                    degrees[u] += 1
                    degrees[v] += 1
    V = max(degrees)
    distribution = [0 for i in range(V + 1)]
    for v in degrees:
        distribution[degrees[v]] += 1
    return distribution 

if __name__ == '__main__':
    args = parse_arguments()
    list_file = args.list
    sums = {}
    count = 0
    with open (list_file, 'r') as graph_list:
        for line in graph_list:
            count += 1
            line = line.strip()
            dist = get_degree_dist(args.direct + "/" + line)
            for i in range(len(dist)):
                if i not in sums:
                    sums[i] = []
                sums[i].append(dist[i])
    avg_dist = [np.mean(sums[s]) for s in sorted(sums.keys())]
    errors = [np.std(sums[s], ddof=1) for s in sorted(sums.keys())]
    ax = plt.subplot(111)
    #ax.bar(list(range(len(avg_dist))),avg_dist,align='center', yerr=errors)
    ax.bar(list(range(len(avg_dist))),avg_dist,align='center')
    ax.set_xlim([int(x) for x in args.xlims.split(',')])

    if not args.fig_name:
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

#! /usr/bin/env python
import argparse
import itertools
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 5, 'lines.linewidth':5})
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math

plt.style.use('seaborn')

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("group", help="Which column to use to group the data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    group_index = int(args.group)
    x_axis = int(args.x_axis)
    data = {}

    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')
                group = line[group_index]
                if group not in data:
                    data[group] = []

                data[group].append(float(line[x_axis]))
            else:
                header = line.split(',')

    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)

    print("x:",header[x_axis])
    print(data)
    series = []
    labels = []
    for group in data:
        labels.append(group)
        series.append(data[group])
    ax.set_xlim([0,1])
    ax.boxplot(series, labels=labels, positions=[0.05, 0.5, 0.95])
    ax.set_xlabel("Base variance")
    ax.set_ylabel("Runtime Ratio")


    fig.suptitle(args.title)

    print("Labels:",labels)
    print("Axes:",ax)

    # special axis: use to draw horizontal/vertical lines
    special_ax = ax.twiny()

    special_ax.axhline(1, ls='--', c='grey', label='200')
    special_ax.text(0.85, 0.95, "1.000")
    special_ax.set_xticks([])
    special_ax.set_xticklabels([])
    special_ax.get_xaxis().set_visible(False)
    special_ax.get_yaxis().set_visible(False)


    if not args.fig_name:
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

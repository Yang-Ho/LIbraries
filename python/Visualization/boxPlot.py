#! /usr/bin/env python

import argparse
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import matplotlib.ticker as tick
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which columns to use as y-axis")
    parser.add_argument("x_label", help="What to use as label for x-axis")
    parser.add_argument("y_label", help="What to use as label for y-axis")
    parser.add_argument("title", help="What to use as chart title")
    #parser.add_argument("subtitle", help="What to use as chart subtitle")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_axis = int(args.x_axis)
    y_axis = int(args.y_axis)
    data = {}
    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')
                x = 100 * float(line[x_axis])
                if x not in data:
                    data[x] = []
                y_value = float(line[y_axis])
                data[x].append(float(line[y_axis]))
            else:
                header = line.split(',')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)
    positions = []
    dataset = []
    labels = ["2n", "4n", "8n", "16n", "32n"]
    for key in data:
        positions.append(key)
        dataset.append(data[key])

    ax.boxplot(dataset, positions=positions, labels=labels)
    fig.suptitle(args.title)
    plt.show()

#! /usr/bin/env python

import argparse
import itertools
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def parse_arguments():
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("data", help="The file containing data")
    parser.add_argument("x_axis", help="The field to use as x-axis")
    parser.add_argument("x_label", help="The field to use as x-axis")
    parser.add_argument('y_axis1', help="The field(s) to use as y axis 1")
    parser.add_argument('y_axis2', help="The field(s) to use as y axis 2")
    parser.add_argument('title', help="The title to use for plot")
    parser.add_argument('y1_label', help="The field(s) to use as y axis 1")
    parser.add_argument('y2_label', help="The field(s) to use as y axis 2")
    parser.add_argument('save_fig', help="Figure filename")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_field = int(args.x_axis)
    y_field_1 = [int(y) for y in args.y_axis1.split(',')]
    y_field_2 = [int(y) for y in args.y_axis2.split(',')]
    title = args.title.strip()
    y1 = {i:[] for i in y_field_1}
    y2 = {i:[] for i in y_field_2}
    x = []
    header = None 
    with open(args.data) as input_file:
        for line in input_file:
            line = line.strip('\n')
            if not header:
                header = line.split(',')
                continue
            line = line.split(',')
            x.append(int(line[x_field]))
            for i in y_field_1:
                y1[i].append(float(line[i]))
            for i in y_field_2:
                y2[i].append(float(line[i]))

    marker = itertools.cycle(('+', '^', 'o', '*'))
    color = itertools.cycle(('r', 'g', 'b', 'c', 'p'))
    print(x, y1, y2)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    miny2, maxy2 = 1000, 0
    for y in y1:
        ax1.plot(x, y1[y], marker=next(marker), color=next(color), label=header[y])
    for y in y2:
        ax2.plot(x, y2[y], marker=next(marker), color=next(color), label=header[y])
        temp_min = min(y2[y])
        temp_max = max(y2[y])
        if temp_min < miny2:
            miny2 = temp_min
        if temp_max > maxy2:
            maxy2 = temp_max
    ax1.set_xlabel(args.x_label)
    ax1.set_xscale('log')
    ax1.set_ylabel(args.y1_label)
    ax2.set_ylabel(args.y2_label)
    ax2.set_yscale('log')

    # Set ticks
    x_lims = [min(x) - min(x)/4, max(x) + max(x)/4]

    ax1.plot(x_lims, [0, 0], '-', dashes=[8,2])
    ax1.set_xlim(x_lims)
    ax1.set_xticks(x)
    ax1.get_xaxis().set_major_formatter(tick.ScalarFormatter())

    ax2.set_xlim(x_lims)
    ax2.set_yticks([miny2, (miny2 + maxy2)/2, maxy2])
    ax2.get_yaxis().set_major_formatter(tick.ScalarFormatter())

    #fig.legend(loc='upper right')
    fig.legend()
    fig.suptitle(title)
    #plt.savefig(args.save_fig)
    plt.show()

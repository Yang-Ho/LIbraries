#! /usr/bin/env python
import argparse
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math
import seaborn as sns

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("group", help="Which column to use to group the data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which columns to use as y-axis")
    parser.add_argument("x_label", help="What to use as label for x-axis")
    parser.add_argument("y_labels", help="What to use as label for y-axis")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--xlog", help="Use log scale for x-axis", action='store_true')
    parser.add_argument("--ylog", help="Use log scale for y-axis", action='store_true')
    parser.add_argument("--connect", help="Connect data points", action='store_true')
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")
    parser.add_argument("--legend_pos", nargs=1, dest='legend_pos', help="Postion to place the legend")
    parser.add_argument("--error", nargs=1, dest='error', help="Column(s) to use as error")
    parser.add_argument("--ymin", nargs=1, dest='y_min', type=float, help="minimum of y axis")
    parser.add_argument("--ymax", nargs=1, dest='y_max', type=float, help="maximum of y axis")
    parser.add_argument("--xmin", nargs=1, dest='x_min', type=float, help="minimum of x axis")
    parser.add_argument("--xmax", nargs=1, dest='x_max', type=float, help="maximum of x axis")
    parser.add_argument("--skip_iter", nargs=1, dest='skip_iter', type=int, default=[0], help="maximum of x axis")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    group_index = int(args.group)
    x_axis = int(args.x_axis)
    y_axes = [int(y) for y in args.y_axis.split(',')]
    error_index = {}
    if args.error:
        print(args.error)
        errors = [int(e) for e in args.error[0].split(',')]
        index = 0
        for y in y_axes:
            error_index[y] = errors[index]
            index += 1

    y_labels= [y for y in args.y_labels.split(',')]
    axes = []
    data = {}

    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')
                group = line[group_index]
                if group not in data:
                    data[group] = {'x':[]}
                    if args.error:
                        data[group]['error'] = {} 
                    for y in y_axes:
                        data[group][y] = []
                        data[group]['label'] = []
                        if args.error:
                            data[group]['error'][y] = []

                data[group]['x'].append(float(line[x_axis]))
                index = 0
                for y in y_axes:
                    y_value = float(line[y])
                    data[group][y].append(float(line[y]))
                    if args.error:
                        error_value = float(line[error_index[y]])
                        if error_value > y_value:
                            error_value = 0.999 * y_value
                        data[group]['error'][y].append(error_value)
                    index += 1
            else:
                header = line.split(',')

    for group in data:
        for y in y_axes:
            data[group]['label'].append(header[y])

    skip_iter = args.skip_iter[0] 
    colors = itertools.cycle(('red', 'lawngreen', 'deepskyblue', 'darkorchid', 'orange', 'm'))
    markers = itertools.cycle(('o', 'v', 'P', '*', 'X', 'D', '<', '>', 'h', '^'))

    for i in range(skip_iter):
        next(markers)
        next(colors)

    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)

    labels = []

    minys = [1000 for y in data]
    maxys = [0 for a in data]
    minx = 1000
    maxx = 0
    print("group:",header[group_index])
    print("x:",header[x_axis])
    for y in y_axes:
        print("y:",header[y].strip())
    for e in error_index:
        print("e:",header[error_index[e]])
    print(data)
    for group in data:
        index = 0

        plot_params ={}
        if not args.connect:
            plot_params['linestyle'] = '-'
        if len(data) > 1:
            plot_params['color'] = next(colors)

        hue_index = 0
        for y in y_axes:
            hue = [data[group]['label'][hue_index] for y in y_axes]

            hue_index += 1

            print("X: {}\n".format(data[group]['x']))
            print("Y: {}\n".format(data[group][y]))
            print("H: {}\n".format(data[group]['label']))

            color = next(colors)
            print("color: {}".format(color))
            sns.stripplot(data[group]['x'], data[group][y], ax=ax, jitter=True, hue=hue, color=color)

            if args.y_min:
                minys[index] = args.y_min[0]
            else:
                temp_min = min(data[group][y])
                if temp_min < minys[index]:
                    minys[index] = temp_min
            if args.y_max:
                maxys[index] = args.y_max[0]
            else:
                temp_max = max(data[group][y])
                if args.error:
                    temp_max += max(data[group]['error'][y])
                if temp_max > maxys[index]:
                    maxys[index] = temp_max
            if len(y_labels) > 1:
                index += 1

        if args.x_max:
            maxx = args.x_max[0]
        else:
            temp_max = max(data[group]['x'])
            if temp_max > maxx:
                maxx = temp_max
        if args.x_min:
            minx = args.x_min[0]
        else:
            temp_min = min(data[group]['x'])
            if temp_min < minx:
                minx = temp_min

    legend_pos = 'best'
    if args.legend_pos:
        legend_pos = int(args.legend_pos[0])
        ax.legend(handles=ax.lines, labels=labels, bbox_to_anchor=(1,0.5), loc='center left', frameon=True)

    if not args.fig_name:
        #plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

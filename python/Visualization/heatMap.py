#! /usr/bin/env python
import argparse
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math

#plt.style.use('seaborn')

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which column to use as y-axis")
    parser.add_argument("value", help="Which column to use as value")
    parser.add_argument("x_label", help="What to use as label for x-axis")
    parser.add_argument("y_label", help="What to use as label for y-axis")
    parser.add_argument("value_label", help="Label of value")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--xlog", help="Use log scale for x-axis", action='store_true')
    parser.add_argument("--ylog", help="Use log scale for y-axis", action='store_true')
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")
    parser.add_argument("--legend_pos", nargs=1, dest='legend_pos', help="Postion to place the legend")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_axis = int(args.x_axis)
    y_axis = int(args.y_axis)
    value_index = int(args.value)

    x_data = []
    y_data = []
    value_data = []
    data = []
    val_min = 1
    val_max = 0
    ymin = 1000
    xmin = 1000
    ymax = 0
    xmax = 0

    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')

                x_value = float(line[x_axis])
                y_value = float(line[y_axis])
                value = float(line[value_index])

                if value > val_max:
                    val_max = value
                if value < val_min:
                    val_min = value
                if x_value > xmax:
                    xmax = x_value
                if x_value < xmin:
                    xmin = x_value
                if y_value > ymax:
                    ymax = y_value
                if y_value < ymin:
                    ymin = y_value

                x_data.append(x_value)
                y_data.append(y_value)
                value_data.append(value)

                data.append((x_value, y_value, value))
            else:
                header = line.split(',')

    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)
    
    print("x:",header[x_axis])
    print("y:",header[y_axis].strip())
    print("value:",header[value_index].strip())

    x = np.array(x_data)
    y = np.array(y_data)
    #x = np.unique(x)
    #y = np.unique(y)

    xu = np.unique(x)
    yu = np.unique(y)
    x = np.append(xu, [xu[-1]+np.diff(xu)[-1]]) - np.diff(xu)[-1]/2.
    y = np.append(yu, [yu[-1]+np.diff(yu)[-1]]) - np.diff(yu)[-1]/2.
    X,Y = np.meshgrid(x,y)

    z = np.array(value_data)
    Z = z.reshape(len(yu), len(xu))

    ary_data = np.array(data)

    #print(xmin, xmax, ymin, ymax)
    #plt.axis([xmin, xmax, ymin, ymax])
    plt.pcolor(X,Y,Z, cmap="RdYlGn_r", edgecolors="black")

    ax = plt.axes()
    x_ticks = ax.get_xticks().tolist()
    temp_labels = ['0', '1', '5', '10']
    for i in range(len(x_ticks)):
        if i % 2 == 0:
            x_ticks[i] = " "
        else:
            x_ticks[i] = temp_labels[int(i / 2)]
    ax.set_xticklabels(x_ticks)

    y_ticks = ax.get_yticks().tolist()
    temp_labels = ['0.025', '0.050', '0.100', '0.200', '0.400', '0.800']
    print(len(y_ticks), len(temp_labels))
    for i in range(len(y_ticks)):
        if i > 0 and i < len(y_ticks) - 1:
            y_ticks[i] = temp_labels[i - 1]
    ax.set_yticklabels(y_ticks)

    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)

    cbar = plt.colorbar()
    cbar.ax.set_ylabel("Runtime ratio", rotation=270, labelpad=15)

    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

#! /usr/bin/env python
import argparse
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math

plt.style.use('seaborn')
matplotlib.rcParams.update({'errorbar.capsize': 7, 'lines.linewidth':1})

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which columns to use as y-axis")
    parser.add_argument("x_label", help="What to use as label for x-axis")
    parser.add_argument("y_label", help="What to use as label for y-axis")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--ylog", help="Use log scale for y-axis", action='store_true')
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")
    parser.add_argument("--error", nargs=1, dest='error', help="Column(s) to use as error")
    parser.add_argument("--ymin", nargs=1, dest='y_min', type=float, help="minimum of y axis")
    parser.add_argument("--ymax", nargs=1, dest='y_max', type=float, help="maximum of y axis")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_axis = int(args.x_axis)
    y_axis = int(args.y_axis)
    error_index = None
    if args.error:
        error_index = int(args.error[0])

    y_label = args.y_label
    X,Y,E = [], [], []

    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')
                X.append(line[x_axis])
                Y.append(float(line[y_axis]))
                if args.error:
                    E.append(float(line[error_index]))
            else:
                header = line.split(',')

    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)

    minys = 1000
    maxys = 0
    minx = 1000
    maxx = 0

    print("x:",header[x_axis])
    print("y:",header[y_axis].strip())
    if args.error:
        print("e:",header[error_index])
    
    print(E)

    x_pos = np.arange(len(X))

    plot_params ={}
    plot_params['align'] = 'center'
    plot_params['alpha'] = 0.75
    #if args.error:
        #plot_params['yerr'] = E
        #plot_params['capsize'] = 10

    ax.bar(x_pos, Y, **plot_params)
    if args.error:
        _, caps, _ = ax.errorbar(x_pos, Y, yerr=E, capsize=15, color='black', fmt='none')
        for cap in caps:
            cap.set_markeredgewidth(1)
    #ax.set_xticks(x_pos, X)
    plt.xticks(x_pos, X)

    fig.suptitle(args.title)

    print("Axes:",ax)

    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)

    # special axis: use to draw horizontal/vertical lines
    special_ax = ax.twiny()

    #special_ax.axhline(1, ls='--', c='grey', label='200')
    #special_ax.text(0.85, 0.95, "1.000")
    #special_ax.set_xticks([])
    #special_ax.set_xticklabels([])
    special_ax.get_xaxis().set_visible(False)
    special_ax.get_yaxis().set_visible(False)

    #print(special_ax.get_xaxis().get_major_ticks())

    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

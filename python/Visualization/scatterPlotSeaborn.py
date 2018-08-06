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

    skip_iter = args.skip_iter[0] 
    if len(data) == 1 and len(y_axes) > 1:
        colors = itertools.cycle(cm.Dark2(range(len(y_axes) + skip_iter)))
    else:
        colors = itertools.cycle(cm.tab10(range(len(data) * len(y_axes) + skip_iter)))
    markers = itertools.cycle(('o', 'v', '<', '*', 'X', 'D', 'P', '>', 'h', '^'))

    for i in range(skip_iter):
        next(markers)
        next(colors)

    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)
    axes.append(ax)
    if len(y_labels) > 1:
        axes.append(ax.twinx())

    lines = []
    labels = []

    minys = [1000 for y in axes]
    maxys = [0 for a in axes]
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
            plot_params['linestyle'] = ''
        if len(data) > 1:
            plot_params['color'] = next(colors)

        for y in y_axes:
            plot_params['marker'] = next(markers)
            plot_params['markersize'] = 9 
            if len(data) == 1:
                plot_params['color'] = next(colors)
            if len(data) > 1 and len(y_axes) > 1:
                plot_params['label'] = ":".join([group.strip(), header[y].strip()])
            elif len(y_axes) > 1:
                plot_params['label'] = header[y].strip()
            else:
                plot_params['label'] = group.strip()
            plot_params['zorder'] = 2

            line = None
            line, = axes[index].plot(data[group]['x'], data[group][y], **plot_params)

            if args.error and "LP" in header[y]:
                _, caps, _ = axes[index].errorbar(data[group]['x'], data[group][y], yerr=data[group]['error'][y], fmt=None, capsize=5, color = plot_params['color'])
                for cap in caps:
                    cap.set_markeredgewidth(1)

            lines.append(line)
            labels.append(plot_params['label'])

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
    fig.suptitle(args.title)

    print("Labels:",labels)
    print("Axes:",axes)
    for i in range(len(axes)):
        axes[i].set_xlabel(args.x_label)
        axes[i].set_ylabel(y_labels[i])
        if args.xlog and i == 0:
            axes[i].set_xscale('log')
            xticks = list(np.logspace(math.log(minx,10), math.log(maxx,10), num=6))
            axes[i].set_xticks(xticks)
        else:
            xticks = list(np.linspace(minx, maxx, 6))
            axes[i].set_xticks(xticks)
        if args.ylog:
            axes[i].set_yscale('log', nonposy='clip')
            yticks = list(np.logspace(math.log(minys[i],10), math.log(maxys[i],10), num=7))
            axes[i].set_yticks(yticks)
        else:
            yticks = list(np.linspace(minys[i], maxys[i], 6))
            axes[i].set_yticks(yticks)


        axes[i].get_xaxis().set_major_formatter(tick.ScalarFormatter())
        axes[i].get_xaxis().set_minor_formatter(tick.NullFormatter())
        axes[i].get_yaxis().set_major_formatter(tick.ScalarFormatter())
        axes[i].get_yaxis().set_minor_formatter(tick.NullFormatter())

        if i > 0:
            axes[i].grid(b=False)
            axes[i].get_xaxis().set_visible(False)

    # special axis: use to draw horizontal/vertical lines
    special_ax = ax.twiny()

    #special_ax.axhline(1, ls='--', c='grey', label='200')
    #special_ax.text(0.85, 0.95, "1.000")
    #special_ax.set_xticks([])
    #special_ax.set_xticklabels([])
    special_ax.get_xaxis().set_visible(False)
    special_ax.get_yaxis().set_visible(False)

    #print(special_ax.get_xaxis().get_major_ticks())

    legend_pos = 'best'
    if args.legend_pos:
        legend_pos = int(args.legend_pos[0])
        #lines[1], lines[2] = lines[2], lines[1]
        #labels[1], labels[2] = labels[2], labels[1]
        lines[0], lines[1] = lines[1], lines[0]
        labels[0], labels[1] = labels[1], labels[0]
        lines.reverse()
        labels.reverse()
        axes[0].legend(lines, labels, bbox_to_anchor=(0.20,0.35), loc=legend_pos)

    if not args.fig_name:
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

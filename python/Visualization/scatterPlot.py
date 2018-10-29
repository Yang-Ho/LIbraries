#! /usr/bin/env python
import argparse
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
import numpy as np
import math

from matplotlib import rc
# Sets 'global' parameters such as font, fontsize, etc.
rc('errorbar', capsize=5)
rc('lines', linewidth=2)
rc('text', usetex=True)
rc('font', size=24, family='Times New Roman', weight='bold')
rc('axes', labelsize=26)
rc('xtick', labelsize=22)
rc('ytick', labelsize=22)
rc('legend', fontsize=20)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The csv file containing data")
    parser.add_argument("group", help="Which column to use to group/categorize the data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which columns to use as y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("x_title", help="What to use as title for x-axis")
    parser.add_argument("y_titles", help="What to use as titles for y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--xlog", action='store_true', help="Flag to enable log scale for x-axis")
    parser.add_argument("--ylog", action='store_true', help="Flag to enable log scale for y-axis")
    parser.add_argument("--connect", action='store_true', help="Flag to connect data points")
    parser.add_argument("--legend", action='store_true', help="Flag to display legend")
    parser.add_argument("--jitter", action='store_true', help="Flag to introduce jitter")
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Save the figure to FIG_NAME (format is pdf)")
    parser.add_argument("--error", nargs=1, dest='error', help="Column(s) to use as error. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--yticks", nargs=1, dest='y_tick_pos', help="Positions of ticks on y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--ylabels", nargs=1, dest='y_tick_labels', help="Labels of ticks on y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--xticks", nargs=1, dest='x_tick_pos', help="Positions of ticks on x-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--xlabels", nargs=1, dest='x_tick_labels', help="Labels of ticks on x-axis. Format is a comma delimited list. e.g. 1,2,3")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    # Process arguments, not the most elegant way of doing this
    use_jitter = args.jitter
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

    y_titles = [y for y in args.y_titles.split(',')]
    axes = []
    data = {}

    # Extract the data
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

    if args.y_tick_pos:
        y_tick_pos = [float(s) for s in args.y_tick_pos[0].split(',')]
    else:
        y_tick_pos = None
    if args.y_tick_labels:
        y_tick_labels = [s for s in args.y_tick_labels[0].split(',')]
    else:
        y_tick_labels = None
    if args.x_tick_pos:
        x_tick_pos = [float(s) for s in args.x_tick_pos[0].split(',')]
    else:
        x_tick_pos = None
    if args.x_tick_labels:
        x_tick_labels = [s for s in args.x_tick_labels[0].split(',')]
    else:
        x_tick_labels = None

    # Setup colors and markers
    if len(data) == 1 and len(y_axes) > 1:
        colors = itertools.cycle(cm.Dark2(range(len(y_axes))))
    else:
        colors = itertools.cycle(cm.tab10(range(len(data) * len(y_axes))))
    markers = itertools.cycle(('o', 'v', 'P', '*', 'X', 'D', '<', '>', 'h', '^'))

    # Create figure/axes
    fig = plt.figure(figsize=(6,5),dpi=100) # figsize sets the size to WxH where W and H are inches
    ax = fig.add_subplot(111)
    axes.append(ax)
    if len(y_titles) > 1:
        axes.append(ax.twinx())

    #ax.axhline(1, ls='--', c='grey', label='200')
    #ax.text(0.90, 0.93, "1.000")

    lines = []
    labels = []

    # Print information for debugging
    print("group:",header[group_index])
    print("x:",header[x_axis])
    for y in y_axes:
        print("y:",header[y].strip())
    for e in error_index:
        print("e:",header[error_index[e]])
    print(data)

    jitter_incr = 0
    if use_jitter:
        jitter_incr = -0.03

    # Plot data
    for group in sorted(data.keys()):
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

            line = None
            jittered_x = [x + jitter_incr for x in data[group]['x']]
            line, = axes[index].plot(jittered_x, data[group][y], **plot_params)
            if use_jitter:
                jitter_incr += 0.015

            if args.error:
                _, caps, _ = axes[index].errorbar(jittered_x, data[group][y], yerr=data[group]['error'][y], fmt='', capsize=5, color = plot_params['color'], linestyle='')
                for cap in caps:
                    cap.set_markeredgewidth(1)

            lines.append(line)
            labels.append(plot_params['label'])

            if len(y_titles) > 1:
                index += 1
    fig.suptitle(args.title)

    # Set axis titles, tick positions/labels, etc.
    for i in range(len(axes)):
        axes[i].set_xlabel(r"{}".format(args.x_title))
        axes[i].set_ylabel(r"{}".format(y_titles[i]))
        if args.xlog and i == 0:
            axes[i].set_xscale('log')
        if args.ylog:
            axes[i].set_yscale('log', nonposy='clip')

        if y_tick_pos:
            axes[i].get_yaxis().set_ticks(y_tick_pos)
        if y_tick_labels:
            axes[i].get_yaxis().set_ticklabels(y_tick_labels)
        if x_tick_pos:
            axes[i].get_xaxis().set_ticks(x_tick_pos)
        if x_tick_labels:
            axes[i].get_xaxis().set_ticklabels(x_tick_labels)

        axes[i].get_yaxis().set_minor_formatter(tick.NullFormatter())
        axes[i].get_xaxis().set_minor_formatter(tick.NullFormatter())

        if i > 0:
            axes[i].grid(b=False)
            axes[i].get_xaxis().set_visible(False)

    if args.legend:
        axes[0].legend(lines, labels, bbox_to_anchor=(1,0.5), loc='center left', frameon=True)

    axes[0].set_facecolor('white')
    axes[0].grid(True)

    # Display or save chart (NOTE: The default view of displaying the chart is different than how it is saved)
    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

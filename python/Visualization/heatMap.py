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
rc('text', usetex=True)
rc('font', size=24, family='Times New Roman', weight='bold')
rc('axes', labelsize=26)
rc('xtick', labelsize=22)
rc('ytick', labelsize=22)
rc('legend', fontsize=22)


# This function was pulled from an online source (that I cannot find again at the moment)
def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero.

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax / (vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False),
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("data_file", help="The file containing data")
    parser.add_argument("x_axis", help="Which column to use as x-axis")
    parser.add_argument("y_axis", help="Which column to use as y-axis")
    parser.add_argument("value", help="Which column to use as value")
    parser.add_argument("x_title", help="What to use as title for x-axis")
    parser.add_argument("y_title", help="What to use as title for y-axis")
    parser.add_argument("value_title", help="title of value")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--xlog", action='store_true', help="Flag to enable log scale for x-axis")
    parser.add_argument("--ylog", action='store_true', help="Flag to enable log scale for y-axis")
    parser.add_argument("--legend", action='store_true', help="Flag to display legend")
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Save the figure to FIG_NAME (format is pdf)")
    parser.add_argument("--group", nargs=1, dest='group', help="Which column to use to group/categorize the data")
    parser.add_argument("--yticks", nargs=1, dest='y_tick_pos', help="Positions of ticks on y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--ylabels", nargs=1, dest='y_tick_labels', help="Labels of ticks on y-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--xticks", nargs=1, dest='x_tick_pos', help="Positions of ticks on x-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--xlabels", nargs=1, dest='x_tick_labels', help="Labels of ticks on x-axis. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--valueticks", nargs=1, dest='value_tick_pos', help="Positions of ticks on the colorbar. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--valuelabels", nargs=1, dest='value_tick_labels', help="Labels of ticks on the colorbar. Format is a comma delimited list. e.g. 1,2,3")
    parser.add_argument("--gamma", nargs='?', dest='gamma', default=1, const=1, help="Gamma parameter to change the 'scale' of the colormap (warning: this is very 'hacky'). Default value is 1 (which produces a linear color scale) and must be > 0.")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_axis = int(args.x_axis)
    y_axis = int(args.y_axis)
    value_index = int(args.value)

    x_data = {}
    y_data = {}
    value_data = {}

    if not args.group:
        x_data = {'default' : []}
        y_data = {'default' : []}
        value_data = {'default' : []}

    # Set tick positions and labels
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
    if args.value_tick_pos:
        value_tick_pos = [float(s) for s in args.value_tick_pos[0].split(',')]
    else:
        value_tick_pos = None
    if args.value_tick_labels:
        value_tick_labels = [s for s in args.value_tick_labels[0].split(',')]
    else:
        value_tick_labels = None

    header = None 
    with open(args.data_file) as input_file:
        for line in input_file:
            if header:
                line = line.split(',')
                x_value = float(line[x_axis])
                y_value = float(line[y_axis])
                if 'X' in line[value_index] or 'x' in line[value_index]:
                    #value = np.nan
                    value = 0
                    continue
                else:
                    value = float(line[value_index])

                if args.group:
                    group = line[int(args.group[0])].strip()
                    if group not in x_data:
                        x_data[group] = []
                        y_data[group] = []
                        value_data[group] = []
                    x_data[group].append(x_value)
                    y_data[group].append(y_value)
                    value_data[group].append(value)
                else:
                    x_data['default'].append(x_value)
                    y_data['default'].append(y_value)
                    value_data['default'].append(value)
            else:
                header = line.split(',')

    print("x:",header[x_axis])
    print("y:",header[y_axis].strip())
    print("value:",header[value_index].strip())
    print(x_data)
    print(y_data)
    print(value_data)

    markers = itertools.cycle(('o', 'v', 'P', '*', 'X', 'D', '<', '>', 'h', '^'))

    lines = []
    plt.figure(figsize=(6,8), dpi=100) # figsize sets the size to WxH where W and H are inches
    if args.ylog:
        plt.yscale('log')
    if args.xlog:
        plt.xscale('log')

    # Plot the data
    for group in sorted(x_data.keys()): 
        print(group)
        x = np.array(x_data[group])
        y = np.array(y_data[group])
        value = np.array(value_data[group])

        orig_cmap = matplotlib.cm.RdYlGn_r
        shifted_cmap = shiftedColorMap(orig_cmap, start=0.0, midpoint=0.5, name='my_shifted')
        line = plt.scatter(x,y,c=value, 
                cmap=orig_cmap,
                s=200, marker=next(markers), label=group, norm=matplotlib.colors.PowerNorm(gamma=float(args.gamma)))
        plt.clim(0,1)
        lines.append(line)

    cbar = plt.colorbar(lines[0],orientation='horizontal', norm=matplotlib.colors.PowerNorm(gamma=0.25), spacing='uniform', pad=0.2)
    cbar.ax.set_xlabel(args.value_title, rotation=0, labelpad=15)
    if value_tick_pos:
        cbar.set_ticks(value_tick_pos)
    if value_tick_labels:
        cbar.set_ticklabels(value_tick_labels)

    # Set visuals
    plt.xlabel(args.x_title)
    plt.ylabel(args.y_title)
    if args.y_tick_labels:
        plt.yticks(y_tick_pos, y_tick_labels)
    if args.x_tick_labels:
        plt.xticks(x_tick_pos, x_tick_labels)
    plt.gca().get_yaxis().set_minor_formatter(tick.NullFormatter())

    if args.legend:
        plt.legend(bbox_to_anchor=(1,0.5), loc='center left', frameon=True)

    plt.gca().set_facecolor('white')
    plt.gca().grid(True)
    plt.gca().set_axisbelow(True)

    # Display or save chart (NOTE: The default view of displaying the chart is different than how it is saved)
    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

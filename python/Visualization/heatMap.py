#! /usr/bin/env python
import argparse
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import matplotlib.cm as cm
#import seaborn as sns
import numpy as np
import math

from matplotlib import rc
rc('text', usetex=True)

plt.style.use('seaborn')

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
    parser.add_argument("x_label", help="What to use as label for x-axis")
    parser.add_argument("y_label", help="What to use as label for y-axis")
    parser.add_argument("value_label", help="Label of value")
    parser.add_argument("title", help="What to use as chart title")
    parser.add_argument("--xlog", help="Use log scale for x-axis", action='store_true')
    parser.add_argument("--ylog", help="Use log scale for y-axis", action='store_true')
    parser.add_argument("--save_fig", nargs=1, dest='fig_name', help="Use log scale for y-axis")
    parser.add_argument("--legend_pos", nargs=1, dest='legend_pos', help="Postion to place the legend")
    parser.add_argument("--group", nargs=1, dest='group', help="Which column to use to group the data")

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
                if 'X' in line[value_index]:
                    #value = np.nan
                    value = 0
                else:
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

    markers = itertools.cycle(('o', 'v', 'P', '*', 'X', 'D', '<', '>', 'h', '^'))

    lines = []
    # "scatterplot"
    for group in x_data: 
        print(group)
        x = np.array(x_data[group])
        y = np.array(y_data[group])
        value = np.array(value_data[group])

        orig_cmap = matplotlib.cm.viridis_r
        shifted_cmap = shiftedColorMap(orig_cmap, start=0.2, midpoint=0.2, name='my_shifted')
        line = plt.scatter(x,y, cmap='my_shifted', c=value, s=200, marker=next(markers), label=group)
        lines.append(line)

    cbar = plt.colorbar(orientation='horizontal')
    cbar.ax.set_xlabel(args.value_label, rotation=0, labelpad=15)
    #cbar.ax.set_xlim([0,1])
    plt.clim(0,1)


    #yticks = [int(t) for t in list(np.logspace(math.log(ymin,10), math.log(ymax,10), num=5))]
    plt.xlabel(args.x_label)
    plt.ylabel(args.y_label)
    #plt.yscale('log')
    #plt.yticks(yticks, yticks)
    #plt.yticks([5, 10, 20, 40, 80, 160], [5, 10, 20, 40, 80, 160])
    #plt.ylim(2.5)
    #plt.get_xaxis().set_major_formatter(tick.ScalarFormatter())
    #plt.get_xaxis().set_minor_formatter(tick.NullFormatter())

    legend_pos = 'best'
    if args.legend_pos:
        legend_pos = int(args.legend_pos[0])
        plt.legend(bbox_to_anchor=(1,0.5), loc='center left', frameon=True)

    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

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
                if 'X' in line[value_index]:
                    value = np.nan
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

                x_data.append(x_value)
                y_data.append(y_value)
                value_data.append(value)

                data.append((y_value, x_value, value))
            else:
                header = line.split(',')

    print("x:",header[x_axis])
    print("y:",header[y_axis].strip())
    print("value:",header[value_index].strip())

    # "scatterplot"
    x = np.array(x_data)
    y = np.array(y_data)
    value = np.array(value_data)

    orig_cmap = matplotlib.cm.viridis_r
    shifted_cmap = shiftedColorMap(orig_cmap, start=0.2, midpoint=0.25, name='my_shifted')
    plt.scatter(x,y, cmap='my_shifted', c=value, s=200)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel("Runtime ratio", rotation=270, labelpad=15)

    plt.xlabel(args.x_label)
    plt.ylabel(args.y_label)
    plt.yscale('log')
    plt.yticks([5, 10, 20, 40, 80, 160], [5, 10, 20, 40, 80, 160])


    # Seaborn
    """
    x = np.array(x_data)
    y = np.array(y_data)

    xu = np.unique(x)
    yu = np.unique(y)
    x = np.append(xu, [xu[-1]+np.diff(xu)[-1]]) - np.diff(xu)[-1]/2.
    y = np.append(yu, [yu[-1]+np.diff(yu)[-1]]) - np.diff(yu)[-1]/2.
    X,Y = np.meshgrid(x,y)

    z = np.array(value_data)
    Z = z.reshape(len(yu), len(xu))

    ary_data = np.array(data)

    x_labels = ['0', '1', '5', '10']
    y_labels = ['5', '10', '20', '40', '80', '160']
    ax = sns.heatmap(Z, robust=True, cmap='inferno_r', square=True, xticklabels=x_labels, yticklabels=y_labels)
    ax.invert_yaxis()
    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)
    cbar.ax.set_ylabel("Runtime ratio", rotation=270, labelpad=15)
    """

    # Old
    """
    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111)
    
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
    temp_labels = ['5', '10', '20', '40', '80', '160']
    print(len(y_ticks), len(temp_labels))
    for i in range(len(y_ticks)):
        if i > 0 and i < len(y_ticks) - 1:
            y_ticks[i] = temp_labels[i - 1]
    ax.set_yticklabels(y_ticks)

    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)

    cbar = plt.colorbar()
    cbar.ax.set_ylabel("Runtime ratio", rotation=270, labelpad=15)
    """

    if not args.fig_name:
        plt.tight_layout()
        plt.show()
    else:
        print(args.fig_name[0])
        plt.savefig(args.fig_name[0], bbox_inches='tight', dpi=1000, format='pdf')

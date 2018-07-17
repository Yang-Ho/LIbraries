#! /usr/bin/env python

import argparse
import itertools
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def parse_arguments():
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("data", help="The file containing data")
    parser.add_argument("x1_axis", help="The field to use as x-axis")
    parser.add_argument("x2_axis", help="The field to use as x-axis")
    parser.add_argument("x1_label", help="The field to use as x-axis")
    parser.add_argument("x2_label", help="The field to use as x-axis")
    parser.add_argument('y1_axis', help="The field(s) to use as y axis 1")
    parser.add_argument('y2_axis', help="The field(s) to use as y axis 2")
    parser.add_argument('y1_label', help="The field(s) to use as y axis 1")
    parser.add_argument('y2_label', help="The field(s) to use as y axis 2")
    parser.add_argument('--same_y', help="Whether to use the same scale for y", action='store_true')
    parser.add_argument('--same_x', help="Whether to use the same scale for x", action='store_true')
    parser.add_argument('--y1_box', help="y1 is supposed to be a box plot", action='store_true')
    parser.add_argument('--x1_multi', help="x1 is supposed to be multiseries", action='store_true')
    parser.add_argument('save_fig', help="Figure filename")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    x_field_1 = int(args.x1_axis)
    x_field_2 = int(args.x2_axis)
    y_field_1 = int(args.y1_axis)
    y_field_2 = int(args.y2_axis)
    x_label_1 = int(args.x1_label)
    x_label_2 = int(args.x2_label)
    y_label_1 = int(args.y1_label)
    y_label_2 = int(args.y2_label)
    y1 = []
    y2 = []
    x1 = []
    x2 = []
    header = None 
    with open(args.data) as input_file:
        for line in input_file:
            line = line.strip('\n')
            if not header:
                header = line.split(',')
                continue
            line = line.split(',')
            if '_' not in line[x_field_1]:
                x1.append(float(line[x_field_1]))
                y1.append(float(line[y_field_1]))
            elif '_' not in line[x_field_2]:
                x2.append(float(line[x_field_2]))
                y2.append(float(line[y_field_2]))

    marker = itertools.cycle(('o', '*', '^', '+'))
    color = itertools.cycle(('r', 'g', 'b', 'c', 'p'))
    print(x1, x2, y1, y2)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, label='1')
    ax2 = fig.add_subplot(111, label='2', frame_on=False)

    plot_params ={}
    plot_params['linestyle'] = 'None'
    if args.y1_box:
        data = {x:[] for x in x1}
        positions = [x for x in data]
        for i in range(len(x1)):
            data[x1[i]].append(y1[i])
        print('Boxplot data:', data)
        print('Postions:',positions)
        dataset = []
        for d in data:
            dataset.append(data[d])
        ax1.boxplot(dataset, positions=positions)
    else:
        ax1.plot(x1, y1, marker=next(marker), color="C0", label=header[x_field_1], **plot_params)
    ax1.set_xlabel(header[x_label_1])
    ax1.set_ylabel(header[y_label_1])

    ax2.plot(x2, y2, marker=next(marker), color="C0", label=header[x_field_2], **plot_params)

    if args.same_x:
        minx1 = min(x1)
        minx2 = min(x2)
        maxx1 = max(x1)
        maxx2 = max(x2)
        x_lims = [min(0, minx1, minx2), max(maxx1, maxx2)]
        ax1.set_xlim(x_lims)
        ax2.set_xlim(x_lims)
    else:
        ax2.set_xlabel(header[x_label_2])
        ax2.xaxis.tick_top()
        ax2.xaxis.set_label_position('top')

    if args.same_y:
        miny1 = min(y1)
        miny2 = min(y2)
        maxy1 = max(y1)
        maxy2 = max(y2)
        y_lims = [min(0, miny1, miny2), max(maxy1, maxy2)]
        ax1.set_ylim(y_lims)
        ax2.set_ylim(y_lims)
    else:
        ax2.set_ylabel(header[y_label_2])
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position('right')

    ax1.legend()
    ax2.legend()

    #plt.savefig(args.save_fig)
    plt.show()

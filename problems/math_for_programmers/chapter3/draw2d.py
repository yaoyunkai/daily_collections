"""


created at 2024/10/9
"""

from math import ceil, floor, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from colors import blue, black, red


class Polygon2D:
    def __init__(self, *vertices, color=blue, fill=None, alpha=0.4):
        self.vertices = vertices
        self.color = color
        self.fill = fill
        self.alpha = alpha


class Points2D:
    def __init__(self, *vectors, color=black):
        self.vectors = list(vectors)
        self.color = color


class Arrow2D:
    def __init__(self, tip, tail=(0, 0), color=red):
        self.tip = tip
        self.tail = tail
        self.color = color


class Segment2D:
    def __init__(self, start_point, end_point, color=blue):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color


def extract_vectors_2d(objects):
    for obj in objects:
        if isinstance(obj, Polygon2D):
            for v in obj.vertices:
                yield v
        elif isinstance(obj, Points2D):
            for v in obj.vectors:
                yield v
        elif isinstance(obj, Arrow2D):
            yield obj.tip
            yield obj.tail
        elif isinstance(obj, Segment2D):
            yield obj.start_point
            yield obj.end_point
        else:
            raise TypeError("Unrecognized object: {}".format(obj))


def draw2d(*objects, origin=True, axes=True,
           grid=(1, 1), nice_aspect_ratio=True,
           width=6, save_as=None):
    all_vectors = list(extract_vectors_2d(objects))
    xs, ys = zip(*all_vectors)

    max_x, max_y, min_x, min_y = max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)

    # sizing
    if grid:
        x_padding = max(ceil(0.05 * (max_x - min_x)), grid[0])
        y_padding = max(ceil(0.05 * (max_y - min_y)), grid[1])

        def round_up_to_multiple(val, size):
            return floor((val + size) / size) * size

        def round_down_to_multiple(val, size):
            return -floor((-val - size) / size) * size

        plt.xlim(floor((min_x - x_padding) / grid[0]) * grid[0],
                 ceil((max_x + x_padding) / grid[0]) * grid[0])
        plt.ylim(floor((min_y - y_padding) / grid[1]) * grid[1],
                 ceil((max_y + y_padding) / grid[1]) * grid[1])
    else:
        x_padding = 0.05 * (max_x - min_x)
        y_padding = 0.05 * (max_y - min_y)

        plt.xlim(min_x - x_padding, max_x + x_padding)
        plt.ylim(min_y - y_padding, max_y + y_padding)

    if origin:
        plt.scatter([0], [0], color='k', marker='x')

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2, color='k')
        plt.gca().axvline(linewidth=2, color='k')

    for obj in objects:
        if type(obj) == Polygon2D:
            if obj.color:
                for i in range(0, len(obj.vertices)):
                    x1, y1 = obj.vertices[i]
                    x2, y2 = obj.vertices[(i + 1) % len(obj.vertices)]
                    plt.plot([x1, x2], [y1, y2], color=obj.color)
            if obj.fill:
                patches = []
                poly = Polygon(obj.vertices, closed=True)
                patches.append(poly)
                p = PatchCollection(patches, color=obj.fill)
                plt.gca().add_collection(p)
        elif type(obj) == Points2D:
            xs = [v[0] for v in obj.vectors]
            ys = [v[1] for v in obj.vectors]
            plt.scatter(xs, ys, color=obj.color)
        elif type(obj) == Arrow2D:
            tip, tail = obj.tip, obj.tail
            tip_length = (plt.xlim()[1] - plt.xlim()[0]) / 20.
            length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(tail[0], tail[1], new_x, new_y,
                            head_width=tip_length / 1.5, head_length=tip_length,
                            fc=obj.color, ec=obj.color)
        elif type(obj) == Segment2D:
            x1, y1 = obj.start_point
            x2, y2 = obj.end_point
            plt.plot([x1, x2], [y1, y2], color=obj.color)
        else:
            raise TypeError("Unrecognized object: {}".format(obj))

    fig = plt.gcf()

    if nice_aspect_ratio:
        coords_height = (plt.ylim()[1] - plt.ylim()[0])
        coords_width = (plt.xlim()[1] - plt.xlim()[0])
        fig.set_size_inches(width, width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()

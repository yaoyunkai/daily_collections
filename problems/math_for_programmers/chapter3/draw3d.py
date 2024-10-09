"""


created at 2024/10/9
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from colors import *


class FancyArrow3D(FancyArrowPatch):
    """
    https://github.com/matplotlib/matplotlib/issues/21688


    """
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    # def draw(self, renderer):
    #     xs3d, ys3d, zs3d = self._verts3d
    #     xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
    #     self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
    #     super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)


class Polygon3D:
    def __init__(self, *vertices, color=blue):
        self.vertices = vertices
        self.color = color


class Points3D:
    def __init__(self, *vectors, color=black):
        self.vectors = list(vectors)
        self.color = color


class Arrow3D:
    def __init__(self, tip, tail=(0, 0, 0), color=red):
        self.tip = tip
        self.tail = tail
        self.color = color


class Segment3D:
    def __init__(self, start_point, end_point, color=blue, linestyle='solid'):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.linestyle = linestyle


class Box3D:
    def __init__(self, *vector):
        self.vector = vector


def extract_vectors_3d(objects):
    for obj in objects:
        if type(obj) == Polygon3D:
            for v in obj.vertices:
                yield v
        elif type(obj) == Points3D:
            for v in obj.vectors:
                yield v
        elif type(obj) == Arrow3D:
            yield obj.tip
            yield obj.tail
        elif type(obj) == Segment3D:
            yield obj.start_point
            yield obj.end_point
        elif type(obj) == Box3D:
            yield obj.vector
        else:
            raise TypeError("Unrecognized object: {}".format(obj))


def draw3d(*objects, origin=True, axes=True, width=6, save_as=None,
           azim=None, elev=None,
           xlim=None, ylim=None, zlim=None,
           xticks=None, yticks=None, zticks=None,
           depthshade=False):
    fig = plt.gcf()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=elev, azim=azim)

    all_vectors = list(extract_vectors_3d(objects))
    if origin:
        all_vectors.append((0, 0, 0))
    xs, ys, zs = zip(*all_vectors)

    max_x, min_x = max(0, *xs), min(0, *xs)
    max_y, min_y = max(0, *ys), min(0, *ys)
    max_z, min_z = max(0, *zs), min(0, *zs)

    x_size = max_x - min_x
    y_size = max_y - min_y
    z_size = max_z - min_z

    padding_x = 0.05 * x_size if x_size else 1
    padding_y = 0.05 * y_size if y_size else 1
    padding_z = 0.05 * z_size if z_size else 1

    plot_x_range = (min(min_x - padding_x, -2), max(max_x + padding_x, 2))
    plot_y_range = (min(min_y - padding_y, -2), max(max_y + padding_y, 2))
    plot_z_range = (min(min_z - padding_z, -2), max(max_z + padding_z, 2))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    def draw_segment(start, end, color=black, linestyle='solid'):
        _xs, _ys, _zs = [[start[ii], end[ii]] for ii in range(0, 3)]
        ax.plot(_xs, _ys, _zs, color=color, linestyle=linestyle)

    if axes:
        draw_segment((plot_x_range[0], 0, 0), (plot_x_range[1], 0, 0))
        draw_segment((0, plot_y_range[0], 0), (0, plot_y_range[1], 0))
        draw_segment((0, 0, plot_z_range[0]), (0, 0, plot_z_range[1]))

    if origin:
        ax.scatter([0], [0], [0], color='k', marker='x')

    for obj in objects:
        if type(obj) == Points3D:
            xs, ys, zs = zip(*obj.vectors)
            ax.scatter(xs, ys, zs, color=obj.color, depthshade=depthshade)

        elif type(obj) == Polygon3D:
            for i in range(0, len(obj.vertices)):
                draw_segment(
                    obj.vertices[i],
                    obj.vertices[(i + 1) % len(obj.vertices)],
                    color=obj.color)

        elif type(obj) == Arrow3D:
            xs, ys, zs = zip(obj.tail, obj.tip)
            a = FancyArrow3D(xs, ys, zs, mutation_scale=20, arrowstyle='-|>', color=obj.color)
            ax.add_artist(a)

        elif type(obj) == Segment3D:
            draw_segment(obj.start_point, obj.end_point, color=obj.color, linestyle=obj.linestyle)

        elif type(obj) == Box3D:
            x, y, z = obj.vector
            kwargs = {'linestyle': 'dashed', 'color': 'gray'}
            draw_segment((0, y, 0), (x, y, 0), **kwargs)
            draw_segment((0, 0, z), (0, y, z), **kwargs)
            draw_segment((0, 0, z), (x, 0, z), **kwargs)
            draw_segment((0, y, 0), (0, y, z), **kwargs)
            draw_segment((x, 0, 0), (x, y, 0), **kwargs)
            draw_segment((x, 0, 0), (x, 0, z), **kwargs)
            draw_segment((0, y, z), (x, y, z), **kwargs)
            draw_segment((x, 0, z), (x, y, z), **kwargs)
            draw_segment((x, y, 0), (x, y, z), **kwargs)
        else:
            raise TypeError("Unrecognized object: {}".format(obj))

    if xlim and ylim and zlim:
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        ax.set_zlim(*zlim)
    if xticks and yticks and zticks:
        plt.xticks(xticks)
        plt.yticks(yticks)
        ax.set_zticks(zticks)

    if save_as:
        plt.savefig(save_as)

    plt.show()

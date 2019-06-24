from random import uniform

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.widgets import AxesWidget, RadioButtons


class MyRadioButtons(RadioButtons):
    # https://stackoverflow.com/questions/55095111/displaying-radio-buttons-horizontally-in-matplotlib
    def __init__(self, ax, labels, active=0, activecolor='blue', size=49,
                 orientation="vertical", **kwargs):
        """
        Add radio buttons to an `~.axes.Axes`.
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The axes to add the buttons to.
        labels : list of str
            The button labels.
        active : int
            The index of the initially selected button.
        activecolor : color
            The color of the selected button.
        size : float
            Size of the radio buttons
        orientation : str
            The orientation of the buttons: 'vertical' (default), or 'horizontal'.
        Further parameters are passed on to `Legend`.
        """
        AxesWidget.__init__(self, ax)
        self.activecolor = activecolor
        axcolor = ax.get_facecolor()
        self.value_selected = None

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        circles = []
        for i, label in enumerate(labels):
            if i == active:
                self.value_selected = label
                facecolor = activecolor
            else:
                facecolor = axcolor
            p = ax.scatter([], [], s=size, marker="o", edgecolor='black',
                           facecolor=facecolor)
            circles.append(p)
        if orientation == "horizontal":
            kwargs.update(ncol=len(labels), mode="expand")
        kwargs.setdefault("frameon", False)
        self.box = ax.legend(circles, labels, loc="center", **kwargs)
        self.labels = self.box.texts
        self.circles = self.box.legendHandles
        for c in self.circles:
            c.set_picker(5)
        self.cnt = 0
        self.observers = {}

        self.connect_event('pick_event', self._clicked)

    def _clicked(self, event):
        if (self.ignore(event) or event.mouseevent.button != 1 or
                event.mouseevent.inaxes != self.ax):
            return
        if event.artist in self.circles:
            self.set_active(self.circles.index(event.artist))


def up_down(rect: Rectangle, to: tuple, step=.1, interval=.001):
    new_step = step
    if to[1] < rect.get_y():
        new_step *= -1

    figure = rect.figure

    up = rect.get_y() < to[1]

    while (rect.get_y() - to[1] <= step / 2) if up else (rect.get_y() - to[1] >= step / 2):
        rect.set_y(rect.get_y() + new_step)
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.pause(interval)


def diagonal(rect: Rectangle, to: tuple, step=.1, interval=.001):
    end = to[0]

    if to[0] < rect.get_x():
        step *= -1
        end += step
    else:
        end += step

    x_range = np.arange(rect.get_x(), end, step)

    slope = (to[1] - rect.get_y()) / (to[0] - rect.get_x())

    start_y = rect.get_y()
    start_x = rect.get_x()

    figure = rect.figure

    for x in x_range:
        rect.set_xy((x, slope * (x - start_x) + start_y))
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.pause(interval)


def right_left(rect: Rectangle, to: tuple, step=.1, interval=.001):
    new_step = step
    if to[0] < rect.get_x():
        new_step *= -1

    figure = rect.figure

    right = rect.get_x() < to[0]

    while (rect.get_x() - to[0] <= step / 2) if right else (rect.get_x() - to[0] >= step / 2):
        rect.set_x(rect.get_x() + new_step)

        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.pause(interval)


def move_to(rect: Rectangle, to: tuple, step=.1, interval=.001, show_animation=True):
    if show_animation:
        if abs(rect.get_x() - to[0]) < .001:
            if not abs(rect.get_y() - to[1]) < .001:
                up_down(rect, to, step, interval)
            else:
                return
        elif abs(rect.get_y() - to[1]) < .001:
            right_left(rect, to, step, interval)
        else:
            diagonal(rect, to, step, interval)

    figure = rect.figure
    rect.set_xy(to)
    figure.canvas.draw()
    figure.canvas.flush_events()
    plt.pause(interval)


if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    plt.ion()
    plt.show()

    # Graphics info
    random_number = 10
    spacing = .5
    print(random_number)

    # Ingot info
    min_width = 6
    max_width = 24

    min_height = 1
    max_height = 8
    #
    # Shelve info
    number_of_shelves = 4
    shelve_height = max_height
    shelve_width = 36.5

    patches = []
    shelves = []

    current_x = 0
    current_y = -max_height - spacing

    print(spacing)
    for i in range(random_number):
        w = uniform(min_width, max_width)
        h = uniform(min_height, max_height)

        rect = Rectangle((current_x, current_y), w, h)
        patches.append(rect)

        current_x += (w + spacing)

    ax.add_collection(PatchCollection(patches))

    current_y = 0
    for i in range(number_of_shelves):
        ax.plot([0, shelve_width], [current_y, current_y], c='r')
        current_y += shelve_height
        shelves.append((shelve_width, []))

    ax.plot([0, 0], [0, current_y], c='r')
    ax.plot([shelve_width, shelve_width], [0, current_y], c='r')

    ax.autoscale_view(True, True, True)
    plt.show(block=True)

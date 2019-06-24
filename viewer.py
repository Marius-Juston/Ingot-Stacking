import ctypes  # An included library with Python install.
import random
from copy import copy
from random import randint, uniform

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button, TextBox, CheckButtons

from helper import MyRadioButtons, move_to
from stacking_algorithm import SimpleStacking, AllKnowing, Stacker


class Viewer:
    valid_stacking_algorithms = {
        "Simple Stacking Algorithm": SimpleStacking,
        "All Knowing Algorithm": AllKnowing
    }

    def __init__(self, ax, width: tuple = (6, 24), height: tuple = (1, 8), number_of_shelves: int = 4,
                 shelve_spec: tuple = (36.5, 8), number_of_ingot: int = 10, air_gap_width: float = 1,
                 random_seed: int = 42,
                 stacking_algorithm: str = "Simple Stacking Algorithm", show_animation: bool = False) -> None:
        super().__init__()

        self.show_animation = show_animation
        if stacking_algorithm not in Viewer.valid_stacking_algorithms:
            raise ValueError("Please enter one of the valid stacking algorithms: {}".format(
                ", ".join(Viewer.valid_stacking_algorithms)))

        self.stacking_algorithm = stacking_algorithm
        self.height = height
        self.width = width
        random.seed(random_seed)

        self.air_gap_width = air_gap_width
        self.number_of_ingot = number_of_ingot
        self.shelve_spec = shelve_spec
        self.number_of_shelves = number_of_shelves
        self.ax = ax

        if isinstance(number_of_ingot, tuple):
            a, b = number_of_ingot
            self.number_of_ingot = randint(a, b)

        self.spacing = .5

        self.ingots = []
        self.ingot_cache = []
        self.shelves = []
        self.setting_widgets = []

        self.setup_environment()
        self.setup_settings()

        self.ax.set_aspect('equal', adjustable='box')
        self.ax.autoscale_view(True, True, True)

    def setup_environment(self):
        self.init_ingots()
        self.init_shelves()

    def init_ingots(self):
        self.ingots.clear()
        self.ingot_cache.clear()

        x = 0
        y = -self.height[1] - self.spacing

        for i in range(self.number_of_ingot):
            w = uniform(*self.width)
            h = uniform(*self.height)

            rect = Rectangle((x, y), w, h)
            self.ingots.append(rect)
            self.ax.add_patch(rect)

            rect = copy(rect)
            self.ingot_cache.append(rect)

            x += (w + self.spacing)

        # FIXME check if it is better to add the ingots individually or all in the same time?
        # self.ax.add_collection(PatchCollection(self.ingots))

    def init_shelves(self):
        self.shelves.clear()

        y = 0

        w, h = self.shelve_spec

        for i in range(self.number_of_shelves):
            self.ax.plot([0, w], [y, y], c='r')
            self.shelves.append([w, self.air_gap_width, y, []])
            y += h

        self.ax.plot([0, 0], [0, y], c='r')
        self.ax.plot([w, w], [0, y], c='r')

    def apply(self, _):
        self.ax.clear()

        self.ingots.clear()

        for rect in self.ingot_cache:
            rect = copy(rect)

            self.ingots.append(rect)
            self.ax.add_patch(rect)

        self.init_shelves()

        self.ax.autoscale_view(True, True, True)

        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()

    def randomize(self, _):
        self.ax.clear()

        self.setup_environment()

        self.ax.autoscale_view(True, True, True)

        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()

    def create_text_box(self, ax: Axes, label: str, get_var, set_var, data_type=float):
        var = str(get_var())

        textbox = TextBox(ax, label, initial=var)

        def update_min_width(text: str):
            try:
                min_width = data_type(text)
                set_var(min_width)
            except ValueError:
                textbox.set_val(var)

        textbox.on_submit(update_min_width)

        self.setting_widgets.append(textbox)

    def set_min_width(self, new_value):
        self.width = (new_value, self.width[1])

    def set_max_width(self, new_value):
        self.width = (self.width[0], new_value)

    def set_min_height(self, new_value):
        self.height = (new_value, self.height[1])

    def set_max_height(self, new_value):
        self.height = (self.height[0], new_value)

    def set_number_of_shelves(self, new_value):
        self.number_of_shelves = new_value

    def set_shelve_width(self, new_value):
        self.shelve_spec = (new_value, self.shelve_spec[1])

    def set_shelve_height(self, new_value):
        self.shelve_spec = (self.shelve_spec[0], new_value)

    def set_number_of_ingots(self, new_value):
        self.number_of_ingot = new_value

    def set_air_gap_width(self, new_value):
        self.air_gap_width = new_value

    def set_stacking_algorithm(self, new_value):
        self.stacking_algorithm = new_value

    def set_show_animation(self, new_value: str):
        self.show_animation = not self.show_animation

    def setup_settings(self):
        setting_fig = plt.figure("Settings")
        grid = GridSpec(12, 3, setting_fig)

        textbox_ax = plt.subplot(grid[0, 1:])
        self.create_text_box(textbox_ax, "Min Ingot Width", lambda: self.width[0], self.set_min_width)

        textbox_ax = plt.subplot(grid[1, 1:])
        self.create_text_box(textbox_ax, "Max Ingot Width", lambda: self.width[1], self.set_max_width)

        textbox_ax = plt.subplot(grid[2, 1:])
        self.create_text_box(textbox_ax, "Min Ingot Height", lambda: self.height[0], self.set_min_height)

        textbox_ax = plt.subplot(grid[3, 1:])
        self.create_text_box(textbox_ax, "Max Ingot Height", lambda: self.height[1], self.set_max_height)

        textbox_ax = plt.subplot(grid[4, 1:])
        self.create_text_box(textbox_ax, "Number of shelves", lambda: self.number_of_shelves,
                             self.set_number_of_shelves, data_type=int)

        textbox_ax = plt.subplot(grid[5, 1:])
        self.create_text_box(textbox_ax, "Shelve width", lambda: self.shelve_spec[0], self.set_shelve_width)

        textbox_ax = plt.subplot(grid[6, 1:])
        self.create_text_box(textbox_ax, "Shelve height", lambda: self.shelve_spec[1], self.set_shelve_height)

        textbox_ax = plt.subplot(grid[7, 1:])
        self.create_text_box(textbox_ax, "Number of ingots", lambda: self.number_of_ingot, self.set_number_of_ingots,
                             data_type=int)

        textbox_ax = plt.subplot(grid[8, 1:])
        self.create_text_box(textbox_ax, "Air Gap Width", lambda: self.air_gap_width, self.set_air_gap_width)

        valid_algorithms = list(Viewer.valid_stacking_algorithms.keys())
        stacking_algorithm_ax = plt.subplot(grid[9, :])
        radio_buttons = MyRadioButtons(stacking_algorithm_ax, valid_algorithms,
                                       orientation="horizontal")
        index = valid_algorithms.index(self.stacking_algorithm)
        radio_buttons.set_active(index)
        radio_buttons.on_clicked(self.set_stacking_algorithm)
        self.setting_widgets.append(radio_buttons)

        # TODO fix checkbox scaling
        show_animation_ax = plt.subplot(grid[10, 1])
        check = CheckButtons(show_animation_ax, ['Show Animation'], [self.show_animation])
        check.on_clicked(self.set_show_animation)
        self.setting_widgets.append(check)

        random_ax = plt.subplot(grid[-1, 0])
        random_button = Button(random_ax, "Randomize")
        random_button.on_clicked(self.randomize)
        self.setting_widgets.append(random_button)

        apply_ax = plt.subplot(grid[-1, 1])
        apply_button = Button(apply_ax, "Apply/Reset")
        apply_button.on_clicked(self.apply)
        self.setting_widgets.append(apply_button)

        run_ax = plt.subplot(grid[-1, 2])
        run_button = Button(run_ax, "Run")
        run_button.on_clicked(self.run)
        self.setting_widgets.append(run_button)

        grid.tight_layout(setting_fig, h_pad=.1)

    def get_stacking_algorithm(self) -> Stacker:
        return self.valid_stacking_algorithms[self.stacking_algorithm](self.shelves, self.air_gap_width)

    def run(self, event):
        algorithm = self.get_stacking_algorithm()
        algorithm.setup(self.ingots)

        print(len(self.ingots))

        for ingot in self.ingots:
            to_position = algorithm.place(ingot)

            if to_position is None:
                break

            move_to(ingot, to_position, step=1, show_animation=self.show_animation)

        ctypes.windll.user32.MessageBoxW(0, "Finished!!", "Finish Message", 0)


if __name__ == '__main__':
    plt.ion()
    plt.show()

    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    fig.canvas.set_window_title("Display")

    viewer = Viewer(ax,
                    show_animation=False
                    )

    plt.ioff()
    plt.show(block=True)

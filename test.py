import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from helper import move_to

if __name__ == '__main__':

    fig, ax = plt.subplots()
    ax.set_xbound(-10, 20)
    ax.set_ybound(-10, 20)
    plt.ion()
    plt.show()
    #
    rect = Rectangle((-10, -10), 10, 10)
    ax.add_patch(rect)

    move_to(rect, (10, 10))
    move_to(rect, (0, 0))
    move_to(rect, (10, 0))
    move_to(rect, (-10, 0))
    move_to(rect, (-10, -10))
    move_to(rect, (-10, 0))
    # Axes().set_x
    plt.ioff()
    plt.show(block=True)

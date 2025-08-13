from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
    implot,
    imgui_fig
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py
from numpy import array, linspace


import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for matplotlib to avoid GUI issues
import matplotlib.pyplot as plt

import time



class line_plot(Node):
    def __init__(self, node_id, name="Line Plot"):
        super().__init__(node_id, name)


        self.input_x = self.add_pin(ID.next_id(), ed.PinKind.input, "X Data[]", left=True, value_type=list)
        self.input_x.set_value([0,0], False)
        self.input_y = self.add_pin(ID.next_id(), ed.PinKind.input, "Y Data[]", left=True, value_type=list)
        self.input_y.set_value([0,0], False)
        
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots()
        gray = 0.22
        self.fig.set_facecolor((gray, gray, gray, 1.0))  # Set the background color to dark
        self.ax.set_facecolor((gray, gray, gray, 1.0))  # Set the axes background color to dark

        self.plot_fps = 10

        self.max_length = 1000  # Maximum number of points to display

        self.last_plot_time = time.time()  # Time of the last plot update



    def normalize_lengths(self, x, y):
        """Ensure x and y are of the same length by truncating the longer one."""
        min_length = min(len(x), len(y))
        return x[:min_length], y[:min_length]
    
    def draw_content(self):
        
        self.ax.clear()
        # Normalize lengths
        x, y = self.normalize_lengths(self.input_x.get_value(), self.input_y.get_value())
        self.ax.plot(x[-self.max_length:], y[-self.max_length:])
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_title("Line Plot")

        refresh = False
        if self.input_x.get_changed_this_frame() or self.input_y.get_changed_this_frame():
            refresh = True
            self.last_plot_time = time.time()
        if time.time() - self.last_plot_time > 1 / self.plot_fps:
            refresh = True
            self.last_plot_time = time.time()
        imgui_fig.fig(f"Line Plot##{self.node_id}", self.fig, refresh_image=refresh)


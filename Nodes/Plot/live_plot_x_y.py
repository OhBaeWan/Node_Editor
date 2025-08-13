from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
    implot,
    immvision,
    imgui_fig
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py
from numpy import array, linspace
import time
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for matplotlib to avoid GUI issues
import matplotlib.pyplot as plt



class live_plot_x_y(Node):
    def __init__(self, node_id, name="Live Plot X Y"):
        super().__init__(node_id, name)
        
        self.x = self.add_pin(ID.next_id(), ed.PinKind.input, "x", left=True, value_type=None)
        self.x.set_value(0, False)

        self.y = self.add_pin(ID.next_id(), ed.PinKind.input, "y", left=True, value_type=None)
        self.y.set_value(0, False)

        self.x_data = self.add_pin(ID.next_id(), ed.PinKind.output, "X data[]", left=False, value_type=list)
        self.y_data = self.add_pin(ID.next_id(), ed.PinKind.output, "Y data[]", left=False, value_type=list)

        self.x_data.set_value([0, 0], False)
        self.y_data.set_value([0, 0], False)

        self.reset = self.add_pin(ID.next_id(), ed.PinKind.input, "Reset", left=True, value_type=None)
        self.reset.set_value(0, False)

        self.times = []
        self.start_time = time.time()

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots()
        gray = 0.22
        self.fig.set_facecolor((gray, gray, gray, 1.0))  # Set the background color to dark
        self.ax.set_facecolor((gray, gray, gray, 1.0))  # Set the axes background color to dark

        self.max_length = 999999999  # Maximum number of points to display

        self.plot_fps = 5

        self.last_plot_time = time.time()  # Time of the last plot update

    def draw_content(self):

        
        # reset data if reset pin is triggered
        if self.reset.get_changed_this_frame():
           self.x_data.set_value([0, 0], True)
           self.y_data.set_value([0, 0], True)
           self.times = []
           self.start_time = time.time()
           refresh = True
        # plot the data
        
        plt.switch_backend('Agg')
        self.ax.clear()
        self.ax.plot(self.x_data.get_value()[-self.max_length:], self.y_data.get_value()[-self.max_length:])
        self.ax.set_xlabel(f"{self.x.name}")
        self.ax.set_ylabel(f"{self.y.name}")
        self.ax.set_title("Live Plot")


        refresh = False
        if self.x.get_changed_this_frame() or self.reset.get_changed_this_frame():
            # add new data if input pin is connected
            if len(self.x.links) > 0 and len(self.y.links) > 0:
                # get the current time and append the input value to the data list
                current_time = time.time() - self.start_time
                self.x_data.set_value(self.x_data.get_value().append(self.x.get_value()), True)
                self.y_data.set_value(self.y_data.get_value().append(self.y.get_value()), True)
                self.times.append(current_time)
            refresh = True
            self.last_plot_time = time.time()
        
        if time.time() - self.last_plot_time > 1 / self.plot_fps:
            refresh = True
            self.last_plot_time = time.time()
        imgui_fig.fig(f"Live Plot##{self.node_id}", self.fig, refresh_image=refresh)



        # add a button to reset the plot
        if imgui.button("Reset Plot"):
            self.x_data.set_value([0, 0], True)
            self.y_data.set_value([0, 0], True)
            self.times = []
            self.start_time = time.time()
            refresh = True

        

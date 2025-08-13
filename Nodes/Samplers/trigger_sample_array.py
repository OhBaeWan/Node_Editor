from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

import time

class trigger_sample_array(Node):
    def __init__(self, node_id, name="Trigger Sample Array"):
        super().__init__(node_id, name)
        self.input= self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=None)
        self.trigger= self.add_pin(ID.next_id(), ed.PinKind.input, "Trigger", left=True, value_type=None)
        self.reset = self.add_pin(ID.next_id(), ed.PinKind.input, "Reset", left=True, value_type=None)
        self.output_x_count = self.add_pin(ID.next_id(), ed.PinKind.output, "X Count", left=False, value_type=list)
        self.output_x_count.set_value([], False)
        self.output_x_time = self.add_pin(ID.next_id(), ed.PinKind.output, "X Time", left=False, value_type=list)
        self.output_x_time.set_value([], False)
        self.output_y = self.add_pin(ID.next_id(), ed.PinKind.output, "Y", left=False, value_type=list)
        self.output_y.set_value([], False)

        self.start_time = time.time()  # Record the start time for the x-axis

    def draw_content(self):
        # Check if the reset pin has changed
        if self.reset.get_changed_this_frame():
            # Reset the output lists
            self.output_x_count.set_value([], increment_change_counter=True)
            self.output_x_time.set_value([], increment_change_counter=True)
            self.output_y.set_value([], increment_change_counter=True)
            self.start_time = time.time()
            return
        # Check if the trigger pin has changed
        if self.trigger.get_changed_this_frame():
            # Get the current value from the input pin
            input_value = self.input.get_value()

            # Append the input value to the output lists
            current_x_count = self.output_x_count.get_value()
            current_x_time = self.output_x_time.get_value()
            current_y = self.output_y.get_value()
            current_y.append(input_value)
            current_x_count.append(current_x_count[-1] + 1 if current_x_count else 0)  # Increment x value
            current_x_time.append(time.time() - self.start_time)

            self.output_x_count.set_value(current_x_count, increment_change_counter=True)
            self.output_x_time.set_value(current_x_time, increment_change_counter=True)
            self.output_y.set_value(current_y, increment_change_counter=True)

        if imgui.button(f"Reset##{self.node_id}"):
            # Reset the output lists when the button is pressed
            self.output_x_count.set_value([], increment_change_counter=True)
            self.output_x_time.set_value([], increment_change_counter=True)
            self.output_y.set_value([], increment_change_counter=True)
            self.start_time = time.time()
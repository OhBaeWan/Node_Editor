from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

import time

class ClockCounter(Node):
    def __init__(self, node_id, name="Clock Counter"):
        super().__init__(node_id, name)
        self.freq_pin = self.add_pin(ID.next_id(), ed.PinKind.input, "Frequency", left=True, value_type=float)
        self.freq_pin.set_value(1.0, False)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=int)
        self.output.set_value(0, False)

        self.last_time = time.time()  # Record the start time for the clock
    
    def draw_content(self):
        imgui.set_next_item_width(100)  # Adjust width to fit the window
        changed, freq = imgui.input_float(f"Frequency (Hz)##{self.node_id}", self.freq_pin.get_value(), step=0.1, step_fast=1.0)
        if changed:
            self.freq_pin.set_value(freq, increment_change_counter=True)
        # increment the output value for every tick of the clock
        current_time = time.time()
        if current_time - self.last_time >= 1.0 / self.freq_pin.get_value():
            current_value = self.output.get_value()
            new_value = current_value + 1
            self.output.set_value(new_value, increment_change_counter=True)
            self.last_time = current_time


        
from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

import time

class trigger_sample(Node):
    def __init__(self, node_id, name="Trigger Sample"):
        super().__init__(node_id, name)
        self.input= self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=None)
        self.trigger= self.add_pin(ID.next_id(), ed.PinKind.input, "Trigger", left=True, value_type=None)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=None)
        self.output.set_value(0, False)


        self.start_time = time.time()  # Record the start time for the x-axis

    def draw_content(self):

        # Check if the trigger pin has changed
        if self.trigger.get_changed_this_frame():
            # Get the current value from the input pin
            input_value = self.input.get_value()

            self.output.set_value(input_value, increment_change_counter=True)

        # display the output value
        imgui.text(f"Output: {self.output.get_value()}")
from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class to_float(Node):
    def __init__(self, node_id, name="to Float"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=None)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=float)
        self.output.set_value(0.0, False)

    def draw_content(self):
        if self.input.get_changed_this_frame():
            input_value = self.input.get_value()
            try:
                float_value = float(input_value)
                self.output.set_value(float_value, increment_change_counter=True)
            except ValueError:
                imgui.text("Invalid input: Cannot convert to float")
        imgui.text(f"Input: {self.input.get_value()}")
        imgui.text(f"Output: {self.output.get_value()}")
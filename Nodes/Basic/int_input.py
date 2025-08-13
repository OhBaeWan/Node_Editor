from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class int_input(Node):
    def __init__(self, node_id, name="Integer Input"):
        super().__init__(node_id, name)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=int)
        self.output.set_value(0, False)

    def draw_content(self):
        imgui.set_next_item_width(100)  # Adjust width to fit the window
        changed, value = imgui.input_int(f"Input##{self.node_id}", int(self.output.get_value()), step=1, step_fast=10)
        if changed:
            self.output.set_value(value, increment_change_counter=True)

        
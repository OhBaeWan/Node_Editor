from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class to_str(Node):
    def __init__(self, node_id, name="to String"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=None)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=str)
        self.output.set_value("", False)

    def draw_content(self):
        if self.input.get_changed_this_frame():
            input_value = self.input.get_value()
            self.output.set_value(str(input_value), increment_change_counter=True)
        imgui.text(f"Input: {self.input.get_value()}")
        imgui.text(f"Output: {self.output.get_value()}")
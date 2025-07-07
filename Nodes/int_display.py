from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class int_display(Node):
    def __init__(self, node_id, name="Integer Display"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=int)
        self.input.set_value(0, False)

    def draw_content(self):
        imgui.text(f"Displaying Integer: {self.input.get_value()}")
        imgui.text(f"Change Counter: {self.input.get_change_counter()}")


        
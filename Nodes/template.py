from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class template(Node):
    def __init__(self, node_id, name="Template"):
        super().__init__(node_id, name)
        self.input_template = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=False, value_type=int)
        self.output_template = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=int)

    
    def draw_content(self):
        pass

        
from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class button_counter(Node):
    def __init__(self, node_id, name="Button Counter"):
        super().__init__(node_id, name)
        self.output_count = self.add_pin(ID.next_id(), ed.PinKind.output, "Count", left=False, value_type=int)
        self.output_count.set_value(0, False)

    
    def draw_content(self):
        if imgui.button("Increment"):
            current_value = self.output_count.get_value()
            new_value = current_value + 1
            self.output_count.set_value(new_value, increment_change_counter=True)

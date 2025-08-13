from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class CounterNode(Node):
    def __init__(self, node_id, name="Counter Node"):
        super().__init__(node_id, name)
        self.trigger = self.add_pin(ID.next_id(), ed.PinKind.input, "Trigger", left=True, value_type=None)
        self.trigger.set_value(0, False)  # Initialize trigger value
        self.reset = self.add_pin(ID.next_id(), ed.PinKind.input, "Reset", left=True, value_type=None)
        self.reset.set_value(0, False)  # Initialize reset value
        self.count = self.add_pin(ID.next_id(), ed.PinKind.output, "Count", left=False, value_type=int)
        self.count.set_value(0, False)
        self.counter = 0



    def draw_content(self):
        
        if self.trigger.get_changed_this_frame():
            self.counter += 1
            self.count.set_value(self.counter)

        if self.reset.get_changed_this_frame():
            self.counter = 0
            self.count.set_value(self.counter)

        imgui.text(f"Counter: {self.counter}")

        if imgui.button(f"Increment##{self.node_id}"):
            self.counter += 1
            self.count.set_value(self.counter)

        if imgui.button(f"Reset##{self.node_id}"):
            self.counter = 0
            self.count.set_value(self.counter)

        
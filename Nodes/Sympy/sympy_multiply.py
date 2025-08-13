from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py
import sympy
import sympy.core
import time
from sympy import init_printing

class Sympy_Multiply(Node):
    def __init__(self, node_id, name="Sympy Multiply"):
        super().__init__(node_id, name)
        self.input1 = self.add_pin(ID.next_id(), ed.PinKind.input, "Input 1", left=True, value_type=sympy.core.Basic)
        self.input2 = self.add_pin(ID.next_id(), ed.PinKind.input, "Input 2", left=True, value_type=sympy.core.Basic)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=sympy.core.Basic)

    def draw_content(self):
        imgui.text(f"Displaying Expression: {self.input1.get_value()} * {self.input2.get_value()}")
        # evaluate the expression
        if self.input1.get_value() is not None and self.input2.get_value() is not None:
            result = self.input1.get_value() * self.input2.get_value()
            self.output.set_value(result, increment_change_counter=True)
            imgui.text(f"Result: {result}")

        imgui.text(f"Change Counter: {self.input1.get_change_counter()}")


        
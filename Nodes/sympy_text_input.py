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

class Sympy_Text_Input(Node):
    def __init__(self, node_id, name="Sympy Text Input"):
        super().__init__(node_id, name)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Output", left=False, value_type=sympy.core.Basic)
        self.output.set_value(sympy.sympify("0"), False)
    def draw_content(self):
        imgui.set_next_item_width(imgui.calc_text_size(f"{self.output.get_value()}").x + 50)  # Adjust width to fit the window
        changed, value = imgui.input_text(f"Input##{self.node_id}", str(self.output.get_value()), flags=imgui.InputTextFlags_.enter_returns_true)
        if changed:
            try:
                value = sympy.sympify(value)
            except Exception as e:
                print(f"Error parsing expression: {e}")
                #imgui.text_colored(imgui.get_color_u32((1.0, 0.0, 0.0, 1.0)), "Invalid expression. Please enter a valid SymPy expression.")
                return
            self.output.set_value(sympy.sympify(value), increment_change_counter=True)
        imgui.text(f"Current Expression: {self.output.get_value()}")
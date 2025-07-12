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

class Sympy_Display(Node):
    def __init__(self, node_id, name="Sympy Display"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=sympy.core.Basic)
        self.input.set_value(sympy.sympify("0"), False)

    def draw_content(self):
        sympy.init_printing(use_unicode=False, wrap_line=False)
        imgui.text(sympy.pretty(self.input.get_value()))
        
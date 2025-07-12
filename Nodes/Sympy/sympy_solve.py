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
from typing import List
from sympy import init_printing

class Sympy_Solve(Node):
    def __init__(self, node_id, name="Sympy Solve"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=sympy.core.Basic)
        self.input.set_value(sympy.sympify("0"), False)

        self.symbols = []
        self.solutions = set()
        self.solution_pins = []
    
    def on_input_update(self, nodes: List['Node']):
        for pin in self.pins:
            if pin.on_input_update(nodes):
                syms = self.extract_symbols(self.input.get_value())
                if syms:
                    self.symbols = syms
                    self.solve()
                    # remove old solution pins
                    for pin in self.solution_pins:
                        self.remove_pin(pin.id)
                    self.solution_pins.clear()
                    # create new solution pins
                    for i, sol in enumerate(self.solutions):
                        pin_id = ID.next_id()
                        new_pin = self.add_pin(pin_id, ed.PinKind.output, f"Solution {i+1}", left=False, value_type=type(sol))
                        new_pin.set_value(sol, False)
                        self.solution_pins.append(new_pin)

    def extract_symbols(self, expr):
        try:
            symbols = list(expr.free_symbols)
            return symbols
        except Exception as e:
            print(f"Error extracting symbols: {e}")
        return []
    
    def solve(self):
        try:
            if self.symbols:
                self.solutions = sympy.solve(self.input.get_value(), dict=True, symbols=self.symbols)
                print(type(self.solutions))
                print(self.solutions)
            else:
                self.solutions = {}
        except Exception as e:
            print(f"Error solving expression: {e}")
            self.solutions = {}


    def draw_content(self):
        sympy.init_printing(use_unicode=False, wrap_line=False)
        imgui.text(sympy.pretty(self.input.get_value()))

        if self.symbols:
            # display each solution
            for dict in self.solutions:
                imgui.text(f"{list(dict.keys())[0]} = {list(dict.values())[0]}")
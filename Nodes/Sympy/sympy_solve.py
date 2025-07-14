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

        # symbol to solve for
        self.solve_for = self.add_pin(ID.next_id(), ed.PinKind.input, "Solve for", left=True, value_type=sympy.core.Basic)


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
                        new_pin = self.add_pin(pin_id, ed.PinKind.output, f"Solution {i+1}", left=False, value_type=type(sol[self.solve_for.get_value()]))
                        new_pin.set_value(sol[self.solve_for.get_value()], False)
                        self.solution_pins.append(new_pin)

    def extract_symbols(self, expr):
        try:
            symbols = list(expr.free_symbols)
            return symbols
        except Exception as e:
            print(f"Error extracting symbols: {e}")
        return []
    


    # a function to map the symbols so that the pin we are trying to solve for is the first alphabetically, this must be reversable
    def map_symbols(self):
        # create a list of symbols from a, b, c, ... to the length of self.symbols
        out = [sympy.Symbol(chr(i)) for i in range(ord('a'), ord('a') + len(self.symbols) + 1)]

        # create a dictionary to map the symbols to the new symbols
        mapping = {}
        for i, sym in enumerate(self.symbols):
            # if the symbol is the one we are trying to solve for, it should be the first in the list
            if sym == self.solve_for.get_value():
                mapping[sym] = out[0]
            else:
                # map the rest of the symbols to the rest of the list
                mapping[sym] = out[i + 1] if i + 1 < len(out) else out[-1]
                
        return mapping

    def solve(self):
        try:
            if self.symbols:
                # sympy.solve solves for the first symbol alphabetically by default, # so we need to specify the symbol to solve for
                print(f"original expression: {self.input.get_value()}")
                print(f"solving for: {self.solve_for.get_value()}")
                print(self.map_symbols())
                # map the symbols to the new symbols
                sym_map = self.map_symbols()
                # replace the symbols in the expression with the new symbols
                for sym, new_sym in sym_map.items():
                    self.input.set_value(self.input.get_value().subs(sym, new_sym), False)

                # print the mapped expression
                print(f"Mapped expression: {self.input.get_value()}")

                self.solutions = sympy.solve(self.input.get_value(), dict=True)
                # replace the new symbols with the original symbols in the solutions keys

                print(f"Solutions: {self.solutions}")

                for sol in self.solutions:
                    for sym, new_sym in sym_map.items():
                        if new_sym in sol:
                            sol[sym] = sol.pop(new_sym)

                print (f"Mapped solutions: {self.solutions}")
                # replace the new synmbols with the original symbols in the solutions values
                
                for sym, new_sym in sym_map.items():
                    try:
                        sol[self.solve_for.get_value()] = sol[self.solve_for.get_value()].subs(new_sym, sym)
                        print(f"new sym: {new_sym}, sym: {sym}")
                        print(type(sol[sym]))
                        print(f"Unmapped solution: {sol[sym]} for {sym} in {sol}")
                    except Exception as e:
                        print(f"Error unmapping solution: {e} for {sym} in {sol}")

                print (f"Unmapped solutions: {self.solutions}")
                # restore the original expression
                self.input.set_value(self.input.get_value().subs({v: k for k, v in sym_map.items()}), False)
                # print the solutions

                print(f"original expression restored: {self.input.get_value()} ")
                
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
from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py
from Node import Pin
import sympy
import sympy.core
import time
from typing import List
from sympy import init_printing

class Sympy_Expression(Node):
    def __init__(self, node_id, name="Sympy Expression"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Input", left=True, value_type=sympy.core.Basic)
        self.input.set_value(sympy.sympify("0"), False)

        # make an output pin for each sympy function

        self.symbols: List[sympy.Symbol] = []

        self.symbol_pins: List[Pin] = []

        #simplify
        self.output_simplified = self.add_pin(ID.next_id(), ed.PinKind.output, "Simplified", left=False, value_type=sympy.core.Basic)
        #expand
        self.output_expanded = self.add_pin(ID.next_id(), ed.PinKind.output, "Expanded", left=False, value_type=sympy.core.Basic)
        #factor
        self.output_factored = self.add_pin(ID.next_id(), ed.PinKind.output, "Factored", left=False, value_type=sympy.core.Basic)
        #cancel
        self.output_cancelled = self.add_pin(ID.next_id(), ed.PinKind.output, "Cancelled", left=False, value_type=sympy.core.Basic)
        #apart
        self.output_apart = self.add_pin(ID.next_id(), ed.PinKind.output, "Partial Fraction", left=False, value_type=sympy.core.Basic)
        #trigsimplify
        self.output_trigsimplified = self.add_pin(ID.next_id(), ed.PinKind.output, "Trig Simplified", left=False, value_type=sympy.core.Basic)
        #expand
        self.output_expanded = self.add_pin(ID.next_id(), ed.PinKind.output, "Expanded", left=False, value_type=sympy.core.Basic)
        #powsimp
        self.output_powsimplified = self.add_pin(ID.next_id(), ed.PinKind.output, "Power Simplified", left=False, value_type=sympy.core.Basic)
        #expand power
        self.output_expand_power = self.add_pin(ID.next_id(), ed.PinKind.output, "Expand Power", left=False, value_type=sympy.core.Basic)
        #logcombine
        self.output_log_combined = self.add_pin(ID.next_id(), ed.PinKind.output, "Log Combined", left=False, value_type=sympy.core.Basic)
        # expand log
        self.output_expand_log = self.add_pin(ID.next_id(), ed.PinKind.output, "Expand Log", left=False, value_type=sympy.core.Basic)

    def on_input_update(self, nodes: List['Node']):
        for pin in self.pins:
            if pin.on_input_update(nodes):
                syms = self.extract_symbols(self.input.get_value())
                if syms != self.symbols:
                    self.symbols = syms
                    # remove all old symbol pins
                    for sym_pin in self.symbol_pins:
                        self.remove_pin(sym_pin.id)
                    self.symbol_pins.clear()
                    # create new symbol pins
                    for sym in self.symbols:
                        sym_pin = self.add_pin(ID.next_id(), ed.PinKind.output, str(sym), left=False, value_type=sympy.core.Basic)
                        sym_pin.set_value(sym, increment_change_counter=False)
                        self.symbol_pins.append(sym_pin)
        
                self.evaluate_expression()


    def extract_symbols(self, expr):
        try:
            symbols = list(expr.free_symbols)
            return symbols
        except Exception as e:
            print(f"Error extracting symbols: {e}")
        return []
    

    def evaluate_expression(self):
        # evaluate the expression
        if self.input.get_value() is not None:
            expr = self.input.get_value()
                   # Simplify
            try:
                simplified = sympy.simplify(expr)
                self.output_simplified.set_value(simplified, increment_change_counter=True)
                #imgui.text(f"Simplified: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(simplified))
            except Exception as e:
                imgui.text(f"Error simplifying expression: {e}")

            # Expand
            try:
                expanded = sympy.expand(expr)
                self.output_expanded.set_value(expanded, increment_change_counter=True)
                #imgui.text(f"Expanded: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(expanded))
            except Exception as e:
                imgui.text(f"Error expanding expression: {e}")

            # Factor
            try:
                factored = sympy.factor(expr)
                self.output_factored.set_value(factored, increment_change_counter=True)
                #imgui.text(f"Factored: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(factored))
            except Exception as e:
                imgui.text(f"Error factoring expression: {e}")

            # Cancel
            try:
                cancelled = sympy.cancel(expr)
                self.output_cancelled.set_value(cancelled, increment_change_counter=True)
                #imgui.text(f"Cancelled: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(cancelled))
            except Exception as e:
                imgui.text(f"Error canceling expression: {e}")

            # Apart
            try:
                apart = sympy.apart(expr)
                self.output_apart.set_value(apart, increment_change_counter=True)
                #imgui.text(f"Apart: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(apart))
            except Exception as e:
                imgui.text(f"Error applying apart: {e}")

            # Trig Simplify
            try:
                trigsimplified = sympy.trigsimp(expr)
                self.output_trigsimplified.set_value(trigsimplified, increment_change_counter=True)
                #imgui.text(f"Trig Simplified: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(trigsimplified))
            except Exception as e:
                imgui.text(f"Error applying trigonometric simplification: {e}")

            # Power Simplify
            try:
                powsimplified = sympy.powsimp(expr)
                self.output_powsimplified.set_value(powsimplified, increment_change_counter=True)
                #imgui.text(f"Power Simplified: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(powsimplified))
            except Exception as e:
                imgui.text(f"Error applying power simplification: {e}")

            # Expand Power
            try:
                expand_power = sympy.expand_power_base(expr)
                self.output_expand_power.set_value(expand_power, increment_change_counter=True)
                #imgui.text(f"Expand Power: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(expand_power))
            except Exception as e:
                imgui.text(f"Error applying power expansion: {e}")

            # Log Combine
            try:
                log_combined = sympy.logcombine(expr, force=True)
                self.output_log_combined.set_value(log_combined, increment_change_counter=True)
                #imgui.text(f"Log Combined: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(log_combined))
            except Exception as e:
                imgui.text(f"Error applying log combination: {e}")

            # Expand Log
            try:
                expand_log = sympy.expand_log(expr, force=True)
                self.output_expand_log.set_value(expand_log, increment_change_counter=True)
                #imgui.text(f"Expand Log: ")
                #imgui.same_line()
                #imgui.text(sympy.pretty(expand_log))
            except Exception as e:
                imgui.text(f"Error applying log expansion: {e}")
        



    def draw_content(self):
        

        # evaluate the expression
        if self.input.get_value() is not None:

            expr = self.input.get_value()

            sympy.init_printing(use_unicode=False, wrap_line=False)
            imgui.text(f"Input: ")
            imgui.same_line()
            imgui.text(sympy.pretty(self.input.get_value()))

            # Simplify
            try:
                simplified = self.output_simplified.get_value()
                #self.output_simplified.set_value(simplified, increment_change_counter=True)
                imgui.text(f"Simplified: ")
                imgui.same_line()
                imgui.text(sympy.pretty(simplified))
            except Exception as e:
                imgui.text(f"Error simplifying expression: {e}")

            # Expand
            try:
                expanded = self.output_expanded.get_value()
                #self.output_expanded.set_value(expanded, increment_change_counter=True)
                imgui.text(f"Expanded: ")
                imgui.same_line()
                imgui.text(sympy.pretty(expanded))
            except Exception as e:
                imgui.text(f"Error expanding expression: {e}")

            # Factor
            try:
                factored = self.output_factored.get_value()
                #self.output_factored.set_value(factored, increment_change_counter=True)
                imgui.text(f"Factored: ")
                imgui.same_line()
                imgui.text(sympy.pretty(factored))
            except Exception as e:
                imgui.text(f"Error factoring expression: {e}")

            # Cancel
            try:
                cancelled = self.output_cancelled.get_value()
                #self.output_cancelled.set_value(cancelled, increment_change_counter=True)
                imgui.text(f"Cancelled: ")
                imgui.same_line()
                imgui.text(sympy.pretty(cancelled))
            except Exception as e:
                imgui.text(f"Error canceling expression: {e}")

            # Apart
            try:
                apart = self.output_apart.get_value()
                #self.output_apart.set_value(apart, increment_change_counter=True)
                imgui.text(f"Apart: ")
                imgui.same_line()
                imgui.text(sympy.pretty(apart))
            except Exception as e:
                imgui.text(f"Error applying apart: {e}")

            # Trig Simplify
            try:
                trigsimplified = self.output_trigsimplified.get_value()
                #self.output_trigsimplified.set_value(trigsimplified, increment_change_counter=True)
                imgui.text(f"Trig Simplified: ")
                imgui.same_line()
                imgui.text(sympy.pretty(trigsimplified))
            except Exception as e:
                imgui.text(f"Error applying trigonometric simplification: {e}")

            # Power Simplify
            try:
                powsimplified = self.output_powsimplified.get_value()
                #self.output_powsimplified.set_value(powsimplified, increment_change_counter=True)
                imgui.text(f"Power Simplified: ")
                imgui.same_line()
                imgui.text(sympy.pretty(powsimplified))
            except Exception as e:
                imgui.text(f"Error applying power simplification: {e}")

            # Expand Power
            try:
                expand_power = self.output_expand_power.get_value()
                #self.output_expand_power.set_value(expand_power, increment_change_counter=True)
                imgui.text(f"Expand Power: ")
                imgui.same_line()
                imgui.text(sympy.pretty(expand_power))
            except Exception as e:
                imgui.text(f"Error applying power expansion: {e}")

            # Log Combine
            try:
                log_combined = self.output_log_combined.get_value()
                #self.output_log_combined.set_value(log_combined, increment_change_counter=True)
                imgui.text(f"Log Combined: ")
                imgui.same_line()
                imgui.text(sympy.pretty(log_combined))
            except Exception as e:
                imgui.text(f"Error applying log combination: {e}")

            # Expand Log
            try:
                expand_log = self.output_expand_log.get_value()
                #self.output_expand_log.set_value(expand_log, increment_change_counter=True)
                imgui.text(f"Expand Log: ")
                imgui.same_line()
                imgui.text(sympy.pretty(expand_log))
            except Exception as e:
                imgui.text(f"Error applying log expansion: {e}")
        

        # Draw symbol pins
        if self.symbols:
            imgui.text("Symbols:")
            for sym_pin in self.symbol_pins:
                value = sym_pin.get_value()
                if value is not None:
                    imgui.text(f"{sym_pin.name}: {sympy.pretty(value)}")
                else:
                    imgui.text(f"{sym_pin.name}: None")
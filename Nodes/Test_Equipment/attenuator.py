# import driver from /home/obi/code/RF_Power_Meter/RF_Power_Meter.py and add it to the path
import sys
sys.path.append('/home/obi/code/Digital_Step_Attenuator')
from ATT_6000 import ATT_6000

from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class attenuator(Node):
    def __init__(self, node_id, name="Attenuator"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Attenuation (dB)", left=True, value_type=float)
        self.input.set_value(0.0, False)
        try:
            self.attenuator = ATT_6000()  # Initialize the Attenuator
            self.connected = True
            self.attenuator.set_attenuation(1.0)  # Set initial attenuation to 0 dB
            self.attenuator.set_attenuation(0.0)  # Set initial attenuation to 0 dB
        except Exception as e:
            self.connected = False
            print(f"Error initializing Attenuator: {e}")

    def draw_content(self):
        if self.connected:
            try:
                #update the attenuator value.
                imgui.set_next_item_width(100)  # Adjust width to fit the window
                changed, new_attenuation = imgui.input_float("Attenuation (dB)", self.input.get_value(), step=0.1, step_fast=1.0)
                if changed:
                    self.input.set_value(new_attenuation, True)
                    self.attenuator.set_attenuation(new_attenuation)

                # If the input pin had a new value, set the attenuation
                if self.input.get_changed_this_frame():
                    attenuation_value = self.input.get_value()
                    self.attenuator.set_attenuation(attenuation_value)
            except Exception as e:
                print(f"Error setting Attenuation: {e}")
                self.connected = False
                self.input.set_value(0, False)
        else:
            # add a button to try to reconnect
            if imgui.button(f"Reconnect##{self.node_id}"):
                try:
                    self.attenuator = ATT_6000()  # Try to reconnect
                    self.connected = True
                except Exception as e:
                    print(f"Error reconnecting to Attenuator: {e}")
                    self.connected = False
        imgui.text(f"Attenuation: {self.input.get_value()} dB")
        #imgui.text(f"Change Counter: {self.output.get_change_counter()}")
        
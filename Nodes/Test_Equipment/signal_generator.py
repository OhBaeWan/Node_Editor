# import driver from /home/obi/code/RF_Power_Meter/RF_Power_Meter.py and add it to the path
import sys
sys.path.append('/home/obi/code/HT008_Signal_Generator')
from HT008 import Ht008

from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class signal_generator(Node):
    def __init__(self, node_id, name="Signal Generator"):
        super().__init__(node_id, name)
        self.input = self.add_pin(ID.next_id(), ed.PinKind.input, "Frequency (Hz)", left=True, value_type=float)
        self.input.set_value(0.0, False)
        try:
            self.signal_generator = Ht008()  # Initialize the Signal Generator
            self.connected = True
            self.signal_generator.set_single_point(0.0)  # Set initial frequency to 0 Hz
        except Exception as e:
            self.connected = False
            print(f"Error initializing Signal Generator: {e}")

    def draw_content(self):
        if self.connected:
            try:
                #update the signal generator frequency.
                imgui.set_next_item_width(100)  # Adjust width to fit the window
                changed, new_frequency = imgui.input_float("Frequency (MHz)",  float(self.input.get_value()), step=1, step_fast=10)
                if changed:
                    self.input.set_value(float(new_frequency), True)
                    self.signal_generator.set_single_point(new_frequency * 1.0e6)

                # If the input pin had a new value, set the frequency
                if self.input.get_changed_this_frame():
                    frequency_value = self.input.get_value()
                    self.signal_generator.set_single_point(frequency_value * 1.0e6)
            except Exception as e:
                print(f"Error setting Frequency: {e}")
                self.connected = False
                self.input.set_value(0, False)
        else:
            # add a button to try to reconnect
            if imgui.button(f"Reconnect##{self.node_id}"):
                try:
                    self.signal_generator = Ht008()  # Try to reconnect
                    self.connected = True
                except Exception as e:
                    print(f"Error reconnecting to Signal Generator: {e}")
                    self.connected = False
        imgui.text(f"Frequency: {self.input.get_value()} MHz")
        #imgui.text(f"Change Counter: {self.output.get_change_counter()}")
        
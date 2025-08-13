# import driver from /home/obi/code/RF_Power_Meter/RF_Power_Meter.py and add it to the path
import sys
sys.path.append('/home/obi/code/RF_Power_Meter')
from RF_Power_Meter import RF_Power_Meter

from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class power_meter(Node):
    def __init__(self, node_id, name="Power Meter"):
        super().__init__(node_id, name)
        self.output = self.add_pin(ID.next_id(), ed.PinKind.output, "Power (dBm)", left=False, value_type=float)
        self.output.set_value(0, False)
        try:
            self.rf_power_meter = RF_Power_Meter()  # Initialize the RF Power Meter
            self.connected = True
        except Exception as e:
            self.connected = False
            print(f"Error initializing RF Power Meter: {e}")

    def draw_content(self):
        # Update the power meter value
        if self.connected:
            try:
                # Read the power value from the RF Power Meter
                power_value = self.rf_power_meter.read()
                self.output.set_value(float(power_value), True)
            except Exception as e:
                print(f"Error reading from RF Power Meter: {e}")
                self.connected = False
                self.output.set_value(0, False)
        else:
            # add a button to try to reconnect
            if imgui.button(f"Reconnect##{self.node_id}"):
                try:
                    self.rf_power_meter = RF_Power_Meter()  # Try to reconnect
                    self.connected = True
                except Exception as e:
                    print(f"Error reconnecting to RF Power Meter: {e}")
                    self.connected = False
        imgui.text(f"Power: {self.output.get_value()} dBm")
        #imgui.text(f"Change Counter: {self.output.get_change_counter()}")
        
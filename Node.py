from dataclasses import dataclass
from typing import List

from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)

class IdProvider:
    """A simple utility to obtain unique ids"""

    _next_id: int = 1

    def next_id(self):
        """Gets a new unique id"""
        r = self._next_id
        self._next_id += 1
        return r

    def reset(self):
        """Resets the counter"""
        self._next_id = 1


ID = IdProvider()

class ImGuiEx:
    """Some additional tools for ImGui. Provide columns via begin/end_group"""

    @staticmethod
    def begin_column():
        imgui.begin_group()

    @staticmethod
    def next_column():
        imgui.end_group()
        imgui.same_line()
        imgui.begin_group()

    @staticmethod
    def end_column():
        imgui.end_group()


# Struct to hold basic information about connection between
# pins. Note that connection (aka. link) has its own ID.
@dataclass
class LinkInfo:
    id: ed.LinkId
    input_id: ed.PinId
    output_id: ed.PinId
    input_node: 'Node'
    output_node: 'Node'
    valid: bool = True  # Flag to indicate if the link is valid
    count: int = -1  # Counter to track the last count from the output pin


class Pin:
    id: ed.PinId
    kind: ed.PinKind
    name: str = ""
    left: bool = True  # True if the pin is on the left side of the node, False if on the right side
    links: list[LinkInfo] = None  # List of links connected to this pin

    def __init__(self, id: ed.PinId, kind: ed.PinKind, name: str = "", left: bool = True, value_type: type = None):
        self.id = id
        self.kind = kind
        self.name = name
        self.left = left
        self.links = []

        self._value = None  # You can add a value attribute if needed, e.g., for storing pin state
        self._value_type: type = value_type  # Type of the value, if needed
        self._change_counter = 0  # Counter to track changes in the pin's value

    def set_value(self, value, increment_change_counter: bool = True):
        """Set the value of this pin"""
        # check if the value is of the correct type, or a subclass of the expected type
        if value.__class__ == self._value_type or issubclass(value.__class__, self._value_type):
            self._value = value
            if increment_change_counter:
                self._change_counter += 1
            return True
        else:
            print(f"Value type mismatch: expected {self._value_type}, got {value.__class__}")
            return False

    def get_value(self):
        """Get the value of this pin"""
        return self._value
    
    def get_change_counter(self):
        """Get the change counter of this pin"""
        return self._change_counter

    def add_link(self, link: LinkInfo):
        """Add a link to this pin"""
        self.links.append(link)

    def remove_link(self, link_id: ed.LinkId):
        """Remove a link from this pin by its ID"""
        self.links = [link for link in self.links if link.id != link_id]

    def is_input(self):
        """Check if this pin is an input pin"""
        return self.kind == ed.PinKind.input

    def on_input_update(self):
        """Update the pin based on input from connected nodes"""
        for link in self.links:
            
            # only update links where this pin is an input
            if self.is_input():

                # find the link's output pin
                output_pin = link.output_node.get_pin(link.output_id)
                if output_pin:

                    # only update if there is a new output value
                    if output_pin.get_change_counter() > link.count:
                        link.count = output_pin.get_change_counter()
                        # update the input pin's value from the output pin. link.valid is true if the type check is passed, and false otherwise. 
                        link.valid = self.set_value(output_pin.get_value())
    
    def on_output_update(self):
        """Override this method to handle updates to the output pin"""
        pass

    def draw_links(self, flipped: bool):
        """Draw the links connected to this pin"""
        for link in self.links:
            if flipped:
                # If the node is flipped, we might want to draw the link differently
                if link.valid:
                    ed.link(link.id, link.output_id, link.input_id)
                else:
                    # If the link is not valid, we can still draw it red
                    ed.link(link.id, link.input_id, link.output_id, color=(1, 0, 0, 1))
            else:
                if link.valid:
                    # Normal drawing of the link
                    ed.link(link.id, link.input_id, link.output_id)
                else:
                    # If the link is not valid, we can still draw it red
                    ed.link(link.id, link.output_id, link.input_id, color=(1, 0, 0, 1))

class Node:
    pins: list[Pin] = None  # List of pins connected to this node


    def __init__(self, node_id, label, position=None):
        self.label = label
        self.node_id = ed.NodeId(node_id)
        self.position = position if position is not None else (0, 0)
        self.pins = []
        self.flipped = False  # Flag to indicate if the node is flipped

        self.edit_mode = False  # Flag to indicate if the node is in edit mode

    def add_pin(self, pin_id:int, pin_kind:ed.PinKind, name:str="", left:bool=True, value_type:type=None):
        """Adds a new pin to this node"""
        self.pins.append(Pin(id=ed.PinId(pin_id), kind=pin_kind, name=name, left=left, value_type=value_type))
        return self.pins[-1]  # Return the newly added pin

    def remove_pin(self, pin_id: ed.PinId):
        """Removes a pin from this node by its ID"""
        self.pins = [pin for pin in self.pins if pin.id != pin_id]

    def get_pin(self, pin_id: ed.PinId):
        """Get a pin by its ID"""
        for pin in self.pins:
            if pin.id == pin_id:
                return pin
        return None

    def add_link(self, link_id: ed.LinkId, input_pin_id: ed.PinId, output_pin_id: ed.PinId, nodes: List['Node']):
        """Adds a new link to this Node if this node contains either of the given pins, if the Pin is an input pin and already has a connection, or if the pin doesnt exist on this node return false, otherwise true"""
        # check if either pin is assigned to this node 
        for pin in self.pins:
            if pin.id == input_pin_id or pin.id == output_pin_id:

                # if the pin is an input pin check that there isnt already an output link connected
                if pin.is_input():
                    input_node = self
                    if len(pin.links) > 0:
                        return False
                    # the pin is on this node and is an input pin
                    else:
                        # find the output node
                        for node in nodes:
                            if node.get_pin(input_pin_id) != None or node.get_pin(output_pin_id) != None:
                                output_node = node

                # the pin is on this node and is an output pin
                else:
                    output_node = self
                    # find the input node
                    for node in nodes:
                        if node.get_pin(input_pin_id) != None or node.get_pin(output_pin_id) != None:
                            input_node = node

                # add the new link to the pin
                pin.add_link(LinkInfo(id=link_id, input_id=input_pin_id, output_id=output_pin_id, input_node=input_node, output_node=output_node))
                return True
        return False
        
                

    def remove_link(self, link_id: ed.LinkId):
        """Remove a link from all pins by its ID"""
        for pin in self.pins:
            pin.remove_link(link_id)

    def set_position(self, x, y):
        """sets the screen position of the node"""
        self.position = (x, y)

    def get_position(self):
        """get the screen position of the node"""
        return self.position
    
    def on_frame(self):
        """Called at each frame to update the node's GUI"""
        ed.begin_node(self.node_id)

        # is the node is sleced and the R button is pressed, then flip the node
        if ed.is_node_selected(self.node_id) and imgui.is_key_pressed(imgui.Key.r):
            self.flipped = not self.flipped
        #ed.set_node_position(self.node_id, self.position)
        self.draw_header()
        

        ImGuiEx.begin_column()
        for pin in self.pins:
            if pin.left != self.flipped:

                ed.begin_pin(pin.id, ed.PinKind.input)
                if pin.kind == ed.PinKind.input:
                    imgui.text(f"-> ")
                else:
                    imgui.text(f"<- ")
                ed.end_pin()
                pin.draw_links(self.flipped)
                imgui.same_line()
                if not self.edit_mode:
                    imgui.set_next_item_allow_overlap()

                if self.edit_mode:
                    imgui.set_next_item_width(imgui.get_content_region_avail()[0] * 0.3)
                    changed, pin.name = imgui.input_text(f"##{pin.id}", pin.name, imgui.InputTextFlags_.enter_returns_true )
                    if changed:
                        self.edit_mode = False
                else:
                    imgui.text(f"{pin.name}")
                    imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + imgui.calc_text_size(f"<- ").x )
                    imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - imgui.calc_text_size(f"{pin.name}").y )
                    if imgui.invisible_button(f"{pin.name}##{pin.id}", imgui.calc_text_size(f"{pin.name}")):
                        print(f"Node {pin.name} clicked")
                        self.edit_mode = True
        if self.edit_mode:
            if imgui.button("+##Left"):
                new_pin_id = ID.next_id()
                self.add_pin(new_pin_id, ed.PinKind.input, f"New Pin", left=True)
                print(f"Added new pin {new_pin_id} to node {self.node_id}")
                    
        ImGuiEx.next_column()
        self.draw_content()
        ImGuiEx.next_column()
        for pin in self.pins:
            if pin.left == self.flipped:
                if not self.edit_mode:
                    imgui.set_next_item_allow_overlap()

                if self.edit_mode:
                    imgui.set_next_item_width(imgui.get_content_region_avail()[0] * 0.4)
                    changed, pin.name = imgui.input_text(f"##{pin.id}", pin.name, imgui.InputTextFlags_.enter_returns_true )
                    if changed:
                        self.edit_mode = False
                else:
                    imgui.text(f"{pin.name}")

                    imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - imgui.calc_text_size(f"{pin.name}").y )
                    if imgui.invisible_button(f"{pin.name}##{pin.id}", imgui.calc_text_size(f"{pin.name}")):
                        print(f"Node {pin.name} clicked")
                        self.edit_mode = True
                imgui.same_line()
                ed.begin_pin(pin.id, ed.PinKind.output)
                if pin.kind == ed.PinKind.input:
                    imgui.text(f" <-")
                else:
                    imgui.text(f" ->")
                ed.end_pin()
                pin.draw_links(self.flipped)
        if self.edit_mode:
            if imgui.button("+##Right"):
                new_pin_id = ID.next_id()
                self.add_pin(new_pin_id, ed.PinKind.output, f"New Pin", left=False)
                print(f"Added new pin {new_pin_id} to node {self.node_id}")
        ImGuiEx.end_column()

        self.draw_footer()
        # Draw links for this node
        #for pin in self.pins:
        #    for link in pin.links:
        #        imgui.text(f"Link from {link.output_id} to {link.input_id}")

        ed.end_node()

    def on_input_update(self):
        """Called at the beginning of each frame before drawing anything to update all input pins"""
        for pin in self.pins:
            pin.on_input_update()

    def draw_header(self):
        """Override this method to draw custom header content"""
        
        if not self.edit_mode:
            imgui.set_next_item_allow_overlap()

        if self.edit_mode:
            imgui.set_next_item_width(imgui.get_content_region_avail()[0] * 0.8)
            changed, self.label = imgui.input_text(f"##{self.node_id}", self.label, imgui.InputTextFlags_.enter_returns_true )
            if changed:
                self.edit_mode = False
        else:
            imgui.text(self.label)


            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - imgui.calc_text_size(self.label).y )
            if imgui.invisible_button(f"{self.label}##{self.node_id}", imgui.calc_text_size(self.label)):
                print(f"Node {self.label} clicked")
                self.edit_mode = True

    def draw_content(self):
        """Override this method to draw custom content inside the node"""
        pass

    def draw_footer(self):
        """Override this method to draw custom footer content"""
        pass
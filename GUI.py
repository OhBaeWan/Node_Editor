from __future__ import annotations
from typing import List
from dataclasses import dataclass
from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from imgui_bundle.immapp import static, run_anon_block

from Node import Node, ID




# GUI is a singleton
class GUI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    nodes: List[Node]

    def __init__(self):
        self.nodes = []


    def discover_nodes(self):
        """Discover nodes in the Node directory and returns a list of Node classes"""
        import os
        import importlib.util

        output = []

        node_dir = os.path.dirname(__file__) + "/Nodes"
        for filename in os.listdir(node_dir):
            if filename.endswith(".py") and filename != "Node.py":
                module_name = filename[:-3]
                module_path = os.path.join(node_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is not None:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    # Check if the module has a class that inherits from Node
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and issubclass(obj, Node) and obj is not Node:
                            output.append(obj)
                            #print(f"Discovered node: {obj.__name__} from {module_name}")

        return output


    def on_frame(self):
        """Called at each frame to update the GUI"""

        # menue bar
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                _, clicked = imgui.menu_item("New", "Ctrl+N", False)
                if clicked:
                    self.nodes.clear()
                    self.links.clear()
                _, clicked = imgui.menu_item("Save", "Ctrl+S", False)
                if clicked:
                    # Save logic here
                    pass
                _, clicked = imgui.menu_item("Load", "Ctrl+L", False)
                if clicked:
                    # Load logic here
                    pass
                _, clicked = imgui.menu_item("Quit", "Ctrl+Q", False)
                if clicked:
                    pass
                imgui.end_menu()  
            # node creation menu
            if imgui.begin_menu("Create Node"):
                _, clicked = imgui.menu_item("New Node", "N", False)
                if clicked:
                    node_id = ID.next_id()
                    node = Node(node_id, "New Node")
                    # add a default pin to the node
                    node.add_pin(ID.next_id(), ed.PinKind.input, "Input Pin", left=True)
                    node.add_pin(ID.next_id(), ed.PinKind.output, "Output Pin", left=False)
                    self.nodes.append(node)
                    node.on_frame()
                
                # dynamically add more nodes here by loading
                # the Node directory and creating instances of the Node classes
                node_classes = self.discover_nodes()
                for node_class in node_classes:
                    node_name = node_class.__name__
                    _, clicked = imgui.menu_item(node_name, "", False)
                    if clicked:
                        node_id = ID.next_id()
                        node = node_class(node_id, node_name)
                        # add a default pin to the node
                        #node.add_pin(ID.next_id(), ed.PinKind.input, "Input Pin", left=True)
                        #node.add_pin(ID.next_id(), ed.PinKind.output, "Output Pin", left=False)
                        self.nodes.append(node)
                        node.on_frame() 

                imgui.end_menu()
            imgui.end_main_menu_bar()

        ed.begin("My Editor", imgui.ImVec2(0.0, 0.0))

        for node in self.nodes:
            node.on_input_update(self.nodes)
            
        for node in self.nodes:
            node.on_frame()
        
        


        if ed.begin_create():
            input_pin_id = ed.PinId()
            output_pin_id = ed.PinId()
            if ed.query_new_link(input_pin_id, output_pin_id):
                # tooltip following the mouse cursor
                #imgui.set_tooltip(f"Input Pin: {input_pin_id}, Output Pin: {output_pin_id}")
                imgui.text(f"Output Pin: {output_pin_id} Input Pin: {input_pin_id}")

                if input_pin_id and output_pin_id:  # both are valid, let's accept link
                    if output_pin_id != input_pin_id:
                        if ed.accept_new_item():
                            link_id = ed.LinkId(ID.next_id())
                            # give the new link to each node
                            result = False
                            input_pin = None
                            input_node = None
                            output_pin = None
                            output_node = None
                            for node in self.nodes:
                                inpin = node.get_pin(input_pin_id)
                                outpin = node.get_pin(output_pin_id)

                                if inpin is not None:
                                    if inpin.is_input():
                                        input_pin = inpin
                                        input_node = node
                                    else:
                                        outpin = inpin
                                        output_node = node
                                if outpin is not None:
                                    if outpin.is_input():
                                        input_pin = outpin
                                        input_node = node
                                    else:
                                        output_pin = outpin
                                        output_node = node
                                    
                            
                            if input_pin is None or output_pin is None:
                                # If we don't have a valid input or output pin, we can reject the link.
                                ed.reject_new_item()
                            elif input_pin is None and output_pin is None:
                                # If both pins are None, we can reject the link.
                                ed.reject_new_item()
                            else:
                                if input_node.add_link(link_id, input_pin.id, output_pin.id):
                                    output_node.add_link(link_id, input_pin.id, output_pin.id)
                            # Draw new link.
                            #ed.link(link_id, input_pin_id, output_pin_id)
            '''
            if ed.query_new_node():
                node_id = ID.next_id()
                node = Node(node_id, "New Node")
                self.nodes.append(node)
                node.on_frame()
            '''
            ed.end_create()
        if ed.begin_delete():
            # There may be many links marked for deletion, let's loop over them.
            deleted_link_id = ed.LinkId()
            while ed.query_deleted_link(deleted_link_id):
                # If you agree that link can be deleted, accept deletion.
                if ed.accept_deleted_item():
                    # Then ask all nodes to remove the link from their data.
                    for node in self.nodes:
                        node.remove_link(deleted_link_id)
                # You may reject link deletion by calling:
                # ed.reject_deleted_item()
            deleted_node_id = ed.NodeId()
            while ed.query_deleted_node(deleted_node_id):
                if ed.accept_deleted_item():
                    for node in self.nodes:
                        if node.node_id == deleted_node_id:
                            # remove all of the node's links from all nodes
                            for pin in node.pins:
                                for link in pin.links:
                                    for n in self.nodes:
                                        n.remove_link(link.id)
                            # remove the node itself
                            self.nodes.remove(node)
                            break
            ed.end_delete()
        ed.end()

@static(GUI=None)
def gui():
    statics = gui
    if statics.GUI is None:
        statics.GUI = GUI()
    statics.GUI.on_frame()



def main():
    import os

    this_dir = os.path.dirname(__file__)
    config = ed.Config()
    config.settings_file = this_dir + "/Node_Editor.json"
    from imgui_bundle import immapp

    immapp.run(gui, with_node_editor_config=config, with_markdown=True, window_size=(800, 600))


if __name__ == "__main__":
    main()
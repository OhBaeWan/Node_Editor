from imgui_bundle import (
    imgui,
    imgui_md,
    imgui_node_editor as ed,
)
from Node import Node, LinkInfo
from Node import ID  # Assuming ID is defined in Node.py

class ErrorNode(Node):
    def __init__(self, node_id, name="Error Node"):
        super().__init__(node_id, name)

    def draw_content(self):
        # throw an error to test the error handling
        raise Exception("This is a test error from ErrorNode")
        
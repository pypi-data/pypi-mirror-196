"""
    Filename: GPA/modules/basic.py
    Description: Definition of Basic Units inside Graphs.
    Version: 0.1.0
    Contributor: Shu Wang, 2023
    Date: 03/09/2023
"""

class CodeNode:
    def __init__(self, 
                 node_id : str = "",
                 code : str = "",
                 node_type : str = "",
                 node_attr : any = None) -> None:
        self.node_id = node_id
        self.code = code
        self.node_type = node_type
        self.node_attr = node_attr
        return
    
    def tokenize(self) -> None:
        pass
    
class CodeEdge:
    def __init__(self,
                 node_out: str,
                 node_in: str,
                 edge_type: str = "",
                 edge_attr: any = None) -> None:
        self.node_out = node_out
        self.node_in = node_in
        self.edge_type = edge_type
        self.edge_attr = edge_attr
        return

"""
    Filename: GPA/graphs.py
    Description: Definition of Code Graphs
    Version: 0.1.0
    Contributor: Shu Wang, 2023
    Date: 03/09/2023
"""

import numpy as np
import scipy.sparse as sp
import graphviz

from .modules.basic import *

class CodePropGraph:
    def __init__(self, 
                 name : str = "",
                 label : int = 0) -> None:
        
        # graph properties.
        self.name = name
        self.type = ""
        self.attr = ""
        self.label = np.array([label])
        # node properties.
        self.nodes = [] 
        self.node_dict = dict()
        self.num_nodes = 0
        # egde propoerties.
        self.edges = [] 
        self.num_edges = 0
        return

    def addnodes(self, 
                 node_id : str, 
                 code : str = "",
                 node_type : str = "",
                 node_attr : any = None) -> int:
        
        # if found the existing node_id.
        if node_id in self.node_dict.keys():
            print("Error: found existing node with the same node id!")
            return -1
        # if it is a new node.
        node = CodeNode(node_id, code, node_type, node_attr)
        self.nodes.append(node)
        self.num_nodes += 1
        self.node_dict[node_id] = self.num_nodes - 1
        return 0

    def addedges(self, 
                 node_out: str, 
                 node_in: str,
                 edge_type: str = "",
                 edge_attr: str = "") -> int:
        
        edge = CodeEdge(node_out, node_in, edge_type, edge_attr)
        self.edges.append(edge)
        self.num_edges += 1
        return 0

    def nodes2mask(self,
                nodes_list : list = []):
        
        return [1 if n.node_id in nodes_list else 0 for n in self.nodes]
    
    def mask2nodes(self,
                   mask : list = []):
        
        if 0 == len(mask):
            return [0] * self.num_nodes
        else:
            return [n.node_id for msk, n in zip(mask, self.nodes) if msk == 1]

    def walk(self, 
             mask : list = [], 
             step : int = 1, 
             direction : str = 'forward', 
             contained : bool = False) -> list: 

        if 0 == len(mask):
            mask = [0] * self.num_nodes
        # get the adjency matrix.
        nodesOut = [self.node_dict[e.node_out] for e in self.edges]
        nodesIn = [self.node_dict[e.node_in] for e in self.edges]
        A = sp.coo_matrix((np.ones(self.num_edges), (nodesOut, nodesIn)), 
                        shape=(self.num_nodes, self.num_nodes), dtype=np.int8)
        I = sp.eye(self.num_nodes, dtype=np.int8) # identity matrix.
        # calcualte total adjency matrix.
        if direction == 'forward':
            M = A
        elif direction == 'backward':
            M = A.T
        elif direction == 'bidirect':
            M = A + A.T
        if contained:
            temp = I
            while (step):
                temp += M ** step
                step -= 1
            M = temp
        else:
            M = M ** step
        # calcualte the mask.
        _mask_ = np.array([1 if i else 0 for i in np.array(mask, dtype=np.int8) * M])

        return _mask_

    def nextstep(self,
                 start_nodes : list,
                 direction : str = 'forward') -> list:
        
        mask = self.nodes2mask(start_nodes)
        _mask_ = self.walk(mask, step=1, direction=direction, contained=False)
        return self.mask2nodes(_mask_)

    def slicing(self, 
                mask : list = [], 
                neighbor : int = 1, 
                direction : str = 'bidirect') -> list:
        
        return self.walk(mask, neighbor, direction, contained=True)

    def draw(self, 
             mask : list = [],
             save_folder : str = None,
             view : bool = False) -> graphviz.Digraph:
        
        if len(mask) == 0:
            mask = np.zeros(self.num_nodes)
        
        dot = graphviz.Digraph()
        for i, n in enumerate(self.nodes):
            dot.node(n.node_id, n.code, style='filled', fillcolor='#CC0000' if mask[i] else '#FFFFFF')
        for e in self.edges:
            dot.edge(e.node_out, e.node_in, e.edge_attr)
        
        if save_folder:
            dot.render(directory=save_folder, view=view) 
        
        return dot
    

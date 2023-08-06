from abc import ABC, abstractmethod
import networkx as nx



class LogicAST(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def accept(self, visitor):
        pass
    
    
    def visualizeAST(self):
        
        G = nx.DiGraph()
        
        tree = self
        
        # attach an identifier to each node
        def attach_id(node: LogicAST):
                
            if isinstance(node,ATOM):
                node._id = id(node)
                return

            node._id = id(node)
            
            if isinstance(node,AND):
                attach_id(node.input1)
                attach_id(node.input2)
                return
            
            if isinstance(node,OR):
                attach_id(node.input1)
                attach_id(node.input2)
                return
            
            if isinstance(node,NEG):
                attach_id(node.input1)
                return
            
            raise Exception(f"Unknown node type {node}")
        
        attach_id(tree)
        
        def visit(node: LogicAST, parent: LogicAST):
            
            if isinstance(node,ATOM):
                if parent is None:
                    G.add_node(node._id, label=node.name)
                else:
                    G.add_node(node._id, label=node.name)
                    G.add_edge(parent._id, node._id)
                return
            
            if parent is None:
                G.add_node(node._id, label=node.name)
            else:
                G.add_node(node._id, label=node.name)
                G.add_edge(parent._id, node._id)
            
            if isinstance(node,AND):
                visit(node.input1, node)
                visit(node.input2, node)
                return
            
            if isinstance(node,OR):
                visit(node.input1, node)
                visit(node.input2, node)
                return
            
            if isinstance(node,NEG):
                visit(node.input1, node)
                return
            
            raise Exception(f"Unknown node type {node}")
        
        visit(tree, None)
        
        # attach color
        for node in G.nodes:
            if G.nodes[node]['label'] == "&":
                G.nodes[node]['color'] = 'red'
            if G.nodes[node]['label'] == "|":
                G.nodes[node]['color'] = 'blue'
            if G.nodes[node]['label'] == "~":
                G.nodes[node]['color'] = 'green'
        
        # label を表示してくれるようにする networkxで描画
        A = nx.nx_agraph.to_agraph(G)
        A.layout('dot')
        # caption
        A.graph_attr['label'] = f"AST of {self}"
        A.draw('ast.png')

        return


class ATOM(LogicAST):
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}"
    
    def accept(self, visitor):
        return visitor.case_atom(self)

class AND(LogicAST):
    
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2
        self.name = "&"
    
    def __str__(self):
        
        left = self.input1
        if not isinstance(left,ATOM):
            left = f"({left})"
        
        right = self.input2
        if not isinstance(right,ATOM):
            right = f"({right})"
        
        return f"{left} & {right}"
    
    def accept(self, visitor):
        return visitor.case_and(self)

class OR(LogicAST):
    
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2
        self.name = "|"
    
    def __str__(self):
        
        left = self.input1
        if not isinstance(left,ATOM):
            left = f"({left})"
        
        right = self.input2
        if not isinstance(right,ATOM):
            right = f"({right})"
        
        return f"{left} | {right}"
    
    def accept(self, visitor):
        return visitor.case_or(self)

class NEG(LogicAST):
                
    def __init__(self, input1):
        self.input1 = input1
        self.name = "~"
    
    
    def __str__(self):
        
        left = self.input1
        if not isinstance(left,ATOM):
            left = f"({left})"
        
        return f"~{left}"

    def accept(self, visitor):
        return visitor.case_neg(self)



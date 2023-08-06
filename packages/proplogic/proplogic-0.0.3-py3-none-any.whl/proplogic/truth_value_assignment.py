from .logic_ast import *
from .logic_parser import LogicParser
import  sys

class TruthValueAssignmentVisitor():
    
    def __init__(self, assignment : dict[str,bool]):
        self.assignment = assignment
        return
    
    def case_atom(self, atom : ATOM) -> bool:
        return self.assignment[atom.name]
    
    def case_and(self, and_node : AND) -> bool:
        return and_node.input1.accept(self) and and_node.input2.accept(self)
    
    def case_or(self, or_node : OR) -> bool:
        return or_node.input1.accept(self) or or_node.input2.accept(self)

    def case_neg(self, neg_node : NEG) -> bool:
        return not neg_node.input1.accept(self)
    



if __name__ == "__main__":
    
    logic = sys.argv[1]
    propositional_var = logic.replace(" ", "").replace("&", " ").replace("|", " ").replace("~", " ").split()
    # remove duplicates
    propositional_var = list(dict.fromkeys(propositional_var))
    
    assignment = dict()
    for var in propositional_var:
        assignment[var] = input(f"Enter value for {var} (if true enter 1, if false enter 0): ") == "1"
    
    parser = LogicParser(logic)
    ast = parser.parse()
    
    print(ast)
    
    visitor = TruthValueAssignmentVisitor(assignment)
    print(ast.accept(visitor))
    
    
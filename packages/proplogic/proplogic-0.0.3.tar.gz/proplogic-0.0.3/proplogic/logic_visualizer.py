
from .logic_parser import LogicParser
from .logic_tokenizer import LogicTokenizer

def visualize_logical_expression(expression: str):
    
    tokens = LogicTokenizer(expression).tokenize()
    
    print ("Tokens:")
    for token in tokens:
        print(token)
    

    parser = LogicParser(expression)
    tree = parser.parse()
    tree.visualizeAST(filename="visualized_ast.png")
    
    return

if __name__ == "__main__":
    visualize_logical_expression("a & b | c & d  & ( x &  ~~y | z & w)")
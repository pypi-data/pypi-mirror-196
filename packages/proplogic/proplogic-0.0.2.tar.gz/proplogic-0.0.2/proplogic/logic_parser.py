from secrets import token_urlsafe
from .logic_tokenizer import TKkind, Token,LogicTokenizer
from  .logic_ast import LogicAST, ATOM, AND, OR, NEG
import traceback
import logging
import sys




class LogicParser():
    
    def __init__(self, input):
        self.input = input
        self.current_pos = 0
        self.tokens = LogicTokenizer(self.input).tokenize()
    
    def parse(self) -> LogicAST:
        tree = self.expression()
        if self.current_pos < len(self.tokens):
            raise Exception("Syntax Error")
        self._ast = tree
        return tree
    
    @property
    def ast(self) -> LogicAST:
        
        if self.current_pos == 0:
            return self.parse()
        
        return self._ast
    
    def consume(self, token_kind: TKkind):
        if self.current_pos < len(self.tokens):
            if self.tokens[self.current_pos].kind == token_kind:
                self.current_pos += 1
                logging.debug(f"Consumed {token_kind} at {self.current_pos - 1}   {self.tokens[self.current_pos - 1]} consume was called from {traceback.extract_stack()[-2][2]}")
                return True
        return False
    
    def expect (self, token_kind: TKkind):
        
        if self.current_pos >= len(self.tokens):
            raise Exception("Syntax Error at EOF")
        
        logging.debug(f"Expecting {token_kind} at {self.current_pos}   {self.tokens[self.current_pos]} expect was called from {traceback.extract_stack()[-2][2]}")
        
        res = self.consume(token_kind)
        

        
        if not res:
            raise Exception(f"Syntax Error at {self.current_pos, str(self.tokens[self.current_pos])}")

        return True
        
    
    def expression(self) -> LogicAST:
        
        expr : LogicAST = self.term()
        
        while self.current_pos < len(self.tokens):
            
            if self.consume(TKkind.OR):
                expr = OR(expr, self.term())
                continue
            
            break
        
        return expr
    
    def term(self) -> LogicAST:
        
        term : LogicAST = self.factor()
        
        while self.current_pos < len(self.tokens):
            
            if self.consume(TKkind.AND):
                term = AND(term, self.factor())
                continue
            
            break
        
        return term
    
    def factor(self) -> LogicAST:
        
        if self.consume(TKkind.NEG):
            return NEG(self.factor())
        
        return self.unit()
    
    def unit (self) -> LogicAST:
        
        if self.consume(TKkind.ATOM):
            return ATOM(self.tokens[self.current_pos - 1].content)
        
        self.expect(TKkind.LPAREN)
        expr = self.expression()
        self.expect(TKkind.RPAREN)
        return expr
        

        

    
if __name__ == "__main__":
    
    logging.basicConfig(filename='logic_parser.log', level=logging.DEBUG)
    
    if len(sys.argv) < 2:
        print("Usage: python logic_parser.py <expression>")
        sys.exit(1)
    
    text = sys.argv[1]
    parser = LogicParser(text)
    try :
        ast = parser.parse()
        ast.visualizeAST()
        
        
        
        
    except Exception as e:
        
        print(e)
        traceback.print_exc()
        
        # print all the tokens
        for token in parser.tokens:
            print(token)
            
        # print the current position
        print(parser.current_pos)

        
        
    
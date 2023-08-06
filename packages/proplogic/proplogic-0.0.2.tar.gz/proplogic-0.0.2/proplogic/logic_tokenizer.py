from enum import Enum

class TKkind(Enum):
    ATOM = 1
    OR = 2
    AND = 3
    NEG = 4
    LPAREN = 5
    RPAREN = 6
    
    

class Token():
    
    def __init__(self, token_kind, content):
        self.kind = token_kind
        self.content = content
    
    def __str__(self):
        return "<" + str(self.kind) + "," + self.content + ">"

class LogicTokenizer():
    
    def __init__(self, input: str):
        self.input = input
        self.current_pos = 0
        self.tokens : list[Token]= []
        
        return

    
    def tokenize(self):
        
        atom_buffer = ""
        
        while self.current_pos < len(self.input):
            
            picked_char = self.input[self.current_pos]
            
            if picked_char == " ":
                self.current_pos += 1
                continue
            
            if picked_char.isalpha():
                atom_buffer += picked_char
                self.current_pos += 1
                continue
            
            if atom_buffer != "":
                self.tokens.append(Token(TKkind.ATOM, atom_buffer))
                atom_buffer = ""
                continue
            
            if picked_char == "|":
                self.tokens.append(Token(TKkind.OR, "|"))
                self.current_pos += 1
                continue
            
            if picked_char == "&":
                self.tokens.append(Token(TKkind.AND, "&"))
                self.current_pos += 1
                continue
            
            if picked_char == "~":
                self.tokens.append(Token(TKkind.NEG, "~"))
                self.current_pos += 1
                continue
            
            if picked_char == "(":
                self.tokens.append(Token(TKkind.LPAREN, "("))
                self.current_pos += 1
                continue
            
            if picked_char == ")":
                self.tokens.append(Token(TKkind.RPAREN, ")"))
                self.current_pos += 1
                continue
            
            raise Exception("Unpredicted character: " + picked_char)

        if atom_buffer != "":
            self.tokens.append(Token(TKkind.ATOM, atom_buffer))
            atom_buffer = ""
            
        return self.tokens
            

            

if __name__ == "__main__":
    res = LogicTokenizer("A & (hdfjs | ~B))").tokenize()
    

    
    for token in res:
        print(token)
        
        
    
    